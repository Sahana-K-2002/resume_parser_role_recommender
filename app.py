import streamlit as st
import os
from pyresparser import ResumeParser
import model as m
import base64
import time
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
import io

st.set_page_config(
   page_title="Resume Parser & Role Recommender",
   page_icon='./logo.png',
)

def save_pdf_file(uploaded_file, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def main():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #080202;  /* Set your desired background color */
            color: #9AFFDC;
            font-family: sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    bg_image = '''
        <style>
        .stApp {
            background-image: url("background.jpg");
            background-size: cover;
        }
        </style>
        '''
    st.markdown(bg_image, unsafe_allow_html=True)
    st.markdown("<h1 style='color: #9AFFDC;'>Resume Parser & <br> Role Recommender</h1><br>", unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>In today's job market, job seekers often find it challenging to identify job roles that match their skillset. With numerous job vacancies and varying job requirements, it can be overwhelming to navigate the recruitment process. </p>", unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Here's a job role recommender system that identifies suitable job roles for you based on your resume. This system analyzes your resume, extracts relevant information, and matches them with appropriate job roles. </p><br>", unsafe_allow_html=True)
    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your resume below to find suitable job roles. (Allowed: pdf)", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            # Save the uploaded PDF file to a temporary location
            temp_path = save_pdf_file(uploaded_file, "pdf_files")

            # Display the saved file path
            st.success("File saved successfully!")
            st.write("Saved File Path:", temp_path)

            # Extract information from the PDF file
            # extracted_data = extract_information_from_pdf(temp_path)
            with open(temp_path, 'rb') as file:
                data = ResumeParser(file.name).get_extracted_data()
                # data = extract_information_from_pdf("temp.pdf")
            show_pdf(temp_path)
            if data:
                resume_text = pdf_reader(temp_path)

                st.header("**Resume Analysis**")
                st.success("Hello "+ data['name'])
                st.subheader("**Basic Information Extracted:**")
                try:
                    st.write('Name: '+ data['name'])
                    st.write('Email ID: ' + data['email'])
                    st.write('Contact Number: ' + data['mobile_number'])
                    st.write('Number of Pages: '+ str(data['no_of_pages']))
                except:
                    pass
                # cand_level = ""
                if data['no_of_pages'] == 1:
                    # cand_level = "Fresher"
                    st.markdown( '''<h5 style='text-align: left; color: #C4B0FF;'>You appear to be a fresher.</h5>''', unsafe_allow_html=True)
                elif data['no_of_pages'] == 2:
                    # cand_level = "Intermediate"
                    st.markdown('''<h5 style='text-align: left; color: #C4B0FF;'>You appear to be at an intermediate level!</h5>''', unsafe_allow_html=True)
                elif data['no_of_pages'] >=3:
                    # cand_level = "Experienced"
                    st.markdown('''<h5 style='text-align: left; color: #C4B0FF;'>You appear to be at an experienced level! </h5>''', unsafe_allow_html=True)
                
            
            skill_new = data['skills']
            # st.write(skill_new)
            predict= ' '.join([str(elem) for elem in skill_new])
            # Display the extracted information
            st.header("Your recommended roles are:")
            roles = m.role(predict)
            for role in roles:
                st.success(role)

            ### Resume writing recommendation
            st.subheader("**Resume Tips & Ideas**")
            resume_score = 0
            if 'objective' in resume_text.lower():
                resume_score = resume_score+20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Good job! You have added your objective.</h5>''', unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFEEB3;'>[-] We recommend you to add your career objectives.</h5>''',unsafe_allow_html=True)

            if 'declaration'  in resume_text.lower():
                resume_score = resume_score + 20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added a delcaration.</h5>''', unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFEEB3;'>[-] We recommend you to add a declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you.</h5>''', unsafe_allow_html=True)

            if 'skills' or 'interests'in resume_text.lower():
                resume_score = resume_score + 20
                st.markdown('''<h5 style='text-align: left; color: #159895;'>[+] Awesome! You have added your skills and interests.</h5>''', unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFEEB3;'>[-] We recommend you to add your skills and interests.</h5>''', unsafe_allow_html=True)

            if 'achievements' in resume_text.lower():
                resume_score = resume_score + 20
                st.markdown('''<h5 style='text-align: left; color: #159895;'>[+] Awesome! You have added your achievements.</h5>''', unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFEEB3;'>[-] We recommend you to add your achievements. </h5>''', unsafe_allow_html=True)

            if 'projects' in resume_text.lower():
                resume_score = resume_score + 20
                st.markdown('''<h5 style='text-align: left; color: #159895;'>[+] Awesome! You have added your projects.</h5>''', unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #FFEEB3;'>[-] We recommend you to add your projects. It will validate your skills and job role requirements.</h5>''', unsafe_allow_html=True)

            st.subheader("**Resume Score**")
            st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #00FFCA;
                        }
                    </style>""",
                    unsafe_allow_html=True,
            )
            my_bar = st.progress(0)
            score = 0
            for percent_complete in range(resume_score):
                score +=1
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1)
            st.success('Your Resume Writing Score: ' + str(score))
            st.warning("Note: This score is calculated based on the content that you have added in your resume.")
            # st.balloons()

if __name__ == "__main__":
    main()

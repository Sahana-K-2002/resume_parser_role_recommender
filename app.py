import streamlit as st
import os
from pyresparser import ResumeParser
import model as m

def save_pdf_file(uploaded_file, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def extract_information_from_pdf(file_path):
    # Extract information from the PDF file using pyresparser
    data = ResumeParser(file_path).get_extracted_data()

    return data

def main():
    st.title("PDF Information Extractor")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

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

            # Extract information from the uploaded PDF file
            
            skill_new = data['skills']
            # st.write(skill_new)
            predict= ' '.join([str(elem) for elem in skill_new])
            # Display the extracted information
            st.header("Your recommended roles are:")
            st.write(m.role(predict))


if __name__ == "__main__":
    main()
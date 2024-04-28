import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import base64
import io
from PIL import Image 
import pdf2image
from utils import get_gemini_response_text, get_gemini_response_image, input_pdf_text, input_pdf_setup


load_dotenv() ## load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Streamlit session state to keep track of which section to show
if 'current_view' not in st.session_state:
    st.session_state.current_view = "Home"  # Default view

# Function to switch sections based on button clicks
def set_view(view_name):
    st.session_state.current_view = view_name

if st.session_state.current_view == "Home":
    st.title("Resume ATS Tracking")

# Buttons to switch between sections
col1, col2 = st.columns([1, 2])  # Proportionally adjust the column widths

# Column layout for buttons with wider space
with col1:
    st.write("Options:")

with col2:
    # Increase button size by having fewer columns
    if st.button("About", use_container_width=True):
        st.session_state.view = "About"
    
    if st.button("Image Reader", use_container_width=True):
        st.session_state.view = "Image Reader"
    
    if st.button("Text Reader", use_container_width=True):
        st.session_state.view = "Text Reader"

# Display content based on session state
if 'view' not in st.session_state:
    st.session_state.view = "Home"
    st.write("Choose the above following option to proceed.")

if st.session_state.view == "About":
    st.header("Project Overview")
    st.write("""
    Our ATS Tracker provides a comprehensive analysis of resumes to determine how well they match specific job descriptions. We use AI-based models to extract and evaluate content from resumes, focusing on relevant keywords, skills, and experience. Users can upload their resumes in PDF format, and the system offers feedback on areas of strength and suggestions for improvement.
    """)

    st.header("Methods of Analysis")
    st.write("""
    - **Image Reading**: This method uses optical character recognition (OCR) to read text from image-based resumes, allowing us to work with resumes in various formats, even if they're not traditional text-based PDFs.
    - **Text Reading**: This method extracts text directly from PDF resumes to analyze the content. It's useful for evaluating resumes based on keywords, skill sets, and other textual elements.
     """)

    st.header("Benefits")
    st.write("""
    Our ATS Tracker benefits both job seekers and employers:

    - **Job Seekers**: Get detailed feedback on how your resume aligns with specific job descriptions. Understand what skills are crucial for your target role and receive personalized recommendations for improvement.
    - **Employers**: Quickly evaluate candidates' resumes based on specific job requirements. Our system helps streamline the hiring process by identifying the best-suited candidates through ATS analysis.
    """)

#######################################################################################################################  

elif st.session_state.view == "Image Reader":

    st.title("Smart ATS")
    st.text("Improve Your Resume ATS through Image Reader")
    input_text=st.text_area("Job Description: ",key="input")
    uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")


    submit1 = st.button("Tell Me About the Resume")

    submit2 = st.button("How Can I Improvise my Skills")

    submit3 = st.button("Percentage match")

    input_prompt1 = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt2 = """
    You are a skilled Technical Recruiter with a deep understanding of the requirements given in job description. 
    Your task is to evaluate the resume and identify "What skills should the candidate have" and "What are effective strategies to get this job." 
    Consider the job description and provide suggestions for improvements and skill acquisition.
    """


    input_prompt3 = """
    You are a skilled Applicant Tracking System (ATS) scanner with a deep understanding of ATS functionality across industries. 
    Your task is to evaluate the resume against the provided job description. Provide a percentage indicating the match between the resume and the job description. 
    Also, list any missing keywords or skills that could improve the resume's compatibility with the job description. Conclude with your final thoughts on the resume's alignment with the role.
    """


    if submit1:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response_image(input_prompt1,pdf_content,input_text)
            st.subheader("Result")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

    elif submit2:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response_image(input_prompt2,pdf_content,input_text)
            st.subheader("Result")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

    elif submit3:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response_image(input_prompt3,pdf_content,input_text)
            st.subheader("Result")
            st.write(response)
        else:
            st.write("Please uplaod the resume")
    
#######################################################################################################################   

elif st.session_state.view == "Text Reader":
    input_prompt="""
    Hey Act Like a skilled or very experience ATS(Application Tracking System)
    with a deep understanding of tech field,software engineering,data science ,data analyst
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving thr resumes. Assign the percentage Matching based 
    on Jd and
    the missing keywords with high accuracy
    resume:{text}
    description:{jd}

    I want the response in one single string having the structure
    {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
    """

    ## streamlit app
    st.title("Smart ATS")
    st.text("Improve Your Resume ATS through Text Reader")
    jd=st.text_area("Job Description: ")
    uploaded_file=st.file_uploader("Upload Your Resume(PDF)...",type="pdf",help="Please uplaod the pdf")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            text=input_pdf_text(uploaded_file)
            response=get_gemini_response_text(input_prompt)
            # Displaying the "JD Match" value
            st.write(response)
            
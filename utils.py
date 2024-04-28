import google.generativeai as genai
import PyPDF2 as pdf
import base64
import io
from PIL import Image 
import pdf2image
import re


def get_gemini_response_text(input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
def get_gemini_response_image(input,pdf_content,prompt):
        model=genai.GenerativeModel('gemini-pro-vision')
        response=model.generate_content([input,pdf_content[0],prompt])
        return response.text

def input_pdf_text(uploaded_file):
    # Create an empty list to store the lines of text
    text_lines = []

    reader = pdf.PdfReader(uploaded_file)

    # Loop through all pages and extract text
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        extracted_text = page.extract_text() or ""

        # Standardize line breaks and remove extra spaces
        extracted_text = re.sub(r'\s+', ' ', extracted_text.replace('\r\n', '\n').replace('\r', '\n'))

        # Split into lines and add each line to the list
        for line in extracted_text.split("\n"):
            cleaned_line = line.strip()  # Remove leading/trailing spaces
            if cleaned_line:  # Avoid adding empty lines
                text_lines.append(cleaned_line)

    return text_lines  # Return the list of text lines

def input_pdf_setup(uploaded_file):
        if uploaded_file is not None:
            ## Convert the PDF to image
            images=pdf2image.convert_from_bytes(uploaded_file.read())

            first_page=images[0]

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                }
            ]
            return pdf_parts
        else:
            raise FileNotFoundError("No file uploaded")
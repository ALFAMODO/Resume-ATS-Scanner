import google.generativeai as genai
import PyPDF2 as pdf
import base64
import io
from PIL import Image 
import pdf2image


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
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

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
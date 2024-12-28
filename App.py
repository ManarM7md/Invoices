import streamlit as st
import os
import base64
from typing import Optional, Literal
from together import Together

# Functions
def encode_image(image_path: str) -> str:
    """Read and encode image to base64."""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_markdown(together: Together, file_path: str) -> str:
    """Process image and convert to markdown using Together AI."""
    final_image_url = f"data:image/jpeg;base64,{encode_image(file_path)}"
    output = together.process_image(final_image_url)
    return output

def ocr(file_path: str, api_key: Optional[str] = None) -> str:
    """
    Perform OCR on an image using Together AI.
    Args:
        file_path: Path to the image file
        api_key: Together AI API key
    Returns:
        Markdown formatted text from the image
    """
    if api_key is None:
        api_key = "YOUR_API_KEY_HERE"

    together = Together(api_key=api_key)  # Initialize Together with the API key

    final_markdown = get_markdown(together, file_path)

    return final_markdown

# Streamlit App
def main():
    st.title("Image to Markdown Converter")
    st.write("Upload an image, and this app will convert its content into Markdown using Together AI.")

    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        temp_file_path = "temp_uploaded_image.png"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(temp_file_path, caption="Uploaded Image", use_container_width=True)

        try:
            api_key = "fafd8f87a381ed63e1bc0409b6947082dddc6b0bc190c9c9007f3545531b0983"
            markdown_content = ocr(temp_file_path, api_key=api_key)
            
            st.markdown("### Extracted Markdown:")
            st.markdown(markdown_content)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        os.remove(temp_file_path)

if __name__ == "__main__":
    main()

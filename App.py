import streamlit as st
import os
from PIL import Image
from together import Together
import base64
from typing import Optional, Literal


# Functions from the original code
def encode_image(image_path: str) -> str:
    """Read and encode image to base64."""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def is_remote_file(file_path: str) -> bool:
    """Check if the file path is a remote URL."""
    return file_path.startswith(('http://', 'https://'))


def get_markdown(
    together: Together,
    vision_llm: str,
    file_path: str
) -> str:
    """Process image and convert to markdown using Together AI."""
    system_prompt = """Convert the provided image into Markdown format. Ensure that all content from the page is included, such as headers, footers, subtexts, images (with alt text if possible), tables, and any other elements.
    Requirements:
    - Output Only Markdown: Return solely the Markdown content without any additional explanations or comments.
    - No Delimiters: Do not use code fences or delimiters like 
markdown.
    - Complete Content: Do not omit any part of the page, including headers, footers, and subtext.
    """

    final_image_url = file_path if is_remote_file(file_path) else f"data:image/jpeg;base64,{encode_image(file_path)}"

    output = together.chat.completions.create(
        model=vision_llm,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": final_image_url
                        }
                    }
                ]
            }
        ]
    )

    return output.choices[0].message.content


def ocr(
    file_path: str,
    api_key: Optional[str] = None,
    model: Literal["Llama-3.2-90B-Vision", "Llama-3.2-11B-Vision", "free"] = "Llama-3.2-90B-Vision"
) -> str:
    """
    Perform OCR on an image using Together AI.

    Args:
        file_path: Path to the image file or URL
        api_key: Together AI API key (defaults to TOGETHER_API_KEY environment variable)
        model: Model to use for vision processing

    Returns:
        Markdown formatted text from the image
    """
    if api_key is None:
        api_key = os.getenv('TOGETHER_API_KEY')
        if api_key is None:
            raise ValueError("API key must be provided either directly or through TOGETHER_API_KEY environment variable")

    vision_llm = f"meta-llama/{model}-Instruct-Turbo" if model != "free" else "meta-llama/Llama-Vision-Free"

    together = Together(api_key=api_key)
    final_markdown = get_markdown(together, vision_llm, file_path)

    return final_markdown


# Streamlit App
def main():
    st.title("Image to Markdown Converter")
    st.write("Upload an image, and this app will convert its content into Markdown using Together AI.")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded image temporarily
        temp_file_path = "temp_uploaded_image.png"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image
        st.image(temp_file_path, caption="Uploaded Image", use_column_width=True)

        # Extract Markdown
        try:
            api_key = os.getenv('TOGETHER_API_KEY')
            markdown_content = ocr(temp_file_path, api_key=api_key, model="Llama-3.2-11B-Vision")
            
            # Display the Markdown content
            st.markdown("### Extracted Markdown:")
            st.markdown(markdown_content)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Remove the temporary file
        os.remove(temp_file_path)


if __name__ == "__main__":
    main()
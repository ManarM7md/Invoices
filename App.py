import os
import base64
from typing import Optional, Literal
from together import Together
import streamlit as st

# Function to encode image to base64
def encode_image(image_path: str) -> str:
    """Read and encode image to base64."""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to check if the file is a remote URL
def is_remote_file(file_path: str) -> bool:
    """Check if the file path is a remote URL."""
    return file_path.startswith(('http://', 'https://'))

# Function to get Markdown output from Together's vision model
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
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": system_prompt},
                {"type": "image_url", "image_url": {"url": final_image_url}}
            ]
        }]
    )

    return output.choices[0].message.content

# OCR function
def ocr(
    file_path: str,
    api_key: Optional[str],
    model: Literal["Llama-3.2-90B-Vision", "Llama-3.2-11B-Vision", "free"] = "Llama-3.2-90B-Vision"
) -> str:
    """
    Perform OCR on an image using Together AI.

    Args:
        file_path: Path to the image file or URL
        api_key: Together AI API key
        model: Model to use for vision processing

    Returns:
        Markdown formatted text from the image
    """
    if api_key is None:
        raise ValueError("API key must be provided")

    vision_llm = f"meta-llama/{model}-Instruct-Turbo" if model != "free" else "meta-llama/Llama-Vision-Free"

    together = Together(api_key=api_key)
    final_markdown = get_markdown(together, vision_llm, file_path)

    return final_markdown

# Streamlit App
def main():
    st.title("OCR: Document to Markdown")
    st.write("Upload an image, and this app will convert its content into Markdown using Together AI.")

    api_key = st.text_input("Enter your Together AI API Key", type="password")

    if not api_key:
        st.warning("Please enter your API key to proceed.")
        return

    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        temp_file_path = "temp_uploaded_image.png"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        col1, col2 = st.columns(2)

        with col1:
            st.image(temp_file_path, caption="Uploaded Image", use_container_width=True)

        with col2:
            try:
                markdown_content = ocr(temp_file_path, api_key, model="Llama-3.2-11B-Vision")
                st.markdown("### Extracted Markdown:")
                st.markdown(markdown_content)
            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Clean up the temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()

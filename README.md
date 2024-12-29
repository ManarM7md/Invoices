# Invoice OCR Toolkit

**Invoice** is a comprehensive toolkit for extracting and converting text from invoice images and documents. Leveraging cutting-edge AI vision models and traditional OCR solutions, this repository offers highly accurate and efficient tools for extracting text and converting it into Markdown or plain text formats.

## Key Features

### 🚀 Advanced AI-Powered OCR
- **Together AI Vision Models:**
  - Extract text and structure (headers, tables, subtexts, etc.) with high precision.
  - Outputs clean, Markdown-formatted documents.
  - Supports multiple model configurations, including Llama-3.2-90B-Vision, Llama-3.2-11B-Vision, and a free-tier model.

### 📜 Lightweight OCR with Tesseract
- Fast, offline, and open-source solution.
- Preprocessing for better accuracy (e.g., noise removal, resizing).
- Supports multilingual text recognition: English, French, Arabic, Spanish, German, Italian, and more.

### 🛠 EasyOCR Integration
- An additional, robust OCR solution.
- Automatic language detection and reliable text extraction.

### 🌟 Streamlit Application
- A user-friendly interface for uploading and converting invoice images to Markdown.
- Access the app here: [Invoice OCR App](https://invoices-bz4djaejhcjykryekf2v74.streamlit.app/).

## Requirements

- Python 3.7+
- Tesseract OCR (installed via `apt-get` or manually)
- Google API Key (for accessing Google's Generative AI)

### Install Dependencies

To install the required Python libraries, use the following command:

```bash
pip install -r requirements.txt
```

### Installing Tesseract OCR

You can install Tesseract OCR using the following commands depending on your OS:

- **For Linux**:

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
sudo apt-get install tesseract-ocr-ara  # Install Arabic language data for Tesseract
```

- **For macOS** (using Homebrew):

```bash
brew install tesseract
```

- **For Windows**:
  - Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
  - Make sure to set the `TESSDATA_PREFIX` environment variable correctly.

### Set up Google API Key

You need a Google API key to access Google Generative AI services. You can get an API key by following the instructions [here](https://developers.google.com/generative-ai).

Once you have your API key, store it in your environment variables or replace `"your_google_api_key"` in the code with the actual API key.

## Usage

1. **Prepare your Image**: Ensure your invoice is in an image format supported by the OCR tools (e.g., JPEG, PNG).

2. **Run OCR and Extract Data**:

```bash
python extract_invoice_data.py path_to_your_invoice_image
```

This will:
- Perform OCR on the invoice image using EasyOCR and Tesseract.
- Extract text in both Arabic and English.
- Use Google Generative AI to further process and structure the data.

3. **Output**:
   - The data will be saved as a CSV file with fields such as Description, RATE, HOURS, and Amount.

Example of CSV output:

```csv
Description, RATE, HOURS, Amount
Content Plan, $50/hr, 4, $200.00
Copy Writing, $50/hr, 2, $100.00
```

## Code Structure

### `extract_invoice_data.py`
- Contains the main logic for image processing, OCR, and data extraction.
- Uses `easyocr` for text extraction and `pytesseract` for Arabic OCR.
- Uses `langchain` and Google's Generative AI for further data structuring.

## Acknowledgments
- Together AI for their exceptional Vision models.
- Tesseract OCR for their open-source OCR solution.
- EasyOCR for their lightweight and robust library.

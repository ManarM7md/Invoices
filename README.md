# OCR Invoice Processing with EasyOCR, Tesseract, and Google AI

This project extracts text and structured data from invoices using Optical Character Recognition (OCR) and generative AI. The system processes images or scanned invoices in both Arabic and English, extracting useful fields such as item ID, description, price, quantity, and total amount, and outputs the results in CSV format.

## Features

- **OCR Extraction**: Extracts text from images using both EasyOCR (for multi-language support) and Tesseract (for Arabic OCR).
- **Multi-Language Support**: Processes invoices in Arabic and English.
- **Table Extraction**: Supports extracting structured data (tables) from invoices.
- **Generative AI for Data Structuring**: Uses Google's Generative AI to extract structured invoice data like item ID, description, unit price, and total amount.
- **CSV Export**: Saves extracted and structured data in CSV format.

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
   - The data will be saved as a CSV file with fields such as Item ID, Item Description, Unit Price, Quantity, Tax, and Total Amount.

Example of CSV output:

```csv
Item ID, Item Description, Unit Price, Quantity, Tax, Total Amount
1234, Product A, 50.00, 2, 10%, 110.00
5678, Product B, 75.00, 1, 5%, 78.75
```

## Code Structure

### `extract_invoice_data.py`
- Contains the main logic for image processing, OCR, and data extraction.
- Uses `easyocr` for text extraction and `pytesseract` for Arabic OCR.
- Uses `langchain` and Google's Generative AI for further data structuring.


## Contributing

Feel free to fork the repository, make improvements, and submit pull requests. Contributions are welcome!

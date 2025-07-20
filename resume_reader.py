import fitz  # PyMuPDF
import docx
import spacy

# Load the spaCy model
# Make sure you have run: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

def read_pdf(file):
    """
    Reads text from a PDF file.
    """
    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def read_docx(file):
    """
    Reads text from a DOCX file.
    """
    try:
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_keywords(text):
    """
    Extracts keywords (nouns, proper nouns, and verbs) from text using spaCy.
    """
    if not text or not nlp:
        return []
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"]]
    return list(set(keywords)) # Return unique keywords
"""
utils/parser.py
Extracts raw text from uploaded .txt, .pdf, or .docx files.
"""
import io


def extract_text_from_file(uploaded_file) -> str:
    """Dispatch to the correct reader based on file extension."""
    name = uploaded_file.name.lower()

    if name.endswith(".txt"):
        return _read_txt(uploaded_file)
    elif name.endswith(".pdf"):
        return _read_pdf(uploaded_file)
    elif name.endswith(".docx"):
        return _read_docx(uploaded_file)
    else:
        return ""


def _read_txt(file) -> str:
    return file.read().decode("utf-8", errors="replace")


def _read_pdf(file) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages)
    except ImportError:
        # Fallback — pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file.read()))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"[PDF read error: {e}]"


def _read_docx(file) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file.read()))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        return f"[DOCX read error: {e}]"

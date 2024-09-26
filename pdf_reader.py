from pypdf import PdfReader


class PDFReader:
    """Opens and handles data from a PDF, extracting text from specific pages."""

    def __init__(self, pdf_file_path: str) -> None:
        self.file_path = pdf_file_path
        self.reader = PdfReader(self.file_path)

    def extract_text(self, page_number: int) -> str:
        page = self.reader.pages[page_number]
        return page.extract_text()

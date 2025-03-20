import re
from collections import Counter
from prettytable import PrettyTable
import fitz  # PyMuPDF for PDF
from docx import Document  # For DOCX

# Function to extract professional experience section from the resume text
def extract_professional_experience(resume_text):
    pattern = r"(?i)(professional experience|work experience|employment history)(.*?)(?=(education|skills|certifications|$))"
    match = re.search(pattern, resume_text, re.DOTALL)
    if match:
        return match.group(2).strip()  # Return the section between "Professional Experience" and next section
    else:
        return None

# Function to match and count keywords in the professional experience section
def count_keyword_occurrences(text, keywords):
    text = text.lower()  # Make the text lowercase for case-insensitive matching
    keyword_counts = Counter()

    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_counts[keyword] = text.count(keyword_lower)

    return keyword_counts

# Function to read keywords from a file (e.g., text or docx)
def read_keywords_from_file(file_path):
    with open(file_path, 'r') as file:
        keywords = file.read().splitlines()  # Read keywords, one per line
    return keywords

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to generate a table report
def generate_table_report(keyword_counts):
    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Keyword", "Count"]

    # Add rows for each keyword and its count
    for keyword, count in keyword_counts.items():
        table.add_row([keyword, count])

    # Print the table
    print(table)

# Main function
def main():
    # Define file paths
    resume_file_path = 'resume.pdf'  # Change to your PDF/Word file path
    keywords_file_path = 'keywords.txt'  # Keywords file path

    # Step 1: Extract professional experience section from the resume
    if resume_file_path.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_file_path)
    elif resume_file_path.endswith('.docx'):
        resume_text = extract_text_from_docx(resume_file_path)
    else:
        print("Unsupported file format")
        return

    # Step 2: Extract professional experience section from resume text
    professional_experience = extract_professional_experience(resume_text)

    if professional_experience:
        print("Professional Experience Section Extracted Successfully!\n")
        
        # Step 3: Read keywords from file
        keywords = read_keywords_from_file(keywords_file_path)
        
        # Step 4: Count occurrences of each keyword in the professional experience section
        keyword_counts = count_keyword_occurrences(professional_experience, keywords)

        # Step 5: Generate table report based on keyword counts
        generate_table_report(keyword_counts)
    else:
        print("No professional experience section found.")

if __name__ == "__main__":
    main()

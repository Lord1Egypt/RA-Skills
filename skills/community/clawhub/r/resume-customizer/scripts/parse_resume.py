#!/usr/bin/env python3
"""
Parse resume from various formats (PDF, Word, text, Markdown, HTML).
Extract structured data: contact info, summary, work experience, education, skills, projects, certifications.
"""

import argparse
import json
import sys
import os
from pathlib import Path

def parse_pdf(file_path):
    """Parse PDF resume."""
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except ImportError:
        print("Error: PyPDF2 not installed. Install with: pip install PyPDF2")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        sys.exit(1)

def parse_docx(file_path):
    """Parse Word document."""
    try:
        import docx
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except ImportError:
        print("Error: python-docx not installed. Install with: pip install python-docx")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        sys.exit(1)

def parse_text(file_path):
    """Parse plain text or Markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(file_path, 'r', encoding='gbk') as f:
            return f.read()
    except Exception as e:
        print(f"Error parsing text file: {e}")
        sys.exit(1)

def parse_html(file_path):
    """Parse HTML file."""
    try:
        from bs4 import BeautifulSoup
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            return soup.get_text()
    except ImportError:
        print("Error: bs4 not installed. Install with: pip install beautifulsoup4")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        sys.exit(1)

def extract_structured_data(text, file_path):
    """
    Extract structured data from resume text.
    This is a simplified version - in production, use NLP/ML for better extraction.
    """
    # Basic structure
    resume_data = {
        "file_name": os.path.basename(file_path),
        "contact": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "website": ""
        },
        "summary": "",
        "work_experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "raw_text": text
    }
    
    # Simple extraction (can be enhanced with NLP)
    lines = text.split('\n')
    
    # Extract name (usually first non-empty line)
    for line in lines:
        if line.strip():
            resume_data["contact"]["name"] = line.strip()
            break
    
    # Extract email
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        resume_data["contact"]["email"] = emails[0]
    
    # Extract phone
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4})'
    phones = re.findall(phone_pattern, text)
    if phones:
        resume_data["contact"]["phone"] = ''.join(phones[0])
    
    # TODO: Enhanced extraction using NLP (spacy, etc.)
    # This is a basic implementation - can be extended
    
    return resume_data

def main():
    parser = argparse.ArgumentParser(description='Parse resume from various formats.')
    parser.add_argument('--input', required=True, help='Input resume file path')
    parser.add_argument('--output', required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    file_path = args.input
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # Parse based on file extension
    ext = Path(file_path).suffix.lower()
    
    if ext == '.pdf':
        text = parse_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        text = parse_docx(file_path)
    elif ext in ['.txt', '.md', '.markdown']:
        text = parse_text(file_path)
    elif ext in ['.html', '.htm']:
        text = parse_html(file_path)
    else:
        print(f"Error: Unsupported file format: {ext}")
        sys.exit(1)
    
    # Extract structured data
    resume_data = extract_structured_data(text, file_path)
    
    # Save to JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(resume_data, f, ensure_ascii=False, indent=2)
    
    print(f"Resume parsed successfully. Output saved to: {args.output}")
    print(f"Extracted: Name: {resume_data['contact']['name']}")
    print(f"           Email: {resume_data['contact']['email']}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Parse job description from various sources (text, URL, PDF, Word, Markdown).
Extract structured data: job title, company, required skills, preferred skills, responsibilities, qualifications, keywords.
"""

import argparse
import json
import sys
import os
import re
from pathlib import Path
from urllib.parse import urlparse

def parse_text(text):
    """Parse JD from plain text."""
    return text

def parse_url(url):
    """Fetch and parse JD from URL."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find JD content (common selectors)
        jd_selectors = [
            'div[class*="job"]', 'div[class*="description"]', 'div[class*="jd"]',
            'section[class*="job"]', 'div[id*="job"]', 'main', 'article'
        ]
        
        text = ""
        for selector in jd_selectors:
            elements = soup.select(selector)
            if elements:
                text = elements[0].get_text(separator='\n', strip=True)
                break
        
        # Fallback to body text
        if not text:
            text = soup.get_text(separator='\n', strip=True)
        
        return text
    except ImportError:
        print("Error: requests or bs4 not installed. Install with: pip install requests beautifulsoup4")
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

def parse_pdf(file_path):
    """Parse PDF JD."""
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
    """Parse Word document JD."""
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

def extract_structured_data(text):
    """
    Extract structured data from JD text.
    This is a simplified version - can be enhanced with NLP.
    """
    jd_data = {
        "job_title": "",
        "company": "",
        "location": "",
        "employment_type": "",  # Full-time, Part-time, Contract, etc.
        "required_skills": [],
        "preferred_skills": [],
        "responsibilities": [],
        "qualifications": [],
        "keywords": [],
        "raw_text": text
    }
    
    lines = text.split('\n')
    
    # Extract job title (usually in first few lines)
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        if line and len(line) < 100:  # Job title is usually short
            jd_data["job_title"] = line
            break
    
    # Extract company name (look for common patterns)
    company_patterns = [
        r'(?:at|@|company:?)\s*([A-Z][A-Za-z0-9\s&]+)',
        r'([A-Z][A-Za-z0-9\s&]+)\s*(?:is|are)\s*(?:hiring|looking|seeking)',
    ]
    for pattern in company_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            jd_data["company"] = matches[0].strip()
            break
    
    # Extract skills (simplified - look for common skill keywords)
    common_skills = [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Go', 'Rust', 'SQL',
        'Machine Learning', 'Deep Learning', 'Data Science', 'AI',
        'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
        'Git', 'Linux', 'Unix', 'Windows',
        'Communication', 'Leadership', 'Teamwork', 'Problem Solving'
    ]
    
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            jd_data["required_skills"].append(skill)
            jd_data["keywords"].append(skill)
    
    # TODO: Enhanced extraction using NLP (spacy, etc.)
    
    return jd_data

def main():
    parser = argparse.ArgumentParser(description='Parse job description from various sources.')
    parser.add_argument('--input', required=True, help='Input JD file path or URL')
    parser.add_argument('--output', required=True, help='Output JSON file path')
    parser.add_argument('--format', help='Input format (text, url, pdf, docx, md). Auto-detect if not specified.')
    
    args = parser.parse_args()
    
    input_source = args.input
    
    # Determine if input is URL or file
    is_url = bool(urlparse(input_source).scheme)
    
    if is_url:
        text = parse_url(input_source)
    else:
        if not os.path.exists(input_source):
            print(f"Error: File not found: {input_source}")
            sys.exit(1)
        
        # Determine format
        if args.format:
            ext = args.format.lower()
        else:
            ext = Path(input_source).suffix.lower()
        
        if ext in ['.pdf']:
            text = parse_pdf(input_source)
        elif ext in ['.docx', '.doc']:
            text = parse_docx(input_source)
        elif ext in ['.txt', '.md', '.markdown']:
            try:
                with open(input_source, 'r', encoding='utf-8') as f:
                    text = f.read()
            except UnicodeDecodeError:
                with open(input_source, 'r', encoding='gbk') as f:
                    text = f.read()
        elif ext in ['.html', '.htm']:
            try:
                from bs4 import BeautifulSoup
                with open(input_source, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    text = soup.get_text()
            except ImportError:
                print("Error: bs4 not installed. Install with: pip install beautifulsoup4")
                sys.exit(1)
        else:
            print(f"Error: Unsupported file format: {ext}")
            sys.exit(1)
    
    # Extract structured data
    jd_data = extract_structured_data(text)
    
    # Save to JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(jd_data, f, ensure_ascii=False, indent=2)
    
    print(f"JD parsed successfully. Output saved to: {args.output}")
    print(f"Extracted: Job Title: {jd_data['job_title']}")
    print(f"           Company: {jd_data['company']}")
    print(f"           Required Skills: {len(jd_data['required_skills'])}")

if __name__ == '__main__':
    main()

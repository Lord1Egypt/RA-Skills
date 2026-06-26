#!/usr/bin/env python3
"""
Extract all content from Word and text files for Google Docs
"""

import os
from docx import Document

def extract_word_content(doc_path):
    """Extract text from Word document"""
    if not os.path.exists(doc_path):
        return []
    
    try:
        doc = Document(doc_path)
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:  # Skip empty paragraphs
                paragraphs.append(text)
        return paragraphs
    except Exception as e:
        print(f"Error reading {doc_path}: {e}")
        return []

def extract_text_file(filename):
    """Extract text from text file"""
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        # Split into paragraphs
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        return paragraphs
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def create_google_docs_content():
    """Create formatted content for Google Docs"""
    
    print("📚 EXTRACTING ALL CONTENT FOR GOOGLE DOCS")
    print("="*50)
    
    all_content = []
    
    # Extract from ORIGINAL Word doc (Chapters 1-3)
    print("\n📄 Extracting from ORIGINAL Word document...")
    word_paras = extract_word_content("BSc-project-report-ORIGINAL.docx")
    
    if word_paras:
        # Find chapter boundaries
        chapters = {}
        current_chapter = None
        
        for para in word_paras:
            if 'فصل' in para[:20]:  # Chapter heading
                current_chapter = para
                chapters[current_chapter] = []
            elif current_chapter:
                chapters[current_chapter].append(para)
        
        print(f"✅ Found {len(chapters)} chapters in Word document")
        
        # Add to all_content
        for chapter, content in chapters.items():
            all_content.append(f"# {chapter}")
            all_content.extend(content)
            all_content.append("")  # Empty line between chapters
    else:
        print("⚠️  No content extracted from Word document")
    
    # Extract from text files (Chapters 4-7)
    text_files = [
        ("chapter4_clean.txt", "فصل ۴: ساخت کلاستر Kubernetes"),
        ("chapter5_clean.txt", "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"),
        ("chapter6_clean.txt", "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"),
        ("chapter7_clean.txt", "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده")
    ]
    
    for filename, chapter_title in text_files:
        print(f"\n📄 Extracting from {filename}...")
        paras = extract_text_file(filename)
        
        if paras:
            all_content.append(f"# {chapter_title}")
            all_content.extend(paras)
            all_content.append("")  # Empty line
            print(f"✅ Added {len(paras)} paragraphs")
        else:
            print(f"⚠️  No content from {filename}")
    
    # Save to file
    output_file = "google_docs_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))
    
    print(f"\n🎉 Content saved to: {output_file}")
    print(f"📏 Total lines: {len(all_content)}")
    print(f"📄 Total chapters: {len([c for c in all_content if c.startswith('# ')])}")
    
    # Also create HTML formatted version for easier copy-paste
    html_file = "google_docs_content.html"
    html_content = []
    
    for line in all_content:
        if line.startswith('# '):
            html_content.append(f'<h1>{line[2:]}</h1>')
        elif line:
            html_content.append(f'<p>{line}</p>')
        else:
            html_content.append('<br>')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<body>\n')
        f.write('\n'.join(html_content))
        f.write('\n</body>\n</html>')
    
    print(f"🌐 HTML version: {html_file}")
    
    return all_content

def create_copy_paste_instructions():
    """Create instructions for manual copy-paste"""
    
    print("\n" + "="*50)
    print("📋 COPY-PASTE INSTRUCTIONS")
    print("="*50)
    
    print("\n🚀 QUICK METHOD:")
    print("1. Open 'google_docs_content.html' in browser")
    print("2. Select all (Cmd+A)")
    print("3. Copy (Cmd+C)")
    print("4. Go to Google Doc")
    print("5. Paste (Cmd+V)")
    print("6. Apply formatting (see below)")
    
    print("\n🎨 FORMATTING INSTRUCTIONS:")
    print("1. Select all text (Cmd+A)")
    print("2. Set font: 'Arial' or 'B Nazanin'")
    print("3. Set size: 14pt for body, 16pt for headings")
    print("4. Justify text (Align → Justify)")
    print("5. Line spacing: 1.5")
    
    print("\n📚 CHAPTER HEADINGS:")
    print("For each '# Chapter Title' line:")
    print("   - Select the line")
    print("   - Apply 'Heading 1' style")
    print("   - Set to 16pt, bold")
    
    print("\n⏱️  ESTIMATED TIME: 10-15 minutes")
    print("\n🎯 ALTERNATIVE: I can paste directly if you grant edit access")
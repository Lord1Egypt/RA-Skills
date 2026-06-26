#!/usr/bin/env python3
"""
Fallback PDF conversion methods for Word documents
"""

import os
import sys
import subprocess
import platform

def check_system():
    """Check system and available tools"""
    system = platform.system()
    print(f"System: {system}")
    
    # Check for various conversion methods
    methods = []
    
    # Method 1: macOS built-in (textutil)
    if system == "Darwin":
        result = subprocess.run(['which', 'textutil'], capture_output=True, text=True)
        if result.returncode == 0:
            methods.append(('textutil', 'macOS built-in text conversion'))
    
    # Method 2: unoconv (LibreOffice wrapper)
    result = subprocess.run(['which', 'unoconv'], capture_output=True, text=True)
    if result.returncode == 0:
        methods.append(('unoconv', 'LibreOffice wrapper'))
    
    # Method 3: docx2pdf Python package
    result = subprocess.run(['python3', '-c', 'import docx2pdf; print("docx2pdf available")'], 
                          capture_output=True, text=True)
    if 'docx2pdf available' in result.stdout:
        methods.append(('docx2pdf', 'Python docx2pdf library'))
    
    # Method 4: AppleScript (macOS only)
    if system == "Darwin":
        methods.append(('applescript', 'macOS AppleScript with Microsoft Word'))
    
    # Method 5: Online conversion (manual)
    methods.append(('online', 'Manual online conversion'))
    
    return methods

def convert_with_textutil(input_file, output_file):
    """Convert using macOS textutil"""
    try:
        cmd = ['textutil', '-convert', 'pdf', input_file, '-output', output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Converted using textutil: {output_file}")
            return True
        else:
            print(f"❌ textutil failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error with textutil: {e}")
        return False

def convert_with_unoconv(input_file, output_file):
    """Convert using unoconv"""
    try:
        cmd = ['unoconv', '-f', 'pdf', input_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # unoconv creates file with .pdf extension
            expected_file = input_file.replace('.docx', '.pdf')
            if os.path.exists(expected_file):
                os.rename(expected_file, output_file)
                print(f"✅ Converted using unoconv: {output_file}")
                return True
        print(f"❌ unoconv failed")
        return False
    except Exception as e:
        print(f"❌ Error with unoconv: {e}")
        return False

def create_manual_conversion_guide(input_file):
    """Create guide for manual conversion"""
    guide = f"""# 📄 Manual PDF Conversion Guide

Since automatic conversion tools are not available, here are manual methods:

## Method 1: Microsoft Word (Recommended)
1. Open {input_file} in Microsoft Word
2. Go to File → Export → Create PDF/XPS
3. Choose PDF format and save

## Method 2: Online Converters
**⚠️ Warning: Only use for non-sensitive documents**
1. Go to a trusted online converter (e.g., ilovepdf.com, smallpdf.com)
2. Upload {input_file}
3. Download the converted PDF
4. **Delete** the online copy immediately

## Method 3: macOS Preview
1. Open {input_file} in Pages or TextEdit
2. Go to File → Print
3. Click "PDF" button → Save as PDF

## Method 4: Google Docs
1. Upload {input_file} to Google Drive
2. Right-click → Open with → Google Docs
3. File → Download → PDF Document

## 🔒 Security Note
For academic documents, **Method 1 (Microsoft Word)** is recommended to protect your intellectual property.
"""
    
    guide_file = "MANUAL_PDF_CONVERSION_GUIDE.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"\n📝 Manual conversion guide created: {guide_file}")
    return guide_file

def main():
    input_file = "BSc-project-report-COMPLETE.docx"
    output_file = "BSc-project-report-FINAL.pdf"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return
    
    print("🔄 Checking available PDF conversion methods...")
    methods = check_system()
    
    print(f"\n📋 Available conversion methods:")
    for i, (method, description) in enumerate(methods, 1):
        print(f"  {i}. {method}: {description}")
    
    # Try available methods in order
    success = False
    
    # Try textutil first (macOS)
    if not success:
        for method, desc in methods:
            if method == 'textutil':
                print(f"\n🔄 Trying textutil conversion...")
                success = convert_with_textutil(input_file, output_file)
                break
    
    # Try unoconv next
    if not success:
        for method, desc in methods:
            if method == 'unoconv':
                print(f"\n🔄 Trying unoconv conversion...")
                success = convert_with_unoconv(input_file, output_file)
                break
    
    # Try docx2pdf
    if not success:
        for method, desc in methods:
            if method == 'docx2pdf':
                print(f"\n🔄 Trying docx2pdf conversion...")
                try:
                    from docx2pdf import convert
                    convert(input_file, output_file)
                    if os.path.exists(output_file):
                        print(f"✅ Converted using docx2pdf: {output_file}")
                        success = True
                except Exception as e:
                    print(f"❌ docx2pdf failed: {e}")
                break
    
    if success:
        print(f"\n🎉 **SUCCESS**: PDF created: {output_file}")
        print(f"📏 File size: {os.path.getsize(output_file):,} bytes")
    else:
        print(f"\n⚠️  **No automatic conversion method worked**")
        print("Creating manual conversion guide...")
        guide = create_manual_conversion_guide(input_file)
        
        print(f"\n📋 Next steps:")
        print(f"  1. Read {guide}")
        print(f"  2. Convert {input_file} to PDF manually")
        print(f"  3. Rename the PDF to {output_file}")

if __name__ == "__main__":
    main()
import sys
import os
import markdown
from htmldocx import HtmlToDocx

def convert_md_to_docx(md_path, docx_path):
    if not os.path.exists(md_path):
        print(f"Error: File {md_path} not found.")
        return False
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # Convert HTML to DOCX
        new_parser = HtmlToDocx()
        new_parser.parse_html_string(html_content, docx_path)
        
        print(f"Successfully exported to {docx_path}")
        return True
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 export_word.py <input_md_path> <output_docx_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    convert_md_to_docx(input_path, output_path)

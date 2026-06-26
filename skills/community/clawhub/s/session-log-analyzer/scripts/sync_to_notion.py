#!/usr/bin/env python3
import os
from notion_client import Client
from nano_pdf import PDFReader

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_REPORTS_DB_ID")

def sync_report_to_notion(pdf_path):
    notion = Client(auth=NOTION_API_KEY)
    
    # Extract text from PDF
    reader = PDFReader(pdf_path)
    report_text = reader.extract_text()
    report_name = os.path.basename(pdf_path)
    
    # Create new page in Notion database
    new_page = notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties={
            "Name": {"title": [{"text": {"content": report_name}}]},
            "Status": {"select": {"name": "Generated"}},
            "Type": {"select": {"name": "Log Analysis"}}
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": report_text[:2000]}}]}
            }
        ]
    )
    
    print(f"Report synced to Notion: {new_page['url']}")
    return new_page['url']

if __name__ == "__main__":
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "pdfs", "session_analysis_report.pdf")
    if os.path.exists(pdf_path):
        sync_report_to_notion(pdf_path)
    else:
        print("Report PDF not found. Run analyze_logs.py first.")
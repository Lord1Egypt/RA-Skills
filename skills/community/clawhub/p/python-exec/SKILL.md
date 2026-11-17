# python-exec - Automated MS Office Document Creation

## Description
This skill executes Python scripts to create/write Excel, Word, or PowerPoint files using `python-docx`, `openpyxl`, and `python-pptx`. It requires Python 3.10+ and the installed libraries.

## Requirements
- Python 3.10+ installed
- Libraries: `python-docx`, `openpyxl`, `python-pptx`
- OpenClaw version 2026.7.1+

## Permissions
Moderator-approved (required for activation due to file system access).

## Example Usage
```python
# Example: Create a Word doc
from docx import Document
doc = Document()
doc.add_heading('Hello', level=1)
doc.save('output.docx')
#!/usr/bin/env python3
"""
PDF Converter
Convert Markdown reports to PDF using md-to-pdf
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path


class PDFConverter:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
        self.css_template = self._get_default_css()

    def _get_default_css(self):
        """Get default CSS for PDF styling"""

        return """@page {
  size: A4;
  margin: 2cm;
  @bottom-center {
    content: counter(page);
    font-size: 10pt;
    color: #666;
  }
}

body {
  font-family: "Noto Sans SC", "Helvetica Neue", Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.8;
  color: #333;
}

h1 {
  font-size: 24pt;
  color: #1a365d;
  border-bottom: 3px solid #3182ce;
  padding-bottom: 0.5em;
  margin-top: 1.5em;
  page-break-before: always;
}

h1:first-of-type {
  page-break-before: avoid;
}

h2 {
  font-size: 16pt;
  color: #2c5282;
  border-left: 4px solid #3182ce;
  padding-left: 1em;
  margin-top: 1.2em;
}

h3 {
  font-size: 13pt;
  color: #3182ce;
  margin-top: 1em;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 10pt;
}

th {
  background-color: #3182ce;
  color: white;
  padding: 0.8em;
  text-align: left;
  font-weight: 600;
}

td {
  border: 1px solid #e2e8f0;
  padding: 0.6em 0.8em;
}

tr:nth-child(even) {
  background-color: #f7fafc;
}

blockquote {
  border-left: 4px solid #718096;
  background-color: #f7fafc;
  padding: 1em;
  margin: 1em 0;
  font-style: italic;
}

.citation {
  font-size: 9pt;
  color: #718096;
  font-style: italic;
}

strong {
  color: #1a365d;
}

code {
  background-color: #edf2f7;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 10pt;
}

pre {
  background-color: #2d3748;
  color: #e2e8f0;
  padding: 1em;
  border-radius: 5px;
  overflow-x: auto;
}

.cover {
  text-align: center;
  padding-top: 30%;
}

.cover h1 {
  font-size: 28pt;
  border: none;
  page-break-before: avoid;
}

.cover .subtitle {
  font-size: 14pt;
  color: #4a5568;
  margin-top: 1em;
}

.cover .date {
  font-size: 12pt;
  color: #718096;
  margin-top: 2em;
}

.toc {
  page-break-after: always;
}

.toc a {
  color: #3182ce;
  text-decoration: none;
}

.footnote {
  font-size: 9pt;
  color: #718096;
  border-top: 1px solid #e2e8f0;
  margin-top: 2em;
  padding-top: 0.5em;
}

.page-break {
  page-break-before: always;
}
"""

    def check_md_to_pdf(self):
        """Check if md-to-pdf is installed"""

        try:
            result = subprocess.run(
                ["npx", "md-to-pdf", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

    def save_css_template(self, output_dir):
        """Save CSS template to output directory"""

        css_file = f"{output_dir}/report.css"

        with open(css_file, "w", encoding="utf-8") as f:
            f.write(self.css_template)

        return css_file

    def convert_to_pdf(self, md_file, output_pdf=None, css_file=None):
        """Convert Markdown file to PDF"""

        # Check md-to-pdf
        if not self.check_md_to_pdf():
            print("❌ md-to-pdf not available. Install with: npm install -g md-to-pdf")
            return None

        # Determine output path
        if output_pdf is None:
            output_pdf = md_file.replace(".md", ".pdf")

        # Get output directory
        output_dir = os.path.dirname(output_pdf)
        os.makedirs(output_dir, exist_ok=True)

        # Save CSS if not provided
        if css_file is None:
            css_file = self.save_css_template(output_dir)

        # Convert
        print(f"📄 Converting to PDF: {md_file} -> {output_pdf}")

        try:
            # Build command
            cmd = [
                "npx",
                "md-to-pdf",
                md_file,
                "--stylesheet",
                css_file,
                "--pdf-options",
                json.dumps(
                    {
                        "format": "A4",
                        "margin": {
                            "top": "2cm",
                            "bottom": "2cm",
                            "left": "2cm",
                            "right": "2cm",
                        },
                    }
                ),
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120, cwd=output_dir
            )

            if result.returncode == 0:
                # md-to-pdf creates file with same name as input
                generated_pdf = md_file.replace(".md", ".pdf")

                # Rename if different from expected
                if generated_pdf != output_pdf and os.path.exists(generated_pdf):
                    os.rename(generated_pdf, output_pdf)

                if os.path.exists(output_pdf):
                    file_size = os.path.getsize(output_pdf)
                    print(f"✅ PDF generated: {output_pdf} ({file_size / 1024:.1f} KB)")
                    return output_pdf
                else:
                    print(f"⚠️ PDF file not found after conversion")
                    return None
            else:
                print(f"⚠️ Conversion failed: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("⚠️ Conversion timeout")
            return None
        except Exception as e:
            print(f"⚠️ Conversion error: {e}")
            return None

    def convert_task_report(self, task_id, output_lang="en"):
        """Convert task report to PDF"""

        workspace = self.workspace
        output_dir = f"{workspace}/deep-research/output/{task_id}"
        md_file = f"{output_dir}/report.md"
        pdf_file = f"{output_dir}/report.pdf"

        if not os.path.exists(md_file):
            print(f"❌ Report not found: {md_file}")
            return None

        return self.convert_to_pdf(md_file, pdf_file)


def main():
    """CLI interface"""

    if len(sys.argv) < 2:
        print("Usage: python3 pdf_converter.py <command> [args]")
        print("Commands:")
        print("  convert <md_file> [pdf_file] - Convert MD to PDF")
        print("  task <task_id> [lang]         - Convert task report")
        print("  check                         - Check md-to-pdf installation")
        sys.exit(1)

    command = sys.argv[1]
    converter = PDFConverter()

    if command == "convert":
        md_file = sys.argv[2] if len(sys.argv) > 2 else None
        pdf_file = sys.argv[3] if len(sys.argv) > 3 else None

        if not md_file:
            print("Error: md_file required")
            sys.exit(1)

        result = converter.convert_to_pdf(md_file, pdf_file)
        if result:
            print(f"PDF: {result}")

    elif command == "task":
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        lang = sys.argv[3] if len(sys.argv) > 3 else "en"

        if not task_id:
            print("Error: task_id required")
            sys.exit(1)

        result = converter.convert_task_report(task_id, lang)
        if result:
            print(f"PDF: {result}")

    elif command == "check":
        if converter.check_md_to_pdf():
            print("✅ md-to-pdf is installed")
        else:
            print("❌ md-to-pdf not installed")
            print("Run: npm install -g md-to-pdf")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Document Parse + Information Extraction example.

Usage:
  python examples/document-example.py path/to/sample.pdf
"""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

import requests
from openai import OpenAI


api_key = os.environ.get("UPSTAGE_API_KEY")
if not api_key:
    raise RuntimeError("Set UPSTAGE_API_KEY before running this example.")

if len(sys.argv) < 2:
    raise SystemExit("Usage: python examples/document-example.py path/to/sample.pdf")

document_path = Path(sys.argv[1]).expanduser().resolve()
if not document_path.exists():
    raise FileNotFoundError(f"Document not found: {document_path}")

# --- Step 1: Parse document to Markdown ---
with document_path.open("rb") as f:
    parse_response = requests.post(
        "https://api.upstage.ai/v1/document-digitization",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"document": f},
        data={
            "model": "document-parse",
            "output_formats": '["markdown"]',
        },
        timeout=120,
    )
parse_response.raise_for_status()
parsed = parse_response.json()
markdown_content = parsed.get("content", {}).get("markdown", "")
print(f"Parsed pages: {parsed.get('numBilledPages', 'unknown')}")
print(f"Content preview: {markdown_content[:200]}...")

# --- Step 2: Extract structured data with IE ---
ie_client = OpenAI(
    api_key=api_key,
    base_url="https://api.upstage.ai/v1/information-extraction",
)


def encode_file(path: Path) -> str:
    with path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


base64_data = encode_file(document_path)

extraction = ie_client.chat.completions.create(
    model="information-extract",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:application/octet-stream;base64,{base64_data}"
                    },
                }
            ],
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "invoice_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "invoice_number": {
                        "type": "string",
                        "description": "Invoice number",
                    },
                    "date": {
                        "type": "string",
                        "description": "Invoice date",
                    },
                    "total_amount": {
                        "type": "string",
                        "description": "Total amount with currency",
                    },
                    "vendor_name": {
                        "type": "string",
                        "description": "Name of the vendor/company",
                    },
                    "line_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string"},
                                "amount": {"type": "string"},
                            },
                            "required": ["description", "amount"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["invoice_number", "total_amount"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
)

result = json.loads(extraction.choices[0].message.content)
print(f"\nExtracted data: {json.dumps(result, indent=2)}")

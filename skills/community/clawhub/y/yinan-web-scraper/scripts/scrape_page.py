#!/usr/bin/env python3
"""
Web Page Scraper
Extract structured data from a single web page.

Usage:
    python scrape_page.py --url "https://example.com" --fields "title=h1,price=.price" --output data.csv
"""

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

def run_agent_browser(args, timeout=60000):
    """Run agent-browser command and return output."""
    cmd = ["agent-browser"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1

def parse_fields(fields_str):
    """Parse field definitions from command line."""
    fields = {}
    for field in fields_str.split(','):
        if '=' in field:
            name, selector = field.split('=', 1)
            fields[name.strip()] = selector.strip()
        else:
            # Assume field name is also the selector
            fields[field.strip()] = field.strip()
    return fields

def extract_element_text(selector):
    """Extract text from an element using agent-browser."""
    stdout, stderr, code = run_agent_browser(["get", "text", selector])
    if code != 0:
        return None
    return stdout.strip()

def extract_element_attr(selector, attr):
    """Extract attribute from an element."""
    stdout, stderr, code = run_agent_browser(["get", "attr", selector, attr])
    if code != 0:
        return None
    return stdout.strip()

def extract_field(selector):
    """Extract field value based on selector type."""
    # Check if selector specifies an attribute (e.g., img.src, a.href)
    if '.' in selector and not selector.startswith('.'):
        parts = selector.rsplit('.', 1)
        base_selector = parts[0]
        attr = parts[1]
        return extract_element_attr(base_selector, attr)
    else:
        return extract_element_text(selector)

def scrape_page(url, fields, wait_time=0):
    """Scrape a single page."""
    print(f"Opening {url}...")
    stdout, stderr, code = run_agent_browser(["open", url])
    if code != 0:
        print(f"Error opening page: {stderr}")
        return None
    
    if wait_time > 0:
        print(f"Waiting {wait_time}s for dynamic content...")
        time.sleep(wait_time)
    
    # Get snapshot for debugging
    # stdout, stderr, code = run_agent_browser(["snapshot", "-i"])
    
    print("Extracting fields...")
    data = {}
    for field_name, selector in fields.items():
        value = extract_field(selector)
        data[field_name] = value if value else ""
        print(f"  {field_name}: {data[field_name][:50] if data[field_name] else 'N/A'}...")
    
    data['_scraped_at'] = datetime.now().isoformat()
    data['_url'] = url
    
    return data

def save_data(data_list, output_path, format='csv'):
    """Save scraped data to file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved JSON to {output_path}")
    
    elif format == 'csv':
        if not data_list:
            print("No data to save")
            return
        
        fieldnames = list(data_list[0].keys())
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_list)
        print(f"✓ Saved CSV to {output_path}")
    
    elif format == 'xlsx':
        try:
            import openpyxl
            from openpyxl import Workbook
            
            wb = Workbook()
            ws = wb.active
            
            if data_list:
                # Headers
                headers = list(data_list[0].keys())
                ws.append(headers)
                
                # Data rows
                for item in data_list:
                    ws.append([item.get(h, '') for h in headers])
                
                # Auto-fit columns (basic)
                for col in ws.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    adjusted_width = min(max_length + 2, 50)
                    ws.column_dimensions[column].width = adjusted_width
            
            wb.save(output_path)
            print(f"✓ Saved Excel to {output_path}")
        except ImportError:
            print("openpyxl not installed, saving as CSV instead")
            save_data(data_list, output_path.with_suffix('.csv'), 'csv')
    
    else:
        print(f"Unknown format: {format}")

def main():
    parser = argparse.ArgumentParser(description='Scrape data from a web page')
    parser.add_argument('--url', required=True, help='Target URL')
    parser.add_argument('--fields', required=True, 
                        help='Field definitions (name=selector,name2=selector2)')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--format', choices=['csv', 'json', 'xlsx'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--wait', type=int, default=0,
                        help='Wait time for dynamic content (seconds)')
    args = parser.parse_args()
    
    # Parse fields
    fields = parse_fields(args.fields)
    print(f"Fields to extract: {list(fields.keys())}")
    print()
    
    # Scrape
    data = scrape_page(args.url, fields, args.wait)
    
    if data:
        # Save
        save_data([data], args.output, args.format)
        print("\n✅ Scraping complete!")
        return 0
    else:
        print("\n❌ Scraping failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())

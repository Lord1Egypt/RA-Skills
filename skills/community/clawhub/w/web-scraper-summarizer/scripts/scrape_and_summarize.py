#!/usr/bin/env python3
"""
Web Scraper & Summarizer
Fetches web pages and generates summaries using Ollama LLM.
Usage: python scrape_and_summarize.py <url> [summary_style] [headings]
  url          - Web page URL to scrape
  summary_style - 'brief', 'detailed', or 'bullet' (default: brief)
  headings     - Number of top headings to extract (default: 5)
"""

import sys
import json
import subprocess
import os

def fetch_page(url):
    """Fetch web page content using curl."""
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
             '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout
    except Exception as e:
        return None

def count_tokens(text):
    """Rough estimate of token count."""
    return len(text) // 4

def truncate_to_limit(text, max_tokens=4096):
    """Truncate text to approximate token limit."""
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[Content truncated due to length...]"
    return text

def build_prompt(content, style, num_headings):
    """Build summarization prompt based on style."""
    
    style_instructions = {
        'brief': "Provide a 2-3 sentence summary capturing the main topic and key takeaways.",
        'detailed': "Provide a comprehensive summary with:\n- Main topic and purpose\n- Key points and arguments (bullet format)\n- Important details and data\n- Conclusions or takeaways",
        'bullet': "Summarize as bullet points:\n- Main topic\n- 5-7 key points\n- Any important data or numbers\n- Conclusions"
    }
    
    instruction = style_instructions.get(style, style_instructions['brief'])
    
    return f"""You are a content analyzer. Analyze the following web page content and provide a summary.

{instruction}

Output in plain text (no markdown formatting needed for brief/detailed, use - for bullets).

WEB PAGE CONTENT:
{content}

SUMMARY:"""

def summarize_with_ollama(content, style):
    """Send content to Ollama for summarization."""
    prompt = build_prompt(content, style, 5)
    
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', prompt],
            capture_output=True,
            text=True,
            timeout=120,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None

def extract_title(html):
    """Extract page title from HTML."""
    import re
    match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    return match.group(1).strip() if match else "Untitled Page"

def clean_html(html):
    """Remove HTML tags, keep readable text."""
    import re
    # Remove script and style elements
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
    # Remove HTML tags
    html = re.sub(r'<[^>]+>', ' ', html)
    # Decode HTML entities
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    html = html.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    # Normalize whitespace
    html = re.sub(r'\s+', ' ', html)
    return html.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: scrape_and_summarize.py <url> [style] [headings]")
        print("  url   - Web page URL")
        print("  style - 'brief', 'detailed', or 'bullet' (default: brief)")
        sys.exit(1)
    
    url = sys.argv[1]
    style = sys.argv[2] if len(sys.argv) > 2 else 'brief'
    
    print(f"Fetching: {url}", file=sys.stderr)
    
    html = fetch_page(url)
    if not html:
        print("Error: Failed to fetch page", file=sys.stderr)
        sys.exit(1)
    
    title = extract_title(html)
    content = clean_html(html)
    
    if not content or len(content) < 100:
        print("Error: Page content too short or empty", file=sys.stderr)
        sys.exit(1)
    
    # Truncate if very long
    content = truncate_to_limit(content)
    
    print(f"Page: {title}", file=sys.stderr)
    print(f"Content length: {len(content)} chars", file=sys.stderr)
    print(f"Generating {style} summary...", file=sys.stderr)
    
    summary = summarize_with_ollama(content, style)
    
    if summary:
        print("\n=== SUMMARY ===")
        print(summary)
    else:
        print("\nError: Failed to generate summary with Ollama", file=sys.stderr)
        print("\n=== PAGE CONTENT (raw) ===")
        print(content[:2000] + "\n...[content truncated]..." if len(content) > 2000 else content)
        sys.exit(1)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Output formatter - Convert OCR results to various formats
"""

import json
from typing import Dict, List


def format_text(result: Dict) -> str:
    """Return clean text only"""
    return result.get('text', '')


def format_json(result: Dict) -> str:
    """Return full JSON output"""
    return json.dumps(result, ensure_ascii=False, indent=2)


def format_structured(result: Dict) -> str:
    """
    Return structured format with key information highlighted.
    
    Format:
    ---
    Text: [extracted text]
    
    Stats:
    - Engine: [engine used]
    - Confidence: [score]
    - Time: [processing time]
    - Lines: [line count]
    ---
    """
    text = result.get('text', '')
    engine = result.get('engine', 'unknown')
    confidence = result.get('confidence', 0)
    time_ms = result.get('processing_time_ms', 0)
    line_count = result.get('line_count', len(text.split('\n')))
    
    # Truncate long text
    display_text = text
    if len(text) > 500:
        display_text = text[:500] + '\n... (truncated)'
    
    output = [
        "---",
        "Text:",
        display_text,
        "",
        "Stats:",
        f"- Engine: {engine}",
        f"- Confidence: {confidence:.2%}" if isinstance(confidence, (int, float)) else f"- Confidence: N/A",
        f"- Time: {time_ms:.2f}ms",
        f"- Lines: {line_count}",
        "---"
    ]
    
    return '\n'.join(output)


def format_verbose(result: Dict) -> str:
    """Return all available information"""
    output = [
        "=" * 60,
        "OCR Result (Verbose)",
        "=" * 60,
        f"Engine: {result.get('engine', 'N/A')}",
        f"Confidence: {result.get('confidence', 0):.4f}",
        f"Processing Time: {result.get('processing_time_ms', 0):.2f}ms",
    ]
    
    # Error info
    if 'error' in result and result['error']:
        output.extend([
            "",
            "ERROR:",
            result['error'],
        ])
    
    # Text
    output.extend([
        "",
        "Extracted Text:",
        "-" * 40,
        result.get('text', ''),
        "-" * 40,
    ])
    
    # Detailed results (if available)
    if 'results' in result and result['results']:
        output.extend([
            "",
            "Detailed Results:",
            f"{'Text':<30} | {'Confidence':<12} | {'BBox'}"
        ])
        
        for item in result['results'][:20]:  # Limit to 20 lines
            text = item.get('text', '')[:28]
            confidence = item.get('confidence', 0)
            bbox = str(item.get('bbox', []))
            
            output.append(f"{text:<30} | {confidence:<12.4f} | {bbox}")
    
    output.append("=" * 60)
    
    return '\n'.join(output)


# Format registry
FORMATTERS = {
    'text': format_text,
    'json': format_json,
    'structured': format_structured,
    'verbose': format_verbose
}


def format_output(format_name: str):
    """Get formatter function by name"""
    return FORMATTERS.get(format_name, format_json)


def get_available_formats() -> List[str]:
    """Return list of available output formats"""
    return list(FORMATTERS.keys())


if __name__ == '__main__':
    # Test formatter
    test_result = {
        'text': '这是一个测试\nAnother line',
        'engine': 'paddle',
        'confidence': 0.95,
        'processing_time_ms': 123.45,
        'line_count': 2
    }
    
    for fmt in get_available_formats():
        print(f"\n{'#'*60}")
        print(f"Format: {fmt}")
        print('#'*60)
        print(format_output(fmt)(test_result))
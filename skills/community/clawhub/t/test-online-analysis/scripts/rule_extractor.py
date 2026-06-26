#!/usr/bin/env python3
"""
Rule Extractor for Online Analysis Skill
Extracts business rules and implicit logic from structured data streams
"""

import json
import re
from typing import List, Dict, Any
from datetime import datetime

class RuleExtractor:
    def __init__(self):
        self.rules = []
        self.patterns = {
            'amount_limit': r'amount.*(greater than|less than|equal to|exceeds|below)\s*(\d+\.?\d*)',
            'time_constraint': r'(before|after|between)\s*(\d{1,2}:\d{2})',
            'status_transition': r'(status|state).*from\s*(\w+)\s*to\s*(\w+)',
            'validation': r'(must|should|required|cannot|must not)\s*(\w+.*?)\.',
        }
    
    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract rules from plain text/logs"""
        extracted = []
        
        for rule_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                rule = {
                    'type': rule_type,
                    'condition': match.group(0),
                    'extracted_at': datetime.now().isoformat(),
                    'confidence': 0.8 if len(match.groups()) > 1 else 0.6
                }
                extracted.append(rule)
        
        self.rules.extend(extracted)
        return extracted
    
    def extract_from_json(self, data: List[Dict]) -> List[Dict[str, Any]]:
        """Extract rules from structured JSON data"""
        extracted = []
        
        # Field value range analysis
        fields = {}
        for entry in data:
            for key, value in entry.items():
                if key not in fields:
                    fields[key] = {'types': set(), 'values': set()}
                fields[key]['types'].add(type(value).__name__)
                if isinstance(value, (int, float, str)) and len(str(value)) < 100:
                    fields[key]['values'].add(value)
        
        # Generate rules from field analysis
        for field, stats in fields.items():
            if len(stats['types']) == 1:
                extracted.append({
                    'type': 'field_type',
                    'condition': f"{field} must be of type {stats['types'].pop()}",
                    'confidence': 1.0
                })
            
            if len(stats['values']) > 0 and len(stats['values']) < 10:
                extracted.append({
                    'type': 'field_enum',
                    'condition': f"{field} must be one of: {', '.join(map(str, stats['values']))}",
                    'confidence': 0.9
                })
        
        self.rules.extend(extracted)
        return extracted
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all extracted rules"""
        return sorted(self.rules, key=lambda x: x['confidence'], reverse=True)
    
    def export_markdown(self) -> str:
        """Export rules as markdown document"""
        md = "# Extracted Business Rules\n\n"
        md += f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += "| Rule Type | Condition | Confidence |\n"
        md += "|-----------|-----------|------------|\n"
        
        for rule in self.get_rules():
            md += f"| {rule['type']} | {rule['condition']} | {rule['confidence']:.1f} |\n"
        
        return md

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python rule_extractor.py <input_file>")
        sys.exit(1)
    
    extractor = RuleExtractor()
    
    with open(sys.argv[1], 'r') as f:
        if sys.argv[1].endswith('.json'):
            data = json.load(f)
            rules = extractor.extract_from_json(data)
        else:
            text = f.read()
            rules = extractor.extract_from_text(text)
    
    print(extractor.export_markdown())

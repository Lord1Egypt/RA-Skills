#!/usr/bin/env python3
"""
Helper script to generate tech analysis reports.
Converts structured content into formatted Markdown for DOCX conversion.
"""

import json
import sys
from datetime import datetime

def generate_report(data):
    """
    Generate a structured report from analysis data.
    
    Args:
        data: Dictionary containing:
            - person_name: str
            - affiliation: str
            - title: str
            - achievements: list
            - core_tech: dict with 'innovations', 'methodologies', 'validation', 'impact'
            - domestic_teams: list of dicts with 'name', 'focus', 'progress'
            - international_teams: list of dicts with 'name', 'focus', 'progress'
            - uniqueness: list
            - landscape_summary: str
    
    Returns:
        Markdown formatted report string
    """
    
    report = f"""# {data['person_name']} Technical Analysis Report

## 1. Person Profile

**Name:** {data['person_name']}  
**Affiliation:** {data['affiliation']}  
**Title:** {data['title']}

### Key Achievements
"""
    
    for achievement in data.get('achievements', []):
        report += f"- {achievement}\n"
    
    report += """
## 2. Core Technical Advantages

### 2.1 Breakthrough Innovations
"""
    
    for innovation in data['core_tech'].get('innovations', []):
        report += f"- {innovation}\n"
    
    report += """
### 2.2 Key Methodologies
"""
    
    for method in data['core_tech'].get('methodologies', []):
        report += f"- {method}\n"
    
    report += """
### 2.3 Performance Validation
"""
    
    for validation in data['core_tech'].get('validation', []):
        report += f"- {validation}\n"
    
    report += """
### 2.4 Academic & Industrial Impact
"""
    
    for impact in data['core_tech'].get('impact', []):
        report += f"- {impact}\n"
    
    # Domestic Teams
    report += """
## 3. Competitive Landscape Analysis

### 3.1 Domestic Teams (China)

| Organization | Research Focus | Key Progress |
|--------------|----------------|--------------|
"""
    
    for team in data.get('domestic_teams', []):
        report += f"| {team['name']} | {team['focus']} | {team['progress']} |\n"
    
    # International Teams
    report += """
### 3.2 International Teams

| Organization | Research Focus | Key Progress |
|--------------|----------------|--------------|
"""
    
    for team in data.get('international_teams', []):
        report += f"| {team['name']} | {team['focus']} | {team['progress']} |\n"
    
    # Summary
    report += """
## 4. Comparative Summary

### 4.1 Target Person's Uniqueness
"""
    
    for item in data.get('uniqueness', []):
        report += f"- {item}\n"
    
    report += f"""
### 4.2 Domestic vs International Landscape

{data.get('landscape_summary', '')}

### 4.3 Technology Trajectory

[Analysis of future directions and trends]

---

*Report generated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    return report


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
        print(generate_report(data))
    else:
        print("Usage: python3 generate_report.py <data.json>")
        sys.exit(1)

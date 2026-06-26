#!/usr/bin/env python3
import json
import os
from collections import defaultdict
from nano_pdf import PDFGenerator

def analyze_logs(log_file_path):
    stats = defaultdict(int)
    skill_usage = defaultdict(int)
    errors = []
    total_duration = 0
    session_count = 0
    
    with open(log_file_path, 'r') as f:
        for line in f:
            entry = json.loads(line.strip())
            if entry['event'] == 'session_start':
                session_count += 1
            if entry['event'] == 'skill_invocation':
                skill_usage[entry['skill_used']] += 1
                if entry['success']:
                    stats['successful_skills'] += 1
                else:
                    stats['failed_skills'] += 1
                    errors.append(entry)
            total_duration += entry.get('duration', 0)
    
    report = {
        'total_sessions': session_count,
        'total_skill_invocations': sum(skill_usage.values()),
        'successful_skills': stats['successful_skills'],
        'failed_skills': stats['failed_skills'],
        'success_rate': (stats['successful_skills'] / sum(skill_usage.values()) * 100) if sum(skill_usage.values()) > 0 else 0,
        'total_duration_hours': round(total_duration / 3600, 2),
        'skill_breakdown': dict(skill_usage),
        'recent_errors': errors
    }
    
    return report

def generate_pdf_report(report, output_path):
    pdf = PDFGenerator()
    pdf.add_title("Agent Session Log Analysis Report")
    pdf.add_heading("Summary Statistics")
    pdf.add_paragraph(f"Total Sessions: {report['total_sessions']}")
    pdf.add_paragraph(f"Total Skill Invocations: {report['total_skill_invocations']}")
    pdf.add_paragraph(f"Successful Skills: {report['successful_skills']}")
    pdf.add_paragraph(f"Failed Skills: {report['failed_skills']}")
    pdf.add_paragraph(f"Success Rate: {report['success_rate']:.1f}%")
    pdf.add_paragraph(f"Total Duration: {report['total_duration_hours']} hours")
    
    pdf.add_heading("Skill Usage Breakdown")
    for skill, count in report['skill_breakdown'].items():
        pdf.add_paragraph(f"{skill}: {count} invocations")
    
    if report['recent_errors']:
        pdf.add_heading("Recent Errors")
        for error in report['recent_errors']:
            pdf.add_paragraph(f"Session {error['session_id']}: {error['error']} at {error['timestamp']}")
    
    pdf.output(output_path)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(__file__), "..", "session_logs", "sample_logs.jsonl")
    report = analyze_logs(log_file)
    pdf_dir = os.path.join(os.path.dirname(__file__), "..", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    generate_pdf_report(report, os.path.join(pdf_dir, "session_analysis_report.pdf"))
    print("Analysis complete!")
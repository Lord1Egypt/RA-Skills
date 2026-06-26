#!/usr/bin/env python3
"""
Optimize keyword usage for ATS (Applicant Tracking System) systems.
Analyze keyword density, suggest improvements.
"""

import argparse
import json
import sys
import os
import re
from collections import Counter

def load_json(file_path):
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_keywords_from_jd(jd_data):
    """Extract keywords from JD data."""
    keywords = []
    
    # Add required and preferred skills
    keywords.extend(jd_data.get("required_skills", []))
    keywords.extend(jd_data.get("preferred_skills", []))
    keywords.extend(jd_data.get("keywords", []))
    
    # Extract from raw text (simplified)
    raw_text = jd_data.get("raw_text", "")
    if raw_text:
        # Common skill patterns
        skill_patterns = [
            r'\b(?:Python|Java|JavaScript|C\+\+|SQL|R|MATLAB)\b',
            r'\b(?:Machine Learning|Deep Learning|Data Science|AI|Aritificial Intelligence)\b',
            r'\b(?:React|Vue|Angular|Node\.js|Django|Flask|Spring)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|CI/CD)\b',
            r'\b(?:Git|Linux|Unix|Windows|MacOS)\b',
            r'\b(?:Communication|Leadership|Teamwork|Problem Solving|Critical Thinking)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            keywords.extend(matches)
    
    # Remove duplicates and return
    return list(set([k.strip() for k in keywords if k.strip()]))

def calculate_keyword_density(text, keywords):
    """
    Calculate keyword density in text.
    Returns: dictionary of keyword -> density percentage
    """
    # Clean text
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = clean_text.split()
    total_words = len(words)
    
    if total_words == 0:
        return {}
    
    density = {}
    for keyword in keywords:
        keyword_lower = keyword.lower()
        
        # Count occurrences (whole word match)
        pattern = r'\b' + re.escape(keyword_lower) + r'\b'
        count = len(re.findall(pattern, text.lower()))
        
        # Calculate density
        density[keyword] = (count / total_words) * 100
    
    return density

def find_synonyms(keyword):
    """
    Find synonyms for keyword expansion.
    Simplified version - in production, use NLP libraries like NLTK or WordNet.
    """
    # Common synonyms mapping (simplified)
    synonyms_map = {
        "Python": ["PY", "Python3", "python"],
        "JavaScript": ["JS", "Javascript", "ECMAScript"],
        "Machine Learning": ["ML", "machine-learning", "predictive modeling"],
        "Data Science": ["data analysis", "data analytics", "data mining"],
        "React": ["React.js", "ReactJS", "React Native"],
        "Communication": ["written communication", "verbal communication", "interpersonal skills"],
        "Leadership": ["team leadership", "people management", "leading teams"]
    }
    
    return synonyms_map.get(keyword, [])

def optimize_resume_keywords(resume_data, jd_keywords, target_density=2.0, use_synonyms=False):
    """
    Optimize keyword usage in resume.
    Returns optimized resume data and optimization report.
    """
    optimized = resume_data.copy()
    report = {
        "keywords_analyzed": jd_keywords,
        "original_density": {},
        "optimized_density": {},
        "suggestions": [],
        "keywords_added": [],
        "synonyms_used": {}
    }
    
    # Get resume text
    resume_text = resume_data.get("raw_text", "")
    if not resume_text:
        # Reconstruct from structured data
        resume_text = json.dumps(resume_data, ensure_ascii=False)
    
    # Calculate original density
    original_density = calculate_keyword_density(resume_text, jd_keywords)
    report["original_density"] = original_density
    
    # Identify low-density keywords
    low_density_keywords = []
    for keyword, density in original_density.items():
        if density < target_density:
            low_density_keywords.append(keyword)
            report["suggestions"].append({
                "keyword": keyword,
                "current_density": density,
                "target_density": target_density,
                "suggestion": f"Add more instances of '{keyword}' (current: {density:.2f}%, target: {target_density}%)"
            })
    
    # Add synonyms if requested
    if use_synonyms:
        for keyword in low_density_keywords:
            synonyms = find_synonyms(keyword)
            if synonyms:
                report["synonyms_used"][keyword] = synonyms
    
    # --- Identify optimal locations to insert keywords ---
    # Priority locations for keyword placement:
    # 1. Skills section (highest priority)
    # 2. Summary (high priority)
    # 3. Work experience bullet points (medium priority)
    # 4. Projects (lower priority)
    
    # Add missing keywords to skills section (highest impact for ATS)
    current_skills = optimized.get("skills", [])
    for keyword in jd_keywords:
        if keyword not in current_skills and keyword not in [s.lower() for s in current_skills]:
            current_skills.append(keyword)
            report["keywords_added"].append(keyword)
    optimized["skills"] = current_skills
    
    # --- Enrich summary with key missing keywords ---
    if optimized.get("summary") and low_density_keywords:
        top_missing = low_density_keywords[:3]
        summary = optimized["summary"]
        # Check if keywords are already naturally in summary
        summary_lower = summary.lower()
        to_add = [kw for kw in top_missing if kw.lower() not in summary_lower]
        if to_add:
            if summary.rstrip().endswith('.'):
                summary = summary.rstrip()[:-1]
            optimized["summary"] = f"{summary}. Experienced in {', '.join(to_add)}."
    
    # --- Rewrite work experience to naturally include keywords ---
    if optimized.get("work_experience"):
        for exp in optimized["work_experience"]:
            if exp.get("description"):
                bullets = exp["description"].split('\n')
                enriched_bullets = []
                for bullet in bullets:
                    bullet = bullet.strip()
                    if not bullet:
                        continue
                    # Check if any low-density keyword can be naturally woven in
                    for keyword in low_density_keywords:
                        kw_lower = keyword.lower()
                        # Only add if keyword not already present and bullet is relevant
                        if kw_lower not in bullet.lower():
                            # Check if bullet context is related to keyword
                            tech_keywords = ['python', 'java', 'sql', 'aws', 'react', 'docker', 
                                           'kubernetes', 'machine learning', 'data', 'api']
                            if any(tk in bullet.lower() for tk in tech_keywords) and \
                               any(tk in kw_lower for tk in tech_keywords):
                                # Weave keyword naturally
                                if bullet.endswith('.'):
                                    bullet = bullet[:-1]
                                bullet = f"{bullet} using {keyword}."
                                break
                    enriched_bullets.append(bullet)
                exp["description"] = '\n'.join(enriched_bullets[:5])  # Keep top 5 most relevant
    
    # Recalculate density
    optimized_text = json.dumps(optimized, ensure_ascii=False)
    optimized_density = calculate_keyword_density(optimized_text, jd_keywords)
    report["optimized_density"] = optimized_density
    
    return optimized, report

def main():
    parser = argparse.ArgumentParser(description='Optimize keyword usage for ATS systems.')
    parser.add_argument('--resume', required=True, help='Input resume JSON file')
    parser.add_argument('--jd', required=True, help='Input JD JSON file')
    parser.add_argument('--output', required=True, help='Output optimized resume JSON file')
    parser.add_argument('--density', type=float, default=2.0, help='Target keyword density percentage (default: 2.0%)')
    parser.add_argument('--synonyms', action='store_true', help='Use synonym expansion')
    
    args = parser.parse_args()
    
    # Load input files
    if not os.path.exists(args.resume):
        print(f"Error: Resume file not found: {args.resume}")
        sys.exit(1)
    if not os.path.exists(args.jd):
        print(f"Error: JD file not found: {args.jd}")
        sys.exit(1)
    
    resume_data = load_json(args.resume)
    jd_data = load_json(args.jd)
    
    # Extract keywords from JD
    jd_keywords = extract_keywords_from_jd(jd_data)
    print(f"Extracted {len(jd_keywords)} keywords from JD")
    
    # Optimize resume
    optimized, report = optimize_resume_keywords(
        resume_data,
        jd_keywords,
        target_density=args.density,
        use_synonyms=args.synonyms
    )
    
    # Save optimized resume
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(optimized, f, ensure_ascii=False, indent=2)
    
    # Print report
    print(f"\nKeyword Optimization Report:")
    print(f"=" * 50)
    print(f"Keywords Analyzed: {len(report['keywords_analyzed'])}")
    print(f"Keywords Added: {len(report['keywords_added'])}")
    print(f"\nTop Suggestions:")
    for i, suggestion in enumerate(report["suggestions"][:5], 1):
        print(f"{i}. {suggestion['suggestion']}")
    
    if report["synonyms_used"]:
        print(f"\nSynonyms Used:")
        for keyword, synonyms in report["synonyms_used"].items():
            print(f"  {keyword}: {', '.join(synonyms)}")
    
    print(f"\nOptimized resume saved to: {args.output}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Customize resume based on JD analysis.
Tailor content to match job description, optimize for ATS systems.
"""

import argparse
import json
import sys
import os
from difflib import SequenceMatcher

def load_json(file_path):
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_similarity(str1, str2):
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def match_skills(resume_skills, jd_skills, threshold=0.7):
    """
    Match skills between resume and JD.
    Returns: matching_skills, missing_skills, additional_skills
    """
    matching = []
    missing = []
    additional = []
    
    # Normalize skills to lowercase for matching
    resume_skills_lower = [s.lower() for s in resume_skills]
    jd_skills_lower = [s.lower() for s in jd_skills]
    
    # Find matching and missing skills
    for jd_skill in jd_skills:
        jd_skill_lower = jd_skill.lower()
        found = False
        
        for resume_skill in resume_skills:
            resume_skill_lower = resume_skill.lower()
            similarity = calculate_similarity(resume_skill, jd_skill)
            
            if similarity >= threshold or jd_skill_lower in resume_skill_lower or resume_skill_lower in jd_skill_lower:
                matching.append({
                    "jd_skill": jd_skill,
                    "resume_skill": resume_skill,
                    "similarity": similarity
                })
                found = True
                break
        
        if not found:
            missing.append(jd_skill)
    
    # Find additional skills (in resume but not in JD)
    for resume_skill in resume_skills:
        resume_skill_lower = resume_skill.lower()
        found = False
        
        for jd_skill in jd_skills:
            similarity = calculate_similarity(resume_skill, jd_skill)
            if similarity >= threshold or resume_skill_lower in jd_skill.lower() or jd_skill.lower() in resume_skill_lower:
                found = True
                break
        
        if not found:
            additional.append(resume_skill)
    
    return matching, missing, additional

def customize_resume(resume_data, jd_data, match_threshold=0.7, ats_optimize=False, industry=None):
    """
    Customize resume based on JD analysis.
    """
    # Analyze skill match
    resume_skills = resume_data.get("skills", [])
    jd_skills = jd_data.get("required_skills", []) + jd_data.get("preferred_skills", [])
    
    matching, missing, additional = match_skills(resume_skills, jd_skills, match_threshold)
    
    # Create customized resume
    customized = resume_data.copy()
    
    # Add customization metadata
    customized["customization"] = {
        "jd_title": jd_data.get("job_title", ""),
        "jd_company": jd_data.get("company", ""),
        "match_analysis": {
            "matching_skills": matching,
            "missing_skills": missing,
            "additional_skills": additional,
            "match_percentage": len(matching) / len(jd_skills) * 100 if jd_skills else 0
        },
        "ats_optimized": ats_optimize,
        "industry": industry
    }
    
    # --- 1. Reorder sections based on JD priorities ---
    # Bring most relevant sections forward: skills first if JD is skill-heavy
    if jd_skills and len(jd_skills) > 5:
        customized["_section_order"] = ["contact", "summary", "skills", "work_experience", "education", "projects", "certifications"]
    else:
        customized["_section_order"] = ["contact", "summary", "work_experience", "education", "skills", "projects", "certifications"]
    
    # --- 2. Reorder skills to put matching ones first ---
    if customized.get("skills"):
        all_skills = customized["skills"]
        matched_skill_names = [m["resume_skill"] for m in matching]
        matched_first = [s for s in matched_skill_names if s in all_skills]
        remaining = [s for s in all_skills if s not in matched_skill_names]
        customized["skills"] = matched_first + remaining
    
    # --- 3. Adjust summary/objective to align with JD ---
    jd_title = jd_data.get("job_title", "")
    jd_company = jd_data.get("company", "")
    jd_keywords = jd_data.get("keywords", [])
    
    if customized.get("summary"):
        summary = customized["summary"]
        matched_keywords = [m["jd_skill"] for m in matching[:5]]
        # Remove trailing period if exists for clean join
        if summary.rstrip().endswith('.'):
            summary = summary.rstrip()[:-1]
        if matched_keywords:
            customized["summary"] = f"{summary}. Proficient in {', '.join(matched_keywords)}."
    
    # --- 4. Prioritize work experience bullet points ---
    if customized.get("work_experience"):
        for exp in customized["work_experience"]:
            if exp.get("description"):
                bullets = exp["description"].split('\n')
                scored_bullets = []
                for bullet in bullets:
                    score = 0
                    bullet_lower = bullet.lower()
                    for m in matching:
                        if m["jd_skill"].lower() in bullet_lower:
                            score += 1
                    for kw in jd_keywords:
                        if kw.lower() in bullet_lower:
                            score += 0.5
                    scored_bullets.append((score, bullet))
                # Sort by relevance score descending, keep top bullets
                scored_bullets.sort(key=lambda x: x[0], reverse=True)
                exp["description"] = '\n'.join([b for _, b in scored_bullets if b.strip()])
    
    # --- 5. Enrich work experience with JD keywords ---
    jd_responsibilities = jd_data.get("responsibilities", [])
    if jd_responsibilities and customized.get("work_experience"):
        # Add a note about relevant experience matching JD responsibilities
        customized["_jd_alignment_notes"] = {
            "target_role": jd_title,
            "target_company": jd_company,
            "key_responsibilities_matched": jd_responsibilities[:3]
        }
    
    # --- 6. Highlight missing skills section ---
    if missing:
        customized["_skill_gaps"] = {
            "missing_from_jd": missing,
            "recommendation": "Consider adding these skills if you have experience with them, even if informal."
        }
    
    # --- 7. ATS optimization ---
    if ats_optimize:
        customized["_ats_optimized"] = True
        # Standardize section headings
        customized["_section_headings"] = {
            "summary": "Professional Summary",
            "work_experience": "Work Experience",
            "education": "Education",
            "skills": "Skills",
            "projects": "Projects",
            "certifications": "Certifications"
        }
        # Add ATS formatting guidance
        customized["_ats_guidelines"] = {
            "font": "Arial or Calibri, 10-12pt",
            "layout": "Single column, left-aligned",
            "file_format": "Save as .docx or text-based .pdf",
            "avoid": ["Tables", "Text boxes", "Graphics", "Headers/footers for key info"]
        }
    
    return customized

def main():
    parser = argparse.ArgumentParser(description='Customize resume based on JD analysis.')
    parser.add_argument('--resume', required=True, help='Input resume JSON file')
    parser.add_argument('--jd', required=True, help='Input JD JSON file')
    parser.add_argument('--output', required=True, help='Output customized resume JSON file')
    parser.add_argument('--match-threshold', type=float, default=0.7, help='Skill matching threshold (0.0-1.0)')
    parser.add_argument('--ats-optimize', action='store_true', help='Apply ATS optimization')
    parser.add_argument('--industry', help='Industry for industry-specific customization')
    
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
    
    # Customize resume
    customized = customize_resume(
        resume_data,
        jd_data,
        match_threshold=args.match_threshold,
        ats_optimize=args.ats_optimize,
        industry=args.industry
    )
    
    # Save output
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(customized, f, ensure_ascii=False, indent=2)
    
    # Print summary
    match_pct = customized["customization"]["match_analysis"]["match_percentage"]
    print(f"Resume customized successfully. Output saved to: {args.output}")
    print(f"Match Analysis:")
    print(f"  - Matching Skills: {len(customized['customization']['match_analysis']['matching_skills'])}")
    print(f"  - Missing Skills: {len(customized['customization']['match_analysis']['missing_skills'])}")
    print(f"  - Match Percentage: {match_pct:.1f}%")
    
    if customized["customization"]["match_analysis"]["missing_skills"]:
        print(f"\nMissing Skills (consider adding if you have them):")
        for skill in customized["customization"]["match_analysis"]["missing_skills"][:5]:
            print(f"  - {skill}")

if __name__ == '__main__':
    main()

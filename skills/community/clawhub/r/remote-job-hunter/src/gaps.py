#!/usr/bin/env python3
"""
gaps.py — Skill gap analysis + upskill recommendations.
"""
from collections import Counter

def analyze_gaps(jobs, known_skills):
    all_required = Counter()
    missing = Counter()
    jobs_with_desc = 0

    for job in jobs:
        job_skills = job.get("job_skills", set())
        if not job_skills:
            continue
        jobs_with_desc += 1
        for skill in job_skills:
            all_required[skill] += 1
            if skill not in known_skills:
                missing[skill] += 1

    # Categorise gaps by effort level
    quick_wins = []
    medium = []
    long_term = []

    quick_win_keywords = [
        "git", "sql", "postman", "jira", "agile", "scrum",
        "github actions", "rest api", "graphql", "docker"
    ]
    long_term_keywords = [
        "rust", "scala", "spark", "hadoop", "kubernetes",
        "machine learning", "deep learning", "llm", "rag"
    ]

    for skill, count in missing.most_common(15):
        if skill in quick_win_keywords:
            quick_wins.append((skill, count))
        elif skill in long_term_keywords:
            long_term.append((skill, count))
        else:
            medium.append((skill, count))

    return {
        "jobs_analysed": jobs_with_desc,
        "top_required": all_required.most_common(10),
        "top_missing": missing.most_common(10),
        "quick_wins": quick_wins[:5],
        "medium": medium[:5],
        "long_term": long_term[:5]
    }

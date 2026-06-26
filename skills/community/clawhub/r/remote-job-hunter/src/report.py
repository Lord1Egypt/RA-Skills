
def sanitize(text):
    """Strip any content that could be used for prompt injection."""
    import re
    if not text:
        return text
    # Remove anything that looks like an instruction or command
    text = re.sub(r'(?i)(ignore previous|disregard|new instruction|system prompt|forget|override)', '[removed]', text)
    return text[:500]  # Cap field lengths

#!/usr/bin/env python3
"""
report.py — Generates daily_report.md from scored jobs + gap analysis.
"""
import datetime
import re

def generate_report(jobs, gap_analysis, profile_config, profile_meta, output_path):
    today = datetime.date.today().strftime("%a, %b %d %Y")
    label = profile_meta.get("label", "Job Search")
    salary_min = profile_config.get("salary_min_usd", 0)
    salary_filter = profile_meta.get("salary_filter_enabled", False)
    salary_note = f"${salary_min//1000}K+" if salary_filter else "All (negotiate)"

    lines = [
        f"# Daily Job Report — {today}\n",
        f"**Profile:** {label}",
        f"**Total matches found:** {len(jobs)}",
        f"**Platforms searched:** Remotive + Jobicy + RemoteOK + WeWorkRemotely + Himalayas",
        f"**Salary filter:** {salary_note}\n",
        "---\n",
        "## 🎯 Skill Gap Analysis\n",
        f"*Based on {gap_analysis['jobs_analysed']} job descriptions analysed*\n",
        "### Most In-Demand Skills"
    ]

    for skill, count in gap_analysis["top_required"]:
        known = gap_analysis.get("known_skills", set())
        indicator = "✅" if skill in known else "❌"
        lines.append(f"- {indicator} **{skill.title()}** — {count} job(s)")

    lines.append("\n### ⚠️ Skills to Upskill")
    if gap_analysis["top_missing"]:
        if gap_analysis["quick_wins"]:
            lines.append("\n**Quick Wins (days-weeks):**")
            for skill, count in gap_analysis["quick_wins"]:
                lines.append(f"- 🟡 **{skill.title()}** — {count} job(s)")
        if gap_analysis["medium"]:
            lines.append("\n**Medium Term (weeks-months):**")
            for skill, count in gap_analysis["medium"]:
                lines.append(f"- 🟠 **{skill.title()}** — {count} job(s)")
        if gap_analysis["long_term"]:
            lines.append("\n**Long Term (months):**")
            for skill, count in gap_analysis["long_term"]:
                lines.append(f"- 🔴 **{skill.title()}** — {count} job(s)")
    else:
        lines.append("- No significant gaps — great coverage! ✅")

    lines.append("\n---\n")
    lines.append("## 📋 Job Listings (sorted by match score)\n")

    for i, job in enumerate(jobs, 1):
        score = job.get("match_score")
        if score is None:
            score_str = "N/A"
            score_emoji = "⚪"
        elif score >= 80:
            score_emoji = "🟢"
            score_str = f"{score}%"
        elif score >= 50:
            score_emoji = "🟡"
            score_str = f"{score}%"
        else:
            score_emoji = "🔴"
            score_str = f"{score}%"

        lines.append(f"## {i}. {sanitize(job['title'])} — {sanitize(job['company'])}") 
        lines.append(f"- **Match Score:** {score_emoji} {score_str}")
        lines.append(f"- **Source:** {job['source']}")
        lines.append(f"- **Salary:** {job['salary']}")
        lines.append(f"- **Location:** {job['location']}")
        if job.get("tags"):
            lines.append(f"- **Tags:** {job['tags']}")
        lines.append(f"- **Posted:** {job['posted']}")
        lines.append(f"- **Apply:** {job['url']}\n")

    report = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\n✅ Report saved to {output_path}")
    return report

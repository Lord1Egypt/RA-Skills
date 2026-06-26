#!/usr/bin/env python3
"""
main.py — Entry point for remote-job-hunter skill.
Usage:
  python3 src/main.py --profile-config path/to/profile.json \
                      --profile-meta profiles/ai-ml.json \
                      --output daily_report.md
"""
import json, argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from search import fetch_all
from scorer import score_jobs
from gaps import analyze_gaps
from report import generate_report
from apply import save_pending, build_pending_whatsapp_message, PENDING_FILE

AUTO_APPLY_THRESHOLD = 70

def main():
    parser = argparse.ArgumentParser(description="remote-job-hunter — AI-powered remote job search")
    parser.add_argument("--profile-config", required=True, help="Path to user profile JSON")
    parser.add_argument("--profile-meta", required=True, help="Path to domain profile JSON")
    parser.add_argument("--output", default="daily_report.md", help="Output report path")
    parser.add_argument("--no-auto-apply", action="store_true", help="Skip auto-apply preview")
    args = parser.parse_args()

    # Load configs
    with open(args.profile_config) as f:
        profile_config = json.load(f)
    with open(args.profile_meta) as f:
        profile_meta = json.load(f)

    domain = profile_meta["domain"]
    phrases = profile_meta["phrases"]
    resume_path = Path(profile_config["resume_path"]).expanduser()
    salary_min = profile_config.get("salary_min_usd", 0)
    salary_filter = profile_meta.get("salary_filter_enabled", False)

    print(f"\n🔍 remote-job-hunter v1.1.0")
    print(f"Profile: {profile_meta['label']} ({profile_config['name']})")
    print(f"Domain: {domain} | Salary: {'${:,}+'.format(salary_min) if salary_filter else 'All'}\n")

    # Fetch
    print("Fetching jobs...")
    jobs = fetch_all(domain, phrases, profile_config)

    # Score
    print("\nScoring jobs against resume...")
    scored_jobs, known_skills = score_jobs(jobs, domain, str(resume_path))

    # Apply salary filter
    if salary_filter and salary_min:
        def salary_ok(job):
            sal = job.get("salary", "")
            if sal == "Not listed":
                return True
            try:
                num = int(''.join(filter(str.isdigit, sal.split("K")[0].replace("$", ""))))
                return num * 1000 >= salary_min
            except:
                return True
        scored_jobs = [j for j in scored_jobs if salary_ok(j)]

    # Analyze gaps
    print("\nAnalyzing skill gaps...")
    gap_analysis = analyze_gaps(scored_jobs, known_skills)
    gap_analysis["known_skills"] = known_skills

    # Generate report
    print("\nGenerating report...")
    generate_report(scored_jobs, gap_analysis, profile_config, profile_meta, args.output)

    # Print summary
    green = [j for j in scored_jobs if j.get("match_score") and j["match_score"] >= 80]
    print(f"\n📊 Summary:")
    print(f"   Total jobs: {len(scored_jobs)}")
    print(f"   🟢 80%+ match: {len(green)}")
    if gap_analysis["top_missing"]:
        print(f"\n⚠️  Top skill gaps:")
        for skill, count in gap_analysis["top_missing"][:5]:
            print(f"   - {skill.title()} ({count} jobs)")

    # ─── Auto-Apply Preview ────────────────────────────────────────────────
    if args.no_auto_apply:
        return

    import html as _html
    pending_jobs = []
    for j in scored_jobs:
        if j.get("match_score") and j["match_score"] >= AUTO_APPLY_THRESHOLD:
            j["title"] = _html.unescape(_html.unescape(j.get("title", "")))
            j["company"] = _html.unescape(_html.unescape(j.get("company", "")))
            pending_jobs.append(j)

    if not pending_jobs:
        print(f"\n🤖 Auto-apply: No jobs above {AUTO_APPLY_THRESHOLD}% threshold today")
        # Save empty pending so confirm.py knows nothing to apply
        whatsapp_preview = None
    else:
        print(f"\n🤖 Auto-apply: {len(pending_jobs)} jobs above {AUTO_APPLY_THRESHOLD}% threshold")
        save_pending(pending_jobs, profile_config.get("name", "User"))
        whatsapp_preview = build_pending_whatsapp_message(pending_jobs, profile_config.get("name", "User"))

    # Save WhatsApp preview message for agent to send
    preview_file = Path(args.output).parent / "whatsapp_preview_message.txt"
    if whatsapp_preview:
        with open(preview_file, "w") as f:
            f.write(whatsapp_preview)
        print(f"   Preview message saved to {preview_file}")
        print(f"\n📱 WhatsApp preview:\n{whatsapp_preview}")
    else:
        # Clear any old preview
        if preview_file.exists():
            preview_file.unlink()

if __name__ == "__main__":
    main()

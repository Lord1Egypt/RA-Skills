#!/usr/bin/env python3
"""
confirm.py — Handles the 30-minute WhatsApp confirmation window.
v1.2.0: Tailors resume per job before applying.

Run at 7:30 AM (30 mins after job search):
- Reads pending_applications.json
- Checks for SKIP replies
- Tailors resume for each job
- Applies with tailored resume
- Sends WhatsApp summary
"""

import json, sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.parent

def load_pending():
    pending_file = WORKSPACE / "pending_applications.json"
    if not pending_file.exists():
        print("No pending applications found")
        return None
    with open(pending_file) as f:
        return json.load(f)

def clear_pending():
    pending_file = WORKSPACE / "pending_applications.json"
    if pending_file.exists():
        pending_file.unlink()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-config", required=True)
    parser.add_argument("--profile-meta", required=True)
    parser.add_argument("--skip", default="", help="SKIP reply e.g. '1,3' or 'ALL'")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default="applied_report.md")
    parser.add_argument("--no-tailor", action="store_true", help="Skip resume tailoring")
    args = parser.parse_args()

    # Load profiles
    with open(args.profile_config) as f:
        profile = json.load(f)
    with open(args.profile_meta) as f:
        meta = json.load(f)

    profile_name = profile.get("name", "User")
    resume_path = Path(profile.get("resume_path", "")).expanduser()

    # Load pending
    pending = load_pending()
    if not pending:
        print("Nothing to apply to")
        sys.exit(0)

    jobs = pending.get("jobs", [])
    if not jobs:
        print("No jobs in pending list")
        sys.exit(0)

    print(f"📋 Processing {len(jobs)} pending applications for {profile_name}")

    # Parse skip list
    from apply import parse_skip_reply, run_auto_apply, build_applied_whatsapp_message
    skip_list = parse_skip_reply(args.skip) if args.skip else None
    if skip_list:
        print(f"  SKIP received: {skip_list}")

    # Apply skip list to jobs
    if skip_list == "all":
        print("  SKIP ALL — cancelling all applications")
        results = [{"job": j, "result": {"status": "skipped", "reason": "SKIP ALL"}} for j in jobs]
        whatsapp_msg = build_applied_whatsapp_message(results, profile_name)
        _save_and_print(whatsapp_msg, args.output, results, profile_name)
        clear_pending()
        return

    if skip_list:
        jobs_to_apply = [j for i, j in enumerate(jobs, 1) if i not in skip_list]
        skipped_jobs = [j for i, j in enumerate(jobs, 1) if i in skip_list]
    else:
        jobs_to_apply = jobs
        skipped_jobs = []

    # ─── Resume Tailoring ────────────────────────────────────────────────────
    tailored_resumes = {}  # job_url → tailored_resume_path

    if not args.no_tailor and resume_path.exists():
        print(f"\n✂️  Tailoring resume for {len(jobs_to_apply)} jobs...")
        try:
            from tailor import tailor_resume
            tailored_dir = WORKSPACE / "tailored_resumes"
            tailored_dir.mkdir(exist_ok=True)

            for job in jobs_to_apply:
                jd_text = job.get("description", "")
                if jd_text and len(jd_text) >= 100:
                    tailored_path = tailor_resume(
                        resume_path=str(resume_path),
                        jd_text=jd_text,
                        job=job,
                        profile=profile,
                        output_dir=str(tailored_dir)
                    )
                    if tailored_path:
                        tailored_resumes[job.get("url", "")] = str(tailored_path)
                        print(f"  ✅ Tailored: {job.get('title')} @ {job.get('company')}")
                    else:
                        print(f"  ⚠️  Tailor failed: {job.get('title')} — using original")
                        tailored_resumes[job.get("url", "")] = str(resume_path)
                else:
                    print(f"  ⏭ No JD text: {job.get('title')} — using original resume")
                    tailored_resumes[job.get("url", "")] = str(resume_path)

        except ImportError:
            print("  ⚠️  tailor.py not found — using original resume for all jobs")
            for job in jobs_to_apply:
                tailored_resumes[job.get("url", "")] = str(resume_path)
    else:
        print(f"\n  Using original resume (tailoring skipped)")
        for job in jobs_to_apply:
            tailored_resumes[job.get("url", "")] = str(resume_path)

    # ─── Apply with tailored resumes ─────────────────────────────────────────
    print(f"\n🚀 Applying to {len(jobs_to_apply)} jobs...")
    results = []

    for job in jobs_to_apply:
        # Inject tailored resume path into profile for this job
        job_profile = dict(profile)
        tailored_path = tailored_resumes.get(job.get("url", ""), str(resume_path))
        job_profile["resume_path"] = tailored_path

        from apply import apply_to_job
        result = apply_to_job(job, job_profile, dry_run=args.dry_run)
        results.append({"job": job, "result": result})

        # Log
        status = result.get("status", "unknown")
        emoji = "✅" if status == "applied" else "❌" if status == "failed" else "⏭"
        print(f"  {emoji} {job.get('title')} @ {job.get('company')} — {status}")
        if status == "applied":
            print(f"     Resume used: {Path(tailored_path).name}")

    # Add skipped jobs to results
    for job in skipped_jobs:
        results.append({"job": job, "result": {"status": "skipped", "reason": "User SKIP request"}})

    # Build WhatsApp message
    whatsapp_msg = build_applied_whatsapp_message(results, profile_name)

    # Add tailoring summary to message
    tailored_count = sum(1 for url, path in tailored_resumes.items()
                        if path != str(resume_path))
    if tailored_count > 0:
        whatsapp_msg += f"\n\n✂️ *Resume tailored for {tailored_count} jobs* — each application used a JD-optimised version"

    _save_and_print(whatsapp_msg, args.output, results, profile_name)
    clear_pending()


def _save_and_print(whatsapp_msg, output_path, results, profile_name):
    """Save WhatsApp message and write report."""
    print("\n" + "="*50)
    print("WhatsApp message:")
    print("="*50)
    print(whatsapp_msg)
    print("="*50)

    msg_file = WORKSPACE / "whatsapp_applied_message.txt"
    with open(msg_file, "w") as f:
        f.write(whatsapp_msg)
    print(f"\n✅ WhatsApp message saved to {msg_file}")

    # Write report
    applied = [r for r in results if r.get("result", {}).get("status") == "applied"]
    report_lines = [
        f"# Auto-Apply Report — {datetime.now().strftime('%Y-%m-%d')}",
        f"Profile: {profile_name}",
        f"Total applied: {len(applied)}/{len(results)}",
        "",
    ]
    for r in results:
        job = r.get("job", {})
        res = r.get("result", {})
        status = res.get("status", "unknown")
        emoji = "✅" if status == "applied" else "❌" if status == "failed" else "⏭"
        report_lines.append(f"{emoji} **{job.get('title')}** — {job.get('company')}")
        report_lines.append(f"   Score: {job.get('match_score')}% | {job.get('url', '')}")
        if res.get("tailored_resume"):
            report_lines.append(f"   Resume: {Path(res['tailored_resume']).name}")
        if status != "applied":
            report_lines.append(f"   Reason: {res.get('reason', '')}")
        report_lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(report_lines))
    print(f"✅ Report saved to {output_path}")


if __name__ == "__main__":
    main()

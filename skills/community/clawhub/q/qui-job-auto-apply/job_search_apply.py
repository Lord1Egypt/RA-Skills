#!/usr/bin/env python3
"""
Job Search and Auto-Apply Script
Searches for jobs and automates application submissions across multiple platforms.
"""

import json
import os
import time
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
_API_BASE = "https://api.heybossai.com/v1"


def _pilot(body: dict) -> dict:
    r = requests.post(
        f"{_API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


class JobPlatform(Enum):
    """Supported job platforms"""
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    ZIPRECRUITER = "ziprecruiter"
    WELLFOUND = "wellfound"  # formerly AngelList


@dataclass
class JobSearchParams:
    """Parameters for job search"""
    title: str
    location: Optional[str] = None
    remote: bool = True
    experience_level: Optional[str] = None  # entry, mid, senior
    job_type: Optional[str] = None  # full-time, part-time, contract
    salary_min: Optional[int] = None
    platforms: List[JobPlatform] = None
    
    def __post_init__(self):
        if self.platforms is None:
            self.platforms = [JobPlatform.LINKEDIN, JobPlatform.INDEED]


@dataclass
class ApplicantProfile:
    """Applicant's profile information"""
    full_name: str
    email: str
    phone: str
    resume_path: str
    cover_letter_template: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    years_experience: Optional[int] = None
    
    # Work authorization
    authorized_to_work: bool = True
    requires_sponsorship: bool = False
    
    # Additional info
    willing_to_relocate: bool = False
    preferred_start_date: Optional[str] = None


def search_jobs(params: JobSearchParams) -> List[Dict]:
    """
    Search for jobs across specified platforms.
    
    Args:
        params: Job search parameters
        
    Returns:
        List of job postings matching criteria
    """
    print(f"🔍 Searching for '{params.title}' jobs...")
    print(f"   Platforms: {[p.value for p in params.platforms]}")
    print(f"   Location: {params.location or 'Remote/Any'}")
    
    # This is a placeholder - in real implementation, this would:
    # 1. Use Selenium/Playwright to scrape job boards
    # 2. Use official APIs where available (LinkedIn, Indeed)
    # 3. Parse job listings and extract relevant data
    
    jobs = []
    
    # Example job structure
    example_job = {
        "id": "job_123",
        "title": params.title,
        "company": "Example Corp",
        "location": params.location or "Remote",
        "platform": JobPlatform.LINKEDIN.value,
        "url": "https://linkedin.com/jobs/view/123",
        "description": "Sample job description",
        "has_easy_apply": True,
        "posted_date": "2024-01-15",
        "salary_range": "$100k - $150k",
    }
    
    print(f"✅ Found {len(jobs)} jobs (example mode)")
    return jobs


def analyze_job_compatibility(job: Dict, profile: ApplicantProfile) -> Dict:
    """
    Analyze if a job is a good match for the applicant using SkillBoss API Hub.

    Args:
        job: Job posting data
        profile: Applicant profile

    Returns:
        Compatibility analysis
    """
    prompt = (
        f"Analyze this job posting and applicant profile for compatibility.\n\n"
        f"Job Title: {job.get('title')}\nCompany: {job.get('company')}\n"
        f"Description: {job.get('description', 'N/A')}\n\n"
        f"Applicant: {profile.full_name}, {profile.years_experience or 0} years experience.\n\n"
        f"Respond with JSON only: "
        f'{{ "match_score": <0.0-1.0>, "key_matches": [...], "missing_requirements": [...], "recommended": <true|false> }}'
    )
    result = _pilot({
        "type": "chat",
        "inputs": {"messages": [{"role": "user", "content": prompt}]},
        "prefer": "balanced",
    })
    text = result["result"]["choices"][0]["message"]["content"]
    try:
        # Strip markdown code fences if present
        cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception:
        return {"match_score": 0.5, "key_matches": [], "missing_requirements": [], "recommended": False}


def generate_cover_letter(job: Dict, profile: ApplicantProfile) -> str:
    """
    Generate a tailored cover letter for the job using SkillBoss API Hub.

    Args:
        job: Job posting data
        profile: Applicant profile

    Returns:
        Personalized cover letter text
    """
    template_hint = ""
    if profile.cover_letter_template:
        template_hint = f"\n\nUse this template as a guide:\n{profile.cover_letter_template}"

    prompt = (
        f"Write a professional, personalized cover letter for the following job application.\n\n"
        f"Job Title: {job.get('title')}\nCompany: {job.get('company')}\n"
        f"Job Description: {job.get('description', 'N/A')}\n\n"
        f"Applicant Name: {profile.full_name}\n"
        f"Years of Experience: {profile.years_experience or 'several'}\n"
        f"LinkedIn: {profile.linkedin_url or 'N/A'}"
        f"{template_hint}\n\n"
        f"Return only the cover letter text, no extra commentary."
    )
    result = _pilot({
        "type": "chat",
        "inputs": {"messages": [{"role": "user", "content": prompt}]},
        "prefer": "balanced",
    })
    return result["result"]["choices"][0]["message"]["content"]


def apply_to_job(job: Dict, profile: ApplicantProfile, dry_run: bool = True) -> Dict:
    """
    Apply to a job posting.
    
    Args:
        job: Job posting data
        profile: Applicant profile
        dry_run: If True, don't actually submit applications
        
    Returns:
        Application result
    """
    print(f"\n📝 {'[DRY RUN] ' if dry_run else ''}Applying to: {job['title']} at {job['company']}")
    print(f"   Platform: {job['platform']}")
    print(f"   URL: {job['url']}")
    
    # In real implementation, this would:
    # 1. Navigate to the application page
    # 2. Fill out application forms
    # 3. Upload resume/cover letter
    # 4. Answer screening questions
    # 5. Submit application
    
    result = {
        "job_id": job["id"],
        "status": "dry_run" if dry_run else "submitted",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "platform": job["platform"],
        "job_title": job["title"],
        "company": job["company"],
    }
    
    if dry_run:
        print("   ⚠️  DRY RUN - Application not submitted")
    else:
        print("   ✅ Application submitted successfully")
    
    return result


def auto_apply_workflow(
    search_params: JobSearchParams,
    profile: ApplicantProfile,
    max_applications: int = 10,
    min_match_score: float = 0.7,
    dry_run: bool = True,
    require_confirmation: bool = True
) -> Dict:
    """
    Complete workflow: search jobs and apply automatically.
    
    Args:
        search_params: Job search parameters
        profile: Applicant profile
        max_applications: Maximum number of applications to submit
        min_match_score: Minimum compatibility score to apply
        dry_run: If True, don't actually submit applications
        require_confirmation: If True, ask for confirmation before each application
        
    Returns:
        Summary of applications submitted
    """
    print("🚀 Starting automated job application workflow\n")
    print(f"   Max applications: {max_applications}")
    print(f"   Min match score: {min_match_score}")
    print(f"   Dry run: {dry_run}")
    print(f"   Confirmation required: {require_confirmation}\n")
    
    # Search for jobs
    jobs = search_jobs(search_params)
    
    if not jobs:
        print("❌ No jobs found matching your criteria")
        return {"applications": [], "total": 0}
    
    applications = []
    applied_count = 0
    
    for job in jobs:
        if applied_count >= max_applications:
            print(f"\n✋ Reached maximum application limit ({max_applications})")
            break
        
        # Analyze compatibility
        compatibility = analyze_job_compatibility(job, profile)
        
        if compatibility["match_score"] < min_match_score:
            print(f"\n⏭️  Skipping: {job['title']} at {job['company']}")
            print(f"   Match score too low: {compatibility['match_score']}")
            continue
        
        print(f"\n✨ Good match found!")
        print(f"   Score: {compatibility['match_score']}")
        print(f"   Matches: {', '.join(compatibility['key_matches'][:3])}")
        
        # Generate cover letter
        cover_letter = generate_cover_letter(job, profile)
        
        # Ask for confirmation if required
        if require_confirmation and not dry_run:
            response = input(f"\n   Apply to this job? (y/n): ")
            if response.lower() != 'y':
                print("   ⏭️  Skipped by user")
                continue
        
        # Apply to job
        result = apply_to_job(job, profile, dry_run=dry_run)
        result["match_score"] = compatibility["match_score"]
        applications.append(result)
        applied_count += 1
        
        # Rate limiting
        time.sleep(2)
    
    # Summary
    print("\n" + "="*60)
    print("📊 APPLICATION SUMMARY")
    print("="*60)
    print(f"Jobs found: {len(jobs)}")
    print(f"Applications submitted: {applied_count}")
    print(f"Success rate: {(applied_count/len(jobs)*100) if jobs else 0:.1f}%")
    
    return {
        "applications": applications,
        "total": applied_count,
        "jobs_found": len(jobs),
        "search_params": {
            "title": search_params.title,
            "location": search_params.location,
            "remote": search_params.remote
        }
    }


def main():
    """Example usage"""
    # Create applicant profile
    profile = ApplicantProfile(
        full_name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        resume_path="~/Documents/resume.pdf",
        linkedin_url="https://linkedin.com/in/johndoe",
        github_url="https://github.com/johndoe",
        years_experience=5,
    )
    
    # Create search parameters
    search_params = JobSearchParams(
        title="Software Engineer",
        location="San Francisco, CA",
        remote=True,
        experience_level="mid",
        job_type="full-time",
        platforms=[JobPlatform.LINKEDIN, JobPlatform.INDEED]
    )
    
    # Run workflow
    results = auto_apply_workflow(
        search_params=search_params,
        profile=profile,
        max_applications=10,
        min_match_score=0.75,
        dry_run=True,  # Set to False for actual applications
        require_confirmation=True
    )
    
    # Save results
    with open("application_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to application_results.json")


if __name__ == "__main__":
    main()

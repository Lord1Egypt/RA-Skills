# Job Description Creation

## Purpose
Create job descriptions that function as filters - attracting the right candidates and repelling the wrong ones.

## When to Use
- "Write a job description for [role]"
- "Create a JD for senior engineer"
- "Help me describe this position"

## Key Principles

### 1. Filter, Not Attract
- Be specific about what the role actually requires
- Describe the hard parts honestly
- Use language of target candidates, not HR compliance

### 2. Requirements vs. Nice-to-Have
- Maximum 3-5 genuine requirements
- Distinguish must-haves from preferences
- Avoid laundry lists that deter good candidates

### 3. The "Day in the Life"
- Describe actual work, not abstract responsibilities
- Include real challenges and expectations
- Set honest expectations about workload/pressure

## Data Structure

```json
{
  "jobs": [
    {
      "id": "JOB-12345",
      "title": "Senior Software Engineer",
      "level": "senior",
      "department": "Engineering",
      "location": "San Francisco / Remote",
      "employment_type": "Full-time",
      "salary_range": "$150k-200k",
      "created_at": "2024-03-01",
      "status": "active",
      
      "role_summary": "Build core platform infrastructure...",
      
      "requirements": [
        "5+ years production experience with distributed systems",
        "Deep expertise in at least one of: Python, Go, or Rust",
        "Track record of mentoring junior engineers"
      ],
      
      "responsibilities": [
        "Design and implement scalable backend services",
        "Review code and provide constructive feedback",
        "Collaborate with product on technical tradeoffs"
      ],
      
      "nice_to_have": [
        "Experience with Kubernetes",
        "Open source contributions",
        "Previous startup experience"
      ],
      
      "screening_criteria": [
        {"criterion": "Distributed systems experience", "weight": "high"},
        {"criterion": "Code quality in samples", "weight": "high"},
        {"criterion": "Communication clarity", "weight": "medium"}
      ],
      
      "challenges": [
        "High ambiguity in early-stage environment",
        "Rapidly evolving technical requirements",
        "Direct customer feedback loops"
      ]
    }
  ]
}
```

## Script Usage

```bash
# Create job posting
python scripts/create_job.py \
  --title "Senior Software Engineer" \
  --level senior \
  --department "Engineering" \
  --location "Remote"

# View job details
python scripts/view_job.py --job-id "JOB-12345"

# Update job
python scripts/update_job.py \
  --job-id "JOB-12345" \
  --field "salary_range" \
  --value "$160k-210k"

# List active jobs
python scripts/list_jobs.py --status active
```

## Output Format

```
JOB POSTING: Senior Software Engineer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ROLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're looking for a Senior Software Engineer to build core 
platform infrastructure that processes 10M+ events daily. 
You'll architect distributed systems that scale with our growth.

This is not a role for someone who wants specs handed to them. 
You'll work with high ambiguity, make significant technical 
decisions, and own outcomes end-to-end.

WHAT YOU'LL DO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Design and implement scalable backend services
• Review code and mentor junior engineers
• Collaborate directly with customers on technical issues
• Make architectural decisions with limited oversight

WHAT YOU NEED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 5+ years production experience with distributed systems
• Deep expertise in Python, Go, or Rust
• Track record of mentoring junior engineers
• Comfort with high ambiguity and rapid change

NICE TO HAVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Kubernetes experience
• Open source contributions
• Previous startup experience (<50 people)

THE HARD PARTS (Read This)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• We move fast. Priorities shift weekly sometimes.
• You'll get direct customer feedback, positive and negative.
• We don't have dedicated ops - engineers own production.
• On-call rotation includes weekends.

IF THIS EXCITES YOU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Apply with your resume and a brief note about a system you 
built that you're proud of and why.

DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: San Francisco or Remote (US timezones)
Salary: $150k-200k + equity
Reports to: CTO
Team size: 8 engineers

COMPENSATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Base: $150,000 - $200,000
Equity: 0.1% - 0.25%
Benefits: Health, dental, 401k matching
```

## Screening Criteria Template

For each job, define 3-5 specific criteria with weights:

```json
{
  "screening_criteria": [
    {
      "criterion": "Distributed systems experience",
      "description": "Has built and operated production distributed systems",
      "weight": "high",
      "evidence": "Resume mentions specific systems, scale metrics"
    },
    {
      "criterion": "Technical communication",
      "description": "Can explain complex concepts clearly",
      "weight": "high",
      "evidence": "Writing samples, documentation, clear resume"
    },
    {
      "criterion": "Language proficiency",
      "description": "Expert-level in required language",
      "weight": "medium",
      "evidence": "Code samples, projects, certifications"
    }
  ]
}
```

## Common Pitfalls to Avoid

### ❌ Don't
- List 15+ "requirements" (deters good candidates)
- Use generic corporate language
- Hide the hard parts (leads to early attrition)
- Copy from other companies without customization

### ✅ Do
- Be honest about challenges
- Write like you're talking to the ideal candidate
- Show personality and culture
- Update based on who's applying vs. who's succeeding

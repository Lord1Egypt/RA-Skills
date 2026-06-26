# Resume Screening

## Purpose
Evaluate candidates against job criteria to identify who is worth interviewing.

## When to Use
- "Screen this resume for the [role]"
- "Evaluate this candidate"
- "Should we interview this person?"

## Screening Process

### 1. Criteria Check
Evaluate against the 3-5 criteria defined in the job description:
- Must-haves (dealbreakers if missing)
- Key requirements (strong preference)
- Nice-to-haves (bonus points)

### 2. Evidence Assessment
Look for specific evidence, not claims:
- ❌ "Expert in Python" → ✅ "Built Python service processing 10M req/day"
- ❌ "Strong leader" → ✅ "Led team of 5, shipped X feature in Y timeline"
- ❌ "Results-driven" → ✅ "Reduced latency by 40% through Z optimization"

### 3. Red Flags
Watch for:
- Frequent job changes without progression
- Gaps without explanation
- Vague descriptions of accomplishments
- Claims not supported by evidence

## Data Structure

```json
{
  "screenings": [
    {
      "id": "SCR-789",
      "job_id": "JOB-12345",
      "candidate_id": "CAND-456",
      "screened_at": "2024-03-15",
      "screener": "Hiring Manager",
      
      "criteria_scores": [
        {
          "criterion": "Distributed systems experience",
          "score": 4,
          "max_score": 5,
          "evidence": "Built message queue at Stripe handling 50M messages/day",
          "notes": "Strong quantitative evidence"
        },
        {
          "criterion": "Technical communication",
          "score": 3,
          "max_score": 5,
          "evidence": "Resume is clear but cover letter is generic",
          "notes": "Should probe in interview"
        }
      ],
      
      "overall_score": 3.5,
      "recommendation": "interview",
      "confidence": "medium",
      
      "strengths": [
        "Strong technical background in relevant area",
        "Quantified impact in previous roles"
      ],
      
      "concerns": [
        "Hasn't worked in startup environment before",
        "Communication skills unclear from materials"
      ],
      
      "questions_to_probe": [
        "Tell me about a time you dealt with ambiguity",
        "How do you approach mentoring junior engineers?"
      ]
    }
  ]
}
```

## Script Usage

```bash
# Screen candidate
python scripts/screen_candidate.py \
  --job-id "JOB-12345" \
  --candidate-id "CAND-456" \
  --resume "resume.pdf"

# View screening result
python scripts/view_screening.py --screening-id "SCR-789"

# List screenings for job
python scripts/list_screenings.py --job-id "JOB-12345"

# Update screening
python scripts/update_screening.py \
  --screening-id "SCR-789" \
  --recommendation "reject" \
  --reason "Missing key requirement"
```

## Output Format

```
CANDIDATE SCREENING
Job: Senior Software Engineer | Candidate: Jane Doe
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 4.2/5.0
Recommendation: ✅ INTERVIEW (High confidence)

CRITERIA EVALUATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Distributed Systems Experience (High weight)
   Score: 5/5 ⭐⭐⭐⭐⭐
   Evidence: Built message queue at Stripe handling 50M messages/day
   Notes: Strong quantitative evidence, relevant scale

2. Language Proficiency - Python (High weight)
   Score: 4/5 ⭐⭐⭐⭐
   Evidence: 6 years Python, mentions asyncio and FastAPI
   Notes: Technical depth appears solid

3. Mentoring Experience (Medium weight)
   Score: 4/5 ⭐⭐⭐⭐
   Evidence: "Mentored 3 junior engineers" with specific outcomes
   Notes: Good evidence, should probe approach in interview

4. Technical Communication (High weight)
   Score: 3/5 ⭐⭐⭐
   Evidence: Resume clear, cover letter generic
   Notes: Unclear - probe in interview with written exercise

5. Startup Experience (Low weight)
   Score: 2/5 ⭐⭐
   Evidence: Only worked at large companies (Stripe, Google)
   Notes: Risk factor but not disqualifying

STRENGTHS ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Strong technical background in core competency (distributed systems)
• Quantified impact in previous roles (metrics, scale)
• Evidence of mentorship with outcomes
• Career progression shows increasing responsibility

CONCERNS ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• No startup/small company experience
• Communication skills unclear - generic cover letter
• May expect more structure than we provide

QUESTIONS TO PROBE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Tell me about a time you had to work with high ambiguity.
   → Assess startup fit

2. Describe how you approach mentoring junior engineers.
   → Validate mentoring claim

3. Write a brief technical explanation of [concept] for a non-technical audience.
   → Assess communication clarity

4. Why are you interested in joining a small startup now?
   → Assess motivation and expectations

NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended: Schedule technical phone screen
Priority: High (top 10% of applicants)
Timeline: Schedule within 3 days

⚠️  Note: This is a screening assessment only. Final hiring 
    decision requires interviews and reference checks.
```

## Scoring Guide

### 5 - Exceptional
- Exceeds requirement significantly
- Strong quantitative evidence
- Clear progression and impact

### 4 - Strong
- Meets requirement well
- Good evidence of capability
- Minor gaps only

### 3 - Adequate
- Meets basic requirement
- Evidence is present but limited
- Would need to develop in role

### 2 - Weak
- Below requirement
- Limited or unclear evidence
- Significant concerns

### 1 - Poor
- Does not meet requirement
- No relevant evidence
- Clear mismatch

## Recommendation Categories

- **Strong Interview** (4.5+): Top priority, schedule quickly
- **Interview** (3.5-4.5): Good fit, standard process
- **Maybe** (3.0-3.5): Borderline, consider phone screen
- **Reject** (<3.0): Does not meet requirements

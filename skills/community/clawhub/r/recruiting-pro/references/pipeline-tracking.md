# Pipeline Tracking

## Purpose
Track candidates through hiring stages with visibility, reminders, and next actions.

## When to Use
- "Update candidate status"
- "Where are we with [candidate]?"
- "What candidates need follow-up?"
- "Show me the pipeline"

## Pipeline Stages

### Standard Stages
1. **Applied** - Initial application received
2. **Screening** - Resume/application review
3. **Phone Screen** - Initial conversation (30 min)
4. **Technical** - Technical assessment or interview
5. **Onsite/Deep Dive** - Full interview loop
6. **Reference Check** - Contact references
7. **Offer** - Extend offer
8. **Hired** - Accepted offer
9. **Rejected** - Not moving forward
10. **Withdrawn** - Candidate withdrew

### Stage Durations (Targets)
| Stage | Target Duration | Alert If Exceeds |
|-------|----------------|------------------|
| Screening | 3 days | 5 days |
| Phone Screen | 5 days | 7 days |
| Technical | 7 days | 10 days |
| Onsite | 10 days | 14 days |
| Reference Check | 5 days | 7 days |
| Offer | 5 days | 7 days |

## Data Structure

```json
{
  "pipeline": {
    "candidates": [
      {
        "id": "CAND-456",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "applied_at": "2024-03-01",
        "source": "LinkedIn",
        
        "current_stage": "technical",
        "stage_history": [
          {"stage": "applied", "entered_at": "2024-03-01", "exited_at": "2024-03-02"},
          {"stage": "screening", "entered_at": "2024-03-02", "exited_at": "2024-03-04"},
          {"stage": "phone_screen", "entered_at": "2024-03-04", "exited_at": "2024-03-08"},
          {"stage": "technical", "entered_at": "2024-03-08", "exited_at": null}
        ],
        
        "stage_deadline": "2024-03-15",
        "next_action": "Schedule technical interview",
        "action_owner": "Engineering Manager",
        
        "rating": "strong",
        "notes": "Great background, fast mover"
      }
    ]
  }
}
```

## Script Usage

```bash
# Add candidate to pipeline
python scripts/add_candidate.py \
  --job-id "JOB-12345" \
  --name "Jane Doe" \
  --email "jane@example.com" \
  --source "LinkedIn"

# Update candidate stage
python scripts/update_pipeline.py \
  --candidate-id "CAND-456" \
  --stage "technical" \
  --next-action "Schedule technical interview" \
  --owner "Engineering Manager"

# View pipeline for job
python scripts/view_pipeline.py --job-id "JOB-12345"

# Check for stale candidates
python scripts/check_pipeline.py --stale-days 7

# Set follow-up reminder
python scripts/set_reminder.py \
  --candidate-id "CAND-456" \
  --date "2024-03-12" \
  --note "Follow up if no response"
```

## Output Format

```
HIRING PIPELINE
Job: Senior Software Engineer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PIPELINE OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Candidates: 23
Active: 12 | Rejected: 8 | Withdrawn: 2 | Hired: 1

STAGE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Applied:           3 candidates
🔍 Screening:         2 candidates  
📞 Phone Screen:      4 candidates
💻 Technical:         2 candidates
🏢 Onsite:            1 candidate
📋 Reference Check:   0 candidates
💰 Offer:             0 candidates

⚠️  STALE CANDIDATES (Action Needed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Phone Screen Stage (>7 days)
• John Smith - In stage 9 days
  Next action: Send rejection or schedule technical
  Owner: Hiring Manager
  
💻 Technical Stage (>10 days)
• Sarah Johnson - In stage 12 days
  Next action: Complete debrief and decide
  Owner: CTO

ACTIVE CANDIDATES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 STRONG CANDIDATES

Jane Doe - 💻 Technical (5 days)
  Rating: ⭐⭐⭐⭐⭐ Strong hire
  Next: Schedule technical interview (due 3/15)
  Owner: Engineering Manager
  Notes: Ex-Stripe, great distributed systems background

Michael Chen - 📞 Phone Screen (3 days)
  Rating: ⭐⭐⭐⭐ Likely hire
  Next: Move to technical
  Owner: Hiring Manager
  Notes: Good communication, solid fundamentals

📊 PIPELINE HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ On track: 8 candidates
⚠️  Stale: 2 candidates
🚨 Critical: 0 candidates

Average time in pipeline: 12 days
Target time to hire: 30 days
Current pace: On track

RECOMMENDED ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Move Sarah Johnson to decision (stale 12 days)
2. Reject John Smith or schedule technical
3. Schedule technical for Jane Doe
4. Send follow-up to 3 candidates awaiting response
```

## Pipeline Health Metrics

### Key Metrics to Track
- **Time to hire** (application to offer accept)
- **Conversion rates** by stage
- **Source quality** (which sources produce hires)
- **Drop-off points** (where candidates exit)
- **Offer acceptance rate**

### Alerts
```
🚨 PIPELINE ALERTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 2 candidates stale >10 days (risk of losing them)
• No candidates in Reference Check stage (bottleneck?)
• Average time to hire: 45 days (target: 30 days)
• Offer acceptance rate: 50% (industry avg: 70%)

Recommended: Review offer competitiveness
```

## Communication Tracking

Track all candidate communications:
```json
{
  "communications": [
    {
      "candidate_id": "CAND-456",
      "type": "email",
      "direction": "outbound",
      "subject": "Interview scheduling",
      "sent_at": "2024-03-10",
      "template_used": "interview_invite",
      "response_received": false,
      "follow_up_date": "2024-03-13"
    }
  ]
}
```

## Best Practices

### Speed Matters
- Respond to applications within 3 days
- Schedule interviews within 5 days of interest
- Make decisions within 2 days of final interview
- Send offers within 3 days of decision

### Communication
- Never ghost candidates
- Set clear expectations at each stage
- Provide timeline estimates
- Give feedback when possible (if candidate requests)

### Bias Prevention
- Use same questions for all candidates at each stage
- Evaluate against criteria before meeting
- Have diverse interview panels
- Document decisions with evidence

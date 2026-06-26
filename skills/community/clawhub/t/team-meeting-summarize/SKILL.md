# Meeting Minutes Generator

## name
meeting-minutes-generator

## description
Transform raw meeting notes into structured, actionable summaries. Automatically extract key decisions, action items, owners, deadlines, and discussion points. Perfect for professionals who attend multiple meetings and need clear, shareable follow-ups.

## instructions
### Overview
This skill takes unstructured meeting notes or transcripts and converts them into professional summaries that anyone can quickly understand. It identifies decisions made, tasks assigned, questions raised, and next steps. Great for team leads, project managers, executives, and anyone who wants better meeting follow-through.

### When to Use
- After any meeting to generate professional summaries
- Before sending meeting notes to attendees
- Creating project documentation from discussions
- Preparing executive summaries for leadership
- Tracking action items across multiple meetings
- Onboarding team members who missed meetings
- Following up on decisions made

### Input Requirements
Provide one of the following:

**Option A - Meeting Notes:**
- Raw notes taken during the meeting (bullet points, fragments, mixed content)
- Date and time of meeting
- Attendees list (if available)
- Meeting title or purpose

**Option B - Audio/Transcript:**
- Meeting transcript (人工转录或自动转录)
- Or audio file URL for analysis
- Meeting context and participants

**Option C - Minimal Input:**
- Meeting topic and date
- A few key points discussed
- Any known outcomes

### Processing Workflow

#### Step 1: Information Extraction
Identify and categorize:
- **Attendees**: All participants mentioned
- **Date/Time**: When the meeting occurred
- **Duration**: Meeting length (if mentioned)
- **Purpose**: Why the meeting was held

#### Step 2: Content Analysis
Extract:
- **Key Discussion Points**: Main topics debated
- **Decisions Made**: Clear outcomes and choices
- **Action Items**: Tasks with assignees and deadlines
- **Questions Raised**: Unanswered items needing follow-up
- **Open Issues**: Topics deferred to future meetings

#### Step 3: Structure Generation
Organize information into clear sections:
1. Meeting Overview
2. Key Decisions
3. Action Items (with owners)
4. Discussion Summary
5. Next Steps
6. Next Meeting (if scheduled)

### Output Format

```
═══════════════════════════════════════════════════════════
                    MEETING SUMMARY
═══════════════════════════════════════════════════════════

📅 Date: [Date] | ⏰ Duration: [Length]
📍 Location/Link: [Meeting Room or Video Call Link]
👥 Attendees: [List of participants]
📝 Prepared by: [Your name/AI Assistant]

───────────────────────────────────────────────────────────
📌 MEETING OVERVIEW
───────────────────────────────────────────────────────────
**Purpose:** [Why this meeting was held]

**Key Outcomes:**
• [Primary outcome 1]
• [Primary outcome 2]
• [Primary outcome 3]

───────────────────────────────────────────────────────────
✅ DECISIONS MADE
───────────────────────────────────────────────────────────
| # | Decision | Rationale |
|---|----------|-----------|
| 1 | [What was decided] | [Why this choice] |
| 2 | [Next decision] | [Supporting reason] |

───────────────────────────────────────────────────────────
📋 ACTION ITEMS
───────────────────────────────────────────────────────────
| Task | Owner | Deadline | Status |
|------|-------|----------|--------|
| [Task description] | [@Person] | [Date] | 🔴 Pending |
| [Task 2] | [@Person2] | [Date] | 🟡 In Progress |

**Priority Actions:**
⚡ **Due Today/This Week:**
- [Urgent task with deadline]

───────────────────────────────────────────────────────────
💬 DISCUSSION SUMMARY
───────────────────────────────────────────────────────────
**Topic 1: [Subject]**
- [Key point discussed]
- [Another point]
- [Outcome or decision]

**Topic 2: [Subject]**
- [Points covered]
- [Notes]

───────────────────────────────────────────────────────────
❓ OPEN QUESTIONS
───────────────────────────────────────────────────────────
| Question | Owner | Due Date |
|----------|-------|----------|
| [Unanswered question] | [@Person] | [Date] |

───────────────────────────────────────────────────────────
📆 NEXT STEPS
───────────────────────────────────────────────────────────
1. [Immediate next action]
2. [Follow-up step]
3. [Future milestone]

**Next Meeting:** [Date/Time if scheduled]
**Meeting Focus:** [Topics for next meeting]

═══════════════════════════════════════════════════════════
```

### Example Transformation

**Input (Raw Meeting Notes):**
```
Team sync - March 15, 2025
Present: Sarah, Mike, Lisa, Tom

Sarah: Q1 sales down 10%
Discussion on pricing strategy
Decided to offer 15% discount for Q2
Mike to create new pricing sheet by Friday
Lisa asked about competitor moves
Need to review competitor analysis next week
Tom: Launch timeline - June 1st
Marketing needs assets by April 15
Sarah to send follow-up email with new pricing
Next sync: March 22
```

**Output:**
```
═══════════════════════════════════════════════════════════
                    MEETING SUMMARY
═══════════════════════════════════════════════════════════

📅 Date: March 15, 2025
👥 Attendees: Sarah, Mike, Lisa, Tom

───────────────────────────────────────────────────────────
📌 MEETING OVERVIEW
───────────────────────────────────────────────────────────
**Purpose:** Q1 Review and Q2 Strategy Planning

**Key Outcomes:**
• Agreed on 15% Q2 discount strategy
• June 1st product launch confirmed
• Marketing deadline set for April 15

───────────────────────────────────────────────────────────
✅ DECISIONS MADE
───────────────────────────────────────────────────────────
| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Implement 15% discount for Q2 | Counter Q1 sales decline |
| 2 | Target June 1st launch date | Aligns with market window |
| 3 | Marketing assets due April 15 | Allow 6 weeks for campaign |

───────────────────────────────────────────────────────────
📋 ACTION ITEMS
───────────────────────────────────────────────────────────
| Task | Owner | Deadline | Status |
|------|-------|----------|--------|
| Create new pricing sheet | Mike | March 20 (Fri) | 🔴 Pending |
| Send pricing follow-up email | Sarah | March 16 | 🔴 Pending |
| Review competitor analysis | Team | March 22 | 🟡 In Progress |
| Prepare marketing assets | Marketing | April 15 | 🔴 Pending |

───────────────────────────────────────────────────────────
❓ OPEN QUESTIONS
───────────────────────────────────────────────────────────
| Question | Owner | Due Date |
|----------|-------|----------|
| What are competitors planning? | Lisa | March 22 |

───────────────────────────────────────────────────────────
📆 NEXT STEPS
───────────────────────────────────────────────────────────
1. Mike completes pricing sheet
2. Sarah distributes updated pricing
3. Schedule competitor deep-dive for next week

**Next Meeting:** March 22, 2025

═══════════════════════════════════════════════════════════
```

### Additional Features
- **Multi-language Support**: Generate summaries in various languages
- **Task Export**: Export action items to task managers (CSV, JSON)
- **Email Integration**: Format for email distribution
- **Template Customization**: Create branded summary templates
- **Meeting Types**: Specialized templates for:
  - Project kickoffs
  - Sprint retrospectives
  - Client calls
  - Board meetings
  - One-on-ones

### Best Practices
1. Start with the clearest notes available
2. Include all attendee names
3. Note any specific deadlines mentioned
4. Add context about meeting type for better accuracy
5. Review and edit before sharing externally

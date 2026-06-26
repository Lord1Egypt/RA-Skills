---
name: sop-generator
description: Turn messy recordings, transcripts, voice notes, or brain dumps into clean, team-ready Standard Operating Procedures (SOPs). Use when you have Loom videos, meeting transcripts, rough notes, or verbal walkthroughs that need to become documented processes. Covers SOP structure, extraction from various input types, quality checklist, and automation strategies. Trigger on "create SOP", "turn this into an SOP", "document this process", "make this team-ready", "convert transcript to SOP", "write a procedure".
---

# SOP Generator

## Overview
SOPs (Standard Operating Procedures) are the difference between a business that runs smoothly and one where everything depends on you remembering how to do it. But most solopreneurs record Looms, dump ideas in docs, or explain processes verbally — then never turn them into usable SOPs. This playbook shows you how to extract clean, operational SOPs from messy inputs in under 30 minutes.

---

## Step 1: Understand What Makes a Good SOP

A good SOP is:
- **Actionable:** Anyone following it can complete the task without asking questions
- **Complete:** Covers every step, even the obvious ones
- **Structured:** Same format every time so it's easy to scan
- **Maintained:** Updated when the process changes

**Bad SOP example:**
```
"Post on social media daily. Make sure it's good content. Engage with comments."
```

**Good SOP example:**
```
PURPOSE: Maintain consistent brand presence and engagement on LinkedIn

TOOLS REQUIRED:
- LinkedIn account
- Content calendar (Notion)
- Canva (for graphics)

STEPS:
1. Open content calendar (Notion → Marketing → LinkedIn Schedule)
2. Find today's scheduled post
3. Copy post text and download associated graphic
4. Go to LinkedIn.com → Start a post
5. Paste text, upload graphic
6. Preview post → Click "Post"
7. Set reminder for 2 hours later to respond to comments
8. Mark post as "Published" in Notion

EDGE CASES:
- If no post scheduled: Use backup content folder (Notion → Content → Backups)
- If graphic missing: Use text-only template in Canva → "LinkedIn Text Post"

METRICS:
- Post published on time? (Yes/No)
- Engagement rate (likes + comments / impressions)
```

**Rule:** If someone new to your business can't follow the SOP without asking you questions, it's not complete.

---

## Step 2: Extract SOPs from Different Input Types

You probably have processes scattered across Loom videos, voice memos, meeting notes, or just in your head. Here's how to extract them.

### From Loom Video or Screen Recording

**Extraction workflow:**
1. Generate transcript (Loom has built-in transcription, or use Otter.ai, Rev, or Claude with the video)
2. Read through transcript and identify:
   - Tools or apps mentioned
   - Sequence of actions (clicks, navigation, data entry)
   - Decision points ("if this, then that")
   - Common errors or edge cases mentioned
3. Map transcript to SOP structure (see Step 3)
4. Watch video one more time while reading SOP draft to catch missed steps
5. Test the SOP yourself or have someone else follow it

**Common issues in Loom transcripts:**
- Rambling or off-topic commentary (delete it)
- Missing steps because you "just did it" on muscle memory (add them)
- Tool-specific jargon (define or simplify)

### From Voice Memo or Meeting Transcript

**Extraction workflow:**
1. Generate transcript if not already text (Whisper, Otter.ai, or Claude)
2. Identify the core process being described (ignore context/small talk)
3. Pull out:
   - What triggers the process ("We do this when...")
   - The steps in order
   - Tools or people involved
   - What success looks like
4. Map to SOP structure
5. Fill gaps (voice memos often skip "obvious" steps — add them)

### From Messy Notes or Brain Dump

**Extraction workflow:**
1. Read through notes and identify:
   - Is this one process or multiple? (If multiple, split into separate SOPs)
   - What's the goal of the process?
   - What's the order of operations?
2. Reorder notes chronologically (most brain dumps are non-linear)
3. Map to SOP structure
4. Add missing details (tools, exact steps, decision points)

---

## Step 3: Use the SOP Template

Every SOP should follow this structure. Copy/paste this and fill it in.

```
# [PROCESS NAME]

## 1. PURPOSE
[Why this process exists. What outcome does it create?]

## 2. TOOLS REQUIRED
[List all software, accounts, or physical tools needed]
- Tool 1 (with login info location if applicable)
- Tool 2
- etc.

## 3. STEP-BY-STEP INSTRUCTIONS

### Preparation (if needed)
- [ ] Pre-step 1
- [ ] Pre-step 2

### Main Process
1. [First action — be specific: "Click X", "Open Y", "Copy Z"]
2. [Second action]
3. [Third action — include screenshots if helpful]
4. [Decision point if applicable]
   - IF [condition]: Do [action A]
   - ELSE: Do [action B]
5. [Continue until complete]

### Completion
- [ ] Final check: [What to verify before considering it done]
- [ ] Mark as complete: [Where to log completion, if tracked]

## 4. EDGE CASES / EXCEPTIONS

**What if [common issue]?**
→ [How to handle it]

**What if [less common issue]?**
→ [How to handle it OR who to escalate to]

## 5. METRICS TO TRACK (if applicable)
- [Metric 1]: [Target or benchmark]
- [Metric 2]: [Target or benchmark]
- [How often to review these metrics]

## 6. LAST UPDATED
[Date] by [Name]

## 7. RELATED SOPs (if applicable)
- Link to [related process 1]
- Link to [related process 2]
```

---

## Step 4: Quality Checklist for SOPs

Before publishing an SOP, run it through this checklist:

- [ ] **Purpose is clear:** Someone reading it knows why this matters
- [ ] **Tools are listed:** All software, logins, or resources are specified
- [ ] **Steps are numbered and sequential:** Easy to follow in order
- [ ] **Steps are specific:** "Click the blue 'Export' button in top right" not "export the data"
- [ ] **Decision points are explicit:** IF/THEN logic is clear
- [ ] **Edge cases are covered:** At least 2-3 common issues or exceptions addressed
- [ ] **Success criteria is defined:** What does "done" look like?
- [ ] **Tested by someone else:** At least one other person has followed it successfully
- [ ] **Screenshots or visuals included (if helpful):** Especially for UI-heavy processes
- [ ] **Last updated date is current:** So team knows if it's stale

**Rule:** If you have to verbally explain something after someone reads the SOP, the SOP is incomplete. Fix it.

---

## Step 5: Organize Your SOP Library

One SOP is useful. 50 scattered SOPs is chaos. Organize them.

**Recommended structure (Notion, Google Docs, Confluence, or wiki):**

```
📁 SOP Library
  📂 Operations
    - Onboarding new clients
    - Weekly invoicing process
    - Monthly financial review
  📂 Marketing
    - Publishing blog posts
    - Social media posting schedule
    - Email campaign setup
  📂 Sales
    - Lead qualification process
    - Proposal creation workflow
    - Contract signing process
  📂 Product/Delivery
    - Feature deployment checklist
    - Bug triage process
    - Customer support ticket workflow
```

**Metadata to track per SOP:**
- Owner (who maintains it)
- Last updated date
- Frequency of use (daily, weekly, monthly, ad-hoc)
- Status (draft, active, deprecated)

**Search tip:** Use consistent naming: `[Department] - [Process Name]`
Example: "Marketing - Publishing Blog Posts" not "How to post blogs"

---

## Step 6: Maintain SOPs Over Time

SOPs rot. Tools change. Processes evolve. Maintenance is critical.

**Maintenance workflow:**

### Quarterly review (30 min):
- [ ] Pull up list of all SOPs
- [ ] Mark any that are outdated or no longer used
- [ ] Update 2-3 high-use SOPs that have changed

### When a process changes:
- [ ] Update the SOP immediately (don't wait)
- [ ] Notify anyone who uses it
- [ ] Update "Last updated" date

### When someone reports an issue with an SOP:
- [ ] Fix the gap in the SOP
- [ ] Test it again
- [ ] Thank them for the feedback (encourage this behavior)

**Red flags an SOP needs updating:**
- Someone following it gets stuck
- A tool mentioned in it no longer exists
- The process takes 2x longer than expected (inefficiency crept in)
- It hasn't been updated in 6+ months

---

## Step 7: Automate SOP Generation (Advanced)

If you're creating SOPs regularly, automate the extraction and formatting.

**Automation workflow (Loom → SOP):**

```
TRIGGER: New Loom video uploaded (or tagged with "SOP")

STEP 1: Extract transcript
  - Tool: Loom API or Zapier/Make integration

STEP 2: Send transcript to Claude with SOP prompt
  - Prompt: "You are an operations consultant. Convert the following Loom transcript into a clean SOP. Use this structure: [paste SOP template]. Remove fluff and filler words. Be specific and actionable."

STEP 3: Generate draft SOP
  - Claude outputs formatted SOP

STEP 4: Save to Notion or Google Docs
  - Auto-create page in SOP Library with draft
  - Tag as "Draft - Needs Review"

STEP 5: Notify you to review
  - Slack message or email: "New SOP draft ready for [process name]"
```

**Tools for automation:**
- **Zapier or Make (Integromat):** Connects Loom → Claude API → Notion
- **n8n (self-hosted):** More control, same workflow
- **Claude API:** For the actual SOP generation

**Cost:** ~$20-50/month for automation tools + API usage (minimal for Claude API unless high volume)

**ROI:** If you create 5+ SOPs/month, this pays for itself immediately.

---

## SOP Generator Mistakes to Avoid
- **Writing SOPs for processes you don't do regularly.** If it's a one-off task, a checklist is enough. SOPs are for repeatable processes.
- **Making SOPs too high-level.** "Post on social media" is not an SOP. "How to schedule and publish a LinkedIn post using Notion + Canva" is.
- **Not testing SOPs with someone else.** You wrote it, so you fill gaps mentally. Test with a team member or contractor.
- **Writing SOPs and never using them.** If no one follows your SOPs, they're decorative. Make them the default way to do things.
- **Perfectionism.** An 80% complete SOP used today is better than a perfect SOP you'll finish "someday." Publish drafts and iterate.
- **Not keeping SOPs updated.** A 6-month-old SOP for a process that's changed is worse than no SOP — it creates confusion.

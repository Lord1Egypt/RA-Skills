---
name: workplace-injury-rights
description: >-
  Workers' compensation navigation and workplace injury rights. Use when someone is injured at work, needs to file a workers' comp claim, is being pressured not to report an injury, or doesn't understand their rights after a workplace accident.
metadata:
  category: rights
  tagline: >-
    What to do when you get hurt on the job — documentation, reporting, your rights, filing workers' comp, and what your employer can't legally do.
  display_name: "Workplace Injury Rights & Workers' Comp"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install workplace-injury-rights"
---

# Workplace Injury Rights & Workers' Comp

Construction workers, food service staff, healthcare aides, warehouse pickers, tradespeople, agricultural workers — the people doing the most physically demanding work get hurt the most and know their rights the least. Every state requires employers to carry workers' compensation insurance. It covers your medical bills and lost wages when you're hurt on the job. But employers routinely pressure workers not to report injuries, insurance companies routinely deny valid claims, and most workers don't know they have the right to push back. This skill gives you the step-by-step protocol to protect yourself from the moment an injury happens.

```agent-adaptation
# Localization note — workers' compensation systems differ completely by country.
- US: State-run workers' comp systems. Every state has different rules, forms, deadlines,
  and dispute processes. Agent MUST identify user's state before giving specific guidance.
  Texas is unique — it's the only state where employers can opt out.
- UK: No workers' comp system. Employer liability insurance + NHS for treatment.
  Claims go through employer's insurer or employment tribunal. HSE (hse.gov.uk) for
  safety reporting. Statutory Sick Pay (SSP) for income replacement.
- AU: State-based WorkCover/WorkSafe systems (e.g., WorkSafe Victoria, SafeWork NSW).
  Similar structure to US workers' comp but administered differently.
- CA: Provincial Workers' Compensation Boards (e.g., WSIB in Ontario, WorkSafeBC).
  Federal workers covered by Government Employees Compensation Act.
- EU: Varies by country. Many have social insurance systems covering workplace injuries.
- Swap: Filing agencies, reporting deadlines, medical treatment rules, dispute resolution
  processes, OSHA equivalent (HSE in UK, Safe Work Australia, CCOHS in Canada).
- Reporting deadlines are CRITICAL and vary: US states range from "immediately" to
  90 days. UK has a 3-year limitation for civil claims. Get the deadline right.
```

## Sources & Verification

- **OSHA Worker Rights** -- Federal workplace safety standards and complaint filing. https://www.osha.gov/workers
- **State Workers' Compensation Board Websites** -- Each state maintains filing procedures, forms, and dispute resolution information. Search "[your state] workers' compensation board."
- **National Council on Compensation Insurance (NCCI)** -- Workers' comp data, research, and state-specific information. https://www.ncci.com
- **US Department of Labor Workers' Compensation Overview** -- Federal overview and links to state programs. https://www.dol.gov/general/topic/workcomp
- **American Bar Association Worker Injury Resources** -- Legal information on workplace injury claims and finding representation. https://www.americanbar.org
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- Someone just got hurt at work and doesn't know what to do
- User is being pressured by employer not to report a workplace injury
- Needs to file a workers' comp claim and doesn't know the process
- Workers' comp claim was denied and they want to appeal
- Employer is retaliating after an injury report (fired, hours cut, moved to worse position)
- Wants to understand their rights to medical treatment and wage replacement
- Unsafe conditions at work caused or could cause injury and they want to report it
- Being told to use personal health insurance for a work injury

## Instructions

### Step 1: Immediate Injury Response

**Agent action**: Walk user through what to do right after a workplace injury. Time-sensitive.

```
WHAT TO DO RIGHT NOW (in order)

1. GET MEDICAL ATTENTION if needed. Call 911 for emergencies. For non-emergencies,
   tell your employer you need to see a doctor. Your health comes first, paperwork second.

2. REPORT THE INJURY TO YOUR EMPLOYER — VERBALLY AND IN WRITING.
   Verbal: Tell your supervisor immediately. Say: "I was injured at work. I need
   to report it."
   Written: Follow up with written notification the same day (email, text, or
   handwritten note). Keep a copy.

3. DOCUMENT EVERYTHING. Right now. On your phone.
   - Photos of the injury
   - Photos of what caused the injury (equipment, spill, hazard)
   - Photos of the scene/location
   - Date and time
   - Names of witnesses
   - What you were doing when it happened
   - Your supervisor's response when you reported it

4. DO NOT sign anything your employer puts in front of you without reading it fully.
   If they hand you paperwork, say: "I'd like to review this before signing."
   Take it home. Read it. Google anything you don't understand.

5. DO NOT use your personal health insurance for a work injury.
   Workers' comp is a separate system. Your employer or their insurer pays — not you.

WHY REPORTING IMMEDIATELY MATTERS:
- Reporting deadlines are short. Some states require notice within 30 days.
  Others give 90 days. Some have no fixed deadline but delays weaken your claim.
- Late reporting is the #1 reason workers' comp claims get denied.
- "It didn't seem bad at the time" is common — but injuries that seem minor
  (back tweaks, repetitive strain) often get worse. Report even "small" injuries.
```

### Step 2: Complete Your Documentation

**Agent action**: Generate an incident documentation template for the user.

```
WORKPLACE INJURY INCIDENT REPORT — YOUR COPY

Record ALL of the following:
- Date, time, and specific location of injury
- Detailed description of what happened and what caused it
- Body part(s) affected and type of injury
- Witnesses: names and phone numbers (get these DAY OF — people leave jobs)
- Supervisor notified: name, time, and their response
- Medical treatment: where, when, provider name, diagnosis
- Photos taken: [ ] Injury  [ ] Scene/hazard  [ ] Equipment involved
- Any prior similar incidents at this workplace
- Safety measures that were or weren't in place

STORAGE: Keep this in a personal folder (not work devices). Back up to
personal email or cloud storage.
```

### Step 3: Employer Notification Letter

**Agent action**: Generate a formal written injury notification for the user to send to their employer.

```
EMPLOYER NOTIFICATION LETTER

[Your Name]
[Date]

To: [Supervisor/Manager Name], [Company Name]

RE: Notification of Workplace Injury — [Date of Injury]

I am providing formal written notice that I sustained a work-related injury
on [date] at approximately [time] while [describe activity] at [specific
location]. I injured my [body part(s)] — [description of injury].

Witnesses include [names]. I reported verbally to [supervisor] at [time]
on [date].

I request that you file a workers' compensation claim on my behalf immediately
and provide me with the claim number, insurance carrier name, and procedure
for obtaining medical treatment. I also request a copy of the company's
incident report.

Sincerely,
[Your Name / Phone / Email]

DELIVERY: Send via email (keep sent copy) AND printed copy to supervisor.
If no email, text a photo of this letter and keep the thread.
```

### Step 4: File the Workers' Comp Claim

**Agent action**: Guide user through the workers' comp filing process for their specific state.

```
WORKERS' COMP FILING — GENERAL PROCESS

1. EMPLOYER FILES THE CLAIM (in most states)
   Your employer is legally required to file the workers' comp claim with their
   insurance carrier after you report the injury. In most states, they must file
   within 7-10 days of your report.

   If your employer refuses to file or "forgets":
   - File directly with your state's workers' compensation board. Every state
     allows this. Search "[your state] workers' compensation file claim."
   - Call the state workers' comp board and report that your employer isn't filing.
     This itself is a violation in most states.

2. SEE AN APPROVED MEDICAL PROVIDER
   Rules vary by state:
   - Some states: Employer chooses the doctor (at least initially).
   - Some states: You can choose your own doctor from the start.
   - Most states: You can switch doctors after initial treatment (often after 1-2 visits).
   - CRITICAL: Tell the doctor this is a work injury. It affects how billing works.

3. GET YOUR CLAIM NUMBER
   After filing, you'll receive a claim number from the insurance company.
   Write it down. You need it for every interaction.

4. FOLLOW UP
   Call the insurance company within 1 week to confirm the claim is open.
   Ask: "What is my claim status? Who is my adjuster? What are my next steps?"

WHAT WORKERS' COMP COVERS:
- All medical treatment related to the injury (doctor visits, surgery, PT, medication)
- Wage replacement (typically 2/3 of your average weekly wage, tax-free)
- Mileage reimbursement for medical appointments
- Vocational rehabilitation if you can't return to your previous job
- Disability payments (temporary or permanent) if the injury limits your ability to work
```

### Step 5: Know Your Rights

**Agent action**: Clearly state the user's legal rights so they can't be intimidated.

```
YOUR RIGHTS — WHAT YOUR EMPLOYER CANNOT DO

1. CANNOT FIRE YOU for filing a claim. That's retaliation. Illegal in every state.
2. CANNOT REQUIRE personal health insurance for a work injury. Workers' comp
   is separate. You pay zero out of pocket.
3. CANNOT PRESSURE you not to report. "We'll handle it internally" and "think
   about the team's safety record" are pressure tactics, not concern.
4. CANNOT MAKE YOU SIGN a waiver or accept cash "to make it go away." Don't sign.
5. CANNOT DENY you medical treatment. If they say "just ice it," insist on a
   doctor and file the claim.
6. YOU HAVE THE RIGHT TO AN ATTORNEY. Workers' comp lawyers work on contingency
   (15-20% of settlement). No upfront cost. Free consultations.
```

### Step 6: Handle Common Employer Tactics

**Agent action**: Provide response scripts for specific intimidation scenarios.

```
WHAT THEY SAY -> WHAT YOU SAY

"Are you sure it happened at work?"
-> "Yes. [Location], [time], [task]. [Witnesses] were present. I need to file a report."

"Let's keep this between us."
-> "I need a formal report and workers' comp claim opened. That protects both of us."

"Filing will hurt our safety record."
-> "I'm injured and have a legal right to file. It needs to be documented."

"If you file, we might have to let you go."
-> "That would be retaliation, which is illegal. I'd like to file now."
   (Document this threat immediately — date, time, who said it, witnesses.)

"Just use your own insurance."
-> "Workers' comp is the correct coverage for a work injury."
```

### Step 7: If Your Claim Is Denied

**Agent action**: Guide user through the appeal process.

```
CLAIM DENIAL — WHAT TO DO

Common denial reasons:
- "Injury not reported timely" — fight this with your written notification letter
- "Injury not work-related" — get a second medical opinion
- "Pre-existing condition" — workers' comp covers aggravation of pre-existing conditions
- "Employer disputes the incident" — present witness statements and documentation

APPEAL PROCESS:
1. Read the denial letter carefully. It must state the reason and your appeal rights.
2. Note the appeal deadline (typically 30-90 days depending on state).
3. Get a workers' comp attorney NOW. Most offer free consultations and work on contingency.
   - State bar referral service
   - Search "workers' compensation attorney [your city]"
   - Legal aid if you qualify
4. Gather additional evidence: Second medical opinion, witness statements,
   photos, your personal documentation.
5. File the appeal with your state workers' comp board. Attorney can handle this.
6. Many states have mediation before a formal hearing. Your attorney prepares you.

DO NOT GIVE UP AFTER A DENIAL.
A significant percentage of initial denials are overturned on appeal. Insurance
companies deny claims hoping workers will go away. Don't go away.
```

### Step 8: Report Unsafe Conditions to OSHA

**Agent action**: If the injury was caused by unsafe working conditions, guide user through OSHA complaint filing.

```
OSHA COMPLAINT — FOR UNSAFE CONDITIONS

If unsafe conditions caused your injury, file an OSHA complaint (separate from
workers' comp). File online (osha.gov/workers/file-complaint), call
1-800-321-OSHA, or visit your local OSHA office.

- Confidential: You can file anonymously. OSHA doesn't tell your employer who filed.
- Retaliation for filing is illegal under Section 11(c) of the OSH Act.
- OSHA may inspect (unannounced), cite violations, and impose penalties
  ($16,000-$160,000+ per violation). Willful violations causing death can
  result in criminal prosecution.
- The hazard that hurt you still exists until someone reports it.
```

## If This Fails

- Employer fires you after filing: Contact a workers' comp attorney immediately. Retaliatory termination cases often result in significant settlements beyond the original injury claim. Document the timeline clearly: injury date, report date, filing date, termination date.
- Can't find an attorney to take your case: Contact your state's legal aid office (lsc.gov) or state bar lawyer referral service. For small claims, your state workers' comp board has an ombudsman who can help you navigate without an attorney.
- Medical provider says it's not work-related: Get a second opinion from a different doctor. Inform them of the specific work activities and circumstances. Request a detailed report linking the injury to your work duties.
- You're undocumented: Workers' comp rights apply regardless of immigration status in every state. Your employer cannot threaten deportation for filing a claim — that's both retaliation and potentially a federal crime. Worker centers and legal aid organizations experienced with immigrant workers can help navigate this.
- It's a repetitive stress injury (carpal tunnel, back problems) without a single incident: These are covered by workers' comp. The "injury" date is typically when you first noticed symptoms or when a doctor diagnosed the condition. Report it as soon as you become aware.

## Rules

- Report every injury, no matter how minor it seems. "Seemed fine at the time" is the beginning of most denied claims for injuries that get worse.
- Get it in writing. Verbal reports are deniable. Written notification creates proof.
- Never sign anything you don't fully understand, especially from the insurance company. "Release of liability" documents and early settlement offers are rarely in your interest without attorney review.
- Keep all medical records and correspondence in a personal location, not on work devices or accounts.
- Follow your doctor's restrictions. If the doctor says light duty, don't let your employer pressure you into full duty. Working beyond restrictions can jeopardize your claim and your health.
- Document everything with dates and times. Your daily log of pain levels, work restrictions, and interactions with employer/insurer is evidence.

## Tips

- Take photos of the injury progression over time. Day 1, day 3, day 7, etc. This documents the severity better than words.
- If your employer has security cameras, request (in writing) that footage be preserved immediately. Camera systems overwrite on 7-30 day cycles.
- Get witness contact information the day of the injury. Coworkers may leave the company later and be hard to reach.
- Workers' comp wage replacement is typically tax-free. So 2/3 of your normal pay (the standard rate) is closer to your actual take-home than it sounds.
- Don't post about your injury on social media. Insurance investigators monitor claimants' profiles. A photo of you at a family BBQ can be used to argue you're not really injured.
- If you're sent back to work on "light duty" and your employer doesn't actually accommodate the restrictions (gives you full duty anyway), document this and inform your doctor and your adjuster.
- Request a copy of your employer's OSHA 300 log — this records all workplace injuries and illnesses. It's public information and shows if there's a pattern of injuries at your workplace.

## Agent State

```yaml
workplace_injury_session:
  injury_date: null
  injury_type: null
  body_part: null
  jurisdiction: null
  employer_notified: false
  written_notification_sent: false
  claim_filed: false
  claim_number: null
  attorney_retained: false
  osha_complaint_filed: false
  return_to_work_status: null
  documentation_complete: false
```

## Automation Triggers

```yaml
triggers:
  - name: reporting_deadline_alert
    condition: "injury reported but written notification or claim not yet filed"
    schedule: "daily_check_first_week"
    action: "Alert user about reporting deadlines for their state and urge written notification and claim filing"
  - name: claim_followup
    condition: "workers' comp claim filed but no response received within 14 days"
    schedule: "14_days_after_filing"
    action: "Prompt user to call insurance adjuster for claim status update and provide adjuster contact guidance"
  - name: denial_appeal_deadline
    condition: "claim denied and appeal deadline approaching"
    schedule: "weekly_check"
    action: "Warn user about approaching appeal deadline and urge attorney consultation if not already retained"
```

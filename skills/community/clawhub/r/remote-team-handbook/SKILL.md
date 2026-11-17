---
name: remote-team-handbook
description: Drafts remote work handbook sections for US distributed teams, with FLSA, leave, state and accessibility items flagged for HR. Use when the user asks for remote work policy template, work from home policy us, distributed team handbook section. For US HR managers and operations leads writing policy for distributed and hybrid teams.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Remote Team Handbook

**Drafts remote work handbook sections for US distributed teams, with FLSA, leave, state and accessibility items flagged for HR.** Written for US HR managers and operations leads writing policy for distributed and hybrid teams.

Use this skill when someone asks for:

- remote work policy template
- work from home policy us
- distributed team handbook section
- async work policy draft
- telework policy state rules

---

## The job

One remote policy is written for one state, so employees elsewhere get the wrong break, overtime and equipment rules, and the handbook is never updated when a state changes its law.

## What you get

1. Collect the states the team works in, the working hours, the equipment rules and the reason behind each policy.
2. Write the section in the order a new hire reads it: where work happens, hours and breaks, equipment, expenses, security and accommodations.
3. Check each section against the FLSA and the FMLA, and against the state rules for the work states in the team.
4. Mark the state-dependent items as open items for HR, so a California rule is never written as a national rule.
5. Set the owner, the effective date and the review cycle for the section, and list the sections that are still missing.

Output contract:

- section - the drafted handbook section with its scope, the rule it states and the exception it allows
- state_items - the rules that change by work state, each with the state named and the source to confirm
- federal_checks - the FLSA, FMLA and ADA points the section touches and the evidence to attach
- open_items - the items HR has to decide, including equipment, expenses and work location rules
- review_block - the owner, the effective date, the review cycle and the sections still to be written

## US specifics that matter

- The FLSA overtime rule (29 USC 207) applies to a remote nonexempt employee the same as it does to an on-site employee, and payroll records are kept under 29 CFR part 516.
- Federal law does not require meal or rest breaks, but state law does, and California's meal and rest break rules (Labor Code 226.7 and 512) apply to an employee whose work is performed in California, including remote work.
- The FMLA (29 USC 2611 et seq.) allows up to 12 weeks of unpaid, job-protected leave, and eligibility turns on 12 months of service, 1,250 hours and 50 employees within 75 miles, which is a single-employer test even for a distributed team.
- A remote employee usually works in the state where they live, so payroll withholding, unemployment insurance and state income tax follow the work state, and some states and cities add a local earnings tax that the employer has to withhold.
- The ADA applies to telework: an employer may have to grant telework as a reasonable accommodation, and EEOC guidance treats the employer's telework policy as part of the interactive process.
- New York City's Commuter Benefits Law (NYC Admin. Code 20-926) reaches most private and nonprofit employers with 20 or more full-time non-union employees in the city, so a hybrid policy there carries a transit benefit rule that a national template does not.

## Guardrails (hard rules)

- Never state a state break, leave, expense or tax rule as settled law; mark it as a state item for HR or counsel to confirm.
- Never put an employee's home address, personal phone number, health information or family situation in a handbook or a shared tracker.
- Never promise equipment reimbursement, a stipend or a home office allowance that the company has not approved.
- Never distribute the handbook as a final policy; it is a draft for HR, for legal and for the employee's work state to review.

## Quickstart

### 1. Fill in the brief

`templates/remote-handbook-section.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/render_handbook_section.py --input remote-handbook-section.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/remote-work-us-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Pay, hours and overtime**

- FLSA overtime at 1.5 times the regular rate above 40 hours in a workweek applies to a remote nonexempt employee.
- The white-collar exemptions in 29 CFR part 541 need a salary test and a duties test, so a remote title alone is not exempt.
- Payroll records are kept for three years under 29 USC 211(c) and 29 CFR part 516.
- A section that states a workday length has to say whether the hours are fixed, flexed or set by the employee.

**Breaks and rest periods**

- Federal law sets no meal or rest break requirement, so a national policy cannot promise breaks on its own authority.
- California's Labor Code 226.7 and 512 apply to work performed in California, including remote work for a California-based employee.
- Other states, such as Colorado, Illinois and Michigan, have their own break or day-rest rules for covered employees.
- Write the break rule per work state and mark the rest as an open item for HR.

**Leave and accommodations**

- FMLA leave is unpaid and job-protected, and eligibility turns on 12 months of service, 1,250 hours and 50 employees within 75 miles.
- Several states add paid leave that covers smaller employers, so the leave paragraph changes with the state and the headcount.
- The ADA applies to telework, and telework can be the reasonable accommodation an employee needs.
- Keep the accommodation request and the medical documentation outside the handbook and outside any shared tracker.

**Work state, tax and local rules**

- A remote employee usually works where they live, so the work state drives withholding, unemployment insurance and state income tax.
- Some states and cities levy a local earnings tax that the employer withholds, so the section names the collection point.
- New York City's Commuter Benefits Law (20-926) applies to many employers with 20 or more full-time non-union employees in the city.
- Keep a work state on every record, and review it whenever an employee moves.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/remote-work-us-rules.md` - US remote work rules and state variation
- `templates/remote-handbook-section.yaml` - the brief to fill in
- `scripts/render_handbook_section.py` - the working script

## Verify the bundle

```bash
python3 scripts/render_handbook_section.py --input remote-handbook-section.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.

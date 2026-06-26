---
name: wage-theft-defense
description: >-
  Tools for identifying, documenting, and recovering stolen wages. Use when someone suspects unpaid overtime, tip theft, minimum wage violations, off-the-clock work, misclassification as independent contractor, or paycheck deductions that seem wrong.
metadata:
  category: rights
  tagline: >-
    Document, report, and recover stolen wages — demand letters, labor board filings, and collective action templates for the #1 workplace crime in America.
  display_name: "Wage Theft Defense Kit"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install wage-theft-defense"
---

# Wage Theft Defense Kit

Wage theft — employers not paying workers what they're legally owed — costs US workers over $15 billion per year. That's more than all robberies, burglaries, and motor vehicle theft combined. It hits food service, construction, personal care, agriculture, and retail the hardest. The workers with the least power lose the most money. This skill gives you the documentation templates, demand letters, and filing procedures to get your money back.

```agent-adaptation
# Localization note — wage and hour laws vary dramatically by jurisdiction.
- Agent MUST detect user's jurisdiction before providing specific legal guidance.
- US: Federal FLSA sets floor. State laws often exceed it. Some cities (NYC, LA, Seattle)
  have additional protections. Check state AND local.
- UK: National Minimum Wage Act. Enforcement through HMRC (gov.uk). Employment tribunal
  for claims. ACAS for early conciliation (mandatory pre-tribunal step).
- AU: Fair Work Act. Fair Work Ombudsman (fairwork.gov.au) handles complaints.
  Modern Awards set industry-specific minimum rates.
- CA: Provincial employment standards. Federal for federally regulated industries.
  Employment Standards branch of provincial labor ministry handles complaints.
- EU: Country-specific. Generally stronger enforcement mechanisms than US.
- Swap: minimum wage amounts, overtime thresholds, filing agencies, statute of
  limitations, legal aid resources, demand letter legal requirements.
- Tip laws vary enormously — US tip credit vs UK/AU where tips are on top of full
  minimum wage. Critical to get this right.
```

## Sources & Verification

- **Economic Policy Institute** -- Wage theft research and policy analysis. Key report: "Employers steal billions from workers' paychecks each year." https://www.epi.org
- **US Department of Labor, Wage and Hour Division** -- Federal wage complaint filing and FLSA enforcement. https://www.dol.gov/agencies/whd
- **National Employment Law Project (NELP)** -- Worker rights advocacy and wage theft prevention resources. https://www.nelp.org
- **State Labor Commissioner Offices** -- Each state maintains a wage claim filing system. Search "[your state] labor commissioner wage claim."
- **Legal Aid Society** -- Free legal representation for low-income workers in wage disputes. Local chapters nationwide.
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- Someone isn't getting paid for all hours worked
- Employer is making illegal deductions from paychecks
- Tips are being skimmed, pooled illegally, or kept by management
- Working "off the clock" before or after shift (setting up, cleaning, meetings)
- Classified as independent contractor but treated as an employee
- Overtime hours aren't being paid at 1.5x rate
- Paid below minimum wage
- Final paycheck after quitting or being fired wasn't received or was short
- Wants to know if what their employer is doing is legal

## Instructions

### Step 1: Identify the Type of Wage Theft

**Agent action**: Ask user about their pay situation and identify which type(s) of wage theft may be occurring.

```
TYPES OF WAGE THEFT

1. UNPAID OVERTIME
   Federal law (FLSA): Non-exempt workers must be paid 1.5x base rate for hours
   over 40/week. Some states have daily overtime (CA: over 8 hours/day).
   Common violations: "Averaging" hours over two weeks, calling workers "salaried"
   when they don't meet exemption requirements, rounding time down.

2. MINIMUM WAGE VIOLATIONS
   Federal minimum: $7.25/hr (some states are $15+). Tipped minimum: $2.13/hr
   federal (employer must make up difference if tips don't reach full minimum).
   Common violations: Paying below state minimum, not making up tipped shortfall,
   paying "training wage" longer than legally allowed.

3. OFF-THE-CLOCK WORK
   Any work you're required to perform must be paid. Period.
   Common violations: Required to arrive early to set up, staying after shift to
   clean/close, working through "unpaid" lunch breaks, answering work texts/calls
   off-shift.

4. TIP THEFT
   Tips belong to the worker. Management cannot take tips (federal law since 2018).
   Common violations: Managers keeping a share of tip pool, requiring tip-outs to
   non-tipped workers (varies by state), skimming from credit card tips.

5. ILLEGAL DEDUCTIONS
   Employers cannot deduct from wages for: cash register shortages (in most states),
   broken equipment, uniforms (if it drops you below minimum wage), walkouts/dine-and-dash.
   Common violations: Deducting for breakage, charging for required uniforms, docking
   pay for customer complaints.

6. MISCLASSIFICATION
   Calling you an "independent contractor" to avoid paying overtime, benefits, and
   employment taxes — while controlling your schedule, methods, and tools.
   Red flags: You have set hours, use company equipment, can't work for competitors,
   work exclusively for one company.
```

### Step 2: Start Documenting NOW

**Agent action**: Generate a personal time log template for the user to begin tracking immediately.

Documentation is everything. Your employer has payroll records. You need your own.

```
PERSONAL TIME LOG — START TODAY

DATE | SHIFT START | SHIFT END | BREAK(S) | TOTAL HOURS | HOURS ON PAYCHECK | DISCREPANCY | NOTES
-----|-------------|-----------|----------|-------------|-------------------|-------------|------
     |             |           |          |             |                   |             |
     |             |           |          |             |                   |             |

DOCUMENTATION RULES:
1. Log EVERY shift. Real start time (when you actually began work), real end time.
2. Note any off-the-clock work: pre-shift setup, post-shift cleaning, working lunch.
3. Keep screenshots of your schedule (posted or app-based).
4. Save every pay stub. Photo them if they're paper. Download PDFs if digital.
5. Note witnesses — who was working the same shift and saw the same hours?
6. If tips: Track your cash tips daily and credit card tip amounts. Compare to what
   shows on your paycheck.
7. Keep this log OUTSIDE of work. Personal phone, home notebook, personal email.
   Do NOT store it on a work device or in a work account.

HOW LONG TO TRACK:
- Minimum 2 weeks to establish a pattern.
- 4+ weeks is stronger for a claim.
- The longer the documentation, the stronger your case.

PRESERVE EVIDENCE:
- Screenshot and email time clock records to yourself weekly.
- If your employer uses an app (Homebase, When I Work, Deputy), screenshot your
  actual punches before they can be edited.
- Save any texts, emails, or messages from managers telling you to clock out
  and keep working, come in early without clocking in, etc.
```

### Step 3: Calculate What You're Owed

**Agent action**: Help user calculate the specific dollar amount of stolen wages.

```
CALCULATION WORKSHEET

UNPAID OVERTIME:
(Hours over 40 per week) x (hourly rate x 0.5) x (number of weeks) = amount owed
Example: 5 hours OT/week x ($15 x 0.5 = $7.50) x 12 weeks = $450

OFF-THE-CLOCK WORK:
(Minutes per day) / 60 x (hourly rate) x (days worked) = amount owed
Example: 20 min/day x ($15/hr = $5) x 60 days = $300

MINIMUM WAGE SHORTFALL:
(State minimum - actual hourly rate) x (hours per week) x (weeks) = amount owed

TIP THEFT:
(Tips earned - tips received) x (shifts affected) = amount owed

TOTAL OWED: Add all categories. Then note: Under FLSA, you may be entitled to
DOUBLE the unpaid wages (liquidated damages) plus attorney's fees.

Federal statute of limitations: 2 years (3 years if violation was willful).
State statutes vary: Some allow 3-6 years. CHECK YOUR STATE.
```

### Step 4: Send a Formal Demand Letter

**Agent action**: Generate a customized demand letter based on user's specific wage theft situation.

Send this BEFORE filing a complaint. It creates a paper trail and sometimes resolves the issue immediately — many employers pay up when they realize you know your rights.

```
DEMAND LETTER TEMPLATE

[Your Name]
[Your Address]
[Date]

[Employer Name]
[Employer Address]

RE: Demand for Payment of Unpaid Wages

Dear [Employer/Manager Name],

I am writing to formally demand payment of wages owed to me for work performed
at [Company Name].

Based on my records, I am owed the following:

[Description of violation — e.g., "Between [start date] and [end date], I worked
approximately [X] hours of overtime per week that were not compensated at the
legally required overtime rate of 1.5 times my regular rate of $[X]/hour."]

The total amount of unpaid wages owed is $[amount].

Under the Fair Labor Standards Act [and/or STATE law], I am entitled to recover
unpaid wages plus an equal amount in liquidated damages, as well as reasonable
attorney's fees and costs.

I request that you remit payment of $[amount] within 15 calendar days of the
date of this letter. If I do not receive payment by [specific date], I intend
to file a formal complaint with the [State Labor Board/US Department of Labor
Wage and Hour Division] and pursue all available legal remedies.

Sincerely,
[Your Name]
[Your Phone Number]
[Your Email]

SENDING INSTRUCTIONS:
- Send via certified mail, return receipt requested. This proves they received it.
- Also send via email if you have a manager's email. Screenshot the sent email.
- Keep a copy of everything.
- Set a calendar reminder for the 15-day deadline.
```

### Step 5: File a Government Complaint

**Agent action**: Guide user through the appropriate complaint filing based on their jurisdiction.

If the demand letter doesn't work (or you want to skip straight to enforcement), file with the government. It's free, you don't need a lawyer, and retaliation for filing is illegal.

```
FEDERAL (DOL): File at dol.gov/agencies/whd/contact/complaints or call
1-866-487-9243. Provide your info, employer info, dates, pay rate, hours,
violation type. Investigation takes weeks to months. DOL can order back pay
AND penalties. Immigration status is irrelevant to wage claims.

STATE (often faster, broader protections): Search "[your state] labor
commissioner wage claim." Many have online filing. State claims can cover
violations beyond FLSA. You can file state AND federal simultaneously.

SMALL CLAIMS (for smaller amounts): Threshold $5,000-$25,000 by state. Filing
fee $30-75. No lawyer needed. Bring your time log, pay stubs, demand letter
with mailing proof, and all communications.
```

### Step 6: Organize Collectively

**Agent action**: If the wage theft is systemic, guide user toward collective action.

```
IF IT'S HAPPENING TO YOU, IT'S HAPPENING TO YOUR COWORKERS

Collective action is more powerful than individual claims:
- Harder for the employer to retaliate against a group.
- The DOL takes multi-worker complaints more seriously.
- Potential for class action or collective action lawsuits.

HOW TO ORGANIZE:
1. Talk to coworkers privately. Off-site, off-clock. Ask: "Are you getting paid
   for [the time you spend doing X]?"
2. If others are affected, document together. Each person keeps their own time log.
3. File complaints as a group — reference each other's complaints by name.
4. Contact a workers' rights organization:
   - National Employment Law Project: nelp.org
   - Your state's legal aid society
   - Worker centers (often focused on immigrant worker communities)
   - Your union, if you have one.

RETALIATION PROTECTION:
Under federal law (FLSA Section 15(a)(3)) and most state laws, your employer
CANNOT fire, demote, cut hours, change your schedule, or otherwise retaliate
against you for filing a wage claim or talking to coworkers about pay.

If they do: That's a SEPARATE violation with its own penalties. Document the
retaliation (date, what happened, witnesses) and report it in your complaint.
```

### Step 7: Find Legal Help

**Agent action**: Connect user with free or low-cost legal resources for wage theft cases.

```
FREE AND LOW-COST LEGAL HELP

- Legal Services Corporation (lsc.gov): Free representation for low-income workers.
- State bar lawyer referral service: Low-cost initial consultation.
- Workers' rights attorneys: Many take wage theft on contingency (33% of recovery).
  Under FLSA, employer pays your attorney fees if you win. Search "wage theft
  attorney [your city]."
- Worker centers: ROC (rocunited.org) for food service, NDLON (ndlon.org) for
  day laborers, Interfaith Worker Justice (iwj.org), Jobs With Justice (jwj.org).
```

## If This Fails

- Employer ignores demand letter: File the government complaint immediately. The demand letter was a courtesy, not a requirement.
- Government investigation is taking months: Follow up monthly by phone. Ask for a status update and case number. Government agencies are understaffed — persistence matters.
- Employer retaliates (fires you, cuts hours): Document the retaliation immediately and add it to your complaint. Retaliation claims often result in larger penalties than the original wage theft.
- Amount is too small for an attorney to take: Use small claims court. No lawyer needed. Filing fee is recoverable if you win.
- You're undocumented and afraid to file: Immigration status does not affect your right to file a wage claim. The DOL does not share information with immigration enforcement. Worker centers specializing in immigrant communities can help navigate this safely.

## Rules

- Document everything. Your memory is not evidence. Your time log, screenshots, and pay stubs are evidence.
- Send the demand letter via certified mail. "I told my boss verbally" is worth nothing in a legal proceeding.
- Never sign anything from your employer related to pay disputes without understanding it fully. If they present a "settlement" or "release," have a legal aid attorney review it first.
- Don't quit in anger before filing your complaint. It's easier to prove ongoing violations while you're still employed. If you're fired, that strengthens your retaliation claim.
- The statute of limitations is real. Federal: 2 years (3 if willful). State: varies but don't wait. File sooner rather than later.
- Talk to coworkers about pay. It's your legal right under the National Labor Relations Act, regardless of any "policy" your employer has against it.

## Tips

- Many employers settle quickly after receiving a formal demand letter because fighting a wage theft claim costs more in legal fees than paying what they owe.
- Your state's attorney general may have a wage theft complaint option separate from the labor board. Some AG offices are more aggressive enforcers.
- If your employer pays you in cash and you have no pay stubs, your time log and witness testimony become your primary evidence. Keep that log meticulous.
- Take photos of the time clock and your punches. Some employers edit time records after the fact.
- If you work through a staffing agency, both the agency AND the client company may be liable for wage theft. File against both.
- Meal and rest break violations are a form of wage theft in states that mandate paid breaks (check your state law — California is especially strict on this).
- Tip theft by managers was made explicitly illegal under federal law in 2018 (Consolidated Appropriations Act). This is settled law, not a gray area.

## Agent State

```yaml
wage_theft_session:
  jurisdiction: null
  violation_types: []
  documentation_started: false
  amount_owed_calculated: false
  demand_letter_sent: false
  complaint_filed: false
  complaint_agency: null
  legal_aid_connected: false
  retaliation_reported: false
  statute_of_limitations_deadline: null
```

## Automation Triggers

```yaml
triggers:
  - name: statute_of_limitations_warning
    condition: "user's earliest documented violation is approaching 18 months old"
    schedule: "monthly_check"
    action: "Warn user about approaching statute of limitations and urge filing if not already done"
  - name: demand_letter_followup
    condition: "demand letter sent and 15-day deadline has passed without resolution"
    schedule: "16_days_after_letter"
    action: "Prompt user to file government complaint and connect with legal aid if not already done"
  - name: retaliation_detection
    condition: "user reports schedule change, demotion, or termination after filing wage complaint"
    schedule: "on_demand"
    action: "Document retaliation and guide user through adding retaliation claim to existing complaint"
```

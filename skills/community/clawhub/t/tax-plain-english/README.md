# tax-plain-english

**US tax questions answered like a knowledgeable friend — not a tax manual.**

Most AI tax answers are either too hedged to be useful, or too confident on things that deserve professional judgment. This skill does neither. It gives you a real answer first, explains the rule simply, tells you exactly what to document, and is honest about when you actually need a CPA.

---

## What it does

Ask any US federal or California tax question in plain language. The skill:

- **Detects the question type** and picks the right output format automatically — a "how do I file my W-4?" gets step-by-step guidance, a "how much will I owe?" gets a worked calculation, an IRS notice question gets a severity assessment first
- **Answers with current 2024 numbers** — brackets, contribution limits, deadlines, credits — from a built-in reference file, not from hallucination
- **Flags complexity honestly** with a 🟢/🟡/🔴 system and a specific reason, not a generic disclaimer
- **Covers all user types** — W-2 employees, freelancers, small business owners, and people with complex situations (international students, renters, investors)

## Example questions it handles well

- *"Is my home office deductible?"*
- *"I freelanced $60k this year — what do I owe?"*
- *"I'm an international student, how do I fill out my W-4?"*
- *"I got a CP2000 notice from the IRS. How scared should I be?"*
- *"Can I contribute to a Roth IRA if I make $150k?"*
- *"I sold crypto across three exchanges — how do I do my taxes?"*

## Five output modes

The skill automatically selects the right structure based on what you asked:

| Question type | Output format |
|---|---|
| Concept ("Is X deductible?") | Direct answer → rule → documentation → flag |
| Procedural ("How do I file X?") | Context → numbered steps → do this now → flag |
| Calculation ("How much will I owe?") | Estimate first → worked math → what changes it → flag |
| Complex situation (multiple variables) | Name the variables → address each → synthesize → flag |
| Panic (IRS notice, back taxes) | Severity → what it means → what NOT to do → action steps |

## Bundled reference files

The skill includes four reference files it loads on demand:

- `references/2024-numbers.md` — every rate, bracket, limit, and deadline for 2024
- `references/irs-publications.md` — 40+ topics mapped to official IRS publications and interactive tools
- `references/state-quirks.md` — notable state-level differences (CA capital gains, no-income-tax states, Social Security treatment, remote work traps)
- `references/escalation-guide.md` — calibration for the 🟢/🟡/🔴 flag with specific examples and professional finder links

## Scope

- **US federal tax law**, current tax year
- State notes included where rules diverge significantly (CA, NY, TX, FL, WA, IL)
- Non-US questions redirected to appropriate local authorities
- Does not prepare returns or fill out forms
- Does not give specific investment advice requiring knowledge of your full financial picture

## Install

```bash
npx clawhub@latest install howie-ge/tax-plain-english
```

Or clone and drop the folder into your skills directory:

```bash
git clone https://github.com/howie-ge/tax-plain-english
cp -r tax-plain-english ~/.openclaw/skills/
```

## License

MIT — free to use, modify, and share.

---

*Numbers and rules are based on 2024 US federal tax law. Always verify with IRS.gov or a licensed tax professional before filing. This skill is educational, not legal or financial advice.*

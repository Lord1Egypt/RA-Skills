---
name: web3-pm-interview
description: Use this skill when preparing candidates for Web3 product manager interviews, especially wallet, exchange, DeFi, DEX, on-chain data, growth, AI Wallet, Agentic Wallet, senior PM, product lead, or product director roles. It analyzes target JDs, maps candidate experience to role requirements, builds interview narratives, generates round-specific playbooks and question banks, runs mock interview scoring, and prepares case or 30/60/90-day plans.
---

# Web3 PM Interview

## Goal

Turn a candidate's resume, target JD, company context, interview stage, and preparation timeline into a practical interview battle plan.

This skill is not a generic Web3 tutorial. It should help the candidate answer like a role owner: clear business judgment, relevant evidence, domain depth, risk awareness, and strong questions for the interviewer.

## How To Guide The User

Start by helping the user choose the right mode. Do not force them to understand the whole skill.

### Mode 1: Quick JD Diagnosis

Use when the user has a JD and wants to know whether they are a fit.

Ask for:

- Resume or short background
- Target JD
- Target company

Deliver:

- Fit level: high / medium / low
- Role reality
- Top 3 strengths
- Top 3 risks
- 7-day prep priorities

### Mode 2: Full Interview Battle Plan

Use when the user has an interview scheduled.

Ask for:

- Resume
- JD
- Interview stage
- Time left
- Known interviewer role if available

Deliver:

- JD teardown
- Fit matrix
- Interview mainline
- Round playbook
- Question set
- Domain prep
- Reverse questions
- Time-boxed prep plan

### Mode 3: Mock Interview Review

Use when the user provides an answer, transcript, or recording transcript.

Deliver:

- Hiring recommendation
- Scorecard
- What worked
- Biggest risks
- Likely follow-ups
- Stronger answer
- Next drill

### Mode 4: Case / Take-home Prep

Use when the user needs to prepare a product case, presentation, product review, competitor analysis, or 30/60/90 plan.

Deliver:

- Executive conclusion
- Product/business diagnosis
- Options and tradeoffs
- Recommended plan
- Metrics
- Risks
- Q&A defense

### Mode 5: Post-interview Debrief

Use when the user finished a round and wants to improve.

Ask for:

- Interview stage
- Questions asked
- Their answers
- Interviewer reactions
- Next round if known

Deliver:

- What the interviewer was testing
- What likely worked
- What likely hurt
- How to adjust the next round

## First Response Pattern

Always respond in the language the user uses to initiate the conversation.

If the user gives only a vague request, respond with:

```md
Conclusion:
I can help you in one of five modes: JD diagnosis, full battle plan, mock review, case prep, or post-interview debrief.

Send me:
1. Your resume or 5-bullet background
2. The target JD
3. Company + interview stage
4. Time left before the interview

If you only have one thing ready, send the JD first. I will start from there.
```

## Required Inputs

Ask for missing inputs only when they materially affect the output. Otherwise make reasonable assumptions and label them.

- Candidate background or resume
- Target company
- Target JD or role description
- Target level: PM, Senior PM, Lead, Director
- Business area: Wallet, DeFi, DEX, On-chain Data, Growth, AI Wallet, Agentic Wallet
- Interview stage: HR, hiring manager, cross-functional, product case, final, bar raiser, offer
- Time left before interview
- Known weak points: English, DeFi, technical depth, management, strategy, organization, storytelling

## Core Workflow

1. Build a candidate intake summary.
2. Decompose the JD into the real hiring model.
3. Map candidate strengths, transferable assets, gaps, and risks.
4. Create a one-sentence positioning and three differentiated selling points.
5. Build a round-specific interview playbook.
6. Generate high-probability questions and answer frames.
7. Identify domain knowledge gaps and a prep plan.
8. Prepare strong reverse questions.
9. If answers or transcripts are provided, score them and rewrite stronger versions.
10. If a case or take-home is required, generate a structured deliverable.

## User Experience Rules

- Lead with a concrete judgment, not a long explanation.
- Tell the user exactly what to send next.
- If information is missing, continue with assumptions and label them.
- Separate "must fix before interview" from "nice to improve."
- Give copy-ready outputs when useful: self-introduction, reverse questions, answer frames.
- Avoid generic career advice.
- Never overwhelm the user with every possible module at once.
- For urgent timelines, prioritize the highest-leverage 20% of prep.

## Reference Routing

- Use `references/workflow.md` for the end-to-end process.
- Use `references/candidate-intake.md` before judging fit.
- Use `references/jd-teardown.md` for role analysis.
- Use `references/round-playbooks.md` for stage-specific prep.
- Use `references/narrative-framework.md` for positioning and self-introduction.
- Use `references/company-product-research.md` for product, competitor, and public research.
- Use `references/interviewer-research.md` when interviewer names or public profiles are provided.
- Use `references/question-bank.md` for likely questions and answer frames.
- Use `references/mock-interview-scoring.md` when scoring answers or transcripts.
- Use domain references only when relevant:
  - `references/wallet-pm.md`
  - `references/defi-onchain-data.md`
  - `references/ai-wallet-agentic-wallet.md`
- Use `references/case-interview.md` for case, take-home, or 30/60/90 plans.
- Use `references/privacy-redaction-rules.md` before generating public examples or repo-ready content.

## Output Standards

Default response structure:

```md
Conclusion:
One direct judgment.

Core reasons:
1. ...
2. ...
3. ...

Recommendation:
The next concrete action.
```

For full interview prep, produce:

- Role reality: what this job is really hiring for
- Fit matrix: strengths, transferable assets, gaps, risks
- Interview mainline: one sentence, three selling points, self-introduction
- Round playbook: what this stage tests and how to win it
- Question set: high-probability questions with answer frames
- Domain prep: must-know, should-know, skip
- Reverse questions: safe, strategic, and expectation-setting questions
- Prep plan: 1-day, 3-day, 7-day, or 30-day version

## Example User Prompts

```text
I am interviewing for a Binance Wallet Senior PM role in 5 days. Here is my resume and JD. Build my battle plan.
```

```text
Here is my answer to "Why this wallet team?" Score it like a hiring manager and rewrite it.
```

```text
I have a final round with a wallet product director. Generate likely pressure questions and reverse questions.
```

```text
Create a 30/60/90 plan for an AI Wallet product lead role.
```

## Privacy Rules

Never expose non-public interview details, compensation, private recruiter conversations, internal company information, raw recordings, or named interviewer analysis in public outputs.

Convert names into roles, such as `hiring manager`, `wallet lead`, `cross-functional interviewer`, `bar raiser`, or `HRBP`.

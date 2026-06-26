# Dynamic Question Generation Mechanism

> ⚠️ This document is a **reference guide for dynamic question generation**, not a fixed question list.
> Questions must be dynamically generated based on the user's specific project context.

---

## Core Principles

**Question Generation = Project Context Analysis + Domain Knowledge + Logical Reasoning**

1. **Project Context Analysis**: Understand what project the user described, what stage they're at, what information they've provided
2. **Domain Knowledge**: Invoke relevant domain knowledge (AI products / content products / tool products) to generate the most likely relevant questions
3. **Logical Reasoning**: Based on known information, deduce what's missing

---

## Heuristic Rules for Question Generation

### Rule 1: From Broad to Specific

Start with broad questions to establish global understanding, then gradually dive into specifics.

```
Broad: What product do you want to build?
    ↓
Specific: Who is the core user?
    ↓
More Specific: What pain point does this solve for them?
```

### Rule 2: Generate Follow-up Questions on Demand

Follow-up questions are not pre-fixed; they emerge **as needed** based on user responses.

| User Response | Triggers Follow-up Questions |
|---------------|------------------------------|
| "I want to build an AI product" | AI adaptability verification, data sources, tech stack selection |
| "I want to build a content product" | Content sources, UGC/PGC, creation incentives |
| "I want to build a tool product" | Usage scenarios, user barriers, willingness to pay |
| "I have no technical background" | Tech approach selection (low-code / outsourcing / self-build) |
| "I have no budget" | Prioritize free tools, open-source solutions, estimate monthly costs |

### Rule 3: Question Trees are Living

Question trees **continuously improve** during planning:

- **Add**: Discover missed important questions
- **Delete**: Confirmed irrelevant questions
- **Split**: Too large/vague questions split into specific sub-questions
- **Merge**: Multiple similar questions consolidated
- **Reorder**: Adjust priorities based on context

---

## Question Patterns by Project Type

> The following are question pattern references for different project types. Specific questions are generated based on actual context.

### AI Products

```
Typical question patterns:
├── Is AI the core feature or a supporting feature?
├── Can existing AI technology support this requirement?
├── Where does the data come from? Is it enough for model training?
├── How do we validate AI effectiveness?
├── What is users' tolerance for "AI errors"?
└── What regulatory/compliance risks exist?
```

### Tool Products

```
Typical question patterns:
├── In what scenario do users use this?
├── What are existing solutions? Why switch?
├── How high is user switching cost?
├── Free or paid? How much?
└── How to acquire first users?
```

### Content / Community Products

```
Typical question patterns:
├── Where does content come from? (UGC/PGC/AIGC)
├── What is the content creator incentive mechanism?
├── How to ensure content quality?
├── How is community tone defined?
└── What is the monetization path?
```

### Platform Products

```
Typical question patterns:
├── Supply side or demand side first?
├── How to cold-start a two-sided user base?
├── How does the platform build trust?
├── What fee percentage is reasonable?
└── How to avoid regulatory risks?
```

---

## Follow-up Question Trigger Conditions

### Common Trigger Conditions

| Condition | Triggers Follow-up Question |
|-----------|----------------------------|
| User mentions specific technology | Tech selection, alternatives, migration costs |
| User mentions target users | User personas, usage scenarios, pain point validation |
| User mentions budget | Cost structure, minimum viable cost, savings options |
| User mentions time | Critical path, MVP definition, time risks |
| User mentions competitors | Differentiation, inherited advantages, disadvantage avoidance |
| User says "I don't know" | Provide options, research options, recommend approach |
| User says "either is fine" | Probe preferences, assume scenarios, recommend one |
| User mentions "risks" | Specific risk scenarios, response plans, monitoring metrics |

### Trigger Timing

1. **Immediately after response**: After user responds, immediately analyze if follow-up is needed
2. **At stage end**: Check if any important questions were missed
3. **At summary stage**: Review all questions for omissions

---

## Question Quality Checklist

Before generating each question, verify it meets these standards:

| Standard | Checklist |
|----------|-----------|
| **Valuable** | Can this question change a decision or reduce uncertainty? |
| **Answerable** | Does the user have enough information to answer? |
| **Specific** | Is the question specific enough, not too broad? |
| **Non-redundant** | Is this question duplicate of ones already asked? |
| **Timely** | Is this the right moment to ask? |

---

## Example: Different Question Trees for the Same "Voice Scoring" Project

### Scenario A: User says they have technical background and want to build a personal product

```
Question Tree:
├── Stage 1: Discovery
│   ├── Core question: What makes this voice scoring tool unique?
│   └── Follow-up: What tech stack are you proficient in? What AI model do you plan to use?
```

### Scenario B: User says they have no technical background and want to build a mini-program

```
Question Tree:
├── Stage 1: Discovery
│   ├── Core question: What do you want users to do in the mini-program?
│   └── Follow-up: Can someone technical help you build it? Or do you want a no-code solution?
```

**Same project, different backgrounds → Different question trees.**

---

_Preamble + Execution flow: See `SKILL.md`_

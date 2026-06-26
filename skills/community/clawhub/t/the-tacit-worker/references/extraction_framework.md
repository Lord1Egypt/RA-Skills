# SECI Externalization Interview Framework

This framework provides the structured interview questions for extracting tacit knowledge from domain experts. It is organized by the Nonaka SECI model's "Externalization" phase — converting unconscious judgment into explicit, machine-readable rules.

## Interview Protocol

Ask ONE question at a time. Wait for the answer before proceeding. Never ask more than 2 follow-ups on the same topic.

### Round 1: Workflow Mapping (The "What")

| # | Question | Purpose |
|---|----------|---------|
| 1 | "Walk me through the last time you did this task from start to finish." | Captures the full workflow sequence |
| 2 | "What tools or systems did you use at each step?" | Maps the tool chain |
| 3 | "How long does each step typically take?" | Establishes time expectations |
| 4 | "What information do you need before you can start?" | Identifies input dependencies |

### Round 2: Decision Points (The "Why")

| # | Question | Purpose |
|---|----------|---------|
| 5 | "At what point in the process do you have to make a judgment call?" | Identifies decision nodes |
| 6 | "What signals tell you to choose option A over option B?" | Extracts decision heuristics |
| 7 | "What does a 'good' result look like vs. a 'bad' one?" | Defines quality criteria |
| 8 | "How do you know when you're done?" | Establishes completion criteria |

### Round 3: Edge Cases and Exceptions (The "What If")

| # | Question | Purpose |
|---|----------|---------|
| 9 | "What's the most common thing that goes wrong?" | Identifies failure modes |
| 10 | "When something goes wrong, what do you do?" | Captures recovery procedures |
| 11 | "Are there situations where you break your own rules?" | Surfaces hidden exceptions |
| 12 | "What would a new hire get wrong on their first attempt?" | Reveals non-obvious pitfalls |

### Round 4: Context and Preferences (The "How")

| # | Question | Purpose |
|---|----------|---------|
| 13 | "What tone or style do you use?" | Captures voice and communication norms |
| 14 | "Who do you communicate with during this task?" | Maps stakeholder relationships |
| 15 | "What's your preferred format for the output?" | Defines output specifications |
| 16 | "Is there anything you always do that others might consider optional?" | Surfaces personal best practices |

## Synthesis Rules

After completing the interview:
1. Group answers into: **Workflow Steps**, **Decision Rules**, **Edge Cases**, and **Preferences**.
2. Write each decision rule as an IF/THEN statement.
3. Write each edge case as a WHEN/THEN exception.
4. Present the synthesis to the user and ask: "Did I capture your decision-making process correctly?"
5. Do NOT proceed until the user confirms.

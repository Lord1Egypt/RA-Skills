# Ambiguity And Fallbacks

Ask targeted questions instead of guessing when:

- the top two candidates are close
- the user did not specify whether they want planning, execution, or both
- platform, account, browser, or tooling constraints are missing
- several output formats would imply different skills
- the task spans multiple phases

## Preferred clarification prompts

Ask at most three focused questions:

1. Do you want a plan, execution, or both?
2. What artifact should be produced: code, document, analysis, browser action, post, automation, or memory update?
3. Are there platform, login, security, or time constraints that could change the route?

## Fallback policy

- If there is no clear winner, present the Top 3 with one-sentence reasons.
- If the best skill is missing, name the missing capability and offer the closest installed substitute.
- If the task is multi-stage, recommend a chain and label each stage.
- If the task is high-risk or policy-sensitive, narrow the scope or refuse instead of routing aggressively.

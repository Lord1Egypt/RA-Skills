## Description:

Discards this thread's accumulated drafts and framings and re-derives the task from a clean problem statement. Use when the user says the thread is contaminated, the conversation is going in circles, or that they want a fresh take.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this workflow when a user says a conversation is contaminated, looping, or needs a fresh take. It helps retain a factual brief and either re-derive the task in-thread for mild drift or recommend a new session or fresh subagent for deep contamination or high-stakes work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad contamination or looping phrase could activate the reset workflow when the user did not intend to set aside earlier drafts.

Mitigation: Use the workflow when the user clearly asks for a fresh take or describes the thread as contaminated or stuck; preserve and check the user's requirements in the extracted brief before re-deriving the task.

Risk: An incomplete brief could cause a fresh session or subagent to overlook constraints or approaches already ruled out.

Mitigation: Include participants, the desired outcome, hard constraints, known facts, and what has already been tried, then check that the brief retains the requirements before handing it off.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenequm/skills/reset-context-contamination)
- [Project homepage](https://github.com/tenequm/skills/tree/main/skills/reset-context-contamination)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Concise conversational guidance and a factual task brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The brief captures participants, desired outcome, constraints, known facts, and approaches already tried.]

## Skill Version(s):

0.1.5 (source: frontmatter; confirmed by server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

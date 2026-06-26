# Error Reference

---

## Common Planning Mode Errors

| Error | Correct Approach |
|-------|-----------------|
| ❌ Using a fixed question list, ignoring project context | Dynamically generate questions based on project context |
| ❌ Questions too broad, not specific enough | From broad to specific, gradually deepening |
| ❌ Question tree is fixed, never improving | Question tree continuously improves during planning |
| ❌ Waiting for user to answer all questions before acting | When knowledge is insufficient, autonomously launch subagent research |
| ❌ Only providing commands without descriptions | Provide descriptions (consequences + differences + risks, etc.) for every option |
| ❌ Assuming consequences without knowing | Launch subagent research — do not assume directly |
| ❌ Skipping to execution before user decides | Wait for user confirmation before execution |
| ❌ Proceeding to next question without confirmation | Confirm after every selection |
| ❌ Not returning after subagent research | After research completes, must return to the original question |

---

## Subagent Research Trigger Scenarios

| Scenario | Research Content |
|----------|------------------|
| Uncertain about technical consequences of an option | Implementation details, pros and cons of the technology |
| Unfamiliar with cost of a solution | Specific pricing, free tiers, long-term costs |
| Need to compare multiple solutions | Detailed comparison table of each solution |
| Unfamiliar with market competitors | Competitor analysis, market share, characteristics |
| An option has unknown dependencies | Required tech stack, integration approach |
| Potential risks with a technology | Known issues, community feedback, stability |

---

## What to Do When Unable to Return from Research

| Issue | Handling |
|-------|----------|
| Research finds original option is not viable | Remove the option, add a new option |
| Research finds a new option is needed | Add new option + description |
| Research results conflict with user expectations | Present research results, let user decide again |
| Research cannot be completed | Inform user, mark the option as "pending confirmation" |

---

## Common User Questions + Response Templates

| User Question | Correct Response |
|---------------|------------------|
| "How much does this solution cost?" | Research first, supplement cost description, then answer |
| "Is there a simpler solution?" | Provide a new option, compare consequences + differences of the simplified version |
| "I don't want to use XXX, is there something else?" | Add alternative options |
| "I don't quite understand what you mean by X" | Rephrase X's consequences in more plain language |
| "This is too complex, can it be simplified?" | Provide a simplified version option + consequences + differences |

---

_Preamble + Execution flow: See `SKILL.md`_
_Dynamic question generation: See `references/dynamic-questions.md`_

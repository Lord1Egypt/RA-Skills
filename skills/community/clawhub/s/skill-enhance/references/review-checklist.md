# Review Checklist

Use this file to review a skill draft before calling it done.

## 1. Trigger Review

- Is the skill description discoverable?
- Is it too broad?
- Is it too narrow?
- Are common user phrasings represented?
- Are obvious exclusions present?

## 2. Execution Review

- Does the workflow have clear steps?
- Is there a fixed workflow instead of loose advice only?
- Are decisions explicit?
- Does the skill guide the agent toward delivery?
- Are references scoped and useful?

## 3. Output Review

- Does the skill say what to produce?
- Is the result shape explicit?
- Is it clear what must be included?

## 4. Artifact Review

- Does the package follow a consistent layout?
- Is `README.md` needed?
- Is `agents/openai.yaml` present?
- Are `evals/evals.json` prompts needed?
- Are references sufficient but not bloated?

## 5. Local Modification Review

- Is the local target skill clearly identified?
- Is the target path known?
- Can the current environment likely write to that path?
- Has the user confirmed the path and edit intent before modification?
- Does the response distinguish review-only mode from applied edits?

## 6. Release Review

- Is the name understandable?
- Is the package understandable to a new user?
- Is there enough material for release review?
- Can you explain what changed and why?

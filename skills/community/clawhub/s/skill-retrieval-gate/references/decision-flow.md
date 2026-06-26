# Decision Flow

Use this file to decide whether retrieval is worth doing before following another skill.

## Retrieval is usually worth it when

- the user says things like `before`, `previously`, `last time`, `continue`, `based on existing notes`, or `according to the project docs`
- the task depends on project history, prior decisions, or local notes
- the task is part of an ongoing project or knowledge-base workflow
- the agent is likely to repeat work that was already organized before

## Retrieval is usually not worth it when

- the task is one-shot and low-context
- the task does not depend on prior work or user-specific knowledge
- the answer can be produced directly from the current request with little ambiguity

## Quick decision rule

Ask:

1. If I skip retrieval, am I likely to miss a previous decision or project fact?
2. If I skip retrieval, am I likely to re-read or re-ask for context that probably already exists?

If the answer is yes to either, retrieval is usually justified.

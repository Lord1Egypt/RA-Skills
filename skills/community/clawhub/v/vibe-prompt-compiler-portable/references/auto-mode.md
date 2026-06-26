# Auto Mode

Default behavior should be automatic, not script-first.

## Core Rule

When this skill is triggered by a rough coding request, do not ask the user to run scripts first.

Instead:

1. Classify the request internally.
2. Compile it mentally into a structured implementation brief.
3. Use that brief as the source of truth for the coding response.
4. Mention scripts only when the user wants portability or explicit CLI usage.

## Output Shape In Auto Mode

Internally structure the work like this:

- task type
- goal
- scope
- out of scope
- constraints
- acceptance criteria
- next action

Use this structure to guide the reply. Do not force the user to see all sections unless helpful.

## Script Usage Policy

Use scripts only when:

- the user wants to reuse the prompt in another tool
- the user wants a saved handoff file
- the user asks for command-line usage

## Collaboration With Other Skills

This skill should work as a preprocessor before execution-oriented skills or IDE agents.

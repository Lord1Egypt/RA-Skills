# Sub-agent Patterns

## Investigation sub-agent

Use for bounded research tasks.
Prompt shape:
- objective
- exact files or directories to inspect
- desired output format
- explicit instruction not to modify unrelated files

## Implementation sub-agent

Use for one isolated patch.
Prompt shape:
- target behavior
- files in scope
- verification command
- instruction to stop after bounded change

## Test sub-agent

Use when test work is separable from implementation.
Prompt shape:
- failing or missing behavior
- target test area
- expected evidence of success

## Reporting back

Require concise output:
- findings
- touched files
- risks
- recommended next step

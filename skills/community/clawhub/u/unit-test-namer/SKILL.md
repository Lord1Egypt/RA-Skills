---
name: unit-test-namer
description: >
  Suggest clear unit-test function names from a short behavior description.
  Use when writing tests and stuck on naming.
---

# Unit Test Namer

## Purpose / Overview
Turns a behavior phrase into 2–3 `test_...` / `it(...)` style names.

## When to Use
- Authoring new tests
- Renaming vague tests like `test1`

## Usage / Instructions
1. Ask for the unit under test and the behavior.
2. Prefer users' pattern in other test cases,if not found use this pattern: `test_<unit>_<condition>_<expected>`.
3. Avoid vague words: correct, works, success.

## Examples
Input: "user with empty email is rejected"
Output: `test_create_user_rejects_empty_email`

## Requirements / Dependencies
None.

## Limitations / Caveats
Does not generate test bodies.

## Security / Permissions
Text-only.

## Description

Suggest clear unit-test function names from a short behavior description.

## License or terms

MIT

## Use case

Use when you are the operator responsible for tasks described as: Suggest clear unit-test function names from a short behavior description.

## Risks and mitigations

## References

## Ethical considerations

Illegal use of this skill is not allowed. The publisher will not be accountable for outcomes arising from unlawful use under country or international law. Prohibited examples include breaking into accounts without authorization, deploying ransomware, and trafficking in stolen personal data. Misuse against third-party systems without authorization is illegal.

---
name: rfc-summarizer
description: >
  Summarize IETF RFC text into problem, approach, and impact bullets. Use
  when the user pastes RFC sections or a link they already fetched.
---

# RFC Summarizer

## Purpose / Overview
Condenses RFC prose for engineers who need a quick briefing.

## When to Use
Onboarding to a protocol or reviewing a standards change.

## Usage / Instructions
1. Prefer user-pasted text over fetching.
2. Emit: Problem, Mechanism, Security considerations (if present), Caveats.
3. Quote normative keywords (MUST/SHOULD) sparingly when critical.

## Examples
User pastes RFC 9110 excerpt → short structured summary.

## Requirements / Dependencies
None for pasted text.

## Limitations / Caveats
Does not replace reading the RFC for implementation work.

## Security / Permissions
Text-only unless the user explicitly asks to fetch a URL they provide.

## Description

Summarize IETF RFC text into problem, approach, and impact bullets.

## License or terms

MIT

## Use case

Who: anyone performing the workflow summarized as “Summarize IETF RFC text into problem, approach, and impact bullets”. Purpose: complete that workflow with guided steps from the `rfc-summarizer` skill.

## Risks and mitigations

## References

- IETF RFC series: https://www.rfc-editor.org/

## Ethical considerations

Illegal use is forbidden. Any application that leads to breaches of country or international law is not acceptable. The publisher will not be accountable for illegal use. Do not employ this skill for cyber-attacks, credential theft, or evasion of lawful investigations. Misuse against third-party systems without authorization is illegal.

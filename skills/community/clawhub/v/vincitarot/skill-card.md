## Description:

Act as a professional tarot reader with multiple spreads, full card meanings, spread selection by question, energy guidance, interpretation, and follow-up dialogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superone77](https://clawhub.ai/user/superone77)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to conduct tarot-style readings, select an appropriate spread for a question, generate card draws and spread imagery, and provide reflective follow-up guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image renderer may fetch URLs or read local image paths from reading JSON.

Mitigation: Use a vetted local --images-dir, avoid user-supplied or edited reading JSON, and run the skill with restricted filesystem and network access.

Risk: The skill runs local Python and may make network requests for card art.

Mitigation: Install and execute it only in a sandboxed environment with reviewed dependencies and controlled network permissions.

Risk: Re-exporting card data uses npm tooling.

Mitigation: Prefer pinned local npm tooling and review package metadata before running export commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superone77/skills/vincitarot)
- [Publisher profile](https://clawhub.ai/user/superone77)
- [Pictorial Key to the Tarot](https://www.sacred-texts.com/tarot/pkt/)
- [Pictorial Key tarot images](https://www.sacred-texts.com/tarot/pkt/img/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON reading results and PNG spread images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local files such as reading JSON and spread PNG images when the Python implementation is used.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

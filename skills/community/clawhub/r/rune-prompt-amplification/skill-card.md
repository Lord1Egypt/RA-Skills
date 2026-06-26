## Description: <br>
Transforms flat prompts into structured 8-layer XML prompts using RUNE's semantic engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsarac](https://clawhub.ai/user/mrsarac) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and prompt engineers use this skill to convert short or ambiguous prompts into structured XML prompts with explicit context, constraints, reasoning strategy, QA criteria, and output instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external local wand.py dependency before producing the amplified prompt. <br>
Mitigation: Inspect and pin or verify the local RUNE repository before use. <br>
Risk: The script sources ~/.secrets and then processes user prompts with RUNE_API_KEY available. <br>
Mitigation: Export only RUNE_API_KEY for a single run when possible, and avoid sensitive prompts until the data flow is clear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrsarac/rune-prompt-amplification) <br>
- [RUNE Skill Homepage](https://github.com/neurabytelabs/rune-skill) <br>
- [RUNE Framework](https://github.com/neurabytelabs/rune) <br>
- [RUNE Playground](https://github.com/neurabytelabs/rune-playground) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text XML prompt emitted to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.11+, a local RUNE repository with wand.py, and RUNE_API_KEY; ANSI color codes are stripped from command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

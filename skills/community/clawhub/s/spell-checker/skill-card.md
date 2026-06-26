## Description: <br>
Use when interpreting user messages that may contain obvious spelling, grammar, speech-to-text, or casing errors, especially before acting on ambiguous instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elimaine](https://clawhub.ai/user/elimaine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to interpret noisy or mistyped user instructions before reasoning, retrieval, planning, or tool use. It normalizes low-risk prose errors while preserving exact strings such as commands, filenames, URLs, configuration keys, code, quoted text, and identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normalization may change the action an agent takes when a typo overlaps with a command, filename, identifier, quoted string, or other exact artifact. <br>
Mitigation: Preserve exact strings by default and ask for confirmation when a correction is ambiguous, risky, or action-changing. <br>
Risk: Quiet typo correction may hide the original wording from downstream review. <br>
Mitigation: Use normalized interpretations for reasoning and retrieval while retaining the original user wording for auditability and exact replay. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elimaine/spell-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown instructions and concise interpretation notices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized interpretations for agent reasoning while preserving byte-sensitive strings.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

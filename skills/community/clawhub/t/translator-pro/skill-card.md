## Description: <br>
Test translation quality with built-in dictionaries and comparison tools for evaluating translations and bilingual documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate translation quality, compare translations, check glossary or dictionary terms, and prepare bilingual documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the helper script may create a local data directory in the user's home folder. <br>
Mitigation: Review the helper behavior before execution and run it only in an environment where creating ~/.local/share/translator-pro-test is acceptable. <br>
Risk: The packaged script version, skill frontmatter version, and server release version do not match. <br>
Mitigation: Use the server release version as the release identifier and verify package metadata alignment before redistribution. <br>


## Reference(s): <br>
- [Translator Pro on ClawHub](https://clawhub.ai/xueyetianya/translator-pro) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local data directory under the user's home directory when the bundled helper script is run.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Seekit Search helps agents run fresh web, video, and social searches with seekit, no API key required, and consume structured search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lexiforest](https://clawhub.ai/user/lexiforest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for fresh search results across web, video, and social providers and receive structured results for downstream reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external seekit Python package and live search providers. <br>
Mitigation: Install only if you are comfortable trusting the seekit package from its source and the selected provider. <br>
Risk: Search queries can be sent to third-party providers. <br>
Mitigation: Avoid sensitive private searches unless you are comfortable sharing those query terms with the selected provider. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell, Python, and JSON examples; search commands may produce JSON or Markdown results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live network searches through third-party providers selected by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

调用 Python 脚本处理文本（当前支持：转换为大写）。 / Python-powered text transformation tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[microshark2024](https://clawhub.ai/user/microshark2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to transform supplied text with a Python script, currently by converting text to uppercase and returning the processed result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route user-provided text through a shell command in an unsafe way.

Mitigation: Review before installing; avoid untrusted text containing shell syntax, and change execution to pass arguments without a shell or read text from stdin.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text returned from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the processed result or script error message directly to the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

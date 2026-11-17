## Description:

查询车载诊断系统（OBD）故障码含义，包含适用车型、故障范围及维修建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up automotive OBD fault codes through TianAPI and present applicable vehicle models, fault categories, Chinese and English meanings, and repair-oriented descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if passed on the command line, stored in shell history, written to logs, or saved in a permissive scripts/.env file.

Mitigation: Prefer TIANAPI_OBDCODE_KEY as an environment variable, avoid command-line key arguments, keep any .env file owner-readable and out of version control, and rotate the key if exposure is suspected.

Risk: The bundled executable script is reported by security evidence as needing a code fix before it will run.

Mitigation: Review and fix the script before installation or operational use, then rerun validation and security checks.

## Reference(s):

- [TianAPI OBD Code API documentation](https://www.tianapi.com/apiview/247)
- [TianAPI OBD Code API endpoint](https://apis.tianapi.com/obdcode/index)
- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-obdcode)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON results with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TianAPI API key and an OBD fault code; results may include code, applicable vehicle model, category, Chinese meaning, English meaning, and description.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use when answering car maintenance, service interval, oil, brake fluid, tire pressure, or ownership questions through the TuhuCar CLI knowledge gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finiking](https://clawhub.ai/user/finiking)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route vehicle maintenance and ownership questions through the TuhuCar CLI, parse the gateway response, and present the returned markdown answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or invoking a third-party CLI can expose users to untrusted package sources or gateway behavior.

Mitigation: Verify that @tuhucar/cli and the Homebrew tap are the intended official sources before installation or use.

Risk: Gateway-supplied answers, links, and notices may be incorrect or inappropriate for a specific vehicle or service context.

Mitigation: Treat returned content as TuhuCar gateway output, preserve update notices, and avoid presenting it as independently verified advice.

Risk: Local configuration output may contain private endpoint or account details.

Mitigation: Do not share `tuhucar config show` output when it includes private configuration values.

## Reference(s):

- [TuhuCar CLI Command Reference](references/command-reference.md)
- [TuhuCar CLI Homepage](https://github.com/tuhucar/cli)
- [ClawHub Skill Page](https://clawhub.ai/finiking/skills/tuhucar-knowledge-assistant)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and parsed CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to parse JSON envelopes from the TuhuCar CLI, preserve successful reply markdown, and avoid exposing raw JSON envelopes to end users.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

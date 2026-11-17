## Description:

Read and analyze IoT sensor data from SKALE blockchain via SmartClaws for sensor readings, measurements, trends, thresholds, and on-chain IoT data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmytrotkk](https://clawhub.ai/user/dmytrotkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to read SmartClaws channel data, parse sensor payloads, and answer natural-language questions about measurements, trends, thresholds, and recent readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow downloads a mutable latest-release binary and can place it in a trusted executable path.

Mitigation: Install from a pinned SmartClaws release in a user-local path and verify checksums or signatures before running the binary.

Risk: Sensor readings may be simulated or mock data depending on how the producer was configured.

Mitigation: When answering questions, clearly state when readings come from a mock or test publisher and avoid presenting simulated data as real device data.

Risk: Using the wrong channel address can produce empty, invalid, or unrelated readings.

Mitigation: Confirm the channel address with the producer before reading or analyzing channel data.

## Reference(s):

- [SmartClaws homepage](https://github.com/skalenetwork/smartclaws)
- [ClawHub skill page](https://clawhub.ai/dmytrotkk/skills/smartclaws-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with shell commands, JSON parsing examples, and concise natural-language answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SmartClaws CLI commands, parsed JSON sensor readings, timestamps, basic statistics, threshold checks, and trend summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

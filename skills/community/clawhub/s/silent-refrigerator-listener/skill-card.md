## Description:

Use when a fridge or freezer sounds wrong (rattling, humming louder, clicking, running constantly) or food spoils early — analyzes a phone recording of the appliance with pure-Python DSP (duty cycle, mains-hum autocorrelation, envelope flutter, click counting) to name the likely failure: over-running compressor, worn mounts, iced fan, or hard-starting relay, with causes and a technician brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners, landlords, and used-appliance buyers use the skill to interpret a phone recording of a refrigerator or freezer, identify likely sound-related faults, and prepare a concise brief for a technician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Demo mode may overwrite files because it uses fixed paths beside the script.

Mitigation: Avoid demo mode until it uses unique temporary files and its cleanup behavior is verified.

Risk: Relay or capacitor repair advice may lead to unsafe electrical work.

Mitigation: Have a qualified technician assess these faults, use model-approved parts, and unplug the appliance before any repair.

Risk: Sound-analysis results may be mistaken for a definitive appliance diagnosis.

Mitigation: Use results only for preliminary troubleshooting and have a qualified technician assess suspected faults.

## Reference(s):

- [Refrigerator Failure Signatures](references/failure-signatures.md)
- [GE Appliance Safety Instructions](https://www.geappliances.com/content/older-pdfs/49-6635.PDF)
- [ClawHub Release](https://clawhub.ai/voronindenis5/skills/silent-refrigerator-listener)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain-text diagnostic summary with measured feature values, likely causes, and a technician brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses relative acoustic patterns; phone microphone loudness is not calibrated.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

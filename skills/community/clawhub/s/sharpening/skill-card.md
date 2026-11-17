## Description:

Sharpening techniques for knives, tools, and bladed implements. Use when someone has dull kitchen knives, needs to maintain garden tools, axes, or shop tools, or wants to learn the foundational maintenance skill for all cutting implements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide practical sharpening and maintenance guidance for kitchen knives, garden tools, axes, chisels, plane blades, scissors, and mower blades. It helps users choose appropriate sharpening equipment, distinguish honing from sharpening, and apply tool-specific techniques.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests filesystem access that is not necessary for sharpening guidance.

Mitigation: Review the requested permissions before installing and restrict filesystem access unless a trusted deployment process requires it.

Risk: The install command is unpinned, which can resolve to a different package version over time.

Mitigation: Use a pinned or otherwise trusted installer source when deploying the skill.

Risk: The skill gives hands-on guidance for sharp tools and powered equipment, where poor setup or unsafe handling can cause injury or damage.

Mitigation: Use eye protection, secure workpieces, disconnect power sources before blade removal or maintenance, keep hands clear of cutting edges, and follow manufacturer guidance and local rules.

## Reference(s):

- [ClawHub Sharpening skill page](https://clawhub.ai/howtousehumans/skills/sharpening)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with step-by-step instructions and code-style instruction blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include safety precautions, tool-specific angle guidance, equipment recommendations, maintenance cadence, and troubleshooting advice.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

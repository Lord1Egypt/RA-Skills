## Description: <br>
Generates SOUL.md persona configuration files from public-person research, SBTI/MBTI presets, or a custom persona description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adenzhou1350](https://clawhub.ai/user/adenzhou1350) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create reusable SOUL.md persona files that shape an assistant's identity, voice, decision style, and response rules from presets, public-person research, or custom background details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated persona files can encode inaccurate, outdated, overly broad, or misleading behavior guidance. <br>
Mitigation: Review each generated SOUL.md before relying on it and edit persona rules that are unsupported or inappropriate. <br>
Risk: Custom persona descriptions may include sensitive personal details that persist in local SOUL.md files. <br>
Mitigation: Avoid placing secrets or unnecessary personal data in persona files, and delete or edit personas that should no longer shape assistant behavior. <br>
Risk: Public-person distillation depends on web search and may reflect low-quality or secondary sources. <br>
Mitigation: Prefer primary sources when distilling a public person and verify important claims before using the generated persona. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adenzhou1350/soul-generator) <br>
- [Skill instructions and SOUL.md format](artifact/SKILL.md) <br>
- [ENFP persona example](artifact/references/good/01-enfp.md) <br>
- [Combined persona example](artifact/references/examples/01-combined.md) <br>
- [Generic persona anti-pattern](artifact/references/bad/01-generic.md) <br>
- [Rigid persona anti-pattern](artifact/references/bad/02-robot.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown SOUL.md persona file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web search for public-person distillation and local preset files for SBTI, MBTI, archetype, anime, movie, and personal personas.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

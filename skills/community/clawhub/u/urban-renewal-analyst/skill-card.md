## Description:

Analyzes urban renewal or renovation site photos across environment, structure, facade, hard landscaping, furniture and fixtures, and greenery, then produces scored findings, renovation guidance, and Gemini image-to-image prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[innocencexy](https://clawhub.ai/user/innocencexy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, planners, designers, and agents use this skill to turn site photos into structured Chinese-language urban-renewal assessments, priority-ranked renovation recommendations, and ready-to-use visual redesign prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases for prompt generation may activate the skill when another image or prompt skill was intended.

Mitigation: Review trigger phrase overlap before enabling it alongside other image-analysis or prompt-generation skills.

Risk: Photo-only assessment can miss hidden structural, safety, accessibility, or regulatory issues.

Mitigation: Treat renovation recommendations as planning support and obtain qualified site inspections before acting on safety-critical findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/innocencexy/skills/urban-renewal-analyst)
- [Publisher profile](https://clawhub.ai/user/innocencexy)
- [analysis_framework.md](references/analysis_framework.md)
- [gemini_prompt_templates.md](references/gemini_prompt_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese-language report with scored analysis sections, renovation recommendations, and image-to-image prompt blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs six dimension scores, a composite renovation level, staged mitigation recommendations, and three prompt styles: photorealistic, architectural visualization, and watercolor or hand-drawn.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

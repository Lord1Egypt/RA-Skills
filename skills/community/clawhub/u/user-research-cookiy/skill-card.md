## Description:

Plans qualitative research, synthesizes interview evidence, and can run AI-moderated interviews or surveys through Cookiy AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenglin97](https://clawhub.ai/user/chenglin97)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, designers, researchers, and external agents use this skill to plan studies, prepare screeners and interview guides, analyze transcripts, create research reports, and optionally run qualitative or quantitative studies through Cookiy AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Cookiy workflow uses a third-party hosted research platform and may send interview transcripts, survey responses, participant details, and internal product context outside the agent environment.

Mitigation: Use the skill only for data appropriate for Cookiy, treat research data as sensitive, and restrict network access to the required Cookiy domain.

Risk: Authentication uses access tokens, and exposing tokens in chat or logs could grant unauthorized access.

Mitigation: Do not paste access tokens into chat; enter secrets directly in the local terminal and store them only in the configured token file.

Risk: The bundled CLI supports API endpoint overrides, which could redirect requests away from the intended service.

Mitigation: Avoid arbitrary API endpoint overrides and keep network egress limited to the required Cookiy domain.

Risk: Recruitment, synthetic interviews, report generation, and billing actions may spend money or initiate participant outreach.

Mitigation: Review billing, checkout, and recruitment previews carefully and require explicit confirmation before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenglin97/skills/user-research-cookiy)
- [Cookiy AI agent introduction](https://cookiy.ai/intro-for-agent.txt)
- [Cookiy AI API domain](https://s-api.cookiy.ai)
- [Qualitative research planner](references/qualitative-research-planner/qualitative-research-planner.md)
- [Synthesize research report](references/synthesize-research-report/synthesize-research-report.md)
- [Cookiy AI workflow](references/cookiy/cookiy.md)
- [Cookiy qualitative workflow](references/cookiy/cookiy-qual.md)
- [Cookiy quantitative workflow](references/cookiy/cookiy-quant.md)
- [Cookiy billing workflow](references/cookiy/cookiy-billing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with research plans, interview guides, reports, JSON survey definitions, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local analysis files and may guide hosted Cookiy AI API calls when the user chooses that workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Create video ads with Pexo from a product, brand brief, or photo; Pexo writes hooks, sequences shots, selects models, and delivers a finished ad with music for platforms such as Meta, TikTok, or YouTube.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to turn product briefs or uploaded media into ready-to-run video ads through Pexo's hosted video agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad briefs and selected media are sent to Pexo's hosted service for generation.

Mitigation: Use the skill only for briefs and media that are appropriate to share with Pexo, and avoid sensitive or unlicensed material.

Risk: The Pexo API key can be exposed if ~/.pexo/config, PEXO_CONFIG, or the environment is readable or modified by untrusted parties.

Mitigation: Keep the config private with restrictive permissions, use trusted environment settings, and rotate the API key if exposure is suspected.

Risk: A tampered PEXO_BASE_URL or PEXO_CONFIG value could redirect script traffic or load unexpected local configuration.

Mitigation: Use the expected Pexo base URL, keep configuration paths under user control, and run pexo-doctor.sh when setup or behavior looks unusual.

## Reference(s):

- [Pexo](https://pexo.ai)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [ClawHub Skill Page](https://clawhub.ai/pexo/skills/video-ad)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with shell commands and JSON returned by helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can return project links, signed asset URLs, local asset cache paths, setup diagnostics, and polling guidance.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter declares 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

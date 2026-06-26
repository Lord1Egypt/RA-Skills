## Description: <br>
Lead generation and qualification system: ICP, source selection, outreach, nurture, reactivation, scoring and pipeline reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business owners, marketers, and sales leaders use this skill to plan and evaluate lead-generation workflows, including customer avatars, lead sources, first-touch outreach, nurture sequences, BANT qualification, reactivation, funnel reporting, and unit economics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead-generation, parsing, enrichment, and reactivation workflows can create privacy, consent, retention, or platform-rules issues if used with improper contact data. <br>
Mitigation: Use only lawfully obtained business contacts, add consent and opt-out checks, define retention rules, and verify platform terms before any campaign. <br>
Risk: Generated outreach, scoring, and funnel recommendations may be inaccurate or unsuitable for a specific market or customer segment. <br>
Mitigation: Manually review every outreach campaign, qualification score, and budget recommendation before acting on it. <br>
Risk: The inspected artifact references .env.example during installation, but that file was not present in the artifact evidence. <br>
Mitigation: Inspect install.sh before running it and provide or remove the missing .env.example dependency as part of deployment review. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/raaipro/raai-leads-pro) <br>
- [README](README.md) <br>
- [Onboarding Guide](docs/onboarding.md) <br>
- [ROI Guide](docs/roi.md) <br>
- [Limitations and Anti-Fail Guide](docs/anti-fail.md) <br>
- [Example Prompts](examples/example_prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with templates, structured tables, configuration examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning and qualification artifacts for human review; does not itself send outreach, parse databases, launch ads, or integrate with CRM systems.] <br>

## Skill Version(s): <br>
3.5.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

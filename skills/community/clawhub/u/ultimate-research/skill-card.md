## Description: <br>
Ultimate Research orchestrates broad or multi-domain research by routing queries through memory, self-improvement, brainstorming, research, web scraping, and market research, then adding specialist skills only when they materially improve recommendations, strategy, competitive analysis, market or SEO guidance, current digests, or structured synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nemesis0017](https://clawhub.ai/user/nemesis0017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route broad research, strategy, comparison, market, SEO, pricing, launch, analytics, and other multi-step questions into one concise, evidence-backed answer. It is especially suited to ambiguous requests that need one clarifying question before research begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may consult prior memory and external web sources during research routing. <br>
Mitigation: Avoid sensitive prompts unless that behavior is acceptable, and review source usage before deployment. <br>
Risk: The artifact routes work to named dependent skills that are not included in this release artifact. <br>
Mitigation: Review the dependent skills separately before relying on the full routing workflow. <br>
Risk: Research-heavy answers may depend on current web evidence and can become stale or incomplete. <br>
Mitigation: Require citations and source links for research-heavy answers, and verify important claims against current sources. <br>


## Reference(s): <br>
- [Routing Guide](references/routing.md) <br>
- [ClawHub listing](https://clawhub.ai/nemesis0017/ultimate-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown or JSON routing plan, with optional shell command usage for the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default answer order is Question breakdown, Skills used, Evidence, Recommendation, and Next steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence, README, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

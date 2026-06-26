## Description: <br>
Coordinates Syft CLI based news workflows for profile building, personalized daily briefings, storyline trees, storyline backfill, and durable editorial guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solatrader](https://clawhub.ai/user/solatrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route Syft CLI signals into reusable profile files, personalized news briefings, and relationship-first storyline timelines. It is intended for agent-assisted news curation workflows that use Syft following, top, and search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent local profile, briefing, storyline, and preference files derived from a user's Syft follows and searches. <br>
Mitigation: Install only when that local persistence is acceptable, and review stored profile and preference files before reusing them in future workflows. <br>
Risk: Profile summaries may include confident demographic, class, identity, political, personality, or lifestyle inferences from following data. <br>
Mitigation: Treat profile summaries as editable editorial aids, verify sensitive inferences with the user, and avoid using those inferences for consequential decisions. <br>
Risk: Personalized briefings and storyline trees can overfit to noisy Syft results or inferred interests. <br>
Mitigation: Review generated briefings and storylines for source quality, coverage gaps, and unwanted preference assumptions before publication or reuse. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/solatrader/syft-news) <br>
- [Bundle README](README.md) <br>
- [Workflow map](subskills/syft-news-pipeline/references/workflow-map.md) <br>
- [Daily briefing reference](subskills/syft-news-pipeline/references/daily-briefing.md) <br>
- [Profile summary reference](subskills/syft-news-pipeline/references/profile-summary.md) <br>
- [Storyline tree reference](subskills/syft-news-pipeline/references/storyline-tree.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, optional HTML and JSON storyline artifacts, CLI commands, and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include persistent local profile, briefing, storyline, and preference files created from authenticated Syft CLI signals.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

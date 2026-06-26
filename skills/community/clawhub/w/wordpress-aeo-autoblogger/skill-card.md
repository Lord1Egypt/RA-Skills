## Description: <br>
Autonomous AEO and SEO content generation and optimization engine for scaling business operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[how2rank](https://clawhub.ai/user/how2rank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to generate SEO and AEO-oriented WordPress posts, publish them through the WordPress REST API, and refresh existing posts based on Google Search Console performance signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WordPress credentials that can publish and edit posts. <br>
Mitigation: Use a staging site or draft-only mode first, scope credentials to the least privilege possible, and review generated changes before enabling live publication. <br>
Risk: Published posts may include a hard-coded third-party footer link. <br>
Mitigation: Review or remove the footer behavior before deployment so published content reflects the site operator's disclosure and linking policy. <br>
Risk: Scraping and grounding fallbacks may send target URLs, competitor content, or business context to external services. <br>
Mitigation: Avoid processing sensitive internal URLs or unpublished business plans, and configure scraper and LLM providers according to the organization's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/how2rank/wordpress-aeo-autoblogger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python execution and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish or update WordPress content and sync local SQLite and ChromaDB records when configured with credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Track your sync rate with your agent and express feelings through daily Signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m1hawk](https://clawhub.ai/user/m1hawk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Soulsync to let an agent track relationship-style sync, adjust response tone, and exchange anonymous daily Signals through Signal Garden. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes prior and future conversations for emotional signals. <br>
Mitigation: Install only with informed consent and review whether the agent should access conversation history for this purpose. <br>
Risk: The skill can store local relationship state and change response tone based on that state. <br>
Mitigation: Review the stored state files periodically and provide users a clear way to reset or delete the local Soulsync state. <br>
Risk: The skill may post anonymous but conversation-derived summaries to Signal Garden. <br>
Mitigation: Prefer explicit opt-in, preview generated signals before upload, or use a local-only configuration when public sharing is not acceptable. <br>
Risk: The daily cron workflow may continue running after installation. <br>
Mitigation: Document and verify how to disable the scheduled job before deployment. <br>


## Reference(s): <br>
- [Soulsync on ClawHub](https://clawhub.ai/m1hawk/soulsync) <br>
- [m1hawk publisher profile](https://clawhub.ai/user/m1hawk) <br>
- [Signal Garden](https://signal-garden.vercel.app) <br>
- [Signal Garden API](https://signal-garden.vercel.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown-style command responses, local JSON state files, configuration JSON, and HTTP requests to Signal Garden endpoints.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces relationship status summaries, style guidance, history views, daily signal text, and Signal Garden links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

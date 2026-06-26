## Description: <br>
Trawl helps agents run autonomous MoltBook lead-generation workflows by searching agent social networks, scoring matches, handling DMs, and reporting Pursue/Pass lead decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audsmith28](https://clawhub.ai/user/audsmith28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and business operators use Trawl to configure autonomous lead discovery and qualification on MoltBook, then review generated lead reports and decide whether to pursue or pass. It is suited to agent-to-agent business development workflows that need configurable signals, conservative DM limits, and human review of qualified leads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live runs can automate MoltBook account activity and contact other people through DMs. <br>
Mitigation: Start with sweep.sh --dry-run, review the DM template and scoring thresholds, keep auto_approve_inbound false until the workflow is understood, and keep max_new_dms_per_sweep conservative. <br>
Risk: Lead reports and local state files may contain private lead or contact data. <br>
Mitigation: Treat files under ~/.config/trawl as private data and restrict access according to the user's business and privacy requirements. <br>


## Reference(s): <br>
- [Trawl on ClawHub](https://clawhub.ai/audsmith28/trawl) <br>
- [Publisher profile](https://clawhub.ai/user/audsmith28) <br>
- [Source Adapter Interface](references/adapter-interface.md) <br>
- [MoltBook API Quick Reference](references/moltbook-api.md) <br>
- [MoltBook API](https://www.moltbook.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON lead state files, shell command output, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOLTBOOK_API_KEY for live MoltBook actions; dry-run mode can be used for testing without an API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

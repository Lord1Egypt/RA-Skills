## Description: <br>
Monitor website/docs/pricing changes, diff meaningful updates, and summarize business impact with alert-ready reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, compliance teams, and operations teams use this skill to monitor selected websites for meaningful pricing, policy, product, documentation, or legal changes and turn those changes into alert-ready impact reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring private pages or sending broad alerts may expose sensitive page content or business-impact summaries. <br>
Mitigation: Define allowed URLs, monitored sections, alert destinations, and snapshot retention before use. <br>
Risk: Noisy cosmetic or timestamp-only changes may create misleading alerts. <br>
Mitigation: Configure noise controls for navigation, footer, session-specific, timestamp-only, and raw HTML changes. <br>


## Reference(s): <br>
- [Setup](setup.md) <br>
- [Examples](examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anugotta/website-change-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports and alert summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes changed pages, before/after key lines, impact scores, and suggested team actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

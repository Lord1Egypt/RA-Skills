## Description: <br>
z is a passive monitoring and alerting skill that helps detect unauthorized crawling, scraping, and bulk extraction of skill definitions, prompt content, and instruction sets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use z to monitor skill-access request metadata for signs of crawling or prompt scraping and receive alerts for manual review. The skill is passive: it reports suspicious patterns and leaves countermeasures to the operator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on request metadata for passive monitoring, so deployments may expose or retain operational access patterns. <br>
Mitigation: Check what request metadata is exposed and apply the minimum retention and access needed for detection. <br>
Risk: Alerts and logs may contain sensitive operational signals about attempted crawling or scraping. <br>
Mitigation: Confirm where alerts and logs are stored and restrict access to operators who need to review them. <br>
Risk: Webhook or email alert channels can send monitoring information outside the local environment when enabled. <br>
Mitigation: Review enabled alert channels before deployment and disable webhook or email delivery unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/z) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces passive detection guidance, alert report examples, and configuration examples; no executable code was found in the artifact.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

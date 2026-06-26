## Description: <br>
AI Skills one-stop monitoring and evaluation platform for seven-factor skill scoring, cross-model benchmarking, centralized dashboards, diagnostics, recommendations, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredwei01](https://clawhub.ai/user/jaredwei01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor installed AI skills, evaluate skill health and performance, compare benchmark results, generate diagnostic reports, and surface recommendations from a web or command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute installed skills without sandboxing. <br>
Mitigation: Run it in a sandbox or dedicated environment and review monitored skills before enabling automated execution. <br>
Risk: Scheduled uploads and reports can transmit telemetry to a configured server. <br>
Mitigation: Verify the destination server and payload contents before enabling scheduled or automatic uploads. <br>
Risk: Fallback credential storage should not be treated as strong encryption. <br>
Mitigation: Prefer OS keychain-backed storage and avoid storing high-value secrets in fallback storage. <br>
Risk: Bundled server authentication should be reviewed before exposing dashboards or APIs beyond localhost. <br>
Mitigation: Keep services local until authentication, network exposure, and deployment settings have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredwei01/skills-monitor) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Deployment guide](artifact/deploy/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text, Markdown reports, JSON API responses, and web dashboard views] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run installed skills, persist monitoring data, schedule reports, and upload telemetry to a configured server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

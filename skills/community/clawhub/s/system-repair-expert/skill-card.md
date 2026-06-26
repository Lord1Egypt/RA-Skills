## Description: <br>
System Repair Expert guides agents through cautious, priority-ordered troubleshooting for system, software, configuration, and error-resolution problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqicxx](https://clawhub.ai/user/xqicxx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to diagnose system, software, configuration, and runtime errors through a structured workflow that prioritizes complete problem understanding, official documentation, existing ClawdHub skills, and verified community fixes before one-off scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting details may expose secrets, private hostnames, customer data, or sensitive configuration through external search or memory-based workflows. <br>
Mitigation: Scrub logs and configuration before use, avoid sharing secrets or private identifiers, and ask the agent not to save troubleshooting details unless persistence is intended. <br>
Risk: Repair commands, generated scripts, or newly proposed skills may make incorrect or unsafe changes if accepted without review. <br>
Mitigation: Manually review proposed commands, scripts, and skill changes before running them; prefer official fixes and require explicit approval before one-off repair scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xqicxx/system-repair-expert) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/USAGE_GUIDE.md) <br>
- [Release Notes](artifact/RELEASE_NOTES.md) <br>
- [Usage Examples](artifact/examples/usage_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with step-by-step troubleshooting guidance, source-oriented recommendations, and inline command or code examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence labels, requests for missing diagnostic information, and risk-aware review prompts before repair commands or scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

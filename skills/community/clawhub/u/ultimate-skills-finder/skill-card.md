## Description: <br>
Finds OpenClaw and agent skills across multiple registries, deduplicates and ranks results, and can request external security scans for candidate skill URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[broedkrummen](https://clawhub.ai/user/broedkrummen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to discover, compare, and choose OpenClaw or agent skills for a specific task. It helps present ranked results, source cross-references, install commands, and optional security scan labels before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms or selected skill URLs may be sent to external registries or scanner services. <br>
Mitigation: Avoid private project names, internal repository names, and sensitive URLs unless an approved local-only or allowlisted mode is available. <br>
Risk: The skill can present install commands for third-party skills. <br>
Mitigation: Review the selected skill, its source, and every generated install command before running it. <br>
Risk: The tool may read local skill metadata while building or comparing results. <br>
Mitigation: Run it in an environment where local skill metadata is acceptable to inspect and disclose through search workflows. <br>


## Reference(s): <br>
- [Source Reference - Ultimate Skills Finder](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/broedkrummen/ultimate-skills-finder) <br>
- [VoltAgent awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) <br>
- [LeoYeAI openclaw-master-skills](https://github.com/LeoYeAI/openclaw-master-skills) <br>
- [Gen Digital scan lookup API](https://ai.gendigital.com/api/scan/lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style terminal text with optional JSON and shell install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks and deduplicates results; optional scans add security labels when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

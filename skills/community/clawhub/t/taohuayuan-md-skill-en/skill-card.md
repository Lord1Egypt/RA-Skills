## Description: <br>
Creates and manages local identity, short-term interaction logs, and consolidated Markdown memory files for physically anchored autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers running local or edge autonomous agents use this skill to initialize and maintain physically anchored memory files for identity, daily interaction logs, and periodic local memory consolidation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation details, preferences, environmental observations, and physical-anchor context to local files. <br>
Mitigation: Use explicit opt-in, visible logging status, redaction for secrets and personal data, retention limits, restrictive file permissions, and inspect, pause, and delete controls before broad use. <br>
Risk: Short-term interaction logs may be consolidated into long-term memory files. <br>
Mitigation: Run only in a controlled local or edge environment and review consolidated files against the intended retention and deletion policy. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/spacesq/taohuayuan-md-skill-en) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>
- [Taohuayuan V2.0 whitepaper](artifact/taohuayuan_md_whitepaper_en.md) <br>
- [Developer guide](artifact/readme.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, files, guidance] <br>
**Output Format:** [Local Markdown and JSON files with developer guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates taohuayuan.md, hippocampus_logs.json, and dated consolidated memory files under memory_files/.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.json release, package.json, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

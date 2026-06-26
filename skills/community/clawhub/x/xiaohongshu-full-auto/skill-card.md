## Description: <br>
Automates Xiaohongshu content workflows from trend discovery and topic matching through copy generation, cover generation, publishing, and logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanlansss](https://clawhub.ai/user/guanlansss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content studios, and developers use this skill to generate, review, and optionally publish Xiaohongshu posts based on trending topics and configured content niches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Xiaohongshu cookies, business identifiers, and API keys are required for publishing and generation workflows. <br>
Mitigation: Store credentials as account secrets, restrict their scope where possible, and avoid sharing configuration files that contain live values. <br>
Risk: The workflow can auto-publish public posts without sufficient review safeguards. <br>
Mitigation: Use semi-auto or assist-only mode and require manual review of topics, copy, images, tags, account scope, and rate limits before publishing. <br>
Risk: Publishing and generation modules referenced by the main script are not fully reviewable in the artifact. <br>
Mitigation: Set publish.enable to false until the missing modules have been inspected or replaced with trusted implementations. <br>
Risk: Trend collection depends on a third-party hot-topic source. <br>
Mitigation: Verify the source, terms, data quality, and failure behavior before relying on it for content decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guanlansss/xiaohongshu-full-auto) <br>
- [Configuration example](references/config-example.yaml) <br>
- [Xiaohongshu developer platform](https://www.xiaohongshu.com/developer) <br>
- [xiaohongshu-mcp reference](https://github.com/openclaw/skills/tree/main/skills/pxfeng/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, YAML configuration, generated post text, JSON-like run results, and local log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create cover image files and append publishing records to a JSONL log when publishing is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Story generation pipeline skill. Supports multi-episode continuous generation, graph management, AI quality check + human confirmation dual control mechanism. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexidyg](https://clawhub.ai/user/hexidyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Writers, creators, and agent developers use this skill to coordinate multi-episode story generation with continuity tracking, AI quality review, and human approval before progression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story drafts, review results, and pipeline state are saved locally as JSON files. <br>
Mitigation: Avoid entering sensitive private material and review local data retention before using the skill in shared or regulated environments. <br>
Risk: The security scan notes that crafted pipeline IDs can cause graph JSON file operations outside the intended data folder. <br>
Mitigation: Use trusted pipeline IDs only until the maintainer validates IDs and confines graph paths to the intended storage directory. <br>
Risk: Generated episodes and AI review scores may be inaccurate, inconsistent, or biased for the intended story context. <br>
Mitigation: Keep the human confirmation step active and review each episode before storing it or continuing the pipeline. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexidyg/story-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/hexidyg) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [AI quality review template](artifact/templates/review_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown prompts, JSON review structures, and Python helper calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists pipeline state and story graph data as local JSON files.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

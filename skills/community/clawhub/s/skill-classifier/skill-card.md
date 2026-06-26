## Description: <br>
OpenClaw 技能分类与统计工具，可扫描本地技能清单，自动分类，检测增量变化和重复技能，并导出 Markdown、JSON 或 HTML 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuntao2011](https://clawhub.ai/user/kuntao2011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and skill maintainers use this skill to inventory local skills, review activation status and metadata, classify skills, detect duplicates or changes, and generate shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local OpenClaw skill inventory and writes report and cache files under the user's profile. <br>
Mitigation: Install and run it only in environments where local skill metadata can be processed and stored in generated reports or cache files. <br>
Risk: Generated HTML reports can render metadata from installed skills, including metadata from untrusted skills. <br>
Mitigation: Review generated HTML before sharing it and be cautious opening reports when the local skill inventory includes untrusted skills. <br>
Risk: The security guidance notes that shell calls should ideally be hardened. <br>
Mitigation: Prefer the modular generate_skill_list.py path and run the tool with normal user privileges in a trusted local OpenClaw workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kuntao2011/skill-classifier) <br>
- [Publisher profile](https://clawhub.ai/user/kuntao2011) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, and HTML report files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include skill names, descriptions, versions, authors, status, category, directory size, and installation time.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Fetches WeChat public account articles from mp.weixin.qq.com links and converts them into clean Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunkguo](https://clawhub.ai/user/hunkguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save WeChat public account articles as Markdown, including article metadata and optional image references, after providing a WeChat article URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided WeChat article URLs and writes Markdown files to disk. <br>
Mitigation: Use only links the user intends to fetch and choose the output directory deliberately before running the script. <br>
Risk: Generated Markdown may retain remote image URLs instead of fully local image copies. <br>
Mitigation: Review generated Markdown before sharing or publishing it, especially when remote image references are not desired. <br>
Risk: The skill relies on Python packages and a Playwright browser runtime. <br>
Mitigation: Install dependencies from trusted sources and keep the browser runtime updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hunkguo/wechat-articles-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter and local or remote image references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The output path is chosen by the user or defaults to the current directory; generated Markdown may reference remote image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

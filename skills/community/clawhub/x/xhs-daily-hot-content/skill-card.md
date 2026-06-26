## Description: <br>
每日自动搜索全网热点，结合 AI教育+亲子育儿赛道定位，批量生成高质量小红书营销文案并追加到文案库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangcongwangcong](https://clawhub.ai/user/wangcongwangcong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, creators, and marketing teams use this skill to find recent online trends in AI education and parenting, generate ten Xiaohongshu-style marketing posts, and prepend them to a YAML post library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill updates templates/posts.yaml as part of its normal workflow, which can overwrite or reorder an important post library if the result is not reviewed. <br>
Mitigation: Keep backups of templates/posts.yaml and ask the agent to preview generated posts before writing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangcongwangcong/xhs-daily-hot-content) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with YAML post entries and optional Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates ten post drafts, prepends them to templates/posts.yaml, and may populate cover filenames when a local card generator is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
统一查询本地研究资料库，默认同时搜索 AlphaPai 归档和 knowledge_bases，支持精确检索、向量检索和混合检索，并默认排除 private 资料库如 personal。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbotrr](https://clawhub.ai/user/clawdbotrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research analysts use this skill to query local AlphaPai and knowledge_bases archives, combine exact and vector retrieval, and generate a mobile-readable research summary while excluding private libraries by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query local AlphaPai and knowledge_bases archives that may contain sensitive research material. <br>
Mitigation: Install and run it only where those local archives are approved for agent access; keep private libraries excluded unless explicitly requested. <br>
Risk: Retrieved snippets may be passed to the AlphaPai AI analysis path for summarization. <br>
Mitigation: Avoid sensitive queries unless that AI analysis path is approved for the data; review generated summaries against source material before relying on them. <br>
Risk: The packaging helper removes the chosen destination before copying the skill. <br>
Mitigation: Use the default disposable build directory or another empty staging directory for package_skill.py. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdbotrr/research-archive-query) <br>
- [Publisher profile](https://clawhub.ai/user/clawdbotrr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON runtime metadata, and terminal output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports and runtime metadata under ~/.openclaw/data/research-archive-query.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

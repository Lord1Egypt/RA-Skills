## Description: <br>
Efficient Lifelong Memory for LLM Agents - semantic compression, cross-session memory, and intent-aware retrieval <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent, cross-session memory with add, retrieve, search, and stats operations. It can use SimpleMem semantic retrieval when configured with an OpenAI API key, or local JSON keyword search as a fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories persist locally and may include sensitive information if users store secrets, regulated personal data, or confidential business material. <br>
Mitigation: Avoid storing sensitive material as memories, and review or clear the skill data directory when needed. <br>
Risk: Full semantic features may process memory content through OpenAI when OPENAI_API_KEY is configured. <br>
Mitigation: Use a dedicated API key and only enable full semantic features for content that is appropriate to send to the configured provider. <br>
Risk: The skill depends on the upstream SimpleMem package for full functionality. <br>
Mitigation: Review or pin the upstream SimpleMem dependency before relying on it in production workflows. <br>


## Reference(s): <br>
- [Simplemem ClawHub page](https://clawhub.ai/nantes/simplemem) <br>
- [SimpleMem homepage](https://github.com/aiming-lab/SimpleMem) <br>
- [SimpleMem paper](https://arxiv.org/abs/2601.02553) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include memory entries, retrieval scores, statistics, and configuration guidance for OPENAI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter remains 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

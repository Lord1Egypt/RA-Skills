## Description: <br>
标签化长期记忆系统。当用户说"记住..."时存储记忆，当用户问"我之前..."时查询记忆，定期生成总结并询问确认，主动核对记忆正确性。支持标签(#偏好、#决定、#项目等)、BM25搜索、时间范围查询、人类审核机制。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckyboybs](https://clawhub.ai/user/luckyboybs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use TagMemory to store, search, review, correct, delete, and summarize local long-term memories with semantic tags and BM25 search. The skill is intended for user-confirmed memory maintenance, including preference, decision, project, person, event, knowledge, and mistake records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores user memories in a local database. <br>
Mitigation: Install only when persistent local memory is intended, avoid storing secrets or highly sensitive personal data, and periodically review and delete stored memories. <br>
Risk: Stored memories can be listed or exposed in bulk through the skill's memory listing and query behavior. <br>
Mitigation: Limit use to trusted local environments and review stored records before sharing command output or summaries. <br>
Risk: The artifact ships with prefilled sample memory summary data. <br>
Mitigation: Inspect or remove artifact/data/pending_summary.json before first use so sample data is not mistaken for user-confirmed memory. <br>
Risk: Runtime metadata is mismatched in the package evidence. <br>
Mitigation: Verify the runtime entry and hook packaging before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luckyboybs/tag-memory) <br>
- [Publisher profile](https://clawhub.ai/user/luckyboybs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown summaries, JSON command results, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves local memory records with tags, timestamps, verification status, source, and agent id fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

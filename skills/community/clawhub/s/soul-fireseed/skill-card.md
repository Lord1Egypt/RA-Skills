## Description: <br>
Soul Fireseed models personality and memory from conversations, offering dialogue extraction and memory-analysis modes with optional daily or weekly background extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanzhishuyuan](https://clawhub.ai/user/sanzhishuyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract personality signals from chats or existing memories, then generate persona snapshots, structured profile data, and evolution reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can infer sensitive personality and memory data from conversations and retain it in local profile, fossil, backup, validation-history, or embedding-cache files. <br>
Mitigation: Enable it only for intentional personal profiling, review stored user-data and cache files regularly, and delete retained profiles or embeddings when they are no longer needed. <br>
Risk: Daily or background extraction can continue analyzing chats after the first setup. <br>
Mitigation: Keep automatic extraction disabled unless explicitly needed, prefer manual or weekly extraction, and require a visible user choice before enabling recurring analysis. <br>
Risk: Using the skill on other people's conversations or employment/team contexts can create privacy and consent concerns. <br>
Mitigation: Use it only on conversations where participants have clear consent, and avoid applying it to workplace, team, or third-party communications without an approved policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanzhishuyuan/soul-fireseed) <br>
- [FireSeed homepage](https://fireseed.online) <br>
- [Gitee repository](https://gitee.com/topofthesky/soul-fireseed) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and JSON, with optional Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local persona, fossil, backup, validation-history, and embedding-cache files under configured user-data and cache paths.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
YoudaoNote helps agents manage Youdao Cloud Notes through the official CLI, including note CRUD, todo management, web clipping, search, and folder operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lephix](https://clawhub.ai/user/lephix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create, read, update, organize, search, clip, and delete content in a user's Youdao Cloud Notes account. It is intended for workflows where the user wants an agent to manage notes, todos, and folders through the YoudaoNote CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive account credentials to access Youdao Cloud Notes. <br>
Mitigation: Install only when the user wants agent access to Youdao Cloud Notes, and configure API keys through the official YoudaoNote CLI flow. <br>
Risk: Commands can update, move, or delete notes and todos. <br>
Mitigation: Review destructive or modifying commands before approval, especially delete, update, and move operations. <br>
Risk: The CLI may include source tracking for skill-triggered commands. <br>
Mitigation: Set YOUDAONOTE_NO_TRACKING=1 if source tracking is not desired. <br>


## Reference(s): <br>
- [YoudaoNote ClawHub Release](https://clawhub.ai/lephix/youdaonote) <br>
- [Youdao Cloud Notes](https://note.youdao.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that read, write, move, or delete user notes and todos through the YoudaoNote CLI.] <br>

## Skill Version(s): <br>
1.0.9 (source: server evidence release.version and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

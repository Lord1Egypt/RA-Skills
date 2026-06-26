## Description: <br>
Zhihu CLI (pyzhihu-cli) lets an agent use a local Zhihu command-line tool for search, hot lists, questions, answers, comments, feeds, profiles, publishing, deletion, voting, following, collections, and notifications while keeping cookies on the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiguangmei](https://clawhub.ai/user/baiguangmei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to translate Zhihu-related requests into local `zhihu` CLI commands, summarize command results, and manage account actions only after the required local login flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to post, vote, follow, or delete content from a logged-in Zhihu account. <br>
Mitigation: Require explicit user confirmation with the exact command and target ID or title before any account-changing action, and avoid `-y` unless the user requested that exact deletion. <br>
Risk: Zhihu QR login and cookies can grant account access if exposed outside the user's trusted environment. <br>
Mitigation: Use QR login only through a private user-confirmed channel, never paste cookies into chat or logs, delete copied QR images after login, and run `zhihu logout` when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baiguangmei/pyzhihu-cli) <br>
- [Source skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Data-query commands should use JSON output when supported; login cookies remain local to the user's machine.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

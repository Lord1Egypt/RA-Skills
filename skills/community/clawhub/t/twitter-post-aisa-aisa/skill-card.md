## Description: <br>
Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa for users who already know the account, tweet, or campaign they want to act on. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Twitter/X context, prepare approved posts, and perform explicit engagement actions such as likes, follows, replies, quotes, and media-backed posts through AIsa. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose the raw AISA_API_KEY in normal command output. <br>
Mitigation: Do not paste command output into chats, tickets, or logs; rotate the key if it has already been exposed. <br>
Risk: The skill can immediately perform public Twitter/X account actions once invoked. <br>
Mitigation: Confirm the exact account, tweet, post text, and media path before every post, like, follow, unlike, or unfollow action. <br>
Risk: Twitter/X reads, posts, engagement actions, and selected media files are relayed through AIsa. <br>
Mitigation: Install and use the skill only if you trust AIsa to process those requests and files. <br>


## Reference(s): <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/twitter-post-aisa-aisa) <br>
- [AIsa](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output from bundled Python clients] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return authorization links, Twitter/X action results, tweet IDs, or tweet links when the AIsa API confirms an operation.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Searches public Telegram channels and groups by keyword through a local Telethon-backed Telegram search command and returns matching public results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirillvrnz](https://clawhub.ai/user/kirillvrnz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover public Telegram channels and groups related to a search query. It is useful when an agent needs structured public Telegram search results without accessing private chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a local executable with access to an authorized Telegram session.

Mitigation: Install only where the local executable and Telegram session are trusted, verify the executable owner and permissions, and use a narrowly scoped Telegram account.

Risk: Searches can expose only public Telegram channels and groups and may miss private or non-discoverable content.

Mitigation: Treat results as public discovery output, not a complete Telegram dataset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirillvrnz/skills/tgsearch-telethon)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 50 public Telegram channel or group results; usernames may be null.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Searches public Telegram channels and groups by keyword through a local Telethon-backed Telegram search helper and returns JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kirillvrnz](https://clawhub.ai/user/Kirillvrnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to search public Telegram channels and groups for a keyword and retrieve up to 50 matching public channel or group records. It is suitable when the operator controls the local Telegram helper and account session used for search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an unreviewed local Telegram helper and an already-authorized Telegram account session. <br>
Mitigation: Install only where the operator controls and trusts /usr/local/bin/tg_search, and prefer a dedicated low-privilege Telegram session. <br>
Risk: Search behavior and account access depend on the local helper rather than the packaged artifact alone. <br>
Mitigation: Verify that the helper performs only intended public Telegram search with the expected result limit before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kirillvrnz/tgsearch-telethon) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON array of public Telegram channel or group search results, or JSON error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a required query string and optional result limit; artifact documentation states a maximum of 50 results.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

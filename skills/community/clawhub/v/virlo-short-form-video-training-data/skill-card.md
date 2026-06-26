## Description: <br>
Virlo social media intelligence for viral video analytics, hashtag rankings, trend digests, and social listening across YouTube, TikTok, and Instagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VirloGit](https://clawhub.ai/user/VirloGit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content strategists, marketers, and developers use this skill to query Virlo for short-form video trends, hashtag rankings, viral video performance data, and social listening across YouTube, TikTok, and Instagram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Virlo's external service using a user-provided VIRLO_API_KEY. <br>
Mitigation: Install it only when the agent is intended to contact Virlo, and protect the API key as a secret. <br>
Risk: Keywords, competitor lists, campaign names, and monitoring targets may be sent to Virlo. <br>
Mitigation: Review inputs before requests and avoid sending sensitive monitoring targets unless that sharing is approved. <br>
Risk: The skill documents actions that can create searches, scheduled monitors, updates, or deletes. <br>
Mitigation: Require user confirmation before creating searches, scheduled monitors, updates, or deletes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VirloGit/virlo-short-form-video-training-data) <br>
- [Virlo homepage](https://dev.virlo.ai) <br>
- [Virlo API documentation](https://dev.virlo.ai/docs) <br>
- [Virlo API playground](https://dev.virlo.ai/docs/playground) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON API response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and VIRLO_API_KEY; requests contact the Virlo API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

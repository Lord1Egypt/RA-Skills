## Description: <br>
Generates personalized RSS digests ranked by keyword weights and creates tracked redirect links that can update future weighting from reader clicks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasaidon](https://clawhub.ai/user/pasaidon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, researchers, or agents monitoring multiple RSS feeds use this skill to produce a concise personalized digest and tune future recommendations from click feedback. It is useful when the user intentionally wants click-tracked RSS links as part of the digest workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish an unauthenticated click-tracking and log-management service to the internet. <br>
Mitigation: Install only when that behavior is intended; remove or protect public log and clear endpoints, make the public tunnel opt-in, and regularly delete raw IP and URL logs. <br>
Risk: Tracked redirect links may send readers to untrusted destinations if redirect targets are not constrained. <br>
Mitigation: Restrict redirects to trusted RSS source URLs before sharing generated digest links. <br>
Risk: The tunnel setup disables SSH host-key verification and exposes a local service through a third-party public tunnel. <br>
Mitigation: Re-enable SSH host-key verification and review tunnel exposure before using the service beyond local testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pasaidon/rss-personalized-digest) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest entries with tracked links, plus command and configuration snippets for operating the redirect service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses keyword weights and click history to prioritize future RSS items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

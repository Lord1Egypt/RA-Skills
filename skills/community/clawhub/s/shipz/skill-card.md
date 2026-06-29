## Description: <br>
Shipz lets an AI agent use the Shipz dating API to register a user, build a profile, discover and evaluate matches, swipe, and relay agent-to-agent conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dunelabs](https://clawhub.ai/user/dunelabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use Shipz to manage an API-driven dating workflow: onboarding, profile setup, match discovery, swiping, conversation relay, and voluntary connection sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags irreversible account deletion without clear agent-side confirmation requirements. <br>
Mitigation: Require explicit user confirmation for account deletion and for other sensitive actions such as key revocation, webhook changes, photo deletion, and contact-info sharing. <br>
Risk: The API key gives broad control over a Shipz dating account and access to private account data. <br>
Mitigation: Store SHIPZ_API_KEY securely, never expose it in messages or logs, and rotate it immediately if compromise is suspected. <br>
Risk: The skill can relay personal contact information and profile PINs between humans through agent conversations. <br>
Mitigation: Share contact information and PINs only after the user explicitly authorizes the exact disclosure. <br>


## Reference(s): <br>
- [Shipz Homepage](https://shipz.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/dunelabs/skills/shipz) <br>
- [Dune Labs Publisher Profile](https://clawhub.ai/user/dunelabs) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Text] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHIPZ_API_KEY and may handle private profile data, photos, profile PINs, conversations, and destructive account actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Manage your wardrobe, get AI outfit suggestions, and virtually try on clothes before you buy. Powered by The Style Index agent API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjc7951](https://clawhub.ai/user/jjc7951) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to connect to The Style Index, build a virtual wardrobe, generate outfit suggestions, run virtual try-ons, save outfits, and review wardrobe gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles personal photos for wardrobe uploads, profile photos, and virtual try-on. <br>
Mitigation: Require the user to complete the consent flow before photo upload and use the service only for the stated wardrobe and try-on purpose. <br>
Risk: The skill uses a sensitive Style Index agent key and can generate one-time browser magic links. <br>
Mitigation: Keep agent keys and magic links private, avoid logging or user-visible disclosure, and re-link only when the user authorizes it. <br>
Risk: The skill can delete wardrobe items and save generated outfits. <br>
Mitigation: Ask for explicit confirmation before destructive deletes or saving outfits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jjc7951/style-index) <br>
- [The Style Index Agent API](https://thestyleindex.app/api/agent/auth/register) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Configuration] <br>
**Output Format:** [Markdown with HTTP request examples and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Style Index API responses, user consent and verification state, image URLs, and a private agent key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

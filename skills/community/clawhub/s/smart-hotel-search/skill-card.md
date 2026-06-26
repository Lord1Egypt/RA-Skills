## Description: <br>
Smart Hotel Search helps agents handle non-standard hotel requests by searching Xiaohongshu user content for candidate hotels and checking FlyAI/Fliggy booking information for prices, rooms, scores, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sgw153759-oss](https://clawhub.ai/user/sgw153759-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to turn scenario-based hotel needs, such as pet-friendly stays, quiet rooms, elder-friendly hotels, or social-media-worthy pools, into hotel recommendations with supporting user-review context and booking details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on third-party CLI tools and browser-extension automation that can use a logged-in Xiaohongshu Chrome session. <br>
Mitigation: Use a separate Chrome profile or low-risk account, review OpenCLI and FlyAI before installing, approve searches before execution, and disable the extension or log out when finished. <br>
Risk: FlyAI usage may require an API key that could be exposed through shell history, logs, or shared environments. <br>
Mitigation: Store FLYAI_API_KEY only in an appropriate local secret store or private environment, avoid pasting it into shared transcripts, and rotate it if exposure is suspected. <br>
Risk: Hotel reviews, prices, availability, and booking links come from external services and user-generated content that may be incomplete, outdated, sponsored, or inaccurate. <br>
Mitigation: Present sources clearly, cross-check results across Xiaohongshu and FlyAI/Fliggy, and advise users to confirm critical details with the hotel or booking platform before booking. <br>


## Reference(s): <br>
- [Smart Hotel Search Examples](references/examples.md) <br>
- [Tool Installation Guide](references/installation.md) <br>
- [OpenCLI GitHub](https://github.com/jackwener/opencli) <br>
- [OpenCLI npm Package](https://www.npmjs.com/package/@jackwener/opencli) <br>
- [FlyAI](https://open.fly.ai/) <br>
- [flyai-cli npm Package](https://www.npmjs.com/package/@fly-ai/flyai-cli) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with inline shell commands and booking/search summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hotel names, review excerpts, prices, scores, and booking links; external results should be verified before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Builds an AI e-commerce customer service web application powered by Tencent RTC Conversational AI, with real-time voice and text interaction, trilingual support, optional digital avatar mode, and e-commerce workflows such as order inquiry, returns, shipping tracking, and promotions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryang-cool](https://clawhub.ai/user/jerryang-cool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and solution engineers use this skill to scaffold or integrate a TRTC ConversationAI customer service application for e-commerce support workflows, including voice, text, multilingual prompts, order context, and optional avatar experiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated app requires Tencent Cloud, TRTC, and LLM credentials. <br>
Mitigation: Use least-privilege Tencent credentials where possible, keep env.yaml out of version control, and rotate any credentials that may have been exposed. <br>
Risk: The /action endpoint can control TRTC conversation actions if exposed publicly without access control. <br>
Mitigation: Add authentication and authorization before exposing /action outside a trusted development environment. <br>
Risk: Chat content and order context may pass through TRTC and the configured LLM provider. <br>
Mitigation: Inform users about data flow, review provider data handling policies, and avoid sending sensitive business or personal data unless the deployment has appropriate safeguards. <br>
Risk: The skill can create and run a web application and install Python packages. <br>
Mitigation: Review the generated project, dependency list, and runtime configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryang-cool/trtc-ai-customer-service) <br>
- [Architecture reference](references/architecture.md) <br>
- [Configuration guide](references/config-guide.md) <br>
- [Frontend integration guide](references/frontend-guide.md) <br>
- [Tencent RTC Conversational AI](https://trtc.io/solutions/conversational-ai) <br>
- [LLM configuration guide](https://trtc.io/document/68338?product=conversationalai) <br>
- [TTS voice configuration](https://trtc.io/document/79682?product=conversationalai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration templates, and generated project files when the scaffold is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Flask and vanilla JavaScript web application scaffold that requires Tencent Cloud, TRTC, and LLM provider credentials.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

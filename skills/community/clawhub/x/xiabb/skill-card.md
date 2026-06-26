## Description: <br>
Xiabb is a macOS voice-to-text tool for Vibe Coding that records with the Globe key, sends audio to Google Gemini, and returns dictated text, translations, optimized prompts, or email drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyz2102](https://clawhub.ai/user/dyz2102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Xiabb to dictate text into macOS applications and to transform spoken input into translations, AI prompts, or email drafts. It is intended for users who are comfortable granting microphone and Accessibility permissions and using Google Gemini for transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool combines microphone capture, Google Gemini cloud transcription, Accessibility control, and auto-paste into the active app. <br>
Mitigation: Install only if those permissions and data flows are acceptable; avoid dictating passwords or confidential material. <br>
Risk: The installer can save a Gemini API key locally and the application depends on that key for transcription. <br>
Mitigation: Use a restricted Gemini API key that can be rotated, and inspect local key storage before deployment. <br>
Risk: The installer offers optional launch-at-login behavior. <br>
Mitigation: Decline launch-at-login unless needed and review install.sh before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyz2102/xiabb) <br>
- [XiaBB homepage](https://xiabb.lol) <br>
- [Google AI Studio API key](https://aistudio.google.com/apikey) <br>
- [Google AI for Developers](https://ai.google.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include dictated text, translated text, optimized prompts, email drafts, installation commands, and setup guidance.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

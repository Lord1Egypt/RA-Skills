## Description: <br>
Sih Ai Photo Editor helps agents use natural-language image editing for clothing changes, background replacement, face swaps, style transfer, and beauty retouching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit images and prompts to a Sih.Ai-compatible image editing API, then receive edited image URLs or downloaded local results. It is aimed at photo editing tasks such as background changes, outfit edits, face fusion, style transfer, and retouching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user images and prompts to Sih.Ai or api.vwu.ai and may handle private-person photos. <br>
Mitigation: Use only with explicit user consent, avoid sensitive or private-person images unless authorized, and document where uploaded images and prompts are processed and retained. <br>
Risk: The artifact includes a live-looking bundled API key. <br>
Mitigation: Rotate and remove bundled credentials; require users or administrators to provide API keys through environment variables or a secret manager. <br>
Risk: The quota workflow stores local user identifiers, usage history, prompts, credits, and top-up links under ~/.sih_ai. <br>
Mitigation: Disclose local storage, minimize logged prompt content, provide deletion instructions, and require confirmation before credit deductions or payment-related redirects. <br>
Risk: Face swaps, clothing edits, and impersonation-oriented prompts can be misused. <br>
Mitigation: Add clear use restrictions for consent, minors, sexualized edits, private-person images, and deceptive impersonation before enabling those workflows. <br>


## Reference(s): <br>
- [Sih.Ai API Guide](references/api_guide.md) <br>
- [Prompt Examples](assets/examples/prompts.txt) <br>
- [Sih.Ai Homepage](https://sih.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/a3273283/sih-ai-photo-editor) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets, API JSON responses, image URLs, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save edited images under ~/Desktop/Sih_Ai_Results/ and maintain local quota and usage files under ~/.sih_ai.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, _meta.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

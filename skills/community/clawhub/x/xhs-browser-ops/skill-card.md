## Description: <br>
xhs Agent helps operators plan Xiaohongshu posts, generate copy and titles, prepare covers, save drafts or publish after confirmation, interact with comments, and review visible creator metrics through the official creator site. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, social media operators, and agents can use this skill to draft and manage Xiaohongshu content, save drafts, publish only after explicit confirmation, reply to comments or messages, and review visible creator dashboard metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in Xiaohongshu creator account and may affect public or private account state. <br>
Mitigation: Require explicit approval before every account action, including replies, messages, likes, favorites, draft saves, and publishing; keep publish confirmation in the current chat turn. <br>
Risk: Optional image-generation API keys may expose external provider access if configured unnecessarily. <br>
Mitigation: Configure GEMINI_API_KEY, IMG_API_KEY, or HUNYUAN_API_KEY only when the corresponding image-generation provider is intentionally used. <br>
Risk: Login, CAPTCHA, SMS, or platform risk controls may block automated browser workflows. <br>
Mitigation: Pause for the user to complete required platform checks and do not attempt to bypass Xiaohongshu account protections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YIKAILucas/xhs-browser-ops) <br>
- [Xiaohongshu creator site](https://creator.xiaohongshu.com) <br>
- [Post Templates](references/post-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown result summaries with action, account, mode, status, details, and next step.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require optional image-generation API keys; publishing requires explicit confirmation in the current chat turn.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

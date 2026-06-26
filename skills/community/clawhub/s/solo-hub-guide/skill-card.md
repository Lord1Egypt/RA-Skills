## Description: <br>
Interactive step-by-step tutor for Solo Hub that guides a human through account setup, model browsing, team management, credits, and LLM/VLA fine-tuning using the Solo Hub web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samarthshukla6](https://clawhub.ai/user/samarthshukla6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Solo Hub users and developers use this skill as a human-in-the-loop tutor for account setup, model browsing, team and credit management, and LLM/VLA fine-tuning in the Solo Hub web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guided workflows can involve credit purchases, subscription changes, team-role changes, and training launches. <br>
Mitigation: Keep the agent in advisory mode and require the user to review and confirm payments, plan upgrades, role changes, and job starts directly in Solo Hub. <br>
Risk: Fine-tuning setup may involve optional Hugging Face or Weights & Biases token entry. <br>
Mitigation: Enter tokens only in the real Solo Hub UI, avoid sharing them in chat or screenshots, use minimum required scopes, and rotate or revoke exposed tokens. <br>
Risk: Incorrect UI guidance can lead to wrong dataset fields, camera counts, plan choices, or credit use. <br>
Mitigation: Use the bundled domain and tutorial JSON as the source for steps, validate each screen state with the user, and stop on validation failures before continuing. <br>


## Reference(s): <br>
- [Solo Hub docs](https://hub.getsolo.tech/docs) <br>
- [Solo Hub web UI](https://hub.getsolo.tech) <br>
- [ClawHub release page](https://clawhub.ai/samarthshukla6/solo-hub-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversational guidance with step validation prompts and Solo Hub documentation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled domain and tutorial JSON for UI steps; does not produce shell commands or executable API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

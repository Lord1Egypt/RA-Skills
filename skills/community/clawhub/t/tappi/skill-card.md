## Description: <br>
tappi provides lightweight Chrome DevTools Protocol browser control for agents that need compact page navigation, element interaction, form entry, file upload, screenshots, and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaihazher](https://clawhub.ai/user/shaihazher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use tappi to automate Chrome or Chromium browsing through CDP when they need token-efficient navigation, form entry, file upload, content extraction, screenshots, or interaction with shadow DOM and canvas-based apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate signed-in browser sessions and execute page JavaScript, which can affect sensitive accounts or trigger unintended page actions. <br>
Mitigation: Use it only on pages you are comfortable automating, supervise sensitive actions closely, and explicitly confirm destructive or high-impact actions before execution. <br>
Risk: Paste and upload commands can send local file contents to websites. <br>
Mitigation: Do not use paste --file or upload with secrets, credentials, private keys, or confidential documents, and verify the target page and file path before sending content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaihazher/tappi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Terminal output with indexed elements, extracted page text, status messages, and optional screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text extraction is capped for token efficiency, and browser actions require a Chrome or Chromium instance with CDP enabled.] <br>

## Skill Version(s): <br>
3.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

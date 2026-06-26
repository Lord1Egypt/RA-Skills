## Description: <br>
Helps an agent use Yunzhan APIs to convert PDF, PPT, Word, and JPG files into online flipbook links, cover previews, and QR codes for sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wancai12](https://clawhub.ai/user/wancai12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to upload or reference documents and create Yunzhan-hosted online flipbooks with shareable links and QR codes. It is intended for documents the user deliberately wants to publish or share online through their own Yunzhan account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to collect Yunzhan account passwords. <br>
Mitigation: Avoid pasting a real account password into chat; prefer a dedicated low-privilege account or a safer provider-controlled login flow when available. <br>
Risk: The skill uploads documents to Yunzhan and creates online flipbooks intended for viewing and sharing. <br>
Mitigation: Use it only for files the user explicitly wants to upload to Yunzhan and publish or share online. <br>
Risk: The artifact includes broader account actions such as listing and deleting existing books. <br>
Mitigation: Do not list or delete existing books unless the user explicitly requests that action and confirms the exact book IDs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wancai12/yunzhan-huace) <br>
- [Yunzhan API reference](references/api_docs.md) <br>
- [Yunzhan service site](https://www.yunzhan365.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown-style progress updates and results containing online viewing links, copy/view actions, cover image references, and QR code display instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload user-selected files to Yunzhan and poll conversion status before returning final sharing outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

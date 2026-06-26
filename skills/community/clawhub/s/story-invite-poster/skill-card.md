## Description: <br>
Creates custom invitation posters from user photos, memories, and event details using a two-stage Mew.design image and layout workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect event details, transform supplied photos into a story-driven hero visual, and generate a polished invitation poster for celebrations such as birthdays, housewarmings, weddings, and anniversaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User photos, event details, and the Mew.design API key are sent to external services during poster generation. <br>
Mitigation: Install only when the user accepts that data flow, prefer public image URLs the user controls, and use a revocable Mew.design API key. <br>
Risk: Local images or chat attachments require a public URL before they can be used by downstream APIs. <br>
Mitigation: Ask for a user-controlled public URL first; if a temporary third-party upload is needed, disclose the privacy tradeoff and get explicit consent before uploading. <br>
Risk: Generated poster layouts can obscure important people, pets, keepsakes, or event facts. <br>
Mitigation: Run the skill's built-in identity, text-safe-area, readability, and retry checks before returning the final poster. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuminliu026/story-invite-poster) <br>
- [Mew.design account and API key setup](https://mew.design/login) <br>
- [Mew.design image process API endpoint](https://api.mew.design/open/api/image/process) <br>
- [Mew.design design generate API endpoint](https://api.mew.design/open/api/design/generate) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with an image link, optional original-image link, and concise status text; API calls are shown as shell commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a final invitation poster URL after collecting event details, public image URLs or consented temporary uploads, and a user-provided Mew.design API key.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

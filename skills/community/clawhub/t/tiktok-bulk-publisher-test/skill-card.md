## Description: <br>
Automates bulk uploading and publishing TikTok videos with customizable titles, privacy settings, comment, duet, stitch controls, and upload status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operations teams use this skill to automate TikTok video uploads, configure post metadata and privacy controls, and check publishing status through command-line or Python workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish videos to a TikTok account, including public posts, using supplied account credentials. <br>
Mitigation: Use a test account or SELF_ONLY privacy first, and review each video, title, and privacy setting before running bulk publishing jobs. <br>
Risk: The skill relies on TikTok access tokens for live posting workflows. <br>
Mitigation: Provide only least-privilege TikTok tokens that are acceptable for the intended account, and rotate or refresh credentials according to TikTok token requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fly3094/tiktok-bulk-publisher-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples; runtime responses are status dictionaries and console text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform TikTok API calls with provided credentials and return publish IDs, video URLs, status values, or error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

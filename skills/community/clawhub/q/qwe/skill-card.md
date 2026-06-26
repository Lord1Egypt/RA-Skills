## Description: <br>
Facebook Publisher Skill (Automate Page Posts via Graph API) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YunneeToiChoi](https://clawhub.ai/user/YunneeToiChoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and page operators use this skill to configure Facebook Graph API Page publishing, exchange user tokens for Page tokens, publish text or image posts, schedule posts, and verify Page token connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful Facebook Page credentials and app secrets. <br>
Mitigation: Install only for Facebook apps and Pages you control, keep tokens in protected environment variables, avoid logging secrets, and rotate any exposed credentials. <br>
Risk: The token helper can save long-lived user and Page tokens to fb_tokens_output.json. <br>
Mitigation: Delete or protect fb_tokens_output.json after use and ensure it is never committed or shared. <br>
Risk: Running fb_publisher_agent.py directly can create a live public test post. <br>
Mitigation: Review scripts before execution and run posting commands only when you intend to publish to the configured Page. <br>
Risk: The artifact references OpenAI and Apify credentials although evidence does not document a required workflow for them. <br>
Mitigation: Do not provide OpenAI or Apify credentials unless a specific reviewed workflow requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YunneeToiChoi/qwe) <br>
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and helper scripts for Facebook Page posting workflows; the helper may create fb_tokens_output.json when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

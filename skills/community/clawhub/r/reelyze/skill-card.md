## Description: <br>
Reelyze helps agents analyze public Instagram Reels, TikToks, and YouTube Shorts, retrieve transcripts or media links, and generate short-form video scripts or content ideas through the Reelyze API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usamalatif](https://clawhub.ai/user/usamalatif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, social media managers, brands, and their agents use this skill to audit public short-form videos, identify hook and retention issues, retrieve transcripts or temporary media links, and draft scripts or content ideas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends public video URLs, content topics, and Reelyze API credentials to the Reelyze service. <br>
Mitigation: Use it only for content that is acceptable to share with Reelyze, avoid private drafts or confidential campaign plans, and store REELYZE_API_KEY securely. <br>
Risk: Changing REELYZE_BASE_URL can redirect requests and credentials to a different service endpoint. <br>
Mitigation: Keep REELYZE_BASE_URL unset or pointed at the trusted Reelyze API endpoint unless the user has explicitly approved another endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/usamalatif/reelyze) <br>
- [Reelyze homepage](https://getreelyze.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with API-result excerpts and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REELYZE_API_KEY for authenticated Reelyze API calls; REELYZE_BASE_URL is optional and should remain pointed at a trusted endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

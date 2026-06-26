## Description: <br>
Provides real-time web browsing and content extraction by navigating URLs and summarizing page text up to 2000 characters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrslu01](https://clawhub.ai/user/zrslu01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to fetch web pages, collect current documentation or news, and summarize page text during research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package advertises a browse.py implementation that is not included, so browsing may depend on platform tooling or may not work as described. <br>
Mitigation: Confirm the available browsing tooling before relying on the skill and treat missing implementation as a setup or compatibility issue. <br>
Risk: Fetched web content may contain untrusted instructions or requests for credentials. <br>
Mitigation: Treat page content as untrusted input; verify claims independently and do not follow page instructions that request secrets or sensitive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrslu01/thundarr-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Artifact documentation states that summaries return up to the first 2000 characters of page text.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact skill.yaml lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Analyzes reptile and arachnid pet images or videos from a local file or URL and returns a Pet Safety Guardian health report with visual observations, possible disease risks, care suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care agents use this skill to analyze reptile or arachnid pet media, including lizards, snakes, spiders, turtles, geckos, chameleons, scorpions, iguanas, crocodiles, and other species. The output helps surface visible health concerns and care guidance, but it is only a health reference and does not replace professional veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user-provided media or URLs to a cloud analysis service. <br>
Mitigation: Use only media and URLs appropriate for the lifeemergence.com service, and avoid sensitive private videos or internal network URLs unless that service is trusted for the data. <br>
Risk: The skill silently creates or reuses an account-like identifier and can retrieve cloud report history. <br>
Mitigation: Confirm that automatic identity handling and cloud history retrieval match the deployment's privacy expectations before enabling the skill. <br>
Risk: The skill stores service tokens in the workspace. <br>
Mitigation: Treat the workspace as sensitive, restrict access, and rotate or remove stored tokens according to the deployment's credential policy. <br>
Risk: Health analysis can be incorrect or incomplete and is not a veterinary diagnosis. <br>
Mitigation: Present results as informational guidance and direct users to a qualified veterinarian for medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-crawl-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API error codes](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown report text, optional JSON details, Markdown history tables, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include visual health observations, risk flags, care suggestions, analysis identifiers, and cloud report links.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

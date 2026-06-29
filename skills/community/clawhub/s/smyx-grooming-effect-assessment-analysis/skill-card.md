## Description: <br>
Analyzes post-grooming pet images or videos for mat residue, dandruff coverage, and coat smoothness, then returns a grooming score and targeted re-grooming or care suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent workflows use this skill to assess grooming quality from pet photos, videos, local files, or URLs, including mat residue, dandruff coverage, coat smoothness, and historical grooming reports. Results are for grooming-effect review and are not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private pet photos, videos, URLs, and identifiers may be sent to lifeemergence.com cloud services. <br>
Mitigation: Install only where cloud processing is acceptable, use approved media, and avoid submitting sensitive or unnecessary content. <br>
Risk: A local workspace database may store account/profile data and tokens. <br>
Mitigation: Run the skill in an isolated workspace and clean local state after use when handling private data. <br>
Risk: History reports are tied to an automatically selected identity. <br>
Mitigation: Review identity handling before deployment and restrict use to environments where automatic account association is acceptable. <br>
Risk: Debug configurations may expose request details in logs. <br>
Mitigation: Keep production configuration enabled by default and use debug configurations only in approved diagnostic environments. <br>
Risk: Visual grooming assessments could be mistaken for medical guidance. <br>
Mitigation: Treat outputs as grooming-quality support only and refer skin or health concerns to a veterinarian. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-grooming-effect-assessment-analysis) <br>
- [API Documentation](references/api_doc.md) <br>
- [Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, guidance] <br>
**Output Format:** [Markdown or JSON structured report with a grooming score, findings, care suggestions, and report link; optional saved output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media paths or media URLs, supports history-report listing, and limits local files to documented formats and size constraints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

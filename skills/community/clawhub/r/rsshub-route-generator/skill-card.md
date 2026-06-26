## Description: <br>
Analyzes website structure and generates RSSHub-compatible TypeScript route code, selector configuration, optional full-text RSS handling, and RSSHub Radar rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benzking](https://clawhub.ai/user/benzking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and RSSHub maintainers use this skill to inspect public website pages and draft RSSHub route files, including selectors, route metadata, and article extraction logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-specified website pages, which can expose private or sensitive URLs if used carelessly. <br>
Mitigation: Use it only with public websites and avoid submitting private, internal, authenticated, or sensitive URLs. <br>
Risk: Generated TypeScript routes and selectors may be inaccurate for complex or changing websites. <br>
Mitigation: Review and test the generated RSSHub route code before adding it to an RSSHub project. <br>
Risk: The skill may write generated route files to the workspace. <br>
Mitigation: Confirm the output path before allowing files to be written. <br>


## Reference(s): <br>
- [RSSHub Route Development Reference](references/dev-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown report with TypeScript code and RSSHub route file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose route files under rsshub-routes/{domain}/ and selector configuration for article lists, dates, categories, and optional full-text content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

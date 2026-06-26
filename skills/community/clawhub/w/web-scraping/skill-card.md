## Description: <br>
Extract structured information from websites using web_fetch for simple pages and browser automation for dynamic sites, login-gated flows, pagination, infinite scroll, or pages that require clicking/searching/filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangqixin9527](https://clawhub.ai/user/zhangqixin9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and operators use this skill to extract requested fields from public or authorized websites and return concise summaries, JSON, or CSV/TSV data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scrape logged-in pages or account-specific content and may save collected data to workspace files. <br>
Mitigation: Confirm the target site, exact fields, authorization to access private data, storage location, and retention expectations before use. <br>
Risk: Scraping can conflict with site access controls, rate limits, or policy expectations. <br>
Mitigation: Test one page first, avoid tight request loops, stop or switch sources when access is blocked, and collect only the fields the user requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangqixin9527/web-scraping) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Files, Guidance] <br>
**Output Format:** [Markdown summaries, JSON arrays, CSV/TSV rows, or workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit fields such as title, URL, source, date, and summary when applicable; larger jobs may checkpoint partial results to workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

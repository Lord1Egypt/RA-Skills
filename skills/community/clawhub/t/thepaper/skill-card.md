## Description: <br>
Provides lightweight analysis, keyword summaries, channel hotspot statistics, and long-form article highlights for public The Paper news pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, editors, and developers use this skill to summarize keyword-matched The Paper news, inspect channel hotspots, and extract concise points from long-form articles on public pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes public The Paper pages and may depend on dynamically rendered page content. <br>
Mitigation: Wait for page content to load before parsing and include collection time and source links in results. <br>
Risk: Automated collection could exceed the intended lightweight analysis scope. <br>
Mitigation: Respect platform rules, avoid batch scraping or API reverse engineering, and keep collection frequency controlled. <br>
Risk: Security evidence notes that VirusTotal is still pending. <br>
Mitigation: Review the included skill artifact before installation and confirm the requested access matches the expected public-page analysis use case. <br>


## Reference(s): <br>
- [The Paper homepage](https://www.thepaper.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/thepaper) <br>
- [Publisher profile](https://clawhub.ai/user/codenova58) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and structured analysis lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should include collection time and source links when public pages are analyzed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

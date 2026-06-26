## Description: <br>
Fetches public hot-list entries from tophub.today into JSON files and can crawl linked article pages into Markdown content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanqiudeng](https://clawhub.ai/user/hanqiudeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to collect public Chinese trend lists, save structured JSON records, and optionally enrich those records with crawled article body content. It is suited for monitoring public news, technology, entertainment, community, and other hot-list sources that tophub.today exposes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content fetching can modify JSON files in place when no output path is provided. <br>
Mitigation: Use the --output option or keep backups when you need to preserve original JSON files. <br>
Risk: Directory mode can update every matching JSON file in the selected folder. <br>
Mitigation: Run directory mode only on folders intended for update, and use --top to limit the batch when appropriate. <br>
Risk: The scripts depend on Python crawling and browser automation packages that execute network requests to public pages. <br>
Mitigation: Review and install the Python and Playwright dependencies only in an environment where public web crawling is allowed. <br>


## Reference(s): <br>
- [TopHub Today](https://tophub.today) <br>
- [ClawHub Skill Page](https://clawhub.ai/hanqiudeng/tophot-chinese) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON file outputs containing optional Markdown article content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated JSON records include title, description, url, timestamps, content, and error fields when content fetching is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Searches YouTube for a keyword, extracts video links from the results page, deduplicates them, and saves formatted local outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuai1iu](https://clawhub.ai/user/shuai1iu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can use this skill to automate YouTube searches and collect topic-specific video URLs for review, research, or content discovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a global browser-automation dependency that contacts YouTube and writes local HTML and link files. <br>
Mitigation: Install only in environments where that dependency and network behavior are acceptable, and review or delete generated files before sharing outputs. <br>
Risk: Search terms and saved results may contain sensitive or private information. <br>
Mitigation: Use non-sensitive search terms and handle generated HTML and link files according to local data-handling requirements. <br>
Risk: Unpinned dependencies can change behavior over time. <br>
Mitigation: Use pinned dependencies or a reviewed lockfile in stricter environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuai1iu/youtube-search-extractor) <br>
- [agent-browser](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated local HTML and text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an HTML snapshot and a deduplicated text file of YouTube video links for the requested search term.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

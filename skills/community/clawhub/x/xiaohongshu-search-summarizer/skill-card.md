## Description: <br>
Searches Xiaohongshu for a keyword, extracts top posts with text, images, and comments, then helps synthesize the collected material into an analytical report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piekill](https://clawhub.ai/user/piekill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to gather Xiaohongshu search results and turn text, comments, and images into a consolidated Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scrapes and stores third-party Xiaohongshu posts, comments, and images locally. <br>
Mitigation: Treat collected content as third-party material, review privacy/copyright/platform obligations, and delete raw outputs when finished. <br>
Risk: Security evidence reports an output-path containment bug. <br>
Mitigation: Use a dedicated output directory and avoid search keywords containing slashes or '..'. <br>
Risk: Xiaohongshu may present a login challenge during browser-based collection. <br>
Mitigation: Supervise the headed browser session and only complete authentication when appropriate for the account and use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piekill/xiaohongshu-search-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown report with local raw-data files and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs browser-based collection through playwright-cli, writes raw extraction Markdown and images to an output directory, and expects the agent to synthesize the results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

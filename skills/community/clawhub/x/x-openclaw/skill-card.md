## Description: <br>
Extract posts from X (Twitter) timeline or profile pages with engagement metrics, media URLs, and download local copies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyliu0](https://clawhub.ai/user/zyliu0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to scrape and archive visible X timeline, profile, or search-result posts with metadata, engagement metrics, and local media references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves scraped X post content and media locally, which can retain private or sensitive timeline material if the user selects those sources. <br>
Mitigation: Use only on pages the user intends to archive, avoid private or sensitive timelines, and review or delete generated ../../intel/x reports and media when they are no longer needed. <br>
Risk: Generated reports may reflect only the posts loaded at scrape time because X timelines are dynamic. <br>
Mitigation: Treat reports as point-in-time archives and verify important findings against the source page before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zyliu0/x-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/zyliu0) <br>
- [X home timeline](https://x.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with local media files and inline shell/browser commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under ../../intel/x and media under ../../intel/x/media when used as directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

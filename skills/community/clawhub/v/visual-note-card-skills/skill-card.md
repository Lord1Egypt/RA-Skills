## Description: <br>
Generates structured Chinese visual note cards and infographics as self-contained HTML, with optional PNG export through a bundled Playwright renderer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beilunyang](https://clawhub.ai/user/beilunyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to turn topics, articles, or concepts into shareable poster-style visual summaries. It is suited for creating bilingual knowledge cards, one-page summaries, and infographic-style notes for social media or print. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may contact Google Fonts and cdnjs when opened. <br>
Mitigation: Review generated HTML before distribution and allow those external font/script dependencies only in environments where they are acceptable. <br>
Risk: The Playwright export script renders HTML in Chromium, so rendering untrusted HTML can execute page scripts. <br>
Mitigation: Only render HTML content from trusted sources or inspect the file before running the PNG export workflow. <br>
Risk: Documented uninstall commands remove skill directories recursively. <br>
Mitigation: Check the target path before running removal commands. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/beilunyang/visual-note-card-skills) <br>
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [html2canvas CDN Dependency](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Self-contained HTML and rendered PNG files, with concise Markdown delivery notes and optional shell command invocation for export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default PNG export uses Playwright at 1.5x scale; generated HTML may load Google Fonts and html2canvas from third-party CDNs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

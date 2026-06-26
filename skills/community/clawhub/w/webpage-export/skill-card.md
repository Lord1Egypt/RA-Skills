## Description: <br>
Export webpages into clean local TXT, DOCX, and PDF files with source metadata, fallback extraction logic, and browser-assisted recovery for difficult pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilw-yezi](https://clawhub.ai/user/lilw-yezi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to archive or share webpage content as local text, Word, PDF, and metadata outputs before downstream review, analysis, or delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs and writes local export files, which can expose internal or sensitive pages if the agent is pointed at them. <br>
Mitigation: Use explicit trusted URLs and output folders; avoid localhost, private-network, file, cloud-metadata, or sensitive logged-in pages unless that access is intended. <br>
Risk: Browser-assisted fallback may execute page JavaScript through local Chrome, Chromium, Node, or Playwright. <br>
Mitigation: Use browser fallback only when needed, rely on trusted local runtime installations, and review metadata warnings before treating outputs as complete. <br>
Risk: Dynamic, blocked, or anti-bot pages may produce partial extraction or incomplete PDF output. <br>
Mitigation: Treat TXT plus JSON metadata as the baseline record, inspect extraction quality and warnings, and avoid relying on PDF alone for accuracy-sensitive work. <br>


## Reference(s): <br>
- [Accuracy and Fallbacks](references/accuracy-and-fallbacks.md) <br>
- [Chrome PDF Guide](references/chrome-pdf-guide.md) <br>
- [Delivery Rules](references/delivery-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Local TXT, DOCX, PDF, and JSON metadata files with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [TXT is the baseline extracted record; JSON metadata records paths, extraction quality, warnings, and partial-failure status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates daily technology news HTML reports from prepared IT Home and MyDrivers news data, including full text, images, and categorized sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choksta](https://clawhub.ai/user/choksta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare a local daily technology news report from collected Chinese tech-news JSON records and matching image files. The generated report is suitable for reviewing categorized phone, AI, automotive, big-tech, and system/app news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The HTML generator contains hard-coded local input and output paths. <br>
Mitigation: Review and update DATA_FILE, IMG_DIR, and OUT_FILE before running the script in a new environment. <br>
Risk: Untrusted JSON content or unexpected image filenames could affect the generated local report. <br>
Mitigation: Use trusted JSON data and simple expected image filenames when preparing report inputs. <br>
Risk: The workflow depends on fetching or preparing content from named third-party news sites. <br>
Mitigation: Confirm the source sites and collection workflow are acceptable before generating the local HTML report. <br>


## Reference(s): <br>
- [Data format reference](artifact/references/data_format.md) <br>
- [IT Home RSS feed](https://www.ithome.com/rss/) <br>
- [MyDrivers news list](https://news.mydrivers.com/) <br>
- [ClawHub skill page](https://clawhub.ai/choksta/tech-news-daily33) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON data-format examples; the included script produces a local HTML file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prepared local JSON data and local image files; output HTML embeds available images as base64 data URIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

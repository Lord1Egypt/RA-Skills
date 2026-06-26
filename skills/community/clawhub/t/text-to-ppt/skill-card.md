## Description: <br>
Converts text, documents, notes, or URLs into single-file HTML slide presentations with themed layouts, charts, icons, and keyboard or touch navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rendylong](https://clawhub.ai/user/rendylong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn pasted text, local files, Obsidian notes, or fetched URLs into polished 16:9 HTML presentation decks. It is suited for reports, summaries, proposals, plans, and other source material that should become slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive source text, local files, notes, or fetched URLs may be incorporated into generated slide decks. <br>
Mitigation: Use pasted text or local files for sensitive material, review input sources before URL fetching, and inspect the generated deck before sharing. <br>
Risk: Generated HTML decks load third-party CDN resources when opened. <br>
Mitigation: Open generated decks only in environments where loading external CDN assets is acceptable, or replace CDN dependencies with approved local assets before distribution. <br>
Risk: The skill specifies a default Obsidian vault save path that may not match the user's intended destination. <br>
Mitigation: Confirm or change the output path before writing the final HTML file. <br>
Risk: The output is executable HTML that can include chart scripts and navigation code. <br>
Mitigation: Review the generated HTML before opening it in sensitive environments or sending it to others. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rendylong/text-to-ppt) <br>
- [Design System Reference](references/design-system.md) <br>
- [HTML Shell Template](references/shell-template.html) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js@4) <br>
- [Chart.js DataLabels CDN](https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2) <br>
- [Font Awesome CDN](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css) <br>
- [Google Fonts Inter](https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, configuration, guidance] <br>
**Output Format:** [JSON slide outline followed by a single-file HTML presentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 8-15 slides by default with a maximum of 20; generated decks may load third-party CDN resources when opened.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

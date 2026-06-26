## Description: <br>
Organize, tag, search, and manage macOS screenshots with OCR, bulk renaming, folder categorization, cleanup, and CleanShot X integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10OSS](https://clawhub.ai/user/10OSS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find, organize, rename, archive, and search macOS screenshots, including OCR-based search and CleanShot X workflow integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk screenshot moves or renames may affect many local files at once. <br>
Mitigation: Ask the agent to preview matched files first, use dry-run options where available, and confirm source and destination folders before running mutating commands. <br>
Risk: Changing the macOS screenshot location is persistent and may confuse later capture workflows. <br>
Mitigation: Record the previous screenshot location and the exact command used so the change can be undone. <br>
Risk: OCR indexing and cloud-upload workflows can expose sensitive screenshot contents. <br>
Mitigation: Avoid cloud upload for sensitive screenshots and review OCR/index destinations before processing private image collections. <br>
Risk: Cleanup automation can remove or archive screenshots that are still needed. <br>
Mitigation: Use date thresholds conservatively, preview affected files, and keep archive or trash recovery paths clear before enabling scheduled cleanup. <br>


## Reference(s): <br>
- [OCR Setup for Screenshot Search](references/ocr-setup.md) <br>
- [CleanShot X Workflows](references/cleancast-x.md) <br>
- [Automation Patterns](references/automation-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local screenshot-management workflows and may suggest file-moving, renaming, OCR, and macOS screenshot-location commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

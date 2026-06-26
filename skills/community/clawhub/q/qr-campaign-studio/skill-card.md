## Description: <br>
Generate marketing QR codes with batch output, UTM tracking links, logo embedding, and poster composition for URL, text, Wi-Fi, and vCard payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, growth teams, and developers use this skill to create individual or batch QR campaign assets with tracking parameters, optional logo embedding, and poster-ready output. It is not intended for payment settlement or payment gateway logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wi-Fi passwords or contact details can appear in generated QR payload previews, metadata files, terminal output, or generated QR images. <br>
Mitigation: Treat generated QR assets, metadata JSON, reports, and logs as sensitive; avoid committing them and store or share them only with the intended audience. <br>
Risk: Batch item names from CSV or JSON input can include path separators and write output files outside the selected output directory. <br>
Mitigation: Use only trusted batch files, review or normalize the name column before running batch generation, and run the skill in a dedicated output directory. <br>


## Reference(s): <br>
- [Format reference](references/format.md) <br>
- [Sample batch CSV](references/sample-batch.csv) <br>
- [ClawHub skill page](https://clawhub.ai/wangziiiiii/qr-campaign-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated PNG or JPEG images and JSON metadata or reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce QR image files, poster composites, metadata JSON, and batch run reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

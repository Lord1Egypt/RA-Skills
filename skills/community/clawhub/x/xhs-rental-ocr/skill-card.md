## Description: <br>
Extracts structured rental and pricing data from local Xiaohongshu or social-media images using offline Apple Vision OCR, optional long-image slicing, and Excel spreadsheet export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangkai258](https://clawhub.ai/user/yangkai258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators can use this skill to run a local macOS OCR workflow that extracts rental, area, and unit-price fields from selected images into spreadsheet data. It is suited for batch extraction from screenshots or long social-media images, with manual review of OCR results before downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads selected local images and writes spreadsheet outputs to the local filesystem. <br>
Mitigation: Run it only on intended images and choose the output path deliberately. <br>
Risk: Long-image slicing creates additional cropped image files next to the original image. <br>
Mitigation: Use slicing only when needed and remove generated cropped files after reviewing the output. <br>
Risk: The documented URL and CSV options are incomplete in the current implementation. <br>
Mitigation: Prefer local image inputs and Excel output unless the code is updated and revalidated. <br>
Risk: OCR and regex extraction can produce incorrect or abnormal rental values. <br>
Mitigation: Review extracted records before using them for reporting, pricing, or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangkai258/xhs-rental-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and local spreadsheet outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local Excel files and may create sliced image files next to the original image when long-image slicing is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

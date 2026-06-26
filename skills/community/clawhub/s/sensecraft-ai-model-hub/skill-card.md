## Description: <br>
Connect OpenClaw to the SenseCraft public model library to search, inspect, export, and download AI vision models for software and edge AI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jancee](https://clawhub.ai/user/jancee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find SenseCraft public vision models, inspect model metadata and download URLs, export searchable catalogs, download artifacts, and validate candidates for OpenClaw or edge AI integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download model artifacts and create local files such as indexes, manifests, models, and captures. <br>
Mitigation: Run download and demo workflows in an isolated workspace, inspect downloaded model files before production use, and remove saved captures or other generated files when they are no longer needed. <br>
Risk: The optional local webcam demo accesses the user's camera and can save annotated frames. <br>
Mitigation: Run the webcam demo only when local camera processing is intended, confirm camera permissions explicitly, and delete saved captures after validation. <br>
Risk: SenseCraft API responses, numeric field meanings, and download URLs may change or may not fully document runtime compatibility. <br>
Mitigation: Use the bundled list, view, and index workflows with retries and mild throttling, preserve raw metadata, and verify downloaded artifacts before claiming exact TFLite or runtime compatibility. <br>
Risk: Vision model preprocessing and output decoding can be model-specific, especially for YOLO-family exports. <br>
Mitigation: Check tensor metadata, labels, quantization, thresholds, and model-specific postprocessing notes before integrating a model or treating demo output as validated. <br>


## Reference(s): <br>
- [SenseCraft Public Model API](references/sensecraft-api.md) <br>
- [Field Mapping Notes](references/field-mapping-notes.md) <br>
- [Integration Notes](references/integration-notes.md) <br>
- [Local Webcam Demo Notes](references/local-webcam-demo.md) <br>
- [Model Catalog](references/model-catalog.md) <br>
- [SenseCraft API Base URL](https://sensecraft.seeed.cc/aiserverapi) <br>
- [SSCMA-Micro Reference Implementation](https://github.com/Seeed-Studio/SSCMA-Micro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON or CSV export paths, download manifests, and integration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local model files, catalog exports, manifests, and annotated webcam captures when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

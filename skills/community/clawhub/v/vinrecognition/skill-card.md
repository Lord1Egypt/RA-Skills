## Description: <br>
Recognizes VIN text from a vehicle or document image and returns the VIN, correctness flag, brand, and manufacturer details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user provides a VIN photo from a windshield, registration document, or similar source and needs the VIN plus basic vehicle maker details extracted. It supports vehicle verification, record entry, and used-car evaluation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VIN photos and any visible vehicle or document details are sent to JisuAPI for OCR processing. <br>
Mitigation: Use a dedicated JisuAPI key where possible, monitor quota or billing, and provide only the intended cropped VIN image rather than broader sensitive paperwork. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/vinrecognition) <br>
- [JisuAPI VIN Recognition API](https://www.jisuapi.com/api/vinrecognition/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result or JSON error object, with guidance for invoking the Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; accepts a local relative image path or base64-encoded image content.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

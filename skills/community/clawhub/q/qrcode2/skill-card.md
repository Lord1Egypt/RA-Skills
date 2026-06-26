## Description: <br>
本地将文本/URL 编成 PNG 二维码，或从图片识别二维码，可与远程 qrcode 技能搭配。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate local PNG QR codes from text or URLs and to decode text from local QR-code image files without relying on an external API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated QR images can overwrite files in the current working directory when an existing output path is reused. <br>
Mitigation: Use a dedicated output directory and review the requested output path before running encode. <br>
Risk: The skill depends on local Python packages for QR generation and decoding. <br>
Mitigation: Install qrcode[pil] and opencv-python from trusted sources, preferably in a virtual environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/qrcode2) <br>
- [JisuAPI QR code API](https://www.jisuapi.com/api/qrcode/) <br>
- [JisuAPI](https://www.jisuapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [JSON responses, shell command examples, and generated PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encode returns a local output path and QR settings; decode returns decoded text, detected points when available, and the input path.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
获取并返回最新的实时卫星云图，并在用户请求云图、卫星云图、实时云图或天气图时下载风云4B卫星云图供代理返回。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliao8](https://clawhub.ai/user/wuliao8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to fetch the latest FY4B satellite cloud image and return it with a human-readable capture time. It is intended for weather-image lookup workflows where a current satellite cloud map is useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads imagery from an external satellite-image URL. <br>
Mitigation: Allow network access only to the disclosed image source when this skill is used, and invoke it only when a satellite cloud image is requested. <br>
Risk: Recent satellite images are stored in a local OpenClaw cache. <br>
Mitigation: Review local cache retention expectations and clear the cache if local image persistence is not desired. <br>
Risk: OCR may fail to read the capture time and fall back to a current timestamp. <br>
Mitigation: Treat the displayed capture time as best-effort and verify it against the image content or source service when timestamp precision matters. <br>
Risk: The skill depends on OCR and image-processing packages plus a system Tesseract installation. <br>
Mitigation: Install dependencies from trusted package sources and confirm the Chinese OCR language data is installed before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuliao8/yuntu) <br>
- [Publisher profile](https://clawhub.ai/user/wuliao8) <br>
- [National Satellite Meteorological Center](https://www.nsmc.org.cn/) <br>
- [FY4B satellite cloud image](https://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_REGC_GCLR.JPG) <br>
- [Tesseract Chinese language data](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown text with a local image media reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads a JPEG satellite image, keeps a small local cache, and may use the current timestamp when OCR cannot read the capture time.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Control MindReset Dot Quote/0 through the local quote0.js CLI and Dot Developer Platform APIs for device configuration, content pushes, status queries, content switching, task listing, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YangguangZhou](https://clawhub.ai/user/YangguangZhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate a MindReset Dot Quote/0 device from an agent by running local Node.js commands that call the Dot Open API. It supports listing devices, checking status, switching content, and pushing text or PNG image content when the required credentials are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DOT_API_KEY grants access to Dot Open API actions for the user's account. <br>
Mitigation: Treat DOT_API_KEY like a password, prefer one-time arguments or temporary environment variables, and never commit it to files. <br>
Risk: Commands using DOT_DEVICE_ID can change the selected device's displayed content or state. <br>
Mitigation: Verify DOT_DEVICE_ID before state-changing commands and use devices or status checks before pushing updates. <br>
Risk: --imageFile reads a local PNG and uploads its contents to the Dot service. <br>
Mitigation: Use only intended non-sensitive PNG files and rely on the script's PNG and size checks before upload. <br>


## Reference(s): <br>
- [ClawHub Quote/0 skill page](https://clawhub.ai/YangguangZhou/quote0) <br>
- [Dot Open API overview](https://dot.mindreset.tech/docs/service/open) <br>
- [Dot API key setup](https://dot.mindreset.tech/docs/service/open/get_api) <br>
- [Dot device ID setup](https://dot.mindreset.tech/docs/service/open/get_device_id) <br>
- [Dot device list API](https://dot.mindreset.tech/docs/service/open/list_devices_api) <br>
- [Dot device status API](https://dot.mindreset.tech/docs/service/open/device_status_api) <br>
- [Dot text API](https://dot.mindreset.tech/docs/service/open/text_api) <br>
- [Dot image API](https://dot.mindreset.tech/docs/service/open/image_api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from quote0.js] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and DOT_API_KEY; device actions also require DOT_DEVICE_ID.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

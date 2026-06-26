## Description: <br>
图图智控（TUTU Smart Control） lets an agent remotely operate an Android phone through TUTU hardware for GUI automation, device status checks, communications, file management, app management, and related phone tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaojiaqi](https://clawhub.ai/user/zhaojiaqi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers with TUTU hardware use this skill to let an agent control and automate Android phones through predefined remote-control actions. Typical tasks include screen inspection, clicking and typing, app workflows, phone status checks, communications, location and notification access, and limited user-storage file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad remote control over an Android phone and can expose sensitive personal data or perform sensitive actions. <br>
Mitigation: Install only for trusted publishers and trusted TUTU devices, use a non-primary or closely monitored phone where possible, and require explicit user intent before messaging, calling, notification reading, file access, app changes, settings changes, downloads, mock location, or GUI automation inside sensitive apps. <br>
Risk: The TUTU API token grants access to the paired device if exposed. <br>
Mitigation: Store TUTU_API_TOKEN only in the platform secret store, never paste it into conversations or logs, and revoke or rotate it immediately if exposure is suspected. <br>
Risk: Security evidence reports inconsistent safety documentation and overly broad activation triggers. <br>
Mitigation: Review the requested phone action before execution and keep platform confirmation enabled for sensitive operations and privacy-data reads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaojiaqi/tutu-smart-control) <br>
- [TUTU Smart Control homepage](https://www.szs.chat) <br>
- [TUTU phone action API endpoint](https://www.szs.chat/api/phone_action.php) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration, JSON] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request or response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TUTU_API_TOKEN and a connected TUTU Android hardware device.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata; artifact frontmatter and claw.json list 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

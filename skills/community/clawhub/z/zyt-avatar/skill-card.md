## Description: <br>
Zyt avatar helps agents use the Chanjing Avatar API to upload source media, create lip-sync video tasks, and poll for generated video URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create text-driven or audio-driven lip-sync avatar videos through Chanjing, including media upload, task creation, status polling, and returning generated video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Chanjing credentials and sends user-provided media, text, audio, and generated video URLs to Chanjing. <br>
Mitigation: Keep credentials in a private local configuration file with restrictive permissions and only submit media intended for Chanjing processing. <br>
Risk: The API base URL can be changed with CHANJING_API_BASE, which could send credentials or media to an unintended endpoint. <br>
Mitigation: Keep CHANJING_API_BASE pointed at https://open-api.chanjing.cc unless another endpoint is deliberately trusted. <br>
Risk: Some helper scripts described by the skill are not present in this artifact. <br>
Mitigation: Confirm available files before running documented examples and add missing helpers only from a trusted source. <br>


## Reference(s): <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and returned URLs or status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns remote video URLs by default and task status or progress while polling.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Connect to Tapo cameras, verify local access, capture snapshots, and inspect frames with local-first RTSP workflows and safe fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to their own Tapo cameras on a trusted local network, validate reachability and authentication, and capture user-approved still images. It is intended for local-first camera troubleshooting and snapshot workflows, not broad surveillance design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive camera access and local camera credentials. <br>
Mitigation: Use it only for user-owned cameras on a trusted local network, keep credentials in a secret manager or short-lived environment variables, and avoid storing passwords or credential hashes in notes. <br>
Risk: Captured still images and local notes may reveal private camera locations, hosts, or scenes. <br>
Mitigation: Save captures only to user-approved local paths, keep ~/tapo-camera/ private, and avoid cloud uploads or shared chat surfaces unless the user explicitly requests them. <br>
Risk: Full RTSP URLs can expose embedded credentials when printed or copied into logs. <br>
Mitigation: Keep RTSP URLs redacted by default and use --show-rtsp only when the user explicitly needs the full URL for a local tool or debugging step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/tapo-camera) <br>
- [Skill homepage](https://clawic.com/skills/tapo-camera) <br>
- [Setup guidance](setup.md) <br>
- [Discovery and authentication](discovery-and-auth.md) <br>
- [Snapshot workflows](snapshot-workflows.md) <br>
- [API fallback guidance](api-fallback.md) <br>
- [Troubleshooting guidance](troubleshooting.md) <br>
- [Local capture helper](tapo-capture.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus a Python helper that can print text or JSON summaries and save JPEG still captures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works with local Tapo camera hosts, python-kasa, ffmpeg, optional credential environment variables, and explicit local output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

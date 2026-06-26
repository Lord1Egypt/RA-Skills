## Description: <br>
AI video editor for YouTube creators — removes pauses, filler words, and dead air automatically via API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esokullu](https://clawhub.ai/user/esokullu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use Tubeify to submit raw YouTube recordings to a paid external video-editing API, poll for completion, and retrieve cleaned-up videos with pauses, filler words, and dead air removed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends video URLs to a paid third-party editing service. <br>
Mitigation: Use only video URLs you are authorized to share with Tubeify, and avoid private or non-public videos unless third-party processing is acceptable. <br>
Risk: The examples use a wallet address, USDC transaction hash, and session cookie. <br>
Mitigation: Never provide wallet private keys or seed phrases, protect the generated session cookie, and verify payment details before submitting a job. <br>


## Reference(s): <br>
- [Tubeify Website](https://tubeify.xyz) <br>
- [ClawHub Skill Page](https://clawhub.ai/esokullu/tubeify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and API parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and access to a public video URL, wallet address, USDC transaction hash, and session cookie for polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

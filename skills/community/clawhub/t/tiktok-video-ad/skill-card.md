## Description: <br>
Create native TikTok video ads with Pexo: vertical 9:16, sound-on, hook-first ads where Pexo writes the script, sequences shots, chooses models, and delivers a ready-to-post video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and agents use this skill to submit a product brief and optional media to Pexo's hosted service, then receive a ready-to-post TikTok video ad and project link. It is scoped to vertical TikTok ads, not landscape or long-form video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, briefs, uploaded media, and generated assets are sent to Pexo's hosted service. <br>
Mitigation: Avoid sending sensitive customer, regulated, or proprietary material unless organizational policy permits it. <br>
Risk: The skill requires a PEXO_API_KEY and can use Pexo account credits when creating or revising video projects. <br>
Mitigation: Treat the API key as a secret, keep ~/.pexo/config private, verify PEXO_BASE_URL points to https://pexo.ai, and confirm credit availability before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pexo/tiktok-video-ad) <br>
- [Pexo](https://pexo.ai) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command usage, JSON status interpretation, project links, and plain-text signed asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PEXO_API_KEY and PEXO_BASE_URL; may upload user-provided media, consume Pexo account credits, poll asynchronous project status, and cache downloaded assets under ~/.pexo/tmp.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

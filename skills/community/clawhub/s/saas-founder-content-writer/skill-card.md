## Description: <br>
Saas Founder Content Writer helps creators, SaaS founders, indie hackers, and product builders turn real product updates, user pain points, technical lessons, launches, or explainers into high-signal posts for X, Reddit, LinkedIn, Xiaohongshu, and YouTube, including optional HTML/CSS-rendered covers, thumbnails, and data cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, creators, indie hackers, and product builders use this skill to convert supplied raw material into platform-fit social content without generic marketing copy. It supports Product and Knowledge modes, platform-specific drafting, image briefs or deterministic text/data graphic rendering, and optional vault archiving after explicit consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated posts can include unsupported marketing, performance, security, financial, or compliance claims if the user's source material is weak or incomplete. <br>
Mitigation: Require raw material before drafting, avoid inventing facts or metrics, flag claims that lack evidence, and have the founder review every draft before publishing. <br>
Risk: Platform-specific self-promotion rules, especially on Reddit and Xiaohongshu, can affect whether content is acceptable or distributed. <br>
Mitigation: Keep promotion secondary to reader value and remind the founder to check the target subreddit or Xiaohongshu promotion rules before posting. <br>
Risk: Optional image rendering runs local HTML/CSS through headless Chrome and can fail or require environment-specific browser configuration. <br>
Mitigation: Use self-contained HTML with no credentials or external network assets, keep the browser sandbox enabled by default, and fall back to the image brief or manual rendering if Chrome cannot launch. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/saas-founder-content-writer) <br>
- [Publisher Profile](https://clawhub.ai/user/archlab-space) <br>
- [Render Image Setup](artifact/render-image-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts with platform-specific sections, optional image briefs, optional HTML/CSS templates, and render commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PNG-rendering commands for text/data graphics; saving drafts or rendered assets is opt-in and requires an explicit vault target or user consent.] <br>

## Skill Version(s): <br>
0.12.0 (source: server release evidence and artifact CHANGELOG, released 2026-06-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

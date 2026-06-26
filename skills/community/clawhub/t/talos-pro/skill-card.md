## Description: <br>
Talos Pro generates multi-platform social media content calendars with daily posting schedules, A/B caption variants, content angle ideas, repurposing guidance, and CSV exports for scheduling tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, content creators, and social media operators use Talos Pro to generate 8- to 12-week posting calendars, caption variants, content angles, and scheduling exports for Twitter, LinkedIn, Instagram, Threads, and TikTok. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is gated by a paid license key. <br>
Mitigation: Confirm the license source before use and provide LICENSE_KEY only in a trusted local environment. <br>
Risk: The documented install command uses --break-system-packages for Python dependency installation. <br>
Mitigation: Install dependencies in a virtual environment or other isolated Python environment instead. <br>
Risk: The skill creates local JSON, CSV, and Markdown calendar export files where it runs. <br>
Mitigation: Run it from an intended workspace and review generated files before importing them into scheduling tools. <br>


## Reference(s): <br>
- [Talos Pro on ClawHub](https://clawhub.ai/occupythemilkyway/talos-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Files, Shell commands, Configuration] <br>
**Output Format:** [Terminal tables plus generated JSON, CSV, and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LICENSE_KEY and writes talos_pro_<topic>_<date> export files in the working directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

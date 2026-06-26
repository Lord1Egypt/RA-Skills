## Description: <br>
Automates health video production planning with topic research, script, character, image prompt, and video prompt generation using the Perplexity API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaotiensinh-abm](https://clawhub.ai/user/xaotiensinh-abm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators and video producers use this skill to turn a health topic or theme into a structured short-form video production plan. The plan includes topic selection, a character prompt, a four-part script, image prompts, and VEO3 video prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the requested video topic and generated planning context to Perplexity. <br>
Mitigation: Use a dedicated Perplexity API key where possible and avoid entering private or regulated health information. <br>
Risk: Generated health scripts or claims may be inaccurate or misleading if published without review. <br>
Mitigation: Review health claims, disclaimers, and generated production plans before publishing. <br>


## Reference(s): <br>
- [TCM Video Factory on ClawHub](https://clawhub.ai/xaotiensinh-abm/tcm-video-factory) <br>
- [Publisher profile: xaotiensinh-abm](https://clawhub.ai/user/xaotiensinh-abm) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance, Files] <br>
**Output Format:** [Markdown file named PLAN_[timestamp].md with script, character, image prompt, and video prompt sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and PERPLEXITY_API_KEY; sends the requested topic and planning context to Perplexity.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

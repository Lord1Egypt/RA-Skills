## Description: <br>
Turn quotes and reflections from books or films into polished shareable check-in posters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn book, film, documentary, anime, drama, or similar reflections into social-ready quote check-in posters. The skill gathers a title, quote, takeaway, tone, optional reference image URL, and optional personal metadata, then guides image generation and final poster composition through Mew APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a user-provided Mew API key. <br>
Mitigation: Use a restricted personal API key, validate it before generation, and replace it if authentication fails or the user requests a key change. <br>
Risk: Quotes, reflections, optional public image URLs, and generated backgrounds are sent to Mew APIs. <br>
Mitigation: Tell users what will be sent before generation and avoid submitting sensitive personal content unless they approve that use. <br>
Risk: Local images or chat attachments are not directly usable by the downstream APIs and may require third-party hosting. <br>
Mitigation: Prefer public image URLs; only upload a local image after clearly explaining the privacy tradeoff and receiving user consent. <br>
Risk: Generated poster text can be unreadable or overlap a busy background. <br>
Mitigation: Inspect the generated background and final poster, retry once with stronger safe-area, typography, and readability cues when needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shuminliu026/quote-check-in-poster) <br>
- [Mew account and API key setup](https://mew.design/login) <br>
- [Mew image-process API endpoint](https://api.mew.design/open/api/image/process) <br>
- [Mew design-generate API endpoint](https://api.mew.design/open/api/design/generate) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with generated poster image link and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a shareable poster image URL when the Mew API workflow succeeds; may include curl examples for API calls.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

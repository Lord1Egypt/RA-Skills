## Description: <br>
Yummy Shared provides shared yummycli operating guidance for first-time setup, Gemini credential checks, JSON output handling, and CLI safety rules before image or video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yummysource](https://clawhub.ai/user/yummysource) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when operating yummycli to verify Gemini authentication, initialize credentials when needed, interpret JSON command output, and apply shared safety rules for generated image or video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents passing a Gemini API key through a command-line argument, which can expose sensitive credentials through shell history or process listings. <br>
Mitigation: Use a dedicated, revocable key through GEMINI_API_KEY, an interactive prompt, or another secret-safe mechanism instead of pasting a live key into chat or a command argument. <br>
Risk: The skill depends on yummycli for generation workflows and credential handling. <br>
Mitigation: Install and run the skill only when the publisher and @yummysource/yummycli package are trusted. <br>


## Reference(s): <br>
- [Yummy Shared on ClawHub](https://clawhub.ai/yummysource/yummy-shared) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yummycli and GEMINI_API_KEY for Gemini-backed commands; generation commands return JSON on stdout.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

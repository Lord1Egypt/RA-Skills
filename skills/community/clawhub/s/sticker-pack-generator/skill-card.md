## Description: <br>
AI sticker pack generator - create custom WhatsApp stickers, Telegram sticker packs, emoji-style art, and kawaii character stickers from any description using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate sticker-style image assets from text prompts for WhatsApp, Telegram, emoji-style reactions, and kawaii or chibi character art. The skill requires a Neta API token and can optionally use a reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sticker prompts, optional reference image UUIDs, and the Neta API token are sent to the external api.talesofai.com service. <br>
Mitigation: Use the skill only with data appropriate for that external service, and avoid secrets, private personal data, regulated data, or proprietary content in prompts. <br>
Risk: Passing a long-lived API token directly on the command line can expose it through shell history or local process inspection. <br>
Mitigation: Use a revocable token and pass it from an environment variable rather than typing the token directly into commands. <br>
Risk: Image generation depends on an external API and can time out or return no image URL. <br>
Mitigation: Treat generated URLs as best-effort output and handle timeout or failed-task responses before relying on the result in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/sticker-pack-generator) <br>
- [Neta API token and access](https://www.neta.art/open/) <br>
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image) <br>
- [Neta artifact task endpoint](https://api.talesofai.com/v1/artifact/task/{taskUuid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL from CLI output, with shell command examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports square, portrait, landscape, and tall image sizes; optional reference image UUID enables style inheritance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

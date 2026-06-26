## Description: <br>
Generate QuotLy-style stickers from forwarded or quoted messages and return one media file path for auto-send. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakullla](https://clawhub.ai/user/sakullla) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents in chat or group automation use this skill to turn selected forwarded or quoted messages into a QuotLy-style WebP sticker and return the generated MEDIA path for delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected message content, sender display data, formatting entities, and optional avatar or status URLs may be sent to the configured QuotLy rendering API. <br>
Mitigation: Use only where users understand that selected chat content is sent to an external renderer, and restrict QUOTLY_API_ALLOW_HOSTS in private or regulated environments. <br>
Risk: Broad implicit invocation can generate stickers accidentally in group chats. <br>
Mitigation: Require a clear user request before auto-sending generated media and include context.event.update_id when available to suppress duplicate retries. <br>
Risk: User-provided avatar and status URLs can be forwarded to the rendering service. <br>
Mitigation: Use trusted input sources for profile media and enable QUOTLY_AUDIT_LOG when request monitoring is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sakullla/quotly-style-sticker) <br>
- [QuotLy Rendering API](https://bot.lyo.su/quote/generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [stdout text with a MEDIA:<absolute-path-to-webp> line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one WebP media file; duplicate retries may emit no MEDIA line.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

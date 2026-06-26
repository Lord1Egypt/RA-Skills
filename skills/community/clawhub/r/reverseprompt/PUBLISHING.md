# Publishing / provenance notes

- Publisher: NanoPhotoHQ
- Service homepage: https://nanophoto.ai
- API key management page: https://nanophoto.ai/settings/apikeys
- Skill purpose: analyze videos with the NanoPhoto.AI reverse-prompt API to extract shot breakdowns, visual prompts, and structured descriptions.

## Required credential

This skill requires exactly one credential:

- `NANOPHOTO_API_KEY` — required

Do not paste the API key into chat. Configure it through the platform's secure environment-variable setting for this skill.

## Safety / usage notes

- Only analyze content you are authorized to upload or process.
- For local files, prefer the bundled script instead of manual shell base64 for reliability.
- This skill does not ask for unrelated credentials.

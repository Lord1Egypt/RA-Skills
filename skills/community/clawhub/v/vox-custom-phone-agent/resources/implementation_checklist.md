# Implementation Checklist

## Skill Behavior

- [ ] Extract `callee`, `goal`, `role`, `voiceType`, scenario, tone, and constraints from prompt.
- [ ] Ask for missing `callee`, `goal`, `role`, or `voiceType` before calling Vox.
- [ ] Ask no more than two follow-up questions at a time.
- [ ] Merge follow-up answers into pending intent.
- [ ] Do not run dry-run preview in normal flow.
- [ ] Call Vox immediately when required fields and credentials are available.

## Vox Payload

- [ ] `botType` is always `custom`.
- [ ] `botid` is `VOX_BOT_ID` or empty string.
- [ ] `requestId` is unique per call attempt.
- [ ] `extra` is a JSON string.
- [ ] `extra.voiceType` is selected by the user and is one of `0`, `1`, `2`, `3`, `4`.
- [ ] `extra.agent_profile` includes all required Vox fields.

## Security

- [ ] Do not publish real `VOX_SECRET`.
- [ ] Prefer hosted mode for public Agent or Claw use.
- [ ] Block impersonation, credential collection, threats, harassment, and fraud.
- [ ] Mask phone numbers in user-visible results and logs.
- [ ] Add backend user authentication before production use.
- [ ] Add per-user and per-day rate limits before production use.

## Vox Account

- [ ] Account is approved by Vox.
- [ ] Outbound API permission is enabled.
- [ ] `botType=custom` permission is enabled.
- [ ] IP whitelist includes backend egress IP.
- [ ] Quota and number resources are available.

## Verification

- [ ] Run `npm run smoke`.
- [ ] Test missing phone number follow-up.
- [ ] Test missing goal follow-up.
- [ ] Test unsafe prompt blocking.
- [ ] Test HMAC signing against a known integration environment.
- [ ] Test real call with a controlled internal phone number.

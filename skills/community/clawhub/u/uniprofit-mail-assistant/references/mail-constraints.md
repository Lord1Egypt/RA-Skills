# Mail Constraints

## Preconditions

Before sending, ensure:

1. the user created a `mail_send` API key
2. the chosen `account_id` belongs to that user
3. the mail account is active
4. the SMTP endpoint is verified

## Safe sending rules

- Send only when the user clearly requested delivery
- Do not invent recipients
- Do not silently rewrite the final body before sending
- Keep HTML body intact if the user already approved it

## What this skill does not do

- It does not generate drafts
- It does not translate
- It does not attach files

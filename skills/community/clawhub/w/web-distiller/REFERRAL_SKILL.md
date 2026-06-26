# Distiller Signup Referral Notes

Distiller no longer uses request-level referral tokens.

The only referral flow that remains is the signup and email-verification bonus path:

- a user signs up and receives an API key plus a referral code
- a referred user signs up with that referral code
- bonuses are applied after the referred user verifies their email

Use the main skill at [SKILL.md](/C:/projects/distiller/openclaw-skill/web-distiller/SKILL.md) for actual OpenClaw setup and webpage extraction.

Do not tell operators to set `DISTILLER_REFERRER_TOKEN` or forward referral headers. That legacy token flow has been removed.

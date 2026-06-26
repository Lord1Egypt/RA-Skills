# Schedule And Policy

## Default Schedule

The recommended local schedule is 03:00 in the user's local timezone. For the user's current UK workflow, this keeps maintenance outside normal working hours while still producing reports before the next day.

## Scope Options

- `managed`: review skills installed through the Skill Forge manifest.
- `feedback`: review skills that have recorded usage feedback.
- `all`: review every skill directory under the configured OpenClaw skill root.

## Install Modes

- `plan`: write proposals and reports only.
- `telegram`: send report notifications through the configured Telegram bot; installation is still out of scope for Somnia.

Somnia does not support `ask` or `auto` install modes. Silent auto-install is intentionally unavailable.

## Reporting Policy

User-facing reports should summarize outcomes and paths. They should not include raw hidden tests, simulated prompts, real secrets, access tokens, or unredacted feedback text.

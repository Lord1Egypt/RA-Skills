# Local Release Checklist

Use this checklist right before generating the final `clawhub publish` command.

## Public-Facing Copy

- `description` exists and includes `Use when ...`
- skill name and slug are literal and stable
- first-screen content is understandable quickly
- no obvious TODO placeholders remain

## Sanitization

- no personal file paths such as `/Users/<name>/...`
- no Windows user-profile paths such as `C:\Users\<name>\...`
- no internal account names, machine names, or local-only references in public docs
- audience language is intentional and consistent

## Release Inputs

- display name chosen
- slug chosen
- version chosen
- changelog drafted
- tags reviewed

## Confidence

- local checker has run
- any warning is understood
- publish command has been reviewed before execution

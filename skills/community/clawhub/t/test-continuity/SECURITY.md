# Security

## Scope

This package handles user continuity state. Treat all live state as sensitive.

## Do not publish

- real session transcripts
- real daily memory content
- real user IDs or chat IDs
- live `profile.json`, `user_model.json`, `emotion_state.json`, `hooks.json`, `incidents.json`
- gateway tokens, auth profiles, provider keys

## Safe publishing pattern

- publish only code, docs, schemas, and sanitized examples
- use sandbox data for harness examples
- keep live OpenClaw state outside the public repo

## Reporting

If a bug risks leaking live state or internal sentinel text to frontstage, treat it as a release blocker for the package.

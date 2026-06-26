# Onboarding Boundary

Use this reference when deciding what the bot should ask the user to do.

## Product boundary

- Sonos official iOS / Android app is the default path for adding and logging in to a music service.
- ZoneFoundry is the readiness and execution layer.
- A local always-on node in the same LAN is the real gate for local bot control.

## Do

- auto-run local preflight when Sonos is mentioned for the first time
- ask for one default room if needed
- explain clearly when the user only has a phone

## Do not

- pretend ZoneFoundry replaces the Sonos official app for service add/login
- promise persistent bot control with only a phone
- expose internal CLI names to end users unless the user is explicitly technical

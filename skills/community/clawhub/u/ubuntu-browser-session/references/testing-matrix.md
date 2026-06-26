# Testing Matrix

## Should Trigger

- "Open GitHub settings on the Ubuntu host and reuse the existing login."
- "Use the server browser and continue with the Google account."
- "This protected site is asking me to sign in again. Recover it."
- "The server browser is open somewhere else. Go back to the right page."
- "Use the `work` session-key for this site."

## Should Not Trigger

- "Search the web for the latest Ubuntu release notes."
- "Fetch this public JSON API and summarize it."
- "Open this site in my local desktop browser."
- "Help me write a curl command for this endpoint."

## Critical Behaviors

- Default site identity reuse:
  - GitHub default session opens GitHub without user help
  - Google default session opens Google without user help

- Wrong-page recovery:
  - browser is logged in but currently on another site
  - wrapper should try to navigate back before asking for noVNC help

- Explicit secondary identity:
  - non-default `session-key` must only activate when explicitly requested
  - agent must not guess between multiple identities automatically

- Manual takeover:
  - output includes both loopback and LAN noVNC URLs when possible
  - capture updates site registry for later reuse

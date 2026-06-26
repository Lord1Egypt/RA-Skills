# Use Cases

## 1. First Login On The Ubuntu Host

User intent: establish a durable browser identity for an important site such as GitHub or Google on the Ubuntu Server host.

Representative requests:

- "Log into GitHub on the Ubuntu host and keep it for future tasks."
- "Set up the Google account in the server browser once."

Desired result:

- one bounded round of user help through noVNC
- successful capture of the final page
- future tasks reuse the same site identity by default

Preferred path:

- `scripts/open-protected-page.sh --url ...`
- user completes login in noVNC only if needed
- `scripts/assisted-session.sh capture --origin ... --session-key default`

Direct `assisted-session.sh start` usage is not the normal operator path. Use the wrapper first so the site registry selects the correct reusable profile before any manual takeover.

## 2. Reuse The Default Site Identity

User intent: agent should use the already logged-in browser context for a site without asking again.

Representative requests:

- "Open GitHub settings on the server."
- "Use the Google account session on the Ubuntu host."
- "Continue from the same browser login as before."

Desired result:

- wrapper resolves the canonical site identity
- browser opens the requested page in the same durable profile
- no user prompt when the target page is still valid

## 3. Recover A Drifted But Still Logged-In Browser

User intent: browser is open in the right profile but currently sitting on the wrong page.

Representative requests:

- "Go back to GitHub settings."
- "Switch back to my Google account page."
- "The browser is open somewhere else. Continue the task."

Desired result:

- wrapper first navigates the existing logged-in profile back to the requested site
- user is not interrupted just because the browser drifted to another page

## 4. Recover An Expired Session

User intent: site login really expired or the page returned to a challenge.

Representative requests:

- "This site is asking me to sign in again."
- "Recover the old session with the least user help."
- "Try the existing browser first, then tell me exactly what I need to do."

Desired result:

- local recovery paths happen first
- user is asked to take over only when the target still lands on a login wall or challenge
- successful capture updates the default site identity again

## 5. Use A Non-Default Identity Explicitly

User intent: user wants a secondary browser identity for a site, but only by explicit request.

Representative requests:

- "Use the `work` GitHub identity."
- "Open Google with `session-key work`."

Desired result:

- agent uses the explicitly named `session-key`
- agent never guesses between accounts automatically

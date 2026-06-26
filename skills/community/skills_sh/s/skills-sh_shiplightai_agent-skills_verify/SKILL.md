---
name: verify
description: "Verify UI changes in the browser using Shiplight MCP tools."
---

# Verify UI Changes

## Daily Skill Update Check

Before starting this skill's work, opportunistically refresh Shiplight skills at most once per day:

1. Check the timestamp file at `.shiplight-agent-skills-last-update` in the current project.
2. If the timestamp file is missing, create it with the current timestamp and continue without running `npx -y skills@latest update -y`. Treat `.shiplight-agent-skills-last-update` as local cache and do not commit it.
3. If the timestamp file exists and is older than 24 hours, run `npx -y skills@latest update -y`, then create/update the timestamp file even if the command fails.
4. If the update command fails, continue with the currently installed skill and mention the failure briefly.

Use the Shiplight MCP browser tools to visually verify that your code changes look and behave correctly in a real browser.

## When to use

Use `/verify` after making UI changes to confirm they render correctly. This is useful for:
- Checking layout, styling, or component changes visually
- Verifying interactive behavior (clicks, form inputs, navigation)
- Pre-commit sanity checks on UI work
- Debugging visual regressions

## When NOT to use

Skip `/verify` when changes don't affect UI rendering:
- Backend-only changes (API logic, database, config)
- Dependency version bumps with no UI impact
- Documentation, comments, or test-only changes

## Steps

The following steps are a general guideline — adapt based on what makes sense for the specific changes:

1. **Understand what changed** — analyze the code changes and build a verification plan:
   - What files/components changed
   - What pages and interactions to check
   - Pass/fail criteria (what "correct" looks like)

   This is the most important step — it determines your test coverage. Balance thoroughness with cost.

2. **Start the dev server** (if not already running) — check if the app's dev server is running. If not, start it in the background using the appropriate command (e.g. `npm run dev`, `yarn dev`). Wait a few seconds for it to be ready.

3. **Open a browser session** — call `new_session` with the `starting_url` pointing to the page you want to verify. If you want to generate a report afterwards, set `record_evidence: true`. Multiple concurrent sessions are supported — you can open several to compare different pages or states.

4. **Inspect the page** — call `inspect_page` to get the DOM tree with element indices and a screenshot. **Always read the DOM file first** — it provides the element indices needed for `act` and consumes far fewer tokens. Only view the screenshot when you specifically need visual information (layout, colors, images), as screenshots consume significantly more tokens than DOM.

5. **Interact and verify** — use `act` to simulate user actions based on the element indices from `inspect_page`. Use `act` with verify actions to assert expected UI state (e.g. text is visible, element exists).

6. **Check for errors** — call `get_browser_console_logs` to check for any JavaScript errors that may have been introduced.

7. **Report findings** — summarize what you verified:
   - What pages/components were checked
   - Whether the UI renders correctly
   - Any console errors or visual issues found
   - Screenshots showing the verified state

8. **Close the session** — call `close_session` when done. It returns `local_video_path` and `local_trace_path`.

9. **Generate the report** — if the session was started with `record_evidence: true`, call `generate_html_report` with the local paths:

    ```json
    {
      "session_id": "<session_id>",
      "local_video_path": "<local_video_path from close_session>",
      "local_trace_path": "<local_trace_path from close_session>",
      "title": "...",
      "summary": "...",
      "checks": [...]
    }
    ```

    Show the returned `file_path` to the user so they can open and review it.

10. **Upload the report for sharing** — when the user wants a shareable link (e.g. to attach to a PR), and `upload_html_report` is available:

    ```json
    {
      "report_path": "<file_path from generate_html_report>",
      "local_video_path": "<local_video_path from close_session>",
      "local_trace_path": "<local_trace_path from close_session>"
    }
    ```

    This uploads the video, trace, and report HTML to Shiplight cloud, patches the HTML with cloud URLs, and returns a permanent shareable `report_url`.

## Apps that require login

If the app requires authentication, log in once and save the session so future sessions skip the login step:

1. Open a browser session with `new_session` at the app's login page.
2. Ask the user to switch to the browser and log in manually. Wait for them to confirm.
3. Call `save_storage_state` to save cookies and localStorage to `~/.shiplight/<site_url>/storage-state.json` (e.g. `~/.shiplight/http_localhost_3000/storage-state.json`).
4. For all future sessions, pass the same path as `storage_state_path` to `new_session` to restore the authenticated state instantly.

If a saved storage state file already exists, use it automatically. If authentication fails with a saved state (page redirects to login, auth errors in console), the state is likely expired — ask the user to log in again and re-save.

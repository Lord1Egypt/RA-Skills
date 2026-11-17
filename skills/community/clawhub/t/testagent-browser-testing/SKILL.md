---
name: testagent-browser-testing
version: 1.4.0
description: Functional testing of web products using Playwright MCP, browser-use CLI, and the openclaw built-in browser, following a full testing SOP — planning, execution, bug logging with screenshots, and finally producing a report and filing it in Coding. Triggered when the user says "go test", "test this", "help me test", "QA" a given URL or feature.
---

# Browser Testing

## ⚠️ Ground rules (must be confirmed before every test — do not skip)

**1. Screenshots must use Playwright MCP — never the built-in browser's screenshot**
The built-in browser's `browser screenshot` only returns AI analysis text; `MEDIA:` can't render it, so the user won't see the image.
The only correct way to take a screenshot: `playwright__browser_take_screenshot` → save to a file → `MEDIA:<path>`

**2. Before using the built-in browser, check the ssrfPolicy allowlist first**
The target domain and the login domain (Auth0, etc.) must be in `allowedHostnames` in `~/.openclaw/openclaw.json`, or navigation will fail with `blocked by policy`.
After changing the config, you must run the full restart sequence: `browser stop` → `gateway restart` → wait 15 seconds → `browser start`

**3. For font/environment issues, first check whether browser-setup has been run — don't troubleshoot manually**
For environment issues like mojibake in Chinese text or browser startup timeouts, first run `bash testagent-browser-setup/scripts/setup.sh` rather than manually installing fonts or debugging step by step.

---

## Testing SOP

### Phase 1: Gather startup info

After receiving a testing request, only ask for information that can't be obtained on your own before logging in:

1. **Target URL** (if not provided by the user)
2. **Test account and password** (for login)
3. **Test goal description** (e.g. "test the create-team feature")

Don't ask about product details (field formats, required fields, secondary accounts, etc.) before you've seen the product — those you can check yourself after logging in.

### Phase 2: Explore the product and draft a test plan (requires user confirmation)

1. Pick the primary tool per [REFERENCE.md tool selection](REFERENCE.md#tool-selection)
2. **If using the built-in browser**, before navigating, confirm that `browser.ssrfPolicy.allowedHostnames` in `~/.openclaw/openclaw.json` already includes the target domain and login domain; if not, add them and run the full restart sequence first (see [REFERENCE.md pitfalls](REFERENCE.md#pitfalls)), then navigate
3. Navigate to the target URL and log in automatically
4. **Viewport check (mandatory, use your own judgment)**: take a screenshot with Playwright MCP and judge for yourself whether the page is suitable for testing:
   - If content looks cramped, elements overlap, buttons are obscured, or the sidebar is crowding the main content area → run `playwright__browser_resize → width=1440, height=900`, then screenshot again to confirm
   - If the page looks fine → proceed directly
   - No need to ask the user — decide on your own whether to adjust
5. Browse the target feature area to understand the actual page structure and interactions
6. **Based on the real page**, produce 3-5 test points, and **wait for the user to confirm or revise them before starting execution**

```
(after logging in and viewing the product) I plan to test the following scenarios — let me know if this works:
1. Create team — fill in the name and required fields, verify creation succeeds
2. Form validation — check whether empty required fields show a prompt
3. Send a message within the team — verify the message displays correctly
4. Boundary input — behavior when the team name is excessively long
```

**Only ask the user for additional info at this stage if exploration reveals it's genuinely needed** (e.g. a test scenario requires a second account, or specific test data).

### Phase 3: Execute the tests (fully autonomous, don't interrupt the user)

- Execute each test point one by one
- **Screenshot a bug the moment it's found** — don't save it for the end (page state can change at any time)
- Screenshot naming: `/root/.openclaw/workspace/bug_<number>_<short description>.png`
- If the same action fails 2-3 times, switch tools or strategy immediately (see [REFERENCE.md pitfalls](REFERENCE.md#pitfalls))

### Phase 4: Produce the test report

Once all test points are complete, output the full report in chat (format in [REFERENCE.md report format](REFERENCE.md#report-format)).

### Phase 5: Confirm filing into Coding (requires user confirmation)

After the report, ask:

```
Should these N bugs be filed into Coding?
You can adjust the suggested priority, assignee, or timeline, then reply "file it", or specify a change to a particular one.
```

Once the user confirms, call the **coding-net skill**'s `create_issue` to bulk-file the bugs:
- `issue_type="DEFECT"`
- `priority`: per the priority rules (see [REFERENCE.md](REFERENCE.md#priority-rules))
- `due_date`: today's date + the suggested fix timeline (in days)
- `assignee_id`: look up the member ID per the assignment rules in AGENTS.md (using `get_team_members_id_and_name` or `extract_members_from_issue_list`)

Once filed, output the Coding issue number for each bug.

---

For detailed tool comparisons, screenshot workflow, and report templates, see [REFERENCE.md](REFERENCE.md)

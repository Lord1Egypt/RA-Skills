# Changelog

## 1.0.3 — local draft, not published

- Add **Browser Resource Budget / Tab Hygiene** guidance:
  - use cheaper tools before visible browser automation;
  - treat existing user tabs as user state, not agent-owned resources;
  - distinguish user tabs, user-requested tabs, agent task tabs, archived tabs, and critical/manual tabs;
  - estimate memory and CDP complexity before non-trivial browser work;
  - stop on high target counts, iframe/worker bursts, reCAPTCHA bursts, stale target/context-destroyed loops, or repeated timeouts;
  - avoid tab fan-out; use one list tab and one reusable detail tab;
  - persist URLs/data into project files instead of using open tabs as task memory;
  - archive tabs before cleanup and close only agent-owned or user-approved archived tabs.
- Add read-only helper `scripts/browser-budget-check.sh`:
  - reads CDP `/json/list`;
  - groups targets by type/domain;
  - flags reCAPTCHA and high iframe/worker pressure;
  - reports Linux memory and Windows Edge memory when available;
  - prints `OK / CAUTION / STOP`;
  - does not close tabs or change browser/system state.
- Fix `scripts/check-win11-visible-browser.sh` section breaks: replace literal `echo "\n..."` with `printf`.
- Keep prior safety mitigations intact: dedicated profile preference, approval for personal profiles and state-changing actions, firewall scoping to WSL/Hyper-V CIDR, and Scheduled Task rollback documentation.

## 1.0.1 — planned fixes from live testing

Test date: 2026-05-12, environment: OpenClaw 2026.5.7 in WSL2 on Windows 11, visible Microsoft Edge via `win-edge` CDP profile.

### Fixes

- Include ClawScan review recommendations as explicit 1.0.1 risk mitigations:
  - prefer a dedicated browser profile by default;
  - require explicit approval before using a personal/logged-in browser profile;
  - require clear action/risk/rollback before browser/account/payment/form/firewall/config changes;
  - verify Windows firewall scope is limited to WSL/Hyper-V CIDR and never expose CDP to LAN/Internet;
  - create persistent Scheduled Tasks only after explicit approval and document `Unregister-ScheduledTask` rollback.
- Make `scripts/check-win11-visible-browser.sh` executable in the published package, or document invocation via `bash {baseDir}/scripts/check-win11-visible-browser.sh win-edge` everywhere.
  - Current installed permissions were `-rw-r--r--`, so direct execution from `SKILL.md` failed with `Permission denied`.
- Replace `echo "\n..."` in `scripts/check-win11-visible-browser.sh` with `printf` so section breaks render correctly instead of literal `\n`.
- Document firewall rule name drift:
  - repair script expects `OpenClaw Browser CDP relay 9223 from WSL`;
  - existing setups may use names such as `OpenClaw Edge CDP relay 9223 from WSL`;
  - running repair with a different name may leave duplicate allow rules.
- Add troubleshooting note for browser action errors like `action targetId must match request targetId`:
  - after `tabs`, prefer the real CDP `targetId` for follow-up `act` calls when tab aliases such as `t2` fail.

### Fixed after ClawScan v1.0.1 scan

- Fix `_meta.json` version mismatch flagged by ASI04: bundled file now reads `1.0.2` to match the registry.

### Added from live testing

- Efficient data extraction pattern:
  - Prefer a single `act kind=evaluate` returning JSON/strings over multiple `snapshot` calls when extracting structured data (prices, specs, search results).
  - One evaluate costs ~a few tokens; one snapshot can cost thousands.
  - Recommended flow: snapshot once to understand layout → evaluate to extract data in bulk.
  - For lazy-loaded content, scroll into view before extraction.
  - Extract all visible results in one pass: title, price, seller, link, delivery.
- Site-specific notes:
  - Ozon, Wildberries, and М.Видео may trigger antibot challenges on automated fetch/web_fetch but work via the visible CDP-attached browser.
  - Яндекс Маркет generally works with both web_fetch and the visible browser.

### Future: visual result presentation (post-backlog)

- **Open result tabs in the visible browser** — instead of or in addition to text, open relevant pages (product cards, articles, videos) in browser tabs the user can see and interact with.
- **Snapshot/screenshot capture** — take a page screenshot and deliver it to the chat so the user can see what the agent found without switching context.
- **Multi-tab orchestration** — open several search results simultaneously, label them, and let the user visually browse while the agent reports key findings.
- **Article/video mode** — for step-by-step guides or video tutorials: open the tab, snapshot the relevant section, and let the user take over for interactive parts.
- **Evidence collection** — when a specific answer matters (price, address, phone), open the exact page and screenshot the relevant block for the user to verify.

### Validation already passed

- `clawhub install win11-visible-browser --force` installed version `1.0.0`.
- PowerShell repair script parsed successfully with Windows PowerShell parser.
- `bash -n scripts/check-win11-visible-browser.sh` passed.
- `win-edge` CDP endpoint answered from WSL at `/json/version`.
- `openclaw browser --browser-profile win-edge doctor` returned OK.
- Browser CLI and browser tool could open `https://example.com`, snapshot it, and click through to IANA.

### Do not change without separate confirmation

The repair script changes Windows/host state: `C:\ProgramData\OpenClaw`, Edge process startup, `netsh portproxy`, and Windows firewall rules. Keep repair execution behind explicit confirmation.

### Additional live-work test findings

- Form interactions work in visible Edge via CDP:
  - text input with `act kind=type`;
  - radio buttons and checkboxes with `act kind=click`;
  - verification via `snapshot` shows entered values and checked states.
- Dropdown/select interaction works with `act kind=select` on a real page.
- JavaScript dialogs work with the browser `dialog` action:
  - alert accepted successfully;
  - prompt accepted with text, but the tested site's snapshot rendered only `You entered:` without the prompt value, so verify prompt result per-site.
- Screenshot works, but the first screenshot attempt timed out while CDP was still otherwise healthy; immediate retry with a longer timeout succeeded. Add troubleshooting note: for external CDP/visible browsers, retry screenshot once and/or allow a longer timeout before diagnosing CDP as broken.
- Reproduced tab alias issue consistently:
  - `snapshot` with `targetId: "t6"` succeeded;
  - `act` with the same alias failed: `action targetId must match request targetId`;
  - `act` with the real CDP target id succeeded.
  - Documentation should recommend using the returned real `targetId` for actions after snapshots when aliases fail.

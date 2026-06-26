---
name: se-browser-automation
description: "Browser automation patterns and best practices for OpenClaw browser control. Use when navigating web apps, filling forms, clicking elements, or extracting data from websites. Covers GHL, Lovable, and general SPA navigation patterns."
version: 1.0.0
---

# Browser Automation Skill

## Profile
- Use profile: `openclaw` for all automated browsing
- Browser is managed by OpenClaw gateway

## Core Patterns

### Navigation
- Use `browser navigate` with direct URLs when possible (faster than clicking through menus)
- Always `sleep 4-6` after navigation — SPAs load content asynchronously
- If page seems blank, try `screenshot` first — content may be rendered but not in DOM snapshot

### Element Interaction
- Use `snapshot` to get element refs, then `act` with refs
- For iframe content: use `frame` parameter in snapshot
- If compact snapshot misses content, try full snapshot or screenshot
- GHL and complex SPAs often render in iframes — check both main page and iframe

### Screenshots vs Snapshots
- **Snapshot** — DOM tree, good for finding clickable refs
- **Screenshot** — Visual image, good for understanding what's actually on screen
- When snapshot shows empty/minimal content but screenshot shows a full page → content is in iframe or shadow DOM

### Login Flows
1. Navigate to login page
2. Snapshot to find form fields
3. Click + type credentials
4. Handle 2FA (check email, enter code)
5. Wait for redirect (sleep 4-6 seconds)
6. Verify logged in via screenshot

### Common Issues
- **Popups/modals blocking** → Press Escape
- **Lazy-loaded content** → Wait longer, refresh, or navigate directly via URL
- **iframe content** → Use frame parameter or evaluate JS to find iframe
- **evaluate function errors** → No `const`, `let`, or arrow functions. Use `var` and `function(){}` syntax.
- **ref required errors** → Must use ref from snapshot, can't use text selectors

### SPA-Specific Tips
- SPAs don't fully reload on navigation — URL changes but DOM updates incrementally
- Some content only appears after JavaScript execution
- If clicking a link doesn't work, try navigating directly to the URL
- F5 refresh can help when SPA state gets stuck

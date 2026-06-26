---
title: Troubleshooting
impact: HIGH
tags: debug, timeout, element-not-found, network, headed-mode
---

# Troubleshooting

## Timeout / Assertion Too Early

AI-driven tests are slower than selector-based tests. Default timeout is 180s per test. Most timeout and premature assertion failures are caused by not waiting for the page/app to be ready.

Include waiting in the `aiAct` prompt itself, so Midscene waits for the page/app to be ready before asserting:

```typescript
// Incorrect — assertion fires before page updates
await ctx.agent.aiAct('click the submit button');
await ctx.agent.aiAct('verify the page shows "Submission successful"');

// Correct — include wait in the action prompt
await ctx.agent.aiAct('click the submit button and wait until the submission completes');
await ctx.agent.aiAct('verify the page shows "Submission successful"');
```

---

## Element Not Found / Wrong Element

Vague or ambiguous descriptions cause AI to match the wrong element or fail entirely.

```typescript
// Incorrect — too vague, multiple buttons may exist
await ctx.agent.aiAct('click the button');
await ctx.agent.aiAct('click the delete button');

// Correct — include position, context, or visual traits
await ctx.agent.aiAct('click the blue "Submit" button at the top of the page');
await ctx.agent.aiAct('click the delete button in the first product row');
```

Tips for precise descriptions:
- Include **position**: top / bottom / first row / left side
- Include **text content**: "Submit" / "Confirm" / "Delete"
- Include **visual traits**: blue / large / with icon

---

## Device Connection

**Android** — ensure a device is connected and ADB is configured:

```bash
adb devices  # Should list your device
```

If using a remote device, set `MIDSCENE_ADB_REMOTE_HOST` and `MIDSCENE_ADB_REMOTE_PORT` in `.env`.

**iOS** — ensure WebDriverAgent is running on the target device/simulator:

```bash
curl http://localhost:8100/status
```

Override the port via `IOSTest.setup(uri, { deviceOptions: { wdaPort: 8100 } })`.

---

## Debugging Tips

- **Headed mode (Web)**: Use `WebTest.setup(url, { headless: false })` to see the browser during test execution
- **Midscene report**: Check the generated report for screenshots and AI decision traces

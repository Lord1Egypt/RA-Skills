---
name: psd-automator-screenshot
description: "Use screenshot + natural language instruction to locate PSD text layers and dispatch automated edits with confidence gating. Requires psd-automator core."
metadata:
  openclaw:
    userInvocable: true
    commandDispatch: tool
    commandTool: psd_automator_screenshot
    commandArgMode: raw
---

# psd-automator-screenshot

This skill dispatches screenshot-driven PSD text updates while keeping the existing psd-automator execution pipeline.

## Preferred command

Use the built-in command first:

```text
/main-image-editor <agentId> <中文需求> --screenshot ~/Desktop/修改3.png
```

Use `/psd-automator-screenshot` only when you need backward-compatible command behavior.

## Usage

```text
/psd-automator-screenshot <agentId> <截图改字指令>
```

Example:

```text
/psd-automator-screenshot design-mac-01 找到banner.psd或banner.psb，将红框区域替换成"限时199元"，保持字体和字号不变
```

## Notes

- High confidence requests are auto-dispatched.
- Medium confidence requests return top candidates for confirmation.
- Every invocation/execution is recorded to skills-usage.json.

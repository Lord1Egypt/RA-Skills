---
name: psd-automator-skill-command
description: "Dispatch PSD automation tasks through skill command entry while reusing the same /psd orchestrator. Requires psd-automator core."
metadata:
  openclaw:
    userInvocable: true
    commandDispatch: tool
    commandTool: psd_automator_skill_command
    commandArgMode: raw
---

# psd-automator-skill-command

This skill command provides a skill-entry equivalent of `/psd` without changing existing `/psd` behavior.

## Usage

```text
/psd-automator-skill-command <agentId> <taskJsonPath|中文需求> [--dry-run] [--index <indexPath>]
```

Example:

```text
/psd-automator-skill-command design-mac-01 帮我找到20260302工位名牌.psd，把姓名改成小一，并保存成png放到桌面
```

## Notes

- This command reuses the same PSD orchestration pipeline as `/psd`.
- It keeps DINGTALK image marker behavior consistent with existing PSD workflow.
- It contributes to the same skills usage statistics store with `entrypoint=skill_command`.

# Pattern 2.5: Component-Scoped Hooks

## 问题

全局 hooks 对所有 session 生效。某些验证逻辑只在特定类型的任务中需要。

## 原理

Claude Code 支持在 SKILL.md 或 agent 定义的 frontmatter 中声明 hooks，这些 hooks 只在该组件被激活时生效。Stop hook 在 subagent frontmatter 中会自动转换为 SubagentStop。

## 示例

```yaml
---
name: security-fix
hooks:
  Stop:
    - type: agent
      agent: "验证安全修复：1) 检查修改的文件无新增漏洞 2) 确认敏感数据已清理 3) 验证权限配置正确。"
---
```

## 配合 `once: true`

`once: true` 让 hook 只在 session 中触发一次后自动停用。适合初始化任务：

```json
{
  "type": "command",
  "command": "bash /path/to/your-init-hook.sh",
  "once": true
}
```

用途：在 session 开始时执行一次性初始化（如注入最新的 handoff 文档），之后自动停用。

## 用途

- 高价值任务（安全修复、生产热修）自带验证门禁
- 不污染全局 hooks 配置
- Skill 级别的质量保证——每个 skill 可以定义自己的验证标准

## 与全局 hooks 的优先级

全局 hooks（settings.json）和组件 hooks（frontmatter）都会执行。执行顺序：全局先，组件后。如果全局 hook 已经 block 了 stop，组件 hook 不会再触发。

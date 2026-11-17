# 示例：Plugin scope 与 owner 冲突

## 输入

- 目录：`plugins/release-bot/`
- `package.json` name：`@openclaw/release-bot`
- 目标 owner：`bonniegeng-max`

## auto 选择

对象是 Plugin 且 package scope 与 owner 涉及发布身份，auto 直接选择 deep。

## 证据

| 层级 | 状态 | 证据 |
|---|---|---|
| package 身份 | 冲突 | scope 为 `@openclaw` |
| 发布身份 | 已知 | owner 为 `bonniegeng-max` |
| validation/dry-run | 未验证 | 尚未执行 |

## 结论

- 实际模式：deep
- 发布结论：先别发
- P0：package scope 与 owner 不匹配，归属与发布权限不可确认
- 置信度：高

## 最小修复路径

确认真实发布主体后，二选一：使用与 `@openclaw` 对应的 owner；或将包名改为发布者有权使用的 scope。随后执行：

```bash
clawhub package validate plugins/release-bot
clawhub package publish plugins/release-bot --dry-run
```

这些命令是建议执行，不代表已验证。Plugin 不得套用 Skill 的 `--slug` / `--name` 参数。

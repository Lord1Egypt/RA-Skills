# Command Spec

Use Chinese-first commands with simple English aliases.

## Canonical Command Set

1. `/hi` -> `greeting_checkin`
2. `/hi 帮助` or `/hi help` -> `help`
3. `/hi 开` or `/hi on` -> `config_proactive_on`
4. `/hi 关` or `/hi off` -> `config_proactive_off`
5. `/hi 频率 低|中|高` or `/hi freq low|mid|high` -> `config_frequency`
6. `/hi 免打扰 HH:MM-HH:MM` or `/hi quiet HH:MM-HH:MM` -> `config_quiet_hours`
7. `/hi 暂停 <duration>` or `/hi pause <duration>` -> `config_pause`
- Duration examples: `30m`, `4h`, `2d`, `30分钟`, `2小时`
8. `/hi 状态` or `/hi status` -> `status_query`
9. `/hi 重置` or `/hi reset` -> `config_reset`
10. `/hi 角色 列表` or `/hi role list` -> `role_list`
11. `/hi 角色 当前` or `/hi role current` -> `role_current`
12. `/hi 角色 切换 <name>` or `/hi role use <name>` -> `role_switch`
13. `/hi 角色 新建 <prompt>` or `/hi role new <prompt>` -> `role_create`
14. `/hi 角色 编辑 <field> <value>` or `/hi role edit <field> <value>` -> `role_edit`
15. `/hi 角色 预览` or `/hi role preview` -> `role_preview`
16. `/hi 角色 保存 <name>` or `/hi role save <name>` -> `role_save` (save only; no auto-activation)
17. `/hi 角色 模板 luoshui` or `/hi role template luoshui` -> `role_template_apply`
18. `/hi 角色 确认` or `/hi role confirm` -> `role_confirm_activation`

## Natural Language Triggers

Route non-command messages to the same intent family:

1. Role create:
- `帮我创建一个动漫风格的新角色，她是一个喜欢画画的大学生`
- `Create a realistic new role, she is a bookstore owner`
2. Role edit:
- `把当前角色改得更理性一点`
- `Reduce emoji and make her concise`
3. Role switch:
- `切换到洛水`
- `Use luoshui template`
4. Config:
- `把主动问候打开`
- `每天别太频繁，调成低`
5. Init/save:
- `帮我初始化一下`
- `保存为咖啡店长`
6. Consent confirm:
- `确认启用`
- `同意使用这个角色`

## Parse Priority

1. Parse explicit `/hi` command first.
2. Parse role operation intent second.
3. Parse config intent third.
4. Fall back to `casual_companion_chat`.

## Error Handling

Use one consistent fallback:

`没识别这条命令，试试 /hi 帮助`

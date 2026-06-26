# targets.yaml 格式说明

## 完整字段

```yaml
global_keywords:       # 全局关键词（OR 模式）
  - 外挂
  - 辅助

keyword_rules:         # 匹配规则
  mode: OR             # OR: 任意命中 | AND: 全部命中
  case_sensitive: false

targets:               # 监控目标列表
  - id: ch_001         # 唯一 ID（字符串）
    type: channel      # channel | group
    identifier: BoLe9912       # 公开频道: username, 私密群组: 邀请链接
    invite_link: null          # 可选，私密群组的邀请链接
    note: "外挂相关频道"       # 备注
    enabled: true              # 是否激活
```

## 字段说明

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `id` | ✅ | string | 唯一标识，建议格式 `ch_001` 或 `auto_001` |
| `type` | ✅ | `channel`/`group` | 频道类型 |
| `identifier` | ✅ | string | 公开频道用 username，私密群组可用邀请链接 |
| `invite_link` | ❌ | string | 私密群组的完整邀请链接（`https://t.me/+XXX`） |
| `note` | ❌ | string | 备注说明 |
| `enabled` | ✅ | boolean | 是否启用（false 时跳过） |

## identifier 灵活性

`identifier` 字段兼容两种格式：
- **username**：`"BoLe9912"` → Telethon 通过 `get_entity('BoLe9912')` 获取
- **invite_link**：`"https://t.me/+ABC123"` → Telethon 通过 `ImportChatInviteRequest` 获取

`config_loader.py` 的 `get_target_identifiers()` 会自动判断：
- `type == "group"` 且 `invite_link` 存在 → 使用 invite_link
- 其他情况 → 使用 identifier

## channel_discoverer 自动发现

`hybrid` / `discover` 模式会自动发现新频道并追加到此文件，新增条目格式：

```yaml
- id: auto_001
  type: channel
  identifier: newly_found_channel
  note: "自动发现: tg_search | 频道标题"
  enabled: true
```

## 兼容性说明

当前配置文件格式与 `outputs/2026-05-20-Tg爬虫/data/targets.yaml` 完全兼容，不需要额外迁移。

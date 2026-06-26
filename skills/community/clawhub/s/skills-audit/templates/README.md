# 通知模板说明

## 模板文件

- `notify.txt` — 变更通知的骨架模板

## 占位符

| 占位符 | 说明 |
|--------|------|
| `{sections}` | 变更分组内容（新增/变更/删除），由脚本动态生成 |
| `{skills_dir}` | skills 目录路径 |
| `{timestamp}` | 检测时间（格式 YYYY-MM-DD HH:MM:SS） |
| `{timezone}` | 时区（如 Asia/Shanghai） |
| `{logs_path}` | 审计日志路径 |
| `{snapshots_dir}` | git 快照仓库路径 |

## 变更分组格式

### 每个分组标题

```
【新增】 / 【变更】 / 【删除】
```

### 每个 skill 一行

```
• <slug>｜风险等级：<risk_label>
```

### 变更详情（文件级，仅【变更】分组）

```
  ↳ 变更文件：file1, file2
  ↳ 新增文件：file3
  ↳ 删除文件：file4
```

## 分层展示规则

| 变更文件数 | 展示策略 |
|-----------|---------|
| ≤ 5 | 全部列出，每个带 +N -N |
| 6~20 | 前 3 个 + "另外 X 个省略" |
| > 20 | 前 3 个 + 省略 + ⚠️ 大规模变更警告 |

当变更 skill 数 > 8 时，高风险（high/extreme）展开详情，低风险压缩为一行列表。

## 风险等级图标

| 等级 | 图标 |
|------|------|
| low | 🟢 低 |
| medium | 🟢 中 |
| high | 🟡 高 |
| extreme | 🔴 极高 |
| unknown | ⚪ 未知 |

## 自定义

直接编辑 `notify.txt` 即可修改通知样式。`{sections}` 占位符的内容由
`skills_watch_and_notify.py` 按上述规则动态生成，不可在模板中自定义。

## 已审核 skill（baseline）

已通过 `skills_audit.py approve` 审核且未发生变更的 skill，不会出现在通知中。

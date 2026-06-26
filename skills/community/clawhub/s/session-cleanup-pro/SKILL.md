---
name: session-cleanup
description: Clean orphan .jsonl files and stale sessions in OpenClaw session storage with safe confirmation flow. 适用于会话列表杂乱、历史会话堆积、需要释放存储空间场景；默认保护 72 小时内会话，删除前必须用户确认。
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🧹", "requires": { "bins": ["bash", "node"] } }, "version": "0.3", "updatedAt": "2026-03-06 20:47 Asia/Shanghai" }
---

# Session Cleanup

清理 OpenClaw 会话目录中的孤儿文件与过期会话，优先安全、可审计。

## 使用方式

先扫描，再确认，再执行：

1. 扫描（只读）
2. 生成清理计划
3. 用户确认
4. 执行清理并回报结果

## 关键文件

- 扫描脚本：`scripts/scan_sessions.sh`
- 清理策略：`references/policy.md`

## 扫描命令（必做）

```bash
./skills/session-cleanup/scripts/scan_sessions.sh scan
```

返回 JSON 包含：
- `orphanFiles`：磁盘存在但 `sessions.json` 未登记的 `.jsonl`
- `staleSessions`：超过 72 小时且非受保护会话
- `protectedSessions`：当前会话 + 72 小时保护窗口内会话

## 执行规则

- 必须先扫描并展示摘要
- 必须询问用户确认后才清理
- 默认不删除受保护会话
- 永不删除 `agent:main:main`

## 清理建议

### A. 先处理孤儿文件（优先）

在用户确认后删除孤儿文件：

```bash
rm ~/.openclaw/agents/main/sessions/<orphan>.jsonl
```

### B. 再处理过期会话（谨慎）

仅在用户明确确认后执行，删除对应 `.jsonl`，并更新 `sessions.json` 去除条目。

## 输出模板

```markdown
🧹 会话清理扫描完成

- 注册会话：X
- 磁盘 jsonl：Y
- 孤儿文件：A
- 过期会话：B
- 受保护会话：C

预计可释放：N MB

是否按上述计划执行清理？
```

## 发布前自检

```bash
# 1) 脚本可执行
./skills/session-cleanup/scripts/scan_sessions.sh scan >/tmp/session-cleanup-report.json

# 2) 输出为有效 JSON
node -e "JSON.parse(require('fs').readFileSync('/tmp/session-cleanup-report.json','utf8')); console.log('OK')"
```

---
name: session-rename
description: "改会话名、rename session、会话标签、修改会话标题、session label"
metadata:
  openclaw:
    displayName: 会话名称修改
    tagline: 直接编辑 sessions.json 给会话加 label，修改 OpenClaw 会话显示名称
    slug: session-rename-zh
    homepage: https://github.com/fhekg/openclaw-session-rename
---

# 会话名称修改 (Session Rename)

通过直接编辑 `sessions.json` 给会话加 `label` 字段来修改显示名称。

OpenClaw 没有 CLI 或 RPC 方式修改会话标题，但 JSON store 可以直接编辑。

## 效果演示

![改名效果](assets/demo.png)

## 触发

用户说「改会话名」「把这个会话叫 XXX」「rename session」「设置会话标签」「修改会话标题」等。

## 工作流

1. 确认目标会话（当前会话 / 指定会话）和想要的名字
2. 如果是当前会话，用 `sessions_list` 拿到当前 session key
3. 用 python3 安全读取、修改、写回 `sessions.json`

## 改当前会话

```bash
python3 -c "
import json

path = '/Users/xingbin/.openclaw/agents/main/sessions/sessions.json'
with open(path, 'r') as f:
    data = json.load(f)

key = '<SESSION_KEY>'  # 从 sessions_list 获取
if key in data:
    data[key]['label'] = '<新名称>'
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'✅ 已设置 label: <新名称>')
"
```

4. 改完后用 `sessions_list` 验证 `displayName` 和 `derivedTitle` 已生效

## 改其他会话

- `sessions_list` 找到目标会话的 key
- 同上流程，替换 key 和 label 值

## 列出所有会话

```bash
python3 -c "
import json
data = json.load(open('/Users/xingbin/.openclaw/agents/main/sessions/sessions.json'))
for k, v in data.items():
    print(f'{k} → {v.get(\"label\", \"(无标签)\")}')
"
```

## 注意事项

- `sessions.json` 路径固定：`~/.openclaw/agents/main/sessions/sessions.json`
- 用 python3 操作 JSON，不要用 sed/shell 字符串拼接，避免破坏格式
- 安全操作：读取→修改→写回，不删不改其他字段
- 只添加 `label` 字段，不影响其他功能

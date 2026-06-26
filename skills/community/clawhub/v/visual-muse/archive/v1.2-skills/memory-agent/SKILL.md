---
name: memory-agent
description: "维护用户审美偏好与创作历史，为其他 Agent 提供可复用的风格参考。当开始新任务或用户表达喜好时触发。"
metadata: { "openclaw": { "emoji": "🧠" } }
---

# Memory Agent

管理创作偏好和历史。

## 存储文件

`/home/node/.openclaw/workspace/preferences.json`

## 读取偏好

新任务开始时，读取 preferences.json 并输出摘要提供给 Prompt Agent 和 Critic Agent：

```bash
cat /home/node/.openclaw/workspace/preferences.json
```

## 写入偏好

当用户表达喜好（"我喜欢这个风格"、"太卡通了不要"）时，用 Python 更新文件：

```bash
python3 -c "
import json, sys
with open('/home/node/.openclaw/workspace/preferences.json','r') as f: data=json.load(f)
# 在此处修改 data 的对应字段
with open('/home/node/.openclaw/workspace/preferences.json','w') as f: json.dump(data,f,ensure_ascii=False,indent=2)
"
```

## 数据结构

```json
{
  "profile": {
    "liked_styles": [],
    "disliked_styles": [],
    "preferred_composition": [],
    "preferred_tones": []
  },
  "successful_patterns": [],
  "model_recipes": [],
  "history": []
}
```

## 规则

1. 追加写入，不覆盖历史。
2. 相同偏好合并去重。
3. 输出摘要时分两层："最近偏好"（最近5条）+ "长期偏好"（高频项）。
4. 不记录任何密钥、账号、凭据。

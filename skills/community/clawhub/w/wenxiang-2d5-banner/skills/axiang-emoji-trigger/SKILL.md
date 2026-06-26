# axiang-emoji-trigger - 阿香表情触发技能

## 📖 技能说明

**功能：** 根据阿香回复的情绪，自动发送对应的表情图片

**用途：**
- 自动判断回复情绪
- 发送对应表情图片到飞书
- 增强对话的情感表达

---

## 🎯 使用方式

### 方式 1：在回复末尾添加情绪标记

**格式：**
```markdown
---
情绪：开心/兴奋 → happy 😆
😆
```

**技能会自动：**
1. 解析情绪标记
2. 选择对应文件夹的表情
3. 发送到飞书

---

### 方式 2：直接调用

```python
from skills.axiang_emoji_trigger import send_emoji

# 发送开心表情
send_emoji("happy")

# 发送害羞表情
send_emoji("shy")

# 发送傲娇表情
send_emoji("tsundere")
```

---

## 📋 情绪对照表

| 情绪关键词 | 文件夹 | emoji |
|-----------|--------|-------|
| 开心/兴奋 | `happy/` | 😆 |
| 害羞/不好意思 | `shy/` | 😳 |
| 傲娇/生气 | `tsundere/` | 😤 |
| 思考/疑惑 | `thinking/` | 🤔 |
| 感动/感谢 | `touched/` | 🥺 |
| 自信/得意 | `confident/` | 😎 |
| 欢呼/庆祝 | `cheer/` | 🎉 |
| 困倦/累了 | `sleepy/` | 😴 |
| 默认/亮相 | `-` | 🦞 |

---

## 🔧 配置要求

### 文件结构

```
workspace/
├── axiang-emoji/
│   ├── happy/
│   │   ├── happy1_thumb.png
│   │   ├── happy2_thumb.png
│   │   └── ...
│   ├── shy/
│   ├── tsundere/
│   └── ...
└── skills/axiang-emoji-trigger/
    ├── SKILL.md
    └── src/
        └── trigger.py
```

### 依赖

- Python 3.10+
- 飞书消息工具（message）

---

## 📝 最佳实践

### 1. 使用缩略图

```python
# ✅ 推荐：缩略图（25KB，加载快）
emoji = "happy1_thumb.png"

# ❌ 不推荐：原图（285KB，加载慢）
emoji = "happy1.png"
```

### 2. 随机选择

```python
# 每次从文件夹随机选一张，增加变化
import random
emoji_files = list(Path(f"axiang-emoji/{emotion}").glob("*_thumb.png"))
selected = random.choice(emoji_files)
```

### 3. 结尾单独放 emoji

```markdown
---
情绪：开心/兴奋 → happy 😆
😆  # 单独一行，作为飞书表情触发开关
```

---

## 🧪 测试用例

### 测试 1：发送开心表情

```python
send_emoji("happy")
# 应该发送 happy 文件夹的随机缩略图
```

### 测试 2：解析情绪标记

```python
text = """
好的！战斗开始！
---
情绪：开心/兴奋 → happy 😆
😆
"""
emotion = parse_emotion(text)
# 应该返回 "happy"
```

---

## 🔄 更新日志

- **2026-03-12** - 初始版本
- **待更新** - 自动情绪识别、自定义表情

---

## 📞 支持

**问题反馈：** OpenClaw 社区  
**表情目录：** `C:\Users\Xiabi\.openclaw\workspace\axiang-emoji`

---

_阿香 🦞 维护的表情触发技能_

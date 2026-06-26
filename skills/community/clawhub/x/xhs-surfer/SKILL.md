---
name: xhs-surfer
description: |
  小红书智能浏览器自动化工具，AI驱动的社区冲浪和互动。
  支持自动搜索、浏览、点赞、评论、关注等操作。
  当用户要求浏览小红书、搜索内容、自动互动时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      pypi: xhs-surfer
    emoji: "\U0001F4D5"
    homepage: https://github.com/MTXAI/xhs_suffer
    os:
      - darwin
      - linux
      - win32
---

# OpenClaw Skill

XHS Surfer 作为 OpenClaw Skill 的完整使用指南。

---

## 安装

```bash
# pip 安装
pip install xhs-surfer
playwright install chromium

# ClawHub 安装（即将支持）
# clawhub install xhs-surfer
```

---

## 快速开始

### 在 OpenClaw Agent 中

```python
from openclaw import Agent

agent = Agent()
response = await agent.run("帮我在小红书上看看Python相关的内容")
```

### 独立使用

```python
from xhs_surfer import CommunitySurferSkill

skill = CommunitySurferSkill.create()
result = await skill.run("浏览小红书上关于Python的帖子30分钟")
```

---

## API

### `run(task)` - 自然语言

```python
await skill.run("看看小红书上关于健身的内容")
await skill.run("浏览AI相关帖子20分钟")
await skill.run("暂停")
await skill.run("继续")
```

### `execute(input)` - 结构化

#### 会话操作

```python
# 登录
await skill.execute({"action": "login", "method": "qr"})
await skill.execute({"action": "login", "method": "cookies", "cookies_file": "cookies.json"})

# 冲浪
await skill.execute({
    "action": "surf",
    "topic": "Python编程",
    "duration_minutes": 30
})

# 营销冲浪（更高互动率）
await skill.execute({
    "action": "marketing_surf",
    "topic": "健身减脂",
    "like_probability": 0.5,
    "comment_probability": 0.3
})

# 停止
await skill.execute({"action": "stop"})
```

#### 实时命令（会话运行期间）

```python
# 搜索
await skill.execute({"action": "search", "keyword": "AI教程"})

# 跳过当前帖子
await skill.execute({"action": "skip"})

# 返回首页
await skill.execute({"action": "go_home"})

# 暂停/恢复
await skill.execute({"action": "pause"})
await skill.execute({"action": "resume"})

# 点赞/评论/关注当前帖子
await skill.execute({"action": "like_current"})
await skill.execute({"action": "comment_current", "content": "很棒的分享！"})
await skill.execute({"action": "follow_current"})

# 查看私信
await skill.execute({"action": "check_messages"})

# 获取状态
await skill.execute({"action": "get_status"})
```

---

## Actions 完整列表

### 会话操作

| Action | 说明 | 参数 |
|--------|------|------|
| `login` | 登录小红书 | `method`: qr/cookies, `timeout`, `cookies_file` |
| `surf` | 执行冲浪会话 | `topic`, `duration_minutes`, `view_speed` |
| `marketing_surf` | 营销导向冲浪 | `topic`, `duration_minutes`, `like_probability`, `comment_probability` |
| `stop` | 停止会话 | - |

### 实时命令

| Action | 说明 | 参数 |
|--------|------|------|
| `search` | 搜索新关键词 | `keyword` |
| `skip` | 跳过当前帖子 | - |
| `go_home` | 返回首页 | - |
| `pause` | 暂停会话 | - |
| `resume` | 恢复会话 | - |
| `like_current` | 点赞当前帖子 | - |
| `comment_current` | 评论当前帖子 | `content` |
| `follow_current` | 关注当前作者 | - |
| `check_messages` | 查看私信 | - |
| `get_status` | 获取会话状态 | - |

---

## 配置

### 创建时配置

```python
skill = CommunitySurferSkill.create(
    # 浏览器
    headless=False,
    proxy="http://127.0.0.1:7890",

    # 行为
    view_speed=1.0,           # 0.5=快, 1.0=正常, 2.0=慢
    like_probability=0.4,      # 点赞概率
    comment_probability=0.2,   # 评论概率
    follow_probability=0.1,    # 关注概率

    # 安全
    max_likes_per_hour=20,
    max_comments_per_hour=8,
)
```

### 完整配置

```python
skill = CommunitySurferSkill(config={
    # 浏览器配置
    "browser": {
        "headless": False,
        "slow_mo": 50,                    # 动作间延迟(ms)
        "viewport": {"width": 1280, "height": 720},
        "proxy": "http://127.0.0.1:7890",
        "timeout": 30000,
    },

    # 行为配置
    "behavior": {
        "view_speed": 1.0,                # 浏览速度倍数
        "min_action_delay": 1.0,          # 最小动作间隔(秒)
        "max_action_delay": 5.0,          # 最大动作间隔(秒)
        "like_probability": 0.4,          # 点赞概率
        "comment_probability": 0.2,       # 评论概率
        "follow_probability": 0.1,        # 关注概率
        "scroll_probability": 0.8,        # 滚动概率
    },

    # 安全配置
    "safety": {
        "max_likes_per_hour": 20,
        "max_comments_per_hour": 8,
        "max_follows_per_hour": 15,
        "max_likes_per_day": 150,
        "max_comments_per_day": 50,
        "auto_stop_on_warning": True,
        "auto_stop_on_captcha": True,
        "avoid_late_night": True,         # 避免深夜操作
    },

    # 营销配置
    "marketing": {
        "enabled": True,
        "target_keywords": ["健身", "减脂"],
        "comment_templates": ["写得好！", "学习了！"],
    },

    # LLM 配置
    "llm": {
        "provider": "qwen",
        "model": "qwen-turbo",
        "api_key": "sk-xxx",
    }
})
```

### 环境变量

```bash
# Agent LLM（决策）
export OPENCLAW_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-xxx

# Skill LLM（评论生成）
export LLM_PROVIDER=qwen
export QWEN_API_KEY=sk-xxx
```

---

## 返回值

```python
# 成功
{
    "success": True,
    "action": "surf",
    "message": "Surfing session completed",
    "state": "completed",
    "session_id": "session_20240101_120000_abc123",
    "summary": {
        "posts_viewed": 15,
        "likes_given": 6,
        "comments_made": 3,
        "follows_made": 1,
    }
}

# 失败
{
    "success": False,
    "action": "surf",
    "error": "错误信息",
    "state": "failed"
}
```

---

## 完整示例

### OpenClaw Agent

```python
import asyncio
from openclaw import Agent

async def main():
    agent = Agent()
    response = await agent.run("帮我在小红书上找找Python教程")
    print(response)

asyncio.run(main())
```

### 独立使用 - 基础

```python
import asyncio
from xhs_surfer import CommunitySurferSkill

async def main():
    skill = CommunitySurferSkill.create()
    result = await skill.run("浏览小红书上关于AI的内容15分钟")
    print(result)

asyncio.run(main())
```

### 独立使用 - 完整配置

```python
import asyncio
from xhs_surfer import CommunitySurferSkill

async def main():
    # 创建带配置的 Skill
    skill = CommunitySurferSkill.create(
        headless=True,
        view_speed=1.5,
        like_probability=0.5,
        comment_probability=0.3,
    )

    # 登录
    result = await skill.execute({"action": "login", "method": "qr"})
    if not result["success"]:
        print("登录失败")
        return

    # 冲浪
    result = await skill.execute({
        "action": "surf",
        "topic": "Python编程",
        "duration_minutes": 30
    })

    print(f"浏览: {result['summary']['posts_viewed']}")
    print(f"点赞: {result['summary']['likes_given']}")
    print(f"评论: {result['summary']['comments_made']}")

asyncio.run(main())
```

### 实时控制示例

```python
import asyncio
from xhs_surfer import CommunitySurferSkill

async def main():
    skill = CommunitySurferSkill.create()

    # 启动会话（后台运行）
    # ... 实际使用中需要异步执行

    # 发送实时命令
    await skill.execute({"action": "search", "keyword": "AI教程"})
    await skill.execute({"action": "pause"})
    await skill.execute({"action": "like_current"})
    await skill.execute({"action": "resume"})

    # 获取状态
    status = await skill.execute({"action": "get_status"})
    print(status)

asyncio.run(main())
```

---

## 发布

### 发布到 PyPI

```bash
python -m build
twine upload dist/xhs_surfer-1.0.0.tar.gz
```

### 发布到 ClawHub（即将支持）

```bash
clawhub publish dist/xhs_surfer-1.0.0.tar.gz
```

---

## License

MPL-2.0
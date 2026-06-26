---
name: scrapling-boss-recruitment
description: "招聘数据爬取Skill，基于Scrapling框架在Boss直聘上执行招聘操作。当需要以下场景时使用：在Boss直聘搜索候选人、批量发送招呼、获取简历信息、解析结构化数据。Trigger phrases: boss直聘、招聘爬取、搜索候选人、获取简历、发送招呼、boss recruitment、zhipin"
---

# Scrapling Boss Recruitment

基于 Scrapling 的 Boss直聘 招聘辅助工具，支持候选人搜索、简历获取、自动打招呼。

## 核心能力

| 功能 | 方法 | 说明 |
|------|------|------|
| 搜索候选人 | `search_candidates()` | 按关键词/条件搜索 |
| 获取简历 | `get_resume()` | 获取候选人详细信息 |
| 批量打招呼 | `batch_greet()` | 批量发送招呼 |
| 解析简历 | `parse_resume()` | 结构化提取简历字段 |

## 快速开始

### 1. 安装依赖

```bash
pip install scrapling
```

### 2. 配置Cookie

用户需提供Boss直聘登录Cookie：

```python
COOKIES = {
    '__zp_stoken__': '用户提供的stoken',
    '__zp_phoenix_id': '用户提供的phoenix_id',
    # ... 其他Cookie
}
```

### 3. 搜索候选人

```python
from scripts.boss_scraper import BossRecruiter

recruiter = BossRecruiter(cookies=COOKIES)
results = recruiter.search_candidates(
    keyword='Python后端',
    city='北京',
    experience='3-5年',
    degree='本科'
)
```

### 4. 发送招呼

```python
recruiter.batch_greet(
    candidate_ids=['候选人ID列表'],
    greeting_template='您好，{name}，我们正在招聘{position}，您有兴趣吗？'
)
```

## 工作流程

```
用户输入招聘需求
    ↓
Agent解析需求 → search_candidates()
    ↓
获取候选人列表 → 展示给用户
    ↓
用户选择候选人 → batch_greet()
    ↓
获取简历 → get_resume()
    ↓
存入人才库
```

## 关键文件

| 文件 | 用途 |
|------|------|
| `scripts/boss_scraper.py` | 主爬虫类 |
| `scripts/parser.py` | 简历解析器 |
| `references/selectors.md` | Boss直聘 CSS选择器 |
| `references/config.md` | 配置说明 |

## 反爬策略

1. **随机延迟**：3-10秒随机间隔
2. **请求限流**：每日搜索≤200次，打招呼≤500次
3. **Cookie刷新**：Token过期后提示用户更新
4. **失败重试**：自动重试3次，间隔递增

## 注意事项

- 仅供用户本人账号使用，禁止批量操作他人账号
- 遵守Boss直聘robots.txt和服务条款
- 定期检查Cookie有效性

# 完整分析工作流手册 v2.0

> 记录：B 治愈系代表 深度分析全过程（三份文档合并 + hsword框架应用）
> 原始 xhsfenxi 工作流见：workflow-xhsfenxi-v2.md

---

## 标准执行管道（Full Pipeline）

```
Step 0  Cookie 健康检查
Step 1  解析输入 → 检查数据库
Step 2  数据采集
Step 3  基础统计
Step 4  三型分类
Step 5  内核三段论（hsword框架）
Step 6  爆款选题公式（6模型）
Step 7  结构化报告 Markdown
Step 8  外部文档合并（如有）
Step 9  写入博主数据库
Step 10 生成黑体 Word
```

---

## Step 0 — Cookie 健康检查

```python
from xhscosmoskill import print_cookie_status, get_best_cookies
cookies = get_best_cookies()
print_cookie_status(cookies)
```

**Cookie 优先顺序：**
1. `shopify-marketing/xhs_cookies.json`（最新，优先）
2. `xiaohongshu_new/xhs_cookies.json`（备用）

**过期判断：** notes 返回 ≤ 1 条 → Cookie 失效 → 运行 `python3 xhs_login.py`

---

## Step 1 — 解析输入

```python
import re
user_id = re.search(r'/user/profile/([a-f0-9]+)', url).group(1)

from xhscosmoskill import get_blogger
existing = get_blogger(creator_name)  # 检查是否已分析过
```

---

## Step 2 — 数据采集

```python
from xhscosmoskill import XhsClient
with XhsClient(cookies_file=cookies, headless=True, scroll_times=10) as xhs:
    notes = xhs.get_user_notes(user_id, limit=50)
    xhs.save(notes, f"/tmp/{creator_name}_notes.json")
```

---

## Step 3-4 — 统计 + 分类

```python
from xhscosmoskill import compute_stats, classify_archetype, build_five_layers

stats     = compute_stats(notes)
archetype = classify_archetype(notes)
five      = build_five_layers(notes, archetype)
```

---

## Step 5 — 内核三段论（hsword框架）

每次分析必须明确三层结构（参见 hsword-frameworks.md）：

```
外壳是什么？→ 表面标签（可模仿）
真正的内核？→ 一句话，带""引号
三层人设：
  表层标签   → 自动提取
  中层特质   → 手动填写（性格/能力/气质）
  深层价值观 → 手动填写（最重要，不可复制）
```

---

## Step 6 — 爆款选题公式

```python
from xhscosmoskill import generate_formula_report
from xhscosmoskill.utils import save_md

formula_md = generate_formula_report(notes, creator_name, archetype)
save_md(formula_md, f"/tmp/{creator_name}-爆款选题公式.md")
```

生成内容：总公式 + 6模型（每个含可套用句式）+ 30个选题方向 + 可迁移模板

---

## Step 7 — 结构化报告

```python
from xhscosmoskill import analyze_account

report_md = analyze_account(notes, creator_name=creator_name, mode="full")
save_md(report_md, f"/tmp/{creator_name}-结构化总结报告.md")
```

---

## Step 8 — 外部文档合并（如有）

用户提供额外分析文档时，按优先级 patch：

| 优先级 | 内容 |
|--------|------|
| 1 | 更高的点赞数（修正我们的数据）|
| 2 | 新笔记数据（我们50篇未收录的）|
| 3 | 新分析维度（我们没有的章节）|
| 4 | 更精炼的提炼（更好的一句话总结）|

**B 治愈系代表 合并经验：**
- 文档1（txt）：补入 3.2万/7490/6231 等数据 + 视觉风格 + 风险分析
- 文档2（md）：补入 8813赞 + 头部集中度38.15% + 可摘抄感 + 新榜链接
- 验证：patch后检查7个关键词确认写入

---

## Step 9 — 写入数据库

```python
from xhscosmoskill import save_blogger
save_blogger(
    creator_name=creator_name,
    user_id=user_id,
    archetype=archetype,
    stats={"avg_likes": stats["avg_likes"], "max_likes": stats["max_likes"],
           "sample_size": stats["total"], "viral_count": stats["brackets"]["1万+"],
           "video_ratio": f"{stats['video_count']}/{stats['total']}"},
    best_topic=five["best_topic"],
    best_topic_avg=five["best_topic_avg"],
    formula="核心公式一句话",
)
```

---

## Step 10 — 生成黑体 Word

```python
from xhscosmoskill.scripts.build_docx import build_word

build_word(f"/tmp/{creator_name}-结构化总结报告.md",
           f"/tmp/{creator_name}-结构化总结报告.docx",
           title=creator_name, subtitle="小红书博主深度结构化分析报告")

build_word(f"/tmp/{creator_name}-爆款选题公式.md",
           f"/tmp/{creator_name}-爆款选题公式.docx",
           title=creator_name, subtitle="爆款选题公式  ·  6大模型  ·  30个选题方向")
```

---

## 证据分级

| 级别 | 来源 | 用法 |
|------|------|------|
| A1 | 小红书公开主页可见数据 | 直接陈述 |
| A2 | 用户提供截图 | 直接陈述 |
| B1 | 第三方公开（新榜/访谈）| 背景补充 |
| C1 | 综合推断 | 明确标注"推断" |

---

## 类型迭代协议

```python
from xhscosmoskill import add_archetype, update_archetype_signals

# 添加新类型（当最高分 < 10 时）
add_archetype(key="D", name="知识科普型", desc="...",
              formula="...", title_signals=[], content_signals=[],
              commercial="...", difficulty="中")

# 迭代已有类型信号词
update_archetype_signals("B", new_content_signals=["新词"])
```

---

## 已分析博主档案

`data/bloggers.json` 在分发版本中为空，每次 `/xhsfx` 调用后会自动追加。

---

## 参考资源

- hsword 实战案例：`openclaw_cosmo/afa/hsword/`
- hsword 框架手册：`references/hsword-frameworks.md`
- 原始 xhsfenxi 工作流：`references/workflow-xhsfenxi-v2.md`
- Word 修复脚本：`openclaw_cosmo/afa/小红书分析与工作流归档/02-Word生成与目录修复脚本/`
- 新榜数据：`https://www.newrank.cn/profile/xiaohongshu/{user_id}`

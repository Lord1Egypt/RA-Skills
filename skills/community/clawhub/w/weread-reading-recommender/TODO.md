# TODO.md — weread-reading-recommender

> 当前状态：草稿已初始化，部分文档已落地；核心代码和正式 skill 说明尚未完成。

## 项目目标
做一个**本地优先（local-first）**的微信读书推荐 skill：

- 通过**本地 cookie**导出微信读书阅读记录
- 将原始数据归一化为推荐友好的 JSON
- 根据：
  1. 用户当前想解决的问题 / 想学习的主题
  2. 用户微信读书里的阅读轨迹
  来推荐下一本或下一组最适合的书

## 已完成
### 文件
- `PLAN.md`
- `SPEC.md`
- `references/data-schema.md`
- `references/privacy-model.md`
- `references/recommendation-rubric.md`
- `assets/sample-weread-raw.json`

### 目录
- `scripts/`
- `references/`
- `assets/`

## 未完成（必须补）

---

# 1. 正式完成 SKILL.md
当前 `SKILL.md` 仍然是 init_skill.py 生成的模板，**必须改成正式版**。

## 要求
### 1.1 说明 skill 是做什么的
明确写清：
- 这是一个本地优先的微信读书阅读画像与图书推荐 skill
- 主要用途是：
  - 导出本地微信读书记录
  - 归一化数据
  - 根据当前目标 / 阅读历史推荐书

### 1.2 说明什么时候用
要覆盖这些触发场景：
- 用户说“根据我的微信读书记录推荐书”
- 用户说“分析我的阅读偏好”
- 用户说“我最近想学某个主题，结合微信读书记录推荐”
- 用户说“帮我导出 / 刷新 / 归一化微信读书数据”

### 1.3 工作流写清楚
推荐结构：
1. 检查是否已有 normalized JSON
2. 如果没有，则先运行导出脚本
3. 再运行 normalize 脚本
4. 再读取 normalized 数据做推荐

### 1.4 要强调安全边界
必须明确写：
- cookie 仅限本地使用
- 不要写进 skill 文件
- 不要输出到导出 JSON
- 不要默认依赖 CookieCloud / 第三方同步服务

### 1.5 写几个真实示例
例如：
- 结合我的微信读书记录，我最近想系统学 AI Agent，推荐 5 本书
- 基于我的阅读历史，推荐下一本最适合现在读的书
- 分析我的阅读偏好，并给我 3 本稳妥推荐 + 2 本探索推荐

---

# 2. 实现 scripts/export_weread.py
这是核心导出脚本，**必须实现**。

## 目标
本地读取 cookie，调用微信读书接口，导出 raw JSON。

## 技术要求
- Python 3
- 尽量只依赖标准库 + `requests`
- 代码要可直接运行
- 错误信息明确，不要吞异常

## 支持的 cookie 输入优先级
按优先级读取：
1. `--cookie`
2. `--cookie-file`
3. `--env-var <NAME>` 指定环境变量
4. 默认环境变量 `WEREAD_COOKIE`

## CLI 参数
至少支持：
- `--out`
- `--cookie`
- `--cookie-file`
- `--env-var`
- `--include-book-info`
- `--detail-limit`
- `--timeout`

## 必须调用的接口
### 2.1 书架同步
`https://weread.qq.com/web/shelf/sync`

### 2.2 笔记本书籍列表
`https://weread.qq.com/api/user/notebook`

### 2.3 可选：按 bookId 获取书籍信息
`https://weread.qq.com/api/book/info`

## 输出 JSON 顶层字段
至少包括：
- `exported_at`
- `source`
- `summary`
- `shelf_sync`
- `notebook`
- `book_info`
- `warnings`（可选）

## 输出要求
- **严禁写入 cookie 到 JSON**
- `summary` 至少统计：
  - total_books
  - finished_books
  - reading_books
  - unread_books
  - notebook_books
- 终端 stdout 打印导出摘要

## 异常处理要求
至少处理：
- 没有 cookie
- cookie 文件不存在
- 接口请求失败
- 接口返回非法 JSON
- cookie 过期 / 未登录

## 建议函数拆分
建议至少拆成：
- `resolve_cookie(...)`
- `build_session(...)`
- `fetch_shelf_sync(...)`
- `fetch_notebook(...)`
- `fetch_book_info(...)`
- `build_summary(...)`
- `main()`

---

# 3. 实现 scripts/normalize_weread.py
这是第二个核心脚本，负责把 raw JSON 转成推荐友好格式。

## 目标
读取 `weread-raw.json`，输出 `weread-normalized.json`。

## CLI
至少支持：
- `--input`
- `--output`

## 每本书必须生成的字段
- `book_id`
- `title`
- `author`
- `translator`
- `categories`
- `book_lists`
- `status`：`finished | reading | unread`
- `is_finished`
- `progress`
- `reading_time_seconds`
- `last_read_at`
- `note_count`
- `bookmark_count`
- `review_count`
- `interaction_count`
- `engagement_score`
- `is_imported`
- `is_paid`
- `public_rating`
- `intro`

## 顶层必须生成的结构
### 3.1 summary
至少包括：
- total_books
- status_counts
- top_categories
- top_book_lists
- imported_vs_native

### 3.2 profile_inputs
至少包括：
- `highest_engagement_books`
- `recent_books`
- `unfinished_books_with_momentum`

### 3.3 llm_hints
生成若干简短提示，帮助推荐阶段快速理解阅读画像，例如：
- 最近阅读偏向哪些类别
- 高互动书主要集中在哪些主题
- 完读率较高的类型

## engagement_score 设计要求
给出一个启发式分数（0~100 即可），综合考虑：
- finishReading
- progress
- readingTime
- noteCount
- bookmarkCount
- reviewCount
- recency

### 建议大致思路
可例如：
- 完读加分
- 进度高加分
- 阅读时长加分（上限截断）
- 交互数加分
- 最近读过加分

## recent_books
按 `last_read_at` 排序取前若干本。

## highest_engagement_books
按 `engagement_score` 排序取前若干本。

## unfinished_books_with_momentum
筛出：
- 未读完
- 但 progress > 0 或 reading_time_seconds > 0
- 并按 momentum 排序

## 建议函数拆分
建议至少拆成：
- `load_raw(...)`
- `parse_categories(...)`
- `build_book_lists_map(...)`
- `compute_status(...)`
- `compute_engagement_score(...)`
- `normalize_books(...)`
- `build_summary(...)`
- `build_profile_inputs(...)`
- `build_llm_hints(...)`
- `main()`

---

# 4. 生成 assets/sample-weread-normalized.json
基于现有的：
- `assets/sample-weread-raw.json`

生成对应的：
- `assets/sample-weread-normalized.json`

## 要求
- 与 normalize 脚本输出结构一致
- 可作为示例输入给 skill 使用
- 字段完整，不要只放极简 stub

---

# 5. 自测
至少做这些最基本的验证：

## 5.1 Python 语法检查
例如：
- `python3 -m py_compile scripts/export_weread.py`
- `python3 -m py_compile scripts/normalize_weread.py`

## 5.2 normalize 跑样例
用现有样例跑一次：
- 输入：`assets/sample-weread-raw.json`
- 输出：`assets/sample-weread-normalized.json`

## 5.3 输出结果检查
确认：
- 文件成功生成
- JSON 合法
- 每本书关键字段都存在
- summary / profile_inputs / llm_hints 存在

## 5.4 最好顺手补 README 级运行说明到 SKILL.md
至少告诉用户：
- 如何设置 cookie
- 如何导出 raw
- 如何 normalize
- 然后如何问推荐问题

---

# 6. 推荐功能层面的设计要求（供完善 SKILL.md / 后续实现参考）
虽然本轮重点是导出和归一化，但 skill 的最终功能目标必须写清：

## 功能目标
### 6.1 有当前目标时
根据：
- 当前问题 / 学习主题
- 微信读书历史
推荐书籍

例如：
- 我最近想系统学 AI Agent，结合我的微信读书记录推荐几本书

### 6.2 没有当前目标时
根据阅读历史做：
- 阅读画像总结
- 稳妥推荐
- 探索推荐
- 可选：暂缓推荐

## 推荐解释需要包含
每本书最好说明：
- 为什么推荐
- 它像你读过的哪几本
- 它补的是哪一块
- 适不适合现在读

---

# 7. 安全要求（实现时必须遵守）
- 不要把 cookie 写入任何 JSON / md / assets / logs
- 不要把第三方 cookie 同步作为默认方案
- 不要要求远端服务代管 cookie
- 保持 local-first

---

# 8. 建议最终交付文件清单
完成后，目录至少应该包含：

```text
weread-reading-recommender/
├── PLAN.md
├── SPEC.md
├── TODO.md
├── SKILL.md
├── scripts/
│   ├── export_weread.py
│   └── normalize_weread.py
├── references/
│   ├── data-schema.md
│   ├── privacy-model.md
│   └── recommendation-rubric.md
└── assets/
    ├── sample-weread-raw.json
    └── sample-weread-normalized.json
```

---

# 9. 完成定义（Definition of Done）
满足以下条件才算本轮完成：

- [ ] `SKILL.md` 已从模板改成正式版
- [ ] `scripts/export_weread.py` 已实现
- [ ] `scripts/normalize_weread.py` 已实现
- [ ] `assets/sample-weread-normalized.json` 已生成
- [ ] 两个 Python 脚本语法通过
- [ ] normalize 脚本已用 sample raw 跑通
- [ ] 没有把 cookie 写入任何输出文件

---

# 10. 可选增强（不是本轮必须）
以下内容可以后续再做：
- 分析划线/笔记文本
- 更强的阅读画像总结
- 外部候选书源召回
- 中英文书名归一化 / 去重
- 热门书评纳入解释层
- 自动刷新脚本

# 精选模式清单 / Pattern Catalog

本清单从 fabric 的 250+ 模式中精选最通用的约 60 个，按场景分类。每个模式一行：**模式名** — 作用。

## 总结 / Summarize

- `summarize` — 20 词句 + 10 要点 + 5 结论的结构化总结
- `summarize_micro` — 20 词句 + 3 要点 + 3 结论的精简总结
- `create_summary` — 20 词句 + 要点 + 结论，带编号列表
- `create_micro_summary` — 20 词精简总结
- `summarize_paper` — 学术论文结构化总结（标题/方法/实验/结论）
- `youtube_summary` — YouTube 视频带时间戳的要点总结
- `summarize_meeting` — 会议记录结构化总结（要点/任务/决策/风险）
- `concall_summary` — 财报/电话会总结（管理层评论/QA/财务洞察）

## 提炼 / Extract

- `extract_wisdom` — 提炼智慧（洞察/金句/习惯/事实/参考/建议）
- `extract_insights` — 提炼最有力量的洞察（16 词要点）
- `extract_ideas` — 提炼所有关键想法（15 词要点）
- `extract_article_wisdom` — 提炼文章精华（分节结构化）
- `extract_book_ideas` — 提炼一本书的 50–100 个想法
- `extract_book_recommendations` — 提炼一本书的 50–100 个可执行建议
- `extract_recommendations` — 提炼简明可执行建议
- `extract_main_idea` — 提炼主旨 + 关键建议（15 词句）
- `extract_core_message` — 一句话提炼核心信息
- `extract_questions` — 提炼访谈/对话中的所有提问
- `extract_references` — 提炼文中引用的书/文章/来源
- `extract_wisdom_with_attribution` — 带发言人署名的智慧提炼

## 分析 / Analyze

- `analyze_claims` — 分析论断可信度（证据/反证/谬误/结论）
- `find_logical_fallacies` — 找逻辑谬误（形式/非形式）
- `check_falsifiability` — 检查论断是否可证伪
- `analyze_prose` — 评价文字的新颖/清晰/文笔并打分
- `label_and_rate` — 打 20 个单字标签 + 评级
- `rate_content` — 标签 + S/A/B/C/D 分级 + 质量分
- `analyze_paper` — 分析论文（发现/严谨性/质量）
- `analyze_risk` — 第三方供应商风险评估
- `analyze_logs` — 分析服务器日志找异常
- `get_wow_per_minute` — 评估内容的价值密度
- `analyze_product_feedback` — 整理用户反馈（主题/优先级）

## 写作 / Writing

- `improve_writing` — 润色（语法/风格/清晰，保留原意）
- `improve_academic_writing` — 学术写作润色
- `fix_typos` — 纠错别字/语法/标点
- `clean_text` — 清洗排版乱的文本（换行/标点/段落）
- `humanize` — 让 AI 文本读起来自然、去 AI 味
- `write_essay` — 按指定作者风格写文章
- `write_micro_essay` — Paul Graham 风格精炼短文
- `create_formal_email` — 写正式邮件
- `create_newsletter_entry` — 写 newsletter 风格摘要
- `translate` — 翻译到指定语言，保持格式与语气

## 代码 / Code

- `explain_code` — 解释代码/配置/工具输出
- `review_code` — 代码审查（正确性/安全/性能）
- `improve_prompt` — 优化提示词
- `create_coding_project` — 从想法生成脚手架
- `explain_math` — 解释数学概念
- `create_git_diff_commit` — 从 diff 生成提交信息

## 会议与协作 / Meeting & Collab

- `transcribe_minutes` — 从转录提炼会议纪要
- `summarize_debate` — 总结辩论（分歧/论据/预测）
- `summarize_pull-requests` — 总结 PR 列表

## 转换与结构化 / Convert & Structure

- `convert_to_markdown` — 把内容转成干净 Markdown
- `export_data_as_csv` — 把数据结构导出 CSV
- `create_mermaid_visualization` — 生成 Mermaid 图
- `create_markmap_visualization` — 生成 MarkMap 图
- `create_conceptmap` — 生成交互式概念图（HTML）
- `create_investigation_visualization` — 生成 Graphviz 调查图
- `create_design_document` — 生成 C4 设计文档
- `create_prd` — 生成 PRD 文档
- `create_recursive_outline` — 递归拆解任务大纲

## 安全 / Security

- `ask_secure_by_design_questions` — 生成安全设计问题集
- `create_stride_threat_model` — STRIDE 威胁建模
- `create_threat_scenarios` — 生成威胁场景
- `analyze_threat_report` — 分析威胁报告（洞察/趋势/建议）
- `analyze_malware` — 分析恶意软件（指标/技术/检测）
- `analyze_email_headers` — 邮件头安全分析（SPF/DKIM/DMARC）
- `check_agreement` — 审查合同/协议（条款/问题/坑）

## 说明 / Notes

- 每个模式的原始指令位于 fabric 仓库 `patterns/<name>/system.md`，可随时读取后手动应用（降级路径）。
- 模式名一律用上述小写下划线形式；用户提到未列出的模式名时，先到官方仓库确认存在再使用。

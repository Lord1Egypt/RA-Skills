# OpenClaw 使用说明 · zhiyan-smart-research

> ClawHub：https://clawhub.ai/skills/zhiyan-smart-research  
> 发布者：@caoling7878-arch

**提问即检索，结论必溯源** — v1.1 起，每个问题输出**六节结构化报告**。

---

## v1.1 你会得到什么

| 章节 | 内容 |
|------|------|
| 结论摘要 | 3–5 句，带 `[n]` 引用 |
| 参考文献 | 表格（标题 · 作者 · 年份 · 链接） |
| 文献综述 | 约 300 字梳理 |
| 研究空白与创新点 | 条目归纳 |
| 研究建议 | 约 200 字 |
| 追问建议 | 3 个深入方向 |

---

## 1. 安装

### 方式 A：ClawHub（推荐）

```bash
clawhub install zhiyan-smart-research
```

或 OpenClaw 命令：

```bash
openclaw skills install @caoling7878-arch/zhiyan-smart-research
```

### 方式 B：安装到指定 workspace

```bash
openclaw skills install @caoling7878-arch/zhiyan-smart-research --global
# 或进入某个 workspace 后不加 --global
```

安装后重启会话或执行 `/new`，让 Agent 加载新 Skill。

---

## 2. 环境要求

| 项 | 说明 |
|----|------|
| Python 3.9+ | 运行检索脚本 |
| 网络 | 可访问 `api.crossref.org`、`eutils.ncbi.nlm.nih.gov` |
| OpenClaw LLM | 在 openclaw.json 中已配置模型（DeepSeek / Claude 等） |

**不需要：** 智研后端、微信、API Key（Skill 内无密钥）。

可选环境变量：

```bash
export CROSSREF_MAILTO=your@email.com   # Crossref 礼貌池，建议填写
```

---

## 3. 怎么用（对话）

安装完成后，直接对 Agent 说：

```
帮我调研 CRISPR 基因编辑近五年的研究空白，要引用文献
```

或使用斜杠命令（若已暴露）：

```
/zhiyan-smart-research
```

Agent 会自动：

1. 检索 Crossref + PubMed 论文  
2. 按 **v1.1 六节模板** 撰写完整报告（摘要 / 综述 / 空白 / 建议 / 3 条追问）  
3. 保存到 `research/sessions/` 供追问  

更新 Skill：

```bash
clawhub update zhiyan-smart-research
# 或 openclaw skills update zhiyan-smart-research
```

---

## 4. 手动命令（可选）

Skill 安装目录下（`{baseDir}`）可手动测试：

```bash
# 健康检查
python3 scripts/health_check.py

# 文献检索
python3 scripts/search_literature.py "machine learning medical imaging"

# 保存研究结果（Agent 通常代劳）
python3 scripts/save_research.py \
  --topic "研究主题" \
  --summary "带 [1][2] 引用的综述正文…" \
  --papers-json /tmp/papers.json
```

---

## 5. 典型场景

| 你想做什么 | 怎么说 |
|-----------|--------|
| 找最新论文 | 「检索 XXX 领域最新英文论文」 |
| 领域综述 | 「梳理 XXX 近五年研究进展，带引用」 |
| 研究空白 | 「分析 XXX 的研究空白与创新点」 |
| 学术争议 | 「对比 XXX 领域的主要争议观点」 |
| 追问 | 「继续上面 CRISPR 的话题，补充 Transformer 相关文献」 |

---

## 6. 输出格式（v1.1）

见 Skill 内 `templates/report-template.md`。Agent 必须输出全部六节，不可只给摘要。

---

## 7. 记忆与追问

- **同一会话内**：OpenClaw 对话历史自动保留上下文  
- **跨会话**：研究结果保存在 Skill 目录 `research/sessions/*.md`  
- 追问时 Agent 会先读历史 session，再决定是否补充检索  

---

## 8. 常见问题

| 问题 | 处理 |
|------|------|
| Skill 未生效 | `/new` 新开会话，或 `openclaw gateway restart` |
| 检索结果为空 | 换英文关键词重试 |
| 回答无深度 | 检查 OpenClaw 是否配置了 LLM 模型 |
| 引用编号错乱 | 以 `papers` 数组顺序为准，`[1]` 对应第一篇 |

---

## 9. 卸载

```bash
clawhub uninstall zhiyan-smart-research
# 或
openclaw skills uninstall zhiyan-smart-research
```

本地研究记录位于 Skill 目录 `research/sessions/`，卸载前可自行备份。

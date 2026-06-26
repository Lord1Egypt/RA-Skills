# topic-research

`topic-research` 是二跳深研 skill。它接在资讯扫描之后，或者接在人工确定的选题之后，用 Tavily CLI 产出可继续写作的 `research.md`。

## 这个 skill 能做什么

- 围绕一个主题做深度研究
- 汇总多来源证据并沉淀为本地研究报告
- 给出写作价值判断、推荐框架、开头钩子和标题方向
- 保存 raw JSON，方便追溯来源和二次利用

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Tavily CLI

按 repo 内置 skill 的说明先安装并登录 `tvly`：

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash && tvly login
```

安装完成后，确保下面命令能正常返回：

```bash
tvly --help
```

## 输入和输出

**输入**

- 一个带 YAML frontmatter 的研究请求文件
- 常用字段：`topic`、`question`、`model`、`source_file`、`seed_urls`

**输出**

- `content-production/inbox/YYYYMMDD-<slug>-research.md`
- `content-production/inbox/raw/research/YYYY-MM-DD/<slug>.json`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill topic-research \
  --input content-production/inbox/20260407-harness-engineering-综合分析-request.md
```

### 常见上游

- `news-collect`
- 人工选中的具体题目

## 什么时候用

- 你已经有一个题目，但还缺证据、结构和判断
- 你想从“今天的资讯”里挑一个值得写长文的方向
- 你需要一份能直接喂给后续写作的研究报告

## 注意事项

- 这是“深研 skill”，不是“宽扫描 skill”
- `tvly` 不存在或未登录时，本 skill 会直接报错，不会静默降级
- 如果只是想先扫一遍市场，不要直接跳过 `news-collect`

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [tavily-research](../tavily-research/SKILL.md)

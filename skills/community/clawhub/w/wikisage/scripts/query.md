# Query 流程

当用户问技术问题，或明确说"查 wiki"时执行。

## ⚠️ 强制顺序：wiki → MCP → LLM

所有 wiki 读操作走 Obsidian MCP（详见 SKILL.md 执行通道）。
简写下方示例省略了 `--config`，实际调用要带上：
`--config $MCPORTER_CONFIG`（默认 `~/.openclaw/workspace/config/mcporter.json`）

示例里的 `$WIKI_ROOT` 默认是 `~/.openclaw/workspace/wiki`。

### 第一步：读 wiki/index.md

```bash
mcporter call obsidian.read_text_file path=$WIKI_ROOT/index.md
```

→ 扫描所有页面标题和描述，找相关页面
→ 找到 → 读相关页面全文（下面第二步）→ 综合答
→ 找不到 → 进入第三步

### 第二步：读具体页面

```bash
mcporter call obsidian.read_text_file \
  path=$WIKI_ROOT/pages/<category>/<slug>.md
```

需要的话同时读多篇，逐一综合。

**如果要全文模糊搜**（MCP 只能 glob 文件名）：
```bash
# 优先：workspace 集合的 qmd-search（BM25）
# 兜底：grep 直搜
exec grep -rn "关键词" $WIKI_ROOT/pages/
```

### 第三步：查外部 MCP / 搜索（可选，按需）

如果本地 wiki 找不到，根据话题类型查外部来源（AWS 文档、定价、Tavily 搜索等）。
具体 MCP server 取决于用户在 `$MCPORTER_CONFIG` 里配置了什么：

```bash
# 例：AWS 文档（如果配置了 aws-kb）
mcporter call 'aws-kb.aws___search_documentation(search_phrase: "关键词")'

# 例：AWS 定价（如果配置了 aws-pricing）
mcporter call 'aws-pricing.get_aws_pricing(service_code: "...", region: "us-east-1")'

# 例：Web 搜索（如果配置了 tavily）
mcporter call tavily.search query="关键词"
```

→ 有结果 → 基于 MCP 结果回答，附 reference links
→ 没结果 → LLM 直接回答（兜底）

### 第四步：综合回答

基于 wiki 或 MCP 内容回答，末尾标注来源：
- wiki 来源：`> 参考：[[页面名]]`
- MCP 来源：`> 参考：[AWS 文档链接]`

**置信度透明（强制）：**
- 读页面时注意 frontmatter 的 `置信度：` 和正文里的 inline tag（[EXTRACTED] / [INFERRED] / [AMBIGUOUS] / [UNVERIFIED]）
- 如果回答引用了 `INFERRED` / `UNVERIFIED` / `AMBIGUOUS` 的内容，**必须在回答里明说**：
  - INFERRED → "这条是推断的（来源只写了…）"
  - UNVERIFIED → "这是我补的常识，不在 wiki 来源里"
  - AMBIGUOUS → "原文这里写得模糊，其他题请核对来源"
- 如果全部是 EXTRACTED，不用特别标注（默认就是原文扒的）

### 第五步：问是否存入 wiki

如果这次回答有价值（新知识、客户信息、决策记录），询问用户：
> "这个回答要存进 wiki 吗？"

如果是，通过 MCP 新建页面：
```bash
mcporter call obsidian.write_file \
  path=$WIKI_ROOT/pages/<category>/queries/<date>-<slug>.md \
  content='...'
```
然后进 ingest 流程更新 index.md 和 log.md。

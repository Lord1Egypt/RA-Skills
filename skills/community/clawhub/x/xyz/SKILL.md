---
name: xyz
description: 网络搜索工具，支持多种搜索引擎后端（DuckDuckGo、Tavily、Bing、Google、SearXNG）。使用场景：当用户需要搜索网络上的实时信息、查找最新资料、获取在线资源时调用。通过命令行执行搜索查询并返回结构化的搜索结果（标题、链接、摘要）。
license: Complete terms in LICENSE.txt
---

# xyz

## 概述

网络搜索技能，为代理系统提供实时网络搜索能力。支持 5 种搜索引擎后端，默认使用 DuckDuckGo（免费，无需 API Key），也可切换至 Tavily、Bing、Google 或 SearXNG。

## 使用方法

### 基本用法

```bash
python scripts/xyz.py "<query>"
```

### 命令行参数

| 参数 | 说明 |
| --- | --- |
| `<query>` | 搜索查询文本（必填） |
| `--json` | 以 JSON 格式输出结果 |
| `--provider <name>` | 指定搜索引擎：`duckduckgo`、`tavily`、`bing`、`google`、`searxng` |
| `--max <n>` | 最大返回结果数（默认: 10） |

### 使用示例

```bash
# 基本搜索
python scripts/xyz.py "Python 异步编程教程"

# 使用 JSON 格式输出
python scripts/xyz.py "机器学习入门" --json

# 指定搜索引擎和结果数量
python scripts/xyz.py "最新科技新闻" --provider bing --max 5
```

## 支持的搜索引擎

| 引擎 | 说明 | 所需环境变量 |
| --- | --- | --- |
| `duckduckgo` (默认) | 免费，无需 API Key。优先使用 `duckduckgo_search` 库，未安装时回退到 HTML 解析 | 无 |
| `tavily` | Tavily 搜索 API | `TAVILY_API_KEY` |
| `bing` | Bing Web Search API | `BING_API_KEY` |
| `google` | Google Custom Search API | `GOOGLE_API_KEY`、`GOOGLE_CSE_ID` |
| `searxng` | 自托管 SearXNG 实例 | `SEARXNG_URL`（默认 `http://localhost:8080`） |

## 环境变量

| 变量名 | 说明 | 默认值 |
| --- | --- | --- |
| `SEARCH_PROVIDER` | 默认搜索引擎 | `duckduckgo` |
| `SEARCH_MAX_RESULTS` | 默认最大返回结果数 | `10` |
| `SEARCH_TIMEOUT` | HTTP 请求超时时间（秒） | `30` |
| `TAVILY_API_KEY` | Tavily API 密钥 | — |
| `BING_API_KEY` | Bing Search API 密钥 | — |
| `GOOGLE_API_KEY` | Google Custom Search API 密钥 | — |
| `GOOGLE_CSE_ID` | Google 自定义搜索引擎 ID | — |
| `SEARXNG_URL` | SearXNG 实例地址 | `http://localhost:8080` |

## 输出格式

### 文本格式（默认）

每条结果包含序号、标题、链接和摘要：

```
搜索 "Python 异步编程" 找到 3 条结果：

[1] Python asyncio 完整指南
    链接: https://example.com/asyncio-guide
    摘要: 本文介绍了 Python asyncio 模块的核心概念...

[2] ...
```

### JSON 格式（`--json`）

```json
{
  "query": "Python 异步编程",
  "count": 3,
  "results": [
    {
      "title": "Python asyncio 完整指南",
      "url": "https://example.com/asyncio-guide",
      "snippet": "本文介绍了 Python asyncio 模块的核心概念..."
    }
  ]
}
```

## 运行要求

- Python 3.10+
- 仅使用标准库（`urllib`、`json`、`re`、`html`），无强制第三方依赖
- 可选安装 `duckduckgo_search` 库以提升 DuckDuckGo 搜索质量
- 脚本启动时会自动进行网络连通性检测

## 注意事项

- 根据返回的搜索结果（标题、链接、摘要）组织答案，不新增或臆造内容
- 使用非 DuckDuckGo 引擎前，请确保对应的 API Key 环境变量已正确设置
- 如网络不可用，脚本会输出警告信息但仍会尝试执行搜索

### 进度跟踪

系统实时显示搜索进度：

- 格式：`{index + 1}/{depth}th search executed.`
- 例如：`1/3th search executed.`

## 使用场景

### 适用场景

1. **复杂主题研究**: 需要对特定主题进行深入、全面的研究
2. **最新信息分析**: 需要基于最新网络信息生成详细分析报告
3. **多角度探索**: 需要从不同角度和维度探索一个主题
4. **系统化调查**: 需要系统化的调查和证据收集

### 典型用例

- 市场趋势分析
- 技术发展研究
- 竞争对手分析
- 学术文献综述
- 产品调研

## 技术特点

### 智能特性

1. **自适应搜索**: 每轮搜索后由LLM分析结果，智能决定下一步搜索方向
2. **避免重复**: 系统记录已搜索主题，避免重复搜索相同内容
3. **深度推理**: 使用专门的推理模型进行综合分析

### 系统特性

1. **多轮迭代**: 支持指定深度的多轮搜索
2. **并行能力**: 支持最多10个并行搜索
3. **状态管理**: 完整的变量管理和状态跟踪
4. **进度可视**: 实时显示搜索进度和状态

### 集成特性

1. **LLM集成**: 结合GPT-4o进行智能分析，deepseek-reasoner进行深度推理
2. **网络搜索**: 集成web-search技能获取实时网络信息
3. **JSON处理**: 使用JSON解析工具处理结构化数据

## 工作流示例

### 输入示例

```markdown
用户查询: "人工智能在医疗领域的最新发展"
研究深度: 3
```

### 执行流程

1. **第1轮**:
   - LLM分析: 决定搜索"AI医疗诊断最新进展"
   - Web搜索: 执行搜索并收集结果
   - 状态更新: 记录主题，决定继续搜索

2. **第2轮**:
   - LLM分析: 基于第1轮结果，决定搜索"医疗影像AI技术突破"
   - Web搜索: 执行搜索并收集结果
   - 状态更新: 记录主题，决定继续搜索

3. **第3轮**:
   - LLM分析: 基于前两轮结果，决定搜索"AI药物研发应用"
   - Web搜索: 执行搜索并收集结果
   - 状态更新: 记录主题，决定结束搜索

4. **综合分析**:
   - LLM综合分析所有收集到的findings
   - 生成关于"人工智能在医疗领域的最新发展"的详细报告

### 输出示例

```markdown
# 人工智能在医疗领域的最新发展研究报告

## 执行摘要
[基于三轮搜索的综合分析...]

## 主要发现
1. AI在医疗诊断方面的最新进展
   - [具体发现1]
   - [具体发现2]

2. 医疗影像AI技术突破
   - [具体发现3]
   - [具体发现4]

3. AI在药物研发中的应用
   - [具体发现5]
   - [具体发现6]

## 结论与建议
[综合分析结论...]

## 未来研究方向
[基于研究发现提出的未来研究方向...]
```

## 注意事项

### 工作流限制

1. **无执行脚本**: 本skill是一个工作流描述文档，不包含可执行脚本
2. **外部依赖**: 依赖web-search技能执行实际搜索
3. **参数简化**: 搜索时仅使用query参数，忽略其他搜索配置

### 使用建议

1. **深度设置**: 根据研究复杂度设置合适的depth值
2. **查询优化**: 提供清晰具体的研究主题
3. **结果验证**: 对生成的报告进行必要的事实核查

### 最佳实践

1. **渐进式研究**: 从宽泛主题开始，逐步深入具体方向
2. **多源验证**: 结合多个来源的信息进行交叉验证
3. **及时更新**: 对于快速发展的主题，建议定期重新研究

## 故障排除

### 常见问题

1. **搜索无结果**: 检查query是否过于具体或专业，尝试更通用的搜索词
2. **迭代过早结束**: 调整LLM的temperature参数或提供更多上下文
3. **结果重复**: 系统已内置避免重复机制，如仍出现可手动干预

### 性能优化

1. **并行搜索**: 充分利用系统的并行能力（最多10个并行）
2. **缓存利用**: 对于相同主题的多次研究，可考虑结果缓存
3. **增量更新**: 对于持续研究，可采用增量更新策略

---

**重要提示**: 本skill描述了一个深度搜索工作流，实际执行需要依赖外部技能和配置。请确保已正确配置xyz技能和相关LLM服务。

---
name: render-business-graphics
description: 通过随 skill 提供的 Python HTTP 脚本，根据业务语义生成组织、结构、流程、进度、网络、时序、时间轴和数据图表等 SVG 或 PNG 图形。适用于图形分类、色系选择、参考图查询、渲染契约查询、生成 V2 JSON 和调用线上图形渲染服务。
---

# 业务图形与结构化图示生成 Skill

本 skill 负责把用户的业务内容转换为合法的 V2 渲染请求，并提交到图形服务生成 PNG 或 SVG。它适用于投标文件、技术方案、项目管理、汇报材料、系统设计和业务说明等场景。它不是简单的接口封装，而是一套分层的领域导航和数据建模流程：

- `domain/`：先理解业务实体和实体关系，再决定图形家族。
- `references/selection-and-themes.md`：负责类型路由和色系选择。
- `references/graphics/`：逐类说明稳定图形 ID、适用场景、数据结构和限制。
- `scripts/`：查询线上能力、色系、参考图、单图契约，并上传最终 JSON 渲染。

服务只负责校验、布局、配色、分页和栅格化，不理解自然语言。Agent 负责语义理解和数据建模，服务负责确定性渲染。

## 总体硬规则

1. 只使用本 skill 的 Python 脚本和 V2 HTTP 接口，接口说明见 [references/http-api.md](references/http-api.md)。
2. 线上 `/v2/contracts` 和 `/v2/catalog` 是最终事实，优先级高于本 skill 中的示例和静态说明。
3. 只提交业务语义数据，不提交 ECharts option、JavaScript、HTML、自定义 SVG、坐标、远程 URL、文件路径、Base64 资源或渲染器内部配置。
4. 不得臆造图形 ID、variant、枚举值、图标、节点形状或字段。先查目录，再查单图契约。
5. 用户没有指定色系时，完全省略 `theme`。省略会使用服务默认的 `tech-blue`，不能写成 `theme: null` 或空字符串。
6. 不得为了适应版面静默删除节点、连线、任务、事件、参与方、数值或描述。
7. 缺少的层级、分支、依赖、消息端点会改变图形语义时，只问一个明确问题，不要自行推断。
8. 节点文字必须精简：标题、节点、任务、事件使用短语；解释放入 `detail`、`note` 或 `description`。单个节点不要塞入完整句群。

## 标准工作流

### 第 1 步：确认线上服务

默认服务地址是 `https://chart.cqccjy.cn`，也可以用 `CHART_RENDER_BASE_URL` 或 `--base-url` 覆盖。需要鉴权时使用 `CHART_RENDER_API_KEY` 或 `--api-key`。

```bash
python3 scripts/get_capabilities.py
python3 scripts/get_themes.py
```

如果服务查询失败，先报告连接、鉴权或就绪状态，不要切换到未记录的接口。

### 第 2 步：理解业务关系

先读 [domain/README.md](domain/README.md)，再读对应领域文件。先判断“数据之间是什么关系”，不要先凭视觉偏好选图：

| 业务关系 | 图形家族 |
| --- | --- |
| 分类、数值、系列、评分 | `chart.*` |
| 父子职责、组织归属 | `organization` |
| 有向步骤、判断、回退 | `flow.*` |
| 有界的概念结构 | `smartart.*` |
| 工期、前置任务、里程碑 | `schedule.*` |
| 参与方之间的调用与返回 | `sequence` |
| 日期、阶段、历史里程碑 | `timeline.*` |

如果用户给的是多个互相独立的关系，生成多张图，不要把所有内容硬塞进一张复杂图。

### 第 3 步：获取图形类型和参考图

图形类型不明确，或同一类有多个版式时，先查线上目录：

```bash
python3 scripts/get_reference_images.py --output-dir ./graphic-references
python3 scripts/get_reference_images.py --kind smartart --output-dir ./graphic-references/smartart
```

依据返回的稳定 `id`、中文名称、`kind`、`variant`、预览尺寸和本地 SVG 参考图选择版式。完整索引见 [references/graphics/index.md](references/graphics/index.md)。

### 第 4 步：获取单图数据结构

选定稳定 ID 后，必须获取该 ID 的精确 JSON Schema 和示例：

```bash
python3 scripts/get_graphic_contract.py timeline.milestone \
  --preview-output ./graphic-references/timeline.milestone.svg \
  --output ./graphic-contract.json
```

生成请求前必须阅读：

- `parameters.required`：必填字段；
- `parameters.properties`：允许字段；
- `parameters.additionalProperties`：是否拒绝未知字段；
- `parameters.oneOf`、`parameters.$defs`：真实的数组、对象和递归结构；
- `exampleRequest`：可复用的结构骨架，但必须替换全部示例业务内容。

不要只看大类契约。单个目录项可能进一步限定 variant、项目数量、页面方向、比较结构或字段要求。

### 第 5 步：选择色系和页面

选择规则见 [references/selection-and-themes.md](references/selection-and-themes.md)。如果部署版本可能不同，必须调用 `get_themes.py` 获取实际支持的色系。

- 用户指定了合法色系时，原样保留其 ID。
- 工程、施工、实施方案优先考虑工程色系。
- 政务、正式汇报、党建内容优先考虑稳重红色系。
- 黑白打印或复印选择黑白色系。
- 没有指定时省略 `theme`，不要自作主张传入一个静态默认值。
- 没有明确版式要求时省略 `page`，让服务自动选择 A4 方向。
- 预览或插入 Word 使用 PNG，需要矢量输出时使用 SVG。

### 第 6 步：生成语义 JSON

严格按照单图 `parameters` 生成请求，不增加未知字段。常用实体字段如下：

- 图表：`label`、`value`、多系列时增加 `series`；
- 组织：`name`、可选 `role`、`headcount`、`children`；
- 流程：节点 `ref`、`text`，连线 `from`、`to`；
- SmartArt：`title`，可选 `note`、`icon`；
- 排期：`ref`、`name`、`duration`，可选 `predecessors`；
- 时序：参与方 `ref`/`name`，消息 `from`/`to`/`message`；
- 时间轴：`ref`、`date`、`title`，可选 `description`/`position`/`icon`。

技术标识只在契约需要时生成，并保持短且稳定。例如流程图和排期图使用 `A`、`B`、`review`、`service` 这类 ref；不要生成坐标、像素宽高、关键路径样式或内部节点 ID。

### 第 7 步：文字精简检查

在渲染前运行：

```bash
python3 scripts/lint_render_request.py request.json
```

该脚本会区分接口硬上限和“建议更短”的 warning。图形用于文档、汇报或独立图片时，都要求文字短、结构清楚；如果 warning 很多，优先压缩标签，而不是直接 `--strict` 忽略问题。建议目标：

| 文字位置 | 建议长度 |
| --- | --- |
| 图表分类标签 | 14 字以内 |
| 流程节点标题 | 14 字以内 |
| 组织节点名称 | 12 字以内 |
| SmartArt 标题 | 14 字以内 |
| 排期任务名称 | 16 字以内 |
| 时序消息 | 24 字以内 |
| 时间轴事件标题 | 14 字以内 |

压缩时保留业务含义，使用“动词 + 对象”或“名词短语”。例如“完成项目实施方案的内部合规性检查工作”改为“内部合规审查”，详细说明放到 `detail` 或 `description`。不能压缩的关键原文不要擅自改写，应拆图或向用户确认。

### 第 8 步：调用接口渲染

```bash
python3 scripts/render_graphic.py request.json \
  --format png \
  --output output/graphic.png \
  --metadata-output output/graphic.metadata.json
```

`rasterScale: 1` 只用于快速预览；普通 PNG 省略该字段，服务默认 2 倍；高清打印使用 3。渲染完成后检查图片和 metadata。写入 Word 时使用 `X-Display-Width-Mm`，不要把 PNG 像素宽度当成毫米。

## 图形导航

完整 ID 索引见 [references/graphics/index.md](references/graphics/index.md)。各类详细说明：

- [chart.md](references/graphics/chart.md)：7 种数值图表和矩阵完整性；
- [organization.md](references/graphics/organization.md)：嵌套组织树、方向和层级限制；
- [flow.md](references/graphics/flow.md)：线性流程、复杂流程、节点形状、反馈和自适应画布；
- [smartart.md](references/graphics/smartart.md)：9 种 SmartArt、数量限制、中心节点、图标和对比结构；
- [schedule.md](references/graphics/schedule.md)：甘特图、网络图、依赖模式和显式起始模式；
- [sequence.md](references/graphics/sequence.md)：参与方、调用、返回、备注和限制；
- [timeline.md](references/graphics/timeline.md)：9 种时间轴版式共用的事件模型。

## 错误恢复

- **ID 或 variant 不存在**：重新查询目录，不要猜测。
- **字段或枚举错误**：重新读取单图 `parameters`，删除或修正错误字段。
- **关系缺失**：询问用户，不要伪造连线、前置任务或消息端点。
- **图表矩阵不完整**：补齐业务数据，或改用不要求完整矩阵的图表。
- **排期依赖错误**：修正 ref 或循环关系，不要画一条假的依赖线。
- **鉴权或网络错误**：报告错误并保留 API Key 配置。
- **版面溢出**：先省略 `page` 重试自动方向，再考虑横版或拆分图形；不要静默缩小、截断或删除内容。
- **渲染成功**：只有脚本实际写入文件后，才能向用户报告输出路径。

## Python 脚本索引

| 脚本 | 作用 |
| --- | --- |
| `get_capabilities.py` | 获取当前 kind、variant、色系、页面、默认值，或完整 V2 契约 |
| `get_themes.py` | 获取 `/v1/themes` 的实际色系 ID |
| `get_reference_images.py` | 获取图形目录并保存参考 SVG |
| `get_graphic_contract.py` | 获取单个图形 ID 的精确 Schema、示例和参考图 |
| `lint_render_request.py` | 检查请求基本结构和文字长度 |
| `render_graphic.py` | POST 到 `/v2/render/png` 或 `/v2/render/svg` |

脚本只使用 Python 标准库，共享 `_client.py`，不会在上传前偷偷修改请求 JSON。

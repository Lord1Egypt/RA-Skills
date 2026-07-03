# 交通标准知识库 (traffic-standards-kb)

## 简介

**traffic-standards-kb** 是一个面向Agent的Skill，用于在编写中国智慧交通解决方案或技术方案时，自动检索和引用相关的国家标准（GB）、交通行业标准（JT）、公共安全行业标准（GA）等。

该技能通过 Solvex API 查询 RAG 知识库，将自然语言问题转化为标准文献检索，并以规范格式返回标准编号、标题、执行单位、适用范围等信息，便于在方案中直接引用。

## 安装

```bash
# 全局安装（所有项目可用）
npx skills add solvex-top/solvex-skills@traffic-standards-kb -g -y

# 安装到当前项目
npx skills add solvex-top/solvex-skills@traffic-standards-kb -y

# 更新到最新版本
npx skills update traffic-standards-kb

# 卸载
npx skills remove traffic-standards-kb
```

**仓库地址：** https://github.com/solvex-top/solvex-skills

## 适用场景

| 场景 | 关键词示例 |
|------|-----------|
| 智慧路口 | 交通信号、自适应信号、信号控制 |
| 智能停车 | 停车诱导、路侧停车、停车场管理 |
| 交通监控 | 电子警察、违章抓拍、车牌识别 |
| 数据采集 | 交通检测、流量检测、地磁、雷达 |
| 电子收费 | ETC、不停车收费 |
| 智慧高速 | 高速监控、智慧高速 |
| 智慧服务区 | 服务区设施、智慧服务 |
| 智慧公交 | BRT、公交优先、智能调度 |
| 车路协同 | V2X、V2V、V2I、C-V2X |
| 出行服务 | MaaS、出行即服务 |
| 新兴领域 | 智能交通、综合交通 |

**触发条件：** 当用户编写上述领域的解决方案、技术方案、投标文件或任何需要引用行业标准的文档时，应主动使用本技能检索相关标准。

## 工作流程

```
用户任务（如：编写智慧路口解决方案）
       ↓
Claude 解析任务，提取领域关键词
       ↓
调用 Solvex API /api/v1/standards/query
       ↓
RAG SearchBots API（两步检索）
  ├─ Step 1: GET /api/v1/searchbots/detail?search_id={search_id}
  │           → 获取 kb_ids（知识库ID列表）
  └─ Step 2: POST /api/v1/searchbots/retrieval_test
                → 使用 kb_ids 和 search_id 执行检索
       ↓
返回标准列表 → 格式化引用 → 插入方案文档
```

## 前置条件

### 1. 获取 API Key

访问 [https://solvexpert.net](https://solvexpert.net) 注册并获取 API Key。

### 2. 配置 API Key

三种配置方式（按优先级排序）：

| 优先级 | 配置方式 | 适用场景 |
|--------|---------|---------|
| 1 | Shell 环境变量 | Bash 命令调用 API |
| 2 | `~/.claude/settings.json` | Claude 内部使用 |
| 3 | 请求头手动传入 | 临时使用 |

**方式一：Shell 环境变量（推荐用于 Bash 命令）**

```bash
export STANDARDS_API_KEY="solvex-your-api-key"  # 替换为实际 API Key
```

> **注意：** 请将示例中的 `solvex-your-api-key` 替换为从 https://solvexpert.net 获取的实际 API Key。

**方式二：Claude settings.json（推荐用于 Claude 内部调用）**

```json
{
  "env": {
    "STANDARDS_API_KEY": "solvex-your-api-key"
  }
}
```

> **注意：** `settings.json` 中的环境变量不会自动传递给 Bash 命令。如果需要在 Bash 中调用 API，必须在 Shell 中 export 或在命令中显式传递。

## API 使用说明

### 请求地址

```
POST https://solvexpert.net/api/v1/standards/query
```

### 认证方式

请求需要**同时**提供两种认证：

1. **请求头：** `X-API-Key: $STANDARDS_API_KEY`
2. **请求体参数：** `searchAuthToken: "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"`（必须）

> 缺少 `searchAuthToken` 会导致 `"Authentication error: API key is invalid!"` 错误，即使 API Key 有效。

### 请求参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `question` | string | 是 | 自然语言查询 | - |
| `searchAuthToken` | string | 是 | SearchBots 认证令牌 | `Thn5ItDQS9aEa3cay-855l2woSmW2Z4U` |
| `domains` | string[] | 否 | 领域过滤，不填则自动检测 | 自动检测 |
| `depth` | string | 否 | 检索深度：`basic`/`medium`/`full` | `medium` |
| `searchId` | string | 否 | 搜索应用 ID（推荐使用默认值） | `4d68cee6226611f19327c66d7f7cba76` |
| `pageSize` | int | 否 | 每页结果数（1-100） | 根据 depth 自动映射 |
| `similarityThreshold` | double | 否 | 相似度阈值（0.0-1.0） | `0.5` |

### 检索深度说明

| depth | pageSize | 返回内容 |
|-------|----------|---------|
| `basic` | 5 | 标准号 + 标题 + 执行单位 + 适用范围 |
| `medium` | 10 | basic + 归口单位 + 发布/实施日期 + 关键条款 |
| `full` | 30 | medium + 完整元数据 + AI 要点总结 + 条文索引 |

### 有效领域值

- `信号控制`
- `停车系统`
- `交通监控`
- `数据采集`
- `收费系统`
- `公共交通`
- `车路协同`
- `出行服务`
- `交通管理`
- `新兴领域`

### 请求示例

```bash
curl -s -X POST "https://solvexpert.net/api/v1/standards/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $STANDARDS_API_KEY" \
  -d '{
    "question": "智慧高速及智慧服务区相关的标准",
    "domains": ["新兴领域"],
    "depth": "medium",
    "searchId": "4d68cee6226611f19327c66d7f7cba76",
    "searchAuthToken": "Thn5ItDQS9aEa3cay-855l2woSmW2Z4U"
  }' | python3 -m json.tool
```

### 响应格式

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "standards": [
      {
        "standardNumber": "GB 14886-2016",
        "title": "道路交通信号灯设置与安装规范",
        "similarity": 0.92,
        "content": "..."
      }
    ],
    "total": 10
  }
}
```

> **说明：** 不同 `depth` 级别返回的字段不同。`basic` 返回标准号、标题、执行单位、适用范围；`medium` 额外返回归口单位、发布/实施日期、关键条款（`keyPoints`）；`full` 返回所有元数据字段（见「标准元数据字段」章节）。`aggregations` 字段仅在存在聚合结果时返回。

### 引用格式

在方案文档中引用标准时，使用以下格式：

```
[1] GB 14886-2016 道路交通信号灯设置与安装规范
[2] GA/T 1400-2017 公安视频监控联网系统
[3] JT/T 1353-2020 公路工程标准体系
```

## 常见问题与错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `401 Unauthorized` | 缺少或无效的 API Key | 检查 `X-API-Key` 请求头是否正确设置 |
| `"Authentication error: API key is invalid!"` | 缺少 `searchAuthToken` | 确保请求体中包含 `searchAuthToken` 参数 |
| `504 Gateway Timeout` | 请求超时（RAG API 响应慢） | 降低 `depth` 参数，或等待后重试 |
| 空的标准数组 | 知识库中无匹配文档 | 检查查询关键词，尝试更换领域或调整问题 |
| `400 Bad Request` | 参数值无效 | 检查 `depth` 只能为 basic/medium/full，`pageSize` 在 1-100 之间 |

## 标准元数据字段

RAG 知识库中的标准文档包含以下元数据：

| 字段 | 说明 | 示例 |
|------|------|------|
| `standard_number` | 标准编号 | GB 14886-2016 |
| `title` | 标准标题 | 道路交通信号灯设置与安装规范 |
| `executing_unit` | 执行单位 | 中华人民共和国公安部 |
| `committee` | 归口单位 | 全国交通工程设施（公路）标准化技术委员会 |
| `drafting_unit` | 起草单位 | 公安部交通管理科学研究所 |
| `drafters` | 起草人 | ["张三", "李四"] |
| `publish_date` | 发布日期 | 2016-12-13 |
| `implement_date` | 实施日期 | 2017-07-01 |
| `replaces` | 替代标准 | GB 14886-2006 |
| `scope` | 适用范围 | 本标准规定了... |
| `category` | 分类 | 信号控制 |
| `level` | 标准层级 | 国家标准/行业标准/地方标准/国际标准 |

## 常见领域与对应标准

| 领域 | 关键词 | 典型标准 |
|------|--------|---------|
| 信号控制 | 智慧路口、交通信号、自适应信号 | GB series, GB series |
| 停车系统 | 智能停车、停车诱导、路侧停车 | GB/T series, JT/T series |
| 交通监控 | 电子警察、违章抓拍、车牌识别 | GA/T series, GB/T series |
| 数据采集 | 交通检测、流量检测、地磁、雷达 | JT/T series, GB/T series |
| 收费系统 | ETC、电子收费 | JT/T series, JTG series |
| 智慧高速 | 智慧高速、高速监控 | JT/T series, JT/T series |
| 智慧服务区 | 智慧服务区、服务区设施 | JTJ series, JT/T series |
| 公共交通 | 智慧公交、BRT、公交优先 | JT/T series |
| 车路协同 | V2X、V2V、V2I、C-V2X | GB/T series, YD/T series |
| 出行服务 | MaaS、出行即服务 | JT/T series |
| 新兴领域 | 新兴领域、智能交通 | GB/T, JT/T, GA/T series |

## 常见误区与真相

| 误区 | 真相 |
|------|------|
| "标准引用可以在最后添加" | 没有标准的方案会被认为不专业，可能直接被拒绝 |
| "我记得主要标准号" | 记忆不准确，GB 标准经常更新，引用错误版本会有问题 |
| "这个项目很简单不需要" | 即使小型项目也需要合规性声明，标准引用体现专业性 |
| "用户没有明确要求" | 行业标准是隐含要求，主动引用体现专业素养 |
| "时间太紧了" | 查询标准只需几秒，但缺少标准可能导致方案被拒 |

## 警示信号 — 必须引用标准

如果出现以下任何想法，**立即停下来检索并引用相关标准**：

- "这个很简单，不需要标准"
- "我凭记忆写就行"
- "用户没要求就不用加"
- "先写框架，后面再补"
- "这个领域不强制标准"
- "我是专家，按我的来"

**以上所有情况都意味着：必须引用相关标准。无例外。**

## 文件结构

```
.claude/skills/traffic-standards-kb/
├── SKILL.md              # 技能主文件（触发条件、使用指南、常见错误）
├── api-reference.md      # API 详细参考文档（认证、参数、架构）
└── README.md             # 本说明文档
```

## 最佳实践

1. **主动检索：** 编写智慧交通方案时，不要等用户要求，应主动检索并引用相关标准
2. **验证响应：** 调用 API 后检查 `code == 0` 且 `data.standards` 非空
3. **统一引用格式：** 使用 `[1]` `[2]` `[3]` 的标准引用格式
4. **不要绕过 API：** 必须通过 Solvex API 查询，不要直接调用 RAG API
5. **注意版本：** GB 标准经常更新，不要凭记忆引用，务必通过 API 确认最新版本号
6. **多个领域组合：** 编写综合方案时，可多次调用 API 覆盖不同领域

# Tavily API 完整文档
版本：v1.0.0
最后更新：2026-03-14

## 端点列表
| 端点 | 方法 | 功能 | 信用点消耗 |
|------|------|------|------------|
| `/search` | POST | 网页搜索 | 1-2 |
| `/extract` | POST | 网页内容提取 | 1/5个URL（基础）/ 2/5个URL（高级） |
| `/crawl` | POST | 整站爬取 | 1/10个页面（无指令）/ 2/10个页面（有指令） |
| `/research` | POST | 创建深度研究任务 | 10+ |
| `/research/{request_id}` | GET | 查询研究任务结果 | 0 |
| `/usage` | GET | 用量查询 | 0 |

## 更新日志
### v1.0.0 (2026-03-14)
- ✅ 修复 Crawl API 参数错误：`root_url` → `url`
- ✅ 修复 Research API 参数错误：`topic` → `input`，`citation_style` → `citation_format`
- ✅ 修复 Extract API 响应格式：结果从字典类型改为列表类型，字段名 `content` → `raw_content`
- ✅ 所有核心功能测试通过

## 错误码说明
| 错误码 | 含义 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | API Key 无效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 429 | 超出速率限制 |
| 432 | 内容政策违规 |
| 433 | 搜索查询违反服务条款 |
| 500 | 服务器内部错误 |

## 速率限制
| 套餐 | 速率限制 | 月度额度 |
|------|----------|----------|
| Free/Researcher | 10请求/分钟 | 1000信用点 |
| Project | 30请求/分钟 | 4000信用点 |
| Bootstrap | 100请求/分钟 | 15000信用点 |
| Startup | 300请求/分钟 | 38000信用点 |
| Growth | 1000请求/分钟 | 100000信用点 |
| Enterprise | 可定制 | 可定制 |

## 各API详细说明

### 1. Search API
**功能**：网页搜索，支持多维度过滤
**请求参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜索关键词 |
| `search_depth` | enum | ❌ | `basic` | 搜索深度：`basic`/`advanced`/`fast`/`ultra-fast` |
| `chunks_per_source` | integer | ❌ | 3 | 每个来源返回的片段数量（1-3，仅advanced有效） |
| `max_results` | integer | ❌ | 5 | 返回结果数量（0-20） |
| `topic` | enum | ❌ | `general` | 搜索主题：`general`/`news`/`finance` |
| `time_range` | enum | ❌ | - | 相对时间范围：`day`/`week`/`month`/`year` |
| `start_date` | string | ❌ | - | 开始日期，格式YYYY-MM-DD |
| `end_date` | string | ❌ | - | 结束日期，格式YYYY-MM-DD |
| `include_answer` | boolean/string | ❌ | false | 包含直接答案：`true`/`basic`/`advanced` |
| `include_raw_content` | boolean/string | ❌ | false | 包含原始内容：`true`/`markdown`/`text` |
| `include_images` | boolean | ❌ | false | 包含图片结果 |
| `include_image_descriptions` | boolean | ❌ | false | 包含图片描述 |
| `include_favicon` | boolean | ❌ | false | 包含网站图标 |
| `include_domains` | array | ❌ | - | 限定搜索的域名列表（最多300个） |
| `exclude_domains` | array | ❌ | - | 排除的域名列表（最多150个） |
| `country` | string | ❌ | - | 优先返回的国家/地区 |
| `auto_parameters` | boolean | ❌ | false | 自动参数优化 |
| `exact_match` | boolean | ❌ | false | 精确匹配查询短语 |
| `include_usage` | boolean | ❌ | false | 包含用量信息 |

---

### 2. Extract API
**功能**：批量提取指定URL的结构化内容
**请求参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `urls` | string/array | ✅ | - | 要提取的URL列表 |
| `query` | string | ❌ | - | 关键词，用于重排内容片段 |
| `chunks_per_source` | integer | ❌ | 3 | 每个URL返回的片段数量（1-5） |
| `extract_depth` | enum | ❌ | `basic` | 提取深度：`basic`/`advanced` |
| `include_images` | boolean | ❌ | false | 包含图片 |
| `include_favicon` | boolean | ❌ | false | 包含网站图标 |
| `format` | enum | ❌ | `markdown` | 输出格式：`markdown`/`text` |
| `timeout` | float | ❌ | - | 超时时间（1-60秒） |
| `include_usage` | boolean | ❌ | false | 包含用量信息 |

---

### 3. Crawl API
**功能**：整站爬取，自动遍历所有相关页面
**请求参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `url` | string | ✅ | - | 根URL |
| `instructions` | string | ❌ | - | 自然语言爬取指令 |
| `chunks_per_source` | integer | ❌ | 3 | 每个页面返回的片段数量（1-5，仅当有instructions时有效） |
| `max_depth` | integer | ❌ | 1 | 最大爬取深度（1-5） |
| `max_breadth` | integer | ❌ | 20 | 每层最大链接数（1-500） |
| `limit` | integer | ❌ | 50 | 总爬取页面上限 |
| `select_paths` | array | ❌ | - | 路径正则白名单 |
| `select_domains` | array | ❌ | - | 域名正则白名单 |
| `exclude_paths` | array | ❌ | - | 路径正则黑名单 |
| `exclude_domains` | array | ❌ | - | 域名正则黑名单 |
| `allow_external` | boolean | ❌ | true | 允许爬取外部域名 |
| `include_images` | boolean | ❌ | false | 包含图片 |
| `extract_depth` | enum | ❌ | `basic` | 提取深度：`basic`/`advanced` |
| `format` | enum | ❌ | `markdown` | 输出格式：`markdown`/`text` |
| `include_favicon` | boolean | ❌ | false | 包含网站图标 |
| `timeout` | float | ❌ | 150 | 超时时间（10-150秒） |
| `include_usage` | boolean | ❌ | false | 包含用量信息 |

---

### 4. Research API
**功能**：生成深度研究报告（异步）
#### 4.1 创建研究任务
**端点**：`POST /research`
**请求参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `input` | string | ✅ | - | 研究主题 |
| `model` | enum | ❌ | `auto` | 研究模型：`mini`/`pro`/`auto` |
| `stream` | boolean | ❌ | false | 流式返回结果 |
| `output_schema` | object | ❌ | - | 自定义输出JSON Schema |
| `citation_format` | enum | ❌ | `numbered` | 引用格式：`numbered`/`mla`/`apa`/`chicago` |

#### 4.2 查询研究结果
**端点**：`GET /research/{request_id}`
**路径参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `request_id` | string | ✅ | 研究任务ID |

**任务状态**：
- `pending`：任务排队中
- `running`：研究进行中
- `completed`：完成
- `failed`：失败

---

### 5. Usage API
**功能**：查询用量统计
**端点**：`GET /usage`
**响应字段**：
```json
{
  "key": {
    "usage": 150,
    "limit": 1000,
    "search_usage": 100,
    "extract_usage": 25,
    "crawl_usage": 15,
    "map_usage": 7,
    "research_usage": 3
  },
  "account": {
    "current_plan": "Researcher",
    "plan_usage": 500,
    "plan_limit": 15000,
    "paygo_usage": 25,
    "paygo_limit": 100,
    "search_usage": 350,
    "extract_usage": 75,
    "crawl_usage": 50,
    "map_usage": 15,
    "research_usage": 10
  }
}
```

## 最佳实践
### 搜索优化
1. **深度选择**：普通查询用`basic`，高精度需求用`advanced`，实时查询用`fast`/`ultra-fast`
2. **新闻查询**：设置`topic: "news"` + `time_range: "day"`获取最新内容
3. **成本优化**：限制`max_results`到实际需要的数量，关闭不需要的`include_*`参数
4. **中文搜索**：设置`country: "china"`提升结果相关性

### 提取优化
1. 批量提取多个URL时优先使用`extract` API，比单独爬取成本低5倍
2. 需要精准内容时使用`query`参数，自动重排最相关的片段
3. 复杂页面使用`extract_depth: "advanced"`提取表格和嵌入内容

### 爬取优化
1. 明确爬取范围时使用`select_paths`/`exclude_paths`减少无效爬取
2. 整站文档爬取设置`max_depth: 3`+`limit: 100`平衡覆盖度和成本
3. 自然语言指令可以精准筛选需要的内容，如"只爬取API文档页面"

### 研究优化
1. 简单主题用`model: "mini"`，复杂多领域主题用`model: "pro"`
2. 自定义`output_schema`可以直接得到结构化的研究结果，无需额外解析
3. 研究任务平均耗时2-5分钟，建议异步查询结果
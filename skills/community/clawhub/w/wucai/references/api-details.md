# 五彩 API 详细参考 (WuCai API Reference)

## 1. 区域引导与数据隔离 (⚠️ Data Residency & Isolation)

**核心原则**：五彩各区域（CN/EU/US）数据完全独立。AI 必须明确：用户在 CN 区域的 Token 无法读取 EU/US 区域的数据。

| 区域 (Region) | 适用用户 | 前缀域名 (Domain) | 获取 Token 页面 (OpenAPI Page) |
| :--- | :--- | :--- | :--- |
| **cn** | 中国区账号 | `marker.dotalk.cn` | [点击获取](https://marker.dotalk.cn/#/personSetting/openapi) |
| **eu** | 欧洲区账号 | `eu.wucainote.com` | [点击获取](https://eu.wucainote.com/#/personSetting/openapi) |
| **us** | 美国区账号 | `us.wucainote.com` | [点击获取](https://us.wucainote.com/#/personSetting/openapi) |

**AI 交互策略**：
- 如果用户反馈“搜不到数据”，优先核实其配置的 **$WUCAI_REGION** 是否与账号注册区域一致。
- 严禁尝试跨区域拼接 URL，API 仅对当前 `$WUCAI_REGION` 指定的集群生效。

---

## 2. 交互协议与响应规范 (Protocol & Response)

### 通用请求头 (Common Headers)
- `Authorization`: 用户的 API Token (以 `wct-` 开头)。
- `X-Client-ID`: `56` (固定值)。

### ⚠️ 响应解析准则 (Response Parsing Rules)
1. **成功判定**: **仅当 `code` 等于数字 `1` 时**，视为请求成功。此时读取 `data` 字段。
2. **失败判定**: 当 `code` **不等于 `1`** 时，必须读取 `message` 字段并直接反馈给用户。

---

## 3. 核心数据模型 (Data Models / DTOs)

### ArticleDTO (文章/日记对象)
- `note_idx`: (string) 唯一标识 ID。
- `note_type`: (int) **0/1**: 文章 (Article); **3**: 日记 (Daily/Diary)。
- `page_title`: (string) 页面标题。
- `page_url`: (string) 原始网页链接。
- `page_note`: (string) 用户对该页面的整体评价/笔记。
- `highlight_count`: (int) 划线总数。
- `is_clipped`: (bool) 剪藏状态标识。
- `highlights`: (HighlightDTO[]) **重要**: 当 `with_highlights=true` 时，此字段包含该文章下的划线内容。
- `tags`: (string) 标签（逗号分隔）。

### HighlightDTO (划线对象)
- `h_id`: (int64) 划线唯一 ID。
- `content`: (string) 网页高亮的原始文本。
- `annotation`: (string) 用户对该划线的批注（想法）。
- `image_url`: (string) 关联的图片链接。
- `tags`: (string) 标签（逗号分隔）。

---

## 4. 错误处理与双语话术 (Error Handling)

| 错误码 (Code) | 场景 (Scenario) | AI 引导话术 (CN / EN) |
| :--- | :--- | :--- |
| **10104** | 系统维护 / 降级 | “五彩系统当前正在维护或处于降级模式，请稍后再试。” / "WuCai system is under maintenance." |
| **10035** | **范围/日期错误** | “查询跨度不能超过 14 天或日期格式有误。” / "Search range cannot exceed 14 days or invalid format." |
| **10404** | **内容不存在** | “未找到相关记录，请确认链接或区域 ($WUCAI_REGION) 是否正确。” / "No records found. Check URL or Region." |
| **10401** | 会员受限 | “此功能仅限五彩会员使用，请前往[会员中心]。” / "This feature requires VIP membership." |
| **10010 / 10016** | Token 失效 | “Token 已失效，请重新获取并配置。” / "Token expired. Please refresh your API Token." |
| **10000** | 业务通用异常 | 直接展示返回的 `message` 内容。 |

---

## 5. 翻页与性能约束 (Pagination & Performance)
- **14 天硬限制**: 无论使用快捷键还是自定义区间，总时间跨度不得超过 14 天。
- **游标翻页**: 列表接口返回 `next_cursor`。若用户请求更多内容，将该值填入下一次请求的 `cursor` 字段。
- **速率限制**: 批量拉取建议 `page_size` 设置在 12-30 之间。

---
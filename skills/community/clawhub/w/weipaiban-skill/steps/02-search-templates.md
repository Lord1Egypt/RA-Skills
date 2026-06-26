# Step 2：搜索模板

## 前置读取

从任务目录读取 `meta.json`，获取 `tags` 和 `keywords` 用于搜索。

---

采用分路检索 + 合并去重 + 默认兜底策略搜索微排版模板库，确保尽可能找到匹配的模板。

## 参数说明

- `tags`：Step 1 中匹配到的类别标签（来自 meta.json），支持多选（如 `tags=节日&tags=推荐`）
- `search`：主题关键词（来自 meta.json 的 keywords），按标题模糊匹配
- 本步骤首轮搜索分为两路：仅 `search` 与仅 `tags`，每路最多取 5 条
- **重要**：所有查询参数中的中文值必须进行 URL 编码。使用 curl 时请使用 `-G --data-urlencode` 自动处理编码。

## 执行门禁（必须遵守）

- 本文所有命令均为**受控执行模板**，仅在用户已明确进入微排版任务并同意继续时才可执行
- 命令中的占位值（如 `关键词`、`类别标签`）必须先由当前任务数据替换，再执行
- 若用户要求暂停、改词或终止，必须先停止调用 API，再等待下一次明确指令

## 数据发送范围（透明披露）

- 请求目标：`${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/templates*`
- 发送字段：`Authorization` 头（Bearer Token）与查询参数（`search`、`tags`、`per_page`）
- 不发送内容：任务目录中的本地文件（如 `elements.json`、`template-profile.json`）及图片二进制

## 搜索策略（按顺序执行）

### 2.1 分路搜索：仅 search + 仅 tags 并行

同时发起以下两个请求，每路 `per_page=5`：

#### 请求 A：仅关键词搜索（search）

```bash
# 受控执行模板：执行前确认用户已同意继续
curl -s -G -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  --data-urlencode "search=关键词" \
  --data-urlencode "per_page=5" \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/templates"
```

#### 请求 B：仅标签搜索（tags）

```bash
# 受控执行模板：执行前确认用户已同意继续
curl -s -G -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  --data-urlencode "tags=类别标签" \
  --data-urlencode "per_page=5" \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/templates"
```

> 如果有多个 `tags`，可在一个请求中传多个 `tags` 参数；也可按标签逐个请求后再合并，最终都按模板 ID 去重。

### 2.2 合并结果并展示给用户

将两路结果按模板 ID 去重合并后展示给用户，展示上限为最多 10 个。

- 合并结果非空：告知用户"已分别按关键词和分类标签搜索，并合并结果供您选择。"
- 合并结果为空：进入 2.3 兜底方案

### 2.3 兜底方案：使用默认模板

两路搜索合并后仍无结果时，通过 API 获取系统默认模板：

```bash
# 受控执行模板：执行前确认用户已同意继续
curl -s -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/templates/default"
```

告知用户："未找到匹配模板，将使用默认模板为您创建作品。"展示默认模板的信息，确认后直接进入 Step 3。

## 响应格式

搜索接口响应格式详见 [references/api-formats.md](../references/api-formats.md#模板搜索响应)。

## 展示格式

将搜索结果展示给用户，每个模板以简短信息进行一行展示：

1. 【[tags]】标题 + 模板预览网址（如：【节日】清明节模板 - ${WEIPAIBAN_API_BASE}/templates/${模板ID}）

> 展示数量上限：最多 10 个（两路各取前 5，合并去重后展示）。
>
> ⏸️ **交互点**：展示搜索结果列表，等待用户明确选择一个模板后才能继续。用户也可以要求更换关键词或标签后重新搜索。**必须等到用户回复后再执行 Step 3，禁止自动选择模板。**

## 后置写入

用户选择模板后，更新任务目录 `meta.json`：将 `templateId` 设为选中的模板 ID，`currentStep` 更新为 `"02"`。

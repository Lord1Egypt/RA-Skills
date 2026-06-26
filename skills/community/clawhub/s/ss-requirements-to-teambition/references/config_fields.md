# 配置项获取指南

## SaleSmartly 配置

### API Key
SS 后台 → 设置 → API 管理 → 创建/查看 API Key

### Project ID
SS 后台 URL 中的数字，如 `https://xxx.salesmartly.com/project/1/...` 中的 `1`

### 标签 ID
SS 后台 → 设置 → 会话标签 → 点击标签，URL 中可见 tagId

### 自定义字段 Key
SS 后台 → 客户 → 自定义字段 → 查看字段名称（如"项目ID"），填入 `customFieldKey`

---

## Teambition 配置

### projectId
打开 TB 项目 → URL 中 `projectId=xxx` 或 `/project/xxx` 的部分

### sfcId（任务类型 ID）
TB 项目 → 项目设置 → 任务类型 → 点击类型，URL 中可见 sfcId

### stageId（任务列表 ID）
TB 项目看板 → 点击目标列的列头设置 → URL 中可见 stageId

### 自定义字段 ID（cfId）
TB 项目 → 项目设置 → 自定义字段 → 点击字段，URL 中可见 cfId

### 自定义字段值 ID（valueId）
对于单选/多选字段，在自定义字段设置中点击选项，URL 中可见 valueId

---

## 快速获取技巧

如果不想手动找 ID，可以直接对 AI 说：

> 「帮我查一下 TB 项目『XXX』的任务类型有哪些，列出 sfcId」
> 「帮我查一下 TB 项目『XXX』的自定义字段有哪些，列出 cfId」

AI 会通过 MCP 工具帮你查。
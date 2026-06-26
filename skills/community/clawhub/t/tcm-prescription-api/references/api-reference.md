# 中医药方剂 API 完整参考文档

## 基本信息

- **API 基础地址**：`https://119.91.226.122/api`
- **网站首页**：`https://119.91.226.122`
- **数据格式**：JSON
- **字符编码**：UTF-8
- **速率限制**：每分钟 100 次请求

## 认证方式

### API Key 认证

注册用户可在网站上生成 API Key。

传递方式：
- 请求头：`X-API-Key: $TCM_API_KEY`（推荐通过环境变量配置）
- 查询参数：`?api_key=$TCM_API_KEY`

### 认证级别

| 级别 | 可访问接口 |
|------|-----------|
| 无认证 | 搜索方剂、方剂分类、方剂详情（部分字段） |
| API Key | 完整方剂搜索、完整方剂详情、症状推荐 |

### API Key 状态查询

查询 API Key 是否有效（公开接口）：

```bash
curl -s "https://119.91.226.122/api/api-keys/status?key=$TCM_API_KEY"
```

---

## 接口详情

### 1. 方剂查询

#### GET /api/prescriptions/search

搜索方剂。支持 API Key 可选认证。

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q / keyword | string | 否 | 搜索关键词 |
| category | string | 否 | 方剂分类筛选 |
| page | number | 否 | 页码，默认 1 |
| limit / pageSize | number | 否 | 每页条数，默认 20 |

**请求示例：**

```bash
# 基本搜索
curl -s "https://119.91.226.122/api/prescriptions/search?q=桂枝"

# 按分类搜索
curl -s "https://119.91.226.122/api/prescriptions/search?category=解表剂&page=1&limit=10"

# 带 API Key 的搜索（获取更完整数据）
curl -s "https://119.91.226.122/api/prescriptions/search?q=麻黄" \
  -H "X-API-Key: $TCM_API_KEY"
```

**响应示例：**

```json
{
  "success": true,
  "message": "搜索成功",
  "data": {
    "prescriptions": [
      {
        "id": 1,
        "name": "桂枝汤",
        "name_en": "Guizhi Tang",
        "name_alias": "桂枝加芍药汤",
        "category": "解表剂",
        "composition": "桂枝、芍药、甘草、生姜、大枣",
        "function": "解肌发表，调和营卫",
        "indications": "外感风寒表虚证",
        "source": "《伤寒论》"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 1,
      "totalPages": 1
    }
  }
}
```

#### GET /api/prescriptions/:id

获取方剂详情。支持 API Key 可选认证。

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | number | 方剂 ID |

**请求示例：**

```bash
curl -s "https://119.91.226.122/api/prescriptions/1" \
  -H "X-API-Key: $TCM_API_KEY"
```

**响应示例：**

```json
{
  "success": true,
  "message": "获取方剂详情成功",
  "data": {
    "id": 1,
    "name": "桂枝汤",
    "name_en": "Guizhi Tang",
    "name_alias": "桂枝加芍药汤",
    "category": "解表剂",
    "subcategory": "辛温解表",
    "composition": "桂枝三两（9g）、芍药三两（9g）、甘草二两炙（6g）、生姜三两切（9g）、大枣十二枚擘（4枚）",
    "function": "解肌发表，调和营卫",
    "indications": "外感风寒表虚证。头痛发热，汗出恶风，鼻鸣干呕，苔白不渴，脉浮缓或浮弱。",
    "analysis": "本证由外感风寒，营卫不和所致...",
    "song": "桂枝汤治太阳风，芍药甘草姜枣同...",
    "usage": "上五味，咀三味，以水七升，微火煮取三升，去滓，适寒温，服一升。",
    "contraindications": "表实无汗，或表寒里热者禁用。",
    "modifications": "若气虚者，加黄芪、人参益气扶正...",
    "source": "《伤寒论》",
    "is_pro": false
  }
}
```

#### GET /api/prescriptions/categories

获取所有方剂分类。

**请求示例：**

```bash
curl -s "https://119.91.226.122/api/prescriptions/categories"
```

**响应示例：**

```json
{
  "success": true,
  "message": "获取方剂分类成功",
  "data": [
    {
      "name": "解表剂",
      "name_en": "Diaphoretic Formulas",
      "count": 15,
      "subcategories": ["辛温解表", "辛凉解表", "扶正解表"]
    },
    {
      "name": "泻下剂",
      "name_en": "Purgative Formulas",
      "count": 8,
      "subcategories": ["寒下", "温下", "润下", "逐水", "攻补兼施"]
    }
  ]
}
```

#### POST /api/prescriptions/recommend

根据症状推荐方剂。需要 API Key 认证。系统会同时对 `indications`（主治）和 `description`（功用）字段进行关键词匹配，按匹配症状数量降序排序。

**请求体：**

```json
{
  "symptoms": ["头痛", "发热", "恶风", "汗出"]
}
```

**请求示例：**

```bash
curl -s -X POST "https://119.91.226.122/api/prescriptions/recommend" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TCM_API_KEY" \
  -d '{"symptoms": ["头痛", "发热", "恶风", "汗出"]}'
```

**响应示例：**

```json
{
  "code": 0,
  "message": "推荐方剂成功",
  "data": {
    "symptoms": ["头痛", "发热"],
    "recommendations": [
      {
        "id": 1,
        "name": "桂枝汤",
        "category": "解表剂",
        "description": "辛温解表，调和营卫",
        "indications": "外感风寒表虚证。症见头痛、发热、恶风、汗出、鼻鸣、干呕、脉浮缓。",
        "matchScore": 2
      }
    ],
    "message": "找到 1 个相关方剂"
  }
}
```

`matchScore` 表示匹配到的症状数量，分数越高表示与用户描述的症状越相关。

---

### 2. API Key 管理

#### GET /api/api-keys/status

查询 API Key 状态（公开接口，无需认证）。

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | API Key |

**请求示例：**

```bash
curl -s "https://119.91.226.122/api/api-keys/status?key=$TCM_API_KEY"
```

---

### 3. 健康检查

#### GET /health

检查服务状态。

```bash
curl -s "https://119.91.226.122/health"
```

**响应示例：**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "uptime": 86400
}
```

---

## 错误响应格式

```json
{
  "success": false,
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

### 常见错误码

| 错误码 | HTTP 状态码 | 说明 |
|--------|------------|------|
| NO_API_KEY | 401 | 未提供 API Key |
| API_KEY_NOT_FOUND | 401 | API Key 不存在 |
| API_KEY_REVOKED | 401 | API Key 已被撤销 |
| RATE_LIMIT_EXCEEDED | 429 | 请求频率超限 |
| NOT_FOUND | 404 | 接口不存在 |
| SEARCH_FAILED | 500 | 搜索方剂失败 |
| MISSING_SYMPTOMS | 400 | 未提供症状描述 |

---

## 数据库方剂分类参考

当前数据库收录的 20 个主要分类：

1. 解表剂 - Diaphoretic Formulas
2. 泻下剂 - Purgative Formulas
3. 和解剂 - Harmonizing Formulas
4. 清热剂 - Heat-Clearing Formulas
5. 祛暑剂 - Summer-Heat-Clearing Formulas
6. 温里剂 - Interior-Warming Formulas
7. 表里双解剂 - Exterior-Interior Resolving Formulas
8. 补益剂 - Supplementing Formulas
9. 安神剂 - Spirit-Calming Formulas
10. 开窍剂 - Orifice-Opening Formulas
11. 固涩剂 - Astringent Formulas
12. 理气剂 - Qi-Regulating Formulas
13. 理血剂 - Blood-Regulating Formulas
14. 治风剂 - Wind-Treating Formulas
15. 治燥剂 - Dryness-Treating Formulas
16. 祛湿剂 - Dampness-Dispelling Formulas
17. 祛痰剂 - Phlegm-Dispelling Formulas
18. 消食剂 - Digestive Formulas
19. 驱虫剂 - Parasite-Expelling Formulas
20. 涌吐剂 - Emetic Formulas

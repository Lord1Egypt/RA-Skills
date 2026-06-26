---
name: swagger-v2-retrofit-generator
description: >
  Generate Android Retrofit/Kotlin client code from Swagger v2 (OpenAPI 2.0) API documentation.
  Supports fetching Swagger docs via HTTP with no auth, Basic Auth, Bearer Token, and API Key auth.
  Use when: (1) User needs to generate Retrofit Service interfaces from Swagger API,
  (2) User wants to create Kotlin data classes from Swagger definitions,
  (3) User needs to fetch Swagger v2 docs from a URL with authentication,
  (4) Converting Swagger API documentation to Android HTTP client code.
---

# Swagger v2 Retrofit 代码生成器

从 Swagger v2 (OpenAPI 2.0) API 文档生成 Android Retrofit + Kotlin 客户端代码。

## 功能

- 从 HTTP URL 获取 Swagger v2 API 文档
- 支持无认证、Basic Auth、Bearer Token、API Key 认证方式
- 生成 Retrofit Service 接口（Kotlin）
- 生成数据类（Kotlin data class）

## 快速开始

### 获取 Swagger 文档

使用 `scripts/fetch_swagger.py` 获取 Swagger JSON：

```bash
# 无认证
python scripts/fetch_swagger.py http://api.example.com/v2/api-docs

# Basic 认证
python scripts/fetch_swagger.py http://api.example.com/v2/api-docs -u admin -p admin

# 保存到文件
python scripts/fetch_swagger.py http://api.example.com/v2/api-docs -u admin -p admin -o swagger.json
```

### 生成 Retrofit 代码

使用 `scripts/generate_retrofit.py` 生成代码：

```bash
# 从文件生成
python scripts/generate_retrofit.py swagger.json -p com.dkzsxt.ruizhidian.api -o ApiService.kt

# 从管道生成
python scripts/fetch_swagger.py http://api.example.com/v2/api-docs -u admin -p admin | \
  python scripts/generate_retrofit.py - -p com.example.api
```

### 完整示例

```bash
# 获取并生成代码（一步完成）
python scripts/fetch_swagger.py http://api.example.com/v2/api-docs \
  -u admin -p admin | \
  python scripts/generate_retrofit.py - \
  -p com.dkzsxt.ruizhidian.api \
  -s ApiService \
  -o app/src/main/java/com/dkzsxt/ruizhidian/api/ApiService.kt
```

## 指定接口生成

### 查看所有可用接口

```bash
# 列出所有接口
python scripts/generate_retrofit.py swagger.json --list

# 搜索包含 "picture" 的接口（搜索 path/summary/description/operationId/tags）
python scripts/generate_retrofit.py swagger.json --list --search picture

# 只在 path 中搜索
python scripts/generate_retrofit.py swagger.json --list --search getPictureDetail --search-field path

# 只在 summary 中搜索
python scripts/generate_retrofit.py swagger.json --list --search "绘本详情" --search-field summary

# 按 tag 列出接口
python scripts/generate_retrofit.py swagger.json --list --tag "绘本接口"

# 列出所有 tags
python scripts/generate_retrofit.py swagger.json --list-tags
```

### 生成指定接口

```bash
# 生成单个接口: POST /picture/getPictureDetailPage
python scripts/generate_retrofit.py swagger.json \
  --path /picture/getPictureDetailPage \
  --method POST \
  -o PictureDetailApi.kt

# 生成多个指定接口
python scripts/generate_retrofit.py swagger.json \
  --path /picture/getPictureDetailPage \
  --path /picture/getPictureList \
  --path /user/getUserInfo \
  -o SelectedApis.kt

# 生成 /picture/ 路径下的所有接口
python scripts/generate_retrofit.py swagger.json \
  --path "/picture/*" \
  -o PictureApis.kt

# 生成所有 POST 请求
python scripts/generate_retrofit.py swagger.json \
  --method POST \
  -o PostApis.kt

# 只生成必要的数据类（减少代码量）
python scripts/generate_retrofit.py swagger.json \
  --path /picture/getPictureDetailPage \
  --method POST \
  --only-used-models \
  -o MinimalApi.kt
```

### 搜索生成

```bash
# 搜索 "绘本" 相关接口并生成
python scripts/generate_retrofit.py swagger.json \
  --search "绘本" \
  -o PictureApis.kt

# 搜索 "getPicture" 路径相关接口
python scripts/generate_retrofit.py swagger.json \
  --search "getPicture" \
  --search-field path \
  -o PictureApis.kt

# 搜索 summary 包含 "首页" 的接口
python scripts/generate_retrofit.py swagger.json \
  --search "首页" \
  --search-field summary \
  -o HomePageApis.kt

# 按 tag 生成接口
python scripts/generate_retrofit.py swagger.json \
  --tag "绘本接口" \
  -o PictureApis.kt

# 多个 tags
python scripts/generate_retrofit.py swagger.json \
  --tag "绘本接口" \
  --tag "用户绘本接口" \
  -o PictureUserApis.kt

# 组合搜索：绘本接口 + POST 方法
python scripts/generate_retrofit.py swagger.json \
  --tag "绘本接口" \
  --method POST \
  --only-used-models \
  -o PicturePostApis.kt
```

## 命令行参数

### fetch_swagger.py

| 参数 | 说明 |
|-----|------|
| `url` | Swagger v2 API 文档 URL |
| `--auth-type` | 认证方式：`none` / `basic` / `bearer` / `api-key` |
| `-u, --username` | Basic Auth 用户名 |
| `-p, --password` | Basic Auth 密码 |
| `--token` | Bearer Token |
| `--api-key` | API Key 值 |
| `--api-key-name` | API Key 名称（默认 `X-API-Key`） |
| `--api-key-in` | API Key 位置：`header` / `query` |
| `-o, --output` | 输出文件路径（默认 stdout） |

### generate_retrofit.py

| 参数 | 说明 |
|-----|------|
| `input` | 输入 JSON 文件，`-` 表示从 stdin 读取 |
| `-p, --package` | 包名（默认: com.example.api） |
| `-s, --service-name` | Service 接口名（默认: ApiService） |
| `--path` | 指定接口路径（可多次使用，支持通配符 `*`） |
| `-m, --method` | 指定 HTTP 方法（GET, POST, PUT, DELETE, PATCH） |
| `--search` | 搜索关键词（搜索 path/summary/description/operationId/tags） |
| `--search-field` | 指定搜索字段（可多次使用） |
| `--tag` | 按 Tag 过滤（可多次使用） |
| `--only-used-models` | 只生成被选中接口使用的数据类 |
| `-l, --list` | 列出所有可用接口 |
| `--list-tags` | 列出所有可用 Tags |
| `-o, --output` | 输出文件路径（默认 stdout） |

## 生成的代码结构

生成的 Kotlin 文件包含：

```kotlin
package com.dkzsxt.ruizhidian.api

import retrofit2.http.*
import okhttp3.ResponseBody

// 数据类
data class User(
    val id: Long,
    val name: String
)

// Service 接口
interface ApiService {
    
    @GET("/users/{id}")
    suspend fun getUserById(
        @Path("id") id: String
    ): User
    
    @POST("/users")
    suspend fun createUser(
        @Body body: User
    ): User
}
```

## 认证方式支持

### Basic Auth

使用 `-u` 和 `-p` 参数：

```bash
python scripts/fetch_swagger.py URL -u username -p password
```

### Bearer Token (JWT)

```bash
python scripts/fetch_swagger.py URL --auth-type bearer --token TOKEN
```

### API Key

```bash
# Header 方式
python scripts/fetch_swagger.py URL --auth-type api-key --api-key KEY --api-key-name X-API-Key

# Query 方式
python scripts/fetch_swagger.py URL --auth-type api-key --api-key KEY --api-key-name token --api-key-in query
```

## 参考文档

- Swagger v2 结构说明: [references/swagger-v2-structure.md](references/swagger-v2-structure.md)
- Retrofit 模板: [references/retrofit-templates.md](references/retrofit-templates.md)

## 限制

- 仅支持 Swagger v2 (OpenAPI 2.0)，不支持 OpenAPI 3.0
- 生成的方法使用 `suspend` 函数（Kotlin 协程）
- 文件上传相关 API 需要手动调整
- 复杂泛型响应可能需要手动修改

## 类名处理

Swagger 中的中文类名（如 `Result«绘本详情信息对象»`）会自动转换为合法的 Kotlin 类名：

| 原始类名 | 生成的类名 |
|---------|-----------|
| `Result«绘本详情信息对象»` | `ResultPictureBookDetailInfoObject` |
| `口语课商品列表对象` | `OralClassGoodsListObject` |
| `List<用户详情>` | `List<UserDetail>` |

转换规则：
1. 移除书名号等特殊字符 (`« » 《 》 < >`)
2. 常见中文词汇自动翻译（如"绘本"→"PictureBook"、"详情"→"Detail"）
3. 其他中文字符替换为 `X`
4. 转换为 PascalCase 格式
5. 确保以字母开头

## 故障排除

### 401 认证失败

检查用户名密码是否正确：
```bash
python scripts/fetch_swagger.py URL -u admin -p admin
```

### 无法解析 JSON

确保 URL 返回的是 Swagger v2 JSON，不是 HTML 页面。

### 类型映射不正确

某些复杂类型（如 `Map`、`Any`）可能需要手动调整。参考生成的代码并手动修复。

### 找不到指定接口

使用 `--list` 查看所有可用接口：
```bash
python scripts/generate_retrofit.py swagger.json --list
python scripts/generate_retrofit.py swagger.json --list --search keyword
python scripts/generate_retrofit.py swagger.json --list --search "绘本" --search-field summary
```

查看所有 tags：
```bash
python scripts/generate_retrofit.py swagger.json --list-tags
```

注意：
- 路径需要完全匹配或使用 `*` 通配符
- 方法名需大写（GET, POST, PUT, DELETE, PATCH）
- 示例：`--path /picture/getPictureDetailPage --method POST`
- 搜索支持中文，会搜索 path/summary/description/operationId/tags

### 生成的代码太多

使用 `--only-used-models` 只生成选中接口依赖的数据类：
```bash
python scripts/generate_retrofit.py swagger.json \
  --path /api/specific \
  --only-used-models \
  -o MinimalApi.kt
```

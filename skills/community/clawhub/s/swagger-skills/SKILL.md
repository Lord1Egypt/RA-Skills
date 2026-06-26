---
name: swagger-skills
description: Use this skill to turn Swagger UI or OpenAPI/Swagger documentation links into organized API calling skills, including Python clients, field references, domain configuration, and feature navigation.
---

# swagger-skills

`swagger-skills` 是一个独立的 Swagger/OpenAPI skill 生成工具。它可以根据接口文档链接编制新的接口调用资料，把 Swagger UI 或 OpenAPI/Swagger spec 转换为按 controller 归类的 Python 调用文件、接口字段说明和功能集成索引。

## 适用场景

当你需要根据接口文档快速生成可调用、可检索、可维护的 API skill 时使用本 skill：

- 从 Swagger UI 页面自动发现真实 OpenAPI/Swagger spec 地址。
- 从 OpenAPI 3.x 或 Swagger 2.0 规格生成接口调用 Python 文件。
- 按 controller 聚合接口说明，方便定位业务能力。
- 将接口调用域名集中维护在 `config/domains.json` 与 `scripts/skill_common.py`。
- 构建 `openapi_field_index.json` 字段索引，支持 lookup 与响应 key 自动映射为中文描述。
- 为每个接口生成一份调用逻辑和一份字段说明文档。

## 默认文档认证

如果 Swagger 文档需要登录或 Basic Auth，请在 `config/sources.json` 中显式填写文档认证信息：

- 用户名：`<DOC_USERNAME>`
- 密码：`<DOC_PASSWORD>`

该认证只用于拉取 Swagger 文档。生成出来的业务接口调用文件不会硬编码业务系统凭据。

## 目录说明

- `scripts/build_swagger_skill.py`：根据 Swagger UI/spec 链接生成接口 skill 内容。
- `scripts/swagger_client.py`：构建期拉取 spec 的 HTTP 工具。
- `scripts/skill_http.py`、`scripts/skill_common.py`、`scripts/field_mapper.py`、`scripts/openapi_fields.py`：复制到产物 skill 的运行时模块。
- `config/sources.example.json`：Swagger 文档来源配置示例。
- 产物 skill 默认位于生成器同级目录（非 `generated/` 子目录）。

## 使用流程

1. 将 `config/sources.example.json` 复制为 `config/sources.json`。
2. 在 `config/sources.json` 中填写一个或多个 Swagger UI 页面链接或 spec 链接。
3. 安装依赖后执行生成命令。

```powershell
cd <swagger-skills目录>
python -m pip install -r requirements.txt
python scripts\build_swagger_skill.py --clean-generated
```

4. 如果 `sources.json` 包含多个链接，生成器会询问产出方式：
   - `combined`：多个接口文档合并产出 1 个 skill。
   - `separate`：每个接口文档分别产出 1 个 skill。
5. 生成完成后，进入同级目录下具体产出的 skill，例如 `..\admin-config-swagger-skills\`，从 `FEATURES.md` 按功能查找接口，再进入对应的 `api_clients/<controller>/<operation>.py` 和 `references/<controller>/<operation>_OPENAPI.md`。

## 输出约定

实际产出的业务 skills 默认位于 `swagger-skills` 的同级目录下，避免生成器 skill 和产物 skill 被同一个父目录扫描时重复注册：

- 合并模式：`..\combined-swagger-skills\`
- 分开模式：`..\<source_id>-swagger-skills\`

产出物的文件夹和文件名只使用英文、数字和下划线。生成器会优先使用英文 tag、operationId、path 片段或 `source_id`；中文名称不会转换为拼音，也不会直接进入路径。

同一个 controller 下的接口会聚合到一个 controller 说明文件中，同时每个具体接口会产生两个关联文件：

- `api_clients/<controller>/<operation>.py`
- `references/<controller>/<operation>_OPENAPI.md`

产物 skill 还包含：

- `openapi_field_index.json`：字段索引（构建期从 OpenAPI schema 生成）
- `scripts/skill_common.py`：各文档调用域名统一管理（读取 `config/domains.json`）
- `scripts/skill_http.py`：统一 HTTP 调用入口，默认对响应 JSON 做字段 key → 中文描述映射
- `scripts/openapi_fields.py lookup <字段名>`：查询字段含义

`config/domains.json` 记录调用域名、`field_mapping.enabled`（默认 `true`）、spec 地址和文档认证。设置 `SWAGGER_RAW_JSON=1` 可单次跳过字段映射。

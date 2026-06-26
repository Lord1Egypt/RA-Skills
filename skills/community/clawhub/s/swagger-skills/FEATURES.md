# swagger-skills 功能集成索引

当前目录提供“根据接口文档链接编制 skills”的能力。填入 Swagger UI 页面或 OpenAPI/Swagger spec 地址后，运行生成器即可生成具体接口功能索引。

## 已内置能力

- Swagger UI 页面探测：自动识别页面中的 `url`、`urls` 配置，并尝试常见 spec 路径。
- OpenAPI/Swagger 解析：支持 OpenAPI 3.x 和 Swagger 2.0 的基础结构。
- Controller 归类：优先按 tag 归类接口，无 tag 时按路径或 operationId 推断。
- 接口调用生成：每个接口生成一个 Python 调用文件。
- 字段说明生成：每个接口生成一个 `*_OPENAPI.md` 描述文件。
- 域名配置生成：按接口文档来源归类服务域名，写入 `config/domains.json`。
- 双产出模式：多个接口文档可合并产出 1 个 skill，也可按链接分别产出多个 skills。
- 英文命名：产出路径只使用英文、数字和下划线，优先取英文 tag、operationId、path 片段或 `source_id`；中文名称不会转拼音，也不会直接进入路径。

## 生成后的定位方式

生成真实接口后，业务 skills 会放在 `generated/` 下。进入具体产出的 skill 后，其中的 `FEATURES.md` 会包含：

- 功能名称和接口摘要。
- HTTP 方法和路径。
- Python 调用逻辑位置，例如 `api_clients/user_controller/get_user.py`。
- 字段说明位置，例如 `references/user_controller/get_user_OPENAPI.md`。
- 所属文档和调用域名配置键。

## 下一步

将 Swagger 文档链接写入 `config/sources.json` 后执行：

```powershell
cd <swagger-skills目录>
python -m pip install -r requirements.txt
python scripts\build_swagger_skill.py --clean-generated
```

多个链接时可显式指定产出方式：

```powershell
python scripts\build_swagger_skill.py --output-mode combined --clean-generated
python scripts\build_swagger_skill.py --output-mode separate --clean-generated
```

产出位置：

- `..\combined-swagger-skills\`
- `..\<source_id>-swagger-skills\`

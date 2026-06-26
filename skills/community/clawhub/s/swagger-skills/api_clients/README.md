# API Clients

该目录用于生成后的业务 skill。运行 `scripts/build_swagger_skill.py` 后，实际产物会写入 `generated/<skill_name>/api_clients/`。

目录结构：

```text
api_clients/
  <controller>/
    <operation>.py
```

合并多个接口文档时，为避免同名 controller 冲突，会增加文档 ID 层级：

```text
api_clients/
  <source_id>/
    <controller>/
      <operation>.py
```

生成的调用文件会读取 `config/domains.json` 中的域名配置，并通过 `requests` 发起 HTTP 请求。

文件夹和文件名只使用英文、数字和下划线。中文 controller/tag 不会转换为拼音，也不会直接进入路径；生成器会改用英文 tag、operationId、path 片段或 `source_id`。

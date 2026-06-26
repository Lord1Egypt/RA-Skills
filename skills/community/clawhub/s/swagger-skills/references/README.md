# References

该目录用于生成后的业务 skill。运行 `scripts/build_swagger_skill.py` 后，实际产物会写入 `generated/<skill_name>/references/`。

目录结构：

```text
references/
  <controller>/
    <operation>_OPENAPI.md
  controllers/
    <controller>.md
```

`references/controllers/<controller>.md` 会聚合同一个 controller 内的所有接口，并链接到对应 Python 调用文件和字段说明文件。

文件夹和文件名只使用英文、数字和下划线。中文 controller/tag 不会转换为拼音，也不会直接进入路径；生成器会改用英文 tag、operationId、path 片段或 `source_id`。

合并多个接口文档时，为避免同名 controller 冲突，会增加文档 ID 层级：

```text
references/
  <source_id>/
    <controller>/
      <operation>_OPENAPI.md
    controllers/
      <controller>.md
```

---
name: text-transformer
description: "调用 Python 脚本处理文本（当前支持：转换为大写）。 / Python-powered text transformation tool."
user-invocable: true
---

当用户请求处理文本，或明确调用 `/text-transformer` 时，请严格执行以下步骤：

1. 提取用户想要处理的核心文本内容。
2. 使用内置的命令行工具（例如 `bash` 或 `exec`），在当前目录（`{baseDir}`）下运行 Python 脚本。
3. 执行命令示例：`python {baseDir}/tool.py "<提取的文本>"`
4. 将终端返回的处理结果直接反馈给用户。

> 注意：如果脚本执行报错，请将错误信息反馈给用户，并尝试分析原因。

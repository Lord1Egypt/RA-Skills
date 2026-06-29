## Step 1 — 输入转换

无论用户提交什么格式的文件，统一使用 markitdown 转换为 Markdown：

```bash
markitdown <用户文件路径> -o <当前工作目录>/<原始文档stem>.md
```

若转换失败，回复用户"不支持的文件格式或文件损坏，请提供可读的 PDF / DOCX / TXT 文件"。

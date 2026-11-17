# 本地索引流程

V2 索引是独立的 SQLite 数据库，位于 `%LOCALAPPDATA%\Codex\wechat-file-finder\index.sqlite3`。建立索引时只读取微信文件，不会修改它们。

## 命令

使用 Windows 包装脚本 `<skill-dir>\scripts\wechat_index.ps1`。它会优先选择 Codex 附带的 Python 运行时，并配置 UTF-8 输出。

执行索引查询前先检查状态：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\wechat_index.ps1" status
```

如果结果是 `index_missing`，或者用户要求刷新索引，则执行构建：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\wechat_index.ps1" build
```

构建过程是增量的：文件大小和修改时间未变化时，保留已经提取的内容与哈希。完整构建成功后，会清理扫描根目录中已经不存在的索引记录。`--root PATH` 把操作限制在明确且可信的目录中。`--max-files N` 仅用于测试，不会清理过期记录。

搜索文件名和已经提取的内容：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\wechat_index.ps1" search "退款条款" --extension docx --since 2026-08-01 --limit 20
```

可用筛选参数包括 `--exact-name`、`--content-only`、`--extension`、`--since`、`--before`、`--min-size` 和 `--max-size`。日期使用本地 ISO 日期或时间戳。`--before` 不包含边界时间。

查找字节级完全相同的重复文件：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\wechat_index.ps1" duplicates --limit 20
```

重复文件组使用 SHA-256 判断。缺少哈希意味着文件超过设定的哈希大小限制或无法读取，不能把它视为唯一文件。未获得明确确认时绝不删除重复文件。

导入可信的发送人、聊天和发送时间元数据：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\wechat_index.ps1" import-metadata "C:\path\metadata.csv"
```

数据结构见 [metadata-index.md](metadata-index.md)。导入记录通过规范化绝对路径关联。无法匹配的记录应明确报告，不能猜测关联关系。

## 内容支持

- 纯文本以及常见源代码、配置格式：在本地解码。
- DOCX：从 OOXML 中提取段落文字。
- XLSX：从 OOXML 中提取共享字符串和工作表值。
- PDF：存在 `pypdf` 时提取文字。扫描件或只有图像的 PDF 返回 `no_text_or_scanned_pdf`；OCR 是需要用户单独提出的操作。
- 其他格式仍可通过文件名和元数据搜索，但内容状态为 `unsupported_type`。

索引在本地保存提取的文字、哈希、路径、大小和文件系统时间。除非导入可信元数据，否则不会保存或推断发送人。

# 微信文件助手

这是一个本地优先的 Windows 智能体技能，用来查找微信或 Weixin 保存的文件，并继续完成用户真正需要的文件处理任务。

## 这个技能能做什么

- 在新版和旧版微信文件目录中精确或模糊搜索文件名。
- 建立本地 SQLite 增量索引，提升重复查询速度。
- 在本地提取 TXT、PDF、DOCX 和 XLSX 文件内容。
- 按日期、扩展名和文件大小筛选。
- 使用 SHA-256 检测内容完全相同的重复文件。
- 可选导入可信的发送人、聊天和发送时间元数据。
- 在 Windows 资源管理器中选中结果，同时保持源文件只读。

## 隐私与安全

技能只在本地搜索文件，并把索引存放在 `%LOCALAPPDATA%\Codex\wechat-file-finder`。它不会解密或修改微信数据库，也不会把文件修改时间当成已经验证的微信发送时间。复制、移动、上传、转发和删除必须由用户单独授权。

## 安装

通过 ClawHub 安装：

```powershell
openclaw skills install wechat-file-assistant
```

用于 Codex 时，将技能目录放到 `%USERPROFILE%\.codex\skills\wechat-file-finder`。技能需要 Windows PowerShell 和 Python 3；安装 `pypdf` 后可提取 PDF 文字。

## 使用示例

- `帮我找微信文件“report.txt”，并打开所在位置。`
- `找一下内容里提到“退款条款”的微信 Word 文件。`
- `查找重复的微信文件，但先不要删除。`
- `找到减脂计划，提取每天的训练安排。`

智能体指令参见 `SKILL.md`，本地索引命令参见 `references/index-workflow.md`。

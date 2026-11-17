# 日程附件处理

## 支持的附件

- 企业微信或其他聊天渠道已下载到本地的文件
- 用户提供的本地文件路径
- 明确的 HTTP/HTTPS 网络链接

常见附件包括通知、会议材料、Word、PDF、表格、图片和汇报材料。

## 本地文件

使用：

```bash
python3 scripts/work_schedule.py attach \
  --id <事项编号> \
  --file "<本地文件路径>" \
  --label "<显示名称>"
```

脚本将文件复制到：

```text
~/.openclaw/workspace/work-schedule/attachments/<事项编号>/
```

并在 `工作日程.md` 中创建相对链接。原聊天下载目录中的临时文件即使被清理，日程附件仍然保留。

## 网络链接

使用：

```bash
python3 scripts/work_schedule.py attach \
  --id <事项编号> \
  --url "https://..." \
  --label "<显示名称>"
```

只允许 HTTP 和 HTTPS。脚本不会主动下载网络内容。

## 聊天附件

如果渠道工具返回了真实本地路径，直接使用该路径关联。若只返回文件 ID、媒体 ID 或临时引用，但没有可读取路径：

1. 先尝试使用渠道提供的下载能力取得本地文件。
2. 无法下载时，告诉用户日程已经保存，但附件尚未归档。
3. 请用户重新上传文件或提供可访问链接。

不得把一个无法访问的文件 ID 伪装成可点击附件。

## 安全要求

- 不执行附件。
- 不自动解压压缩文件。
- 不自动打开宏、脚本或可执行文件。
- 不保存密码、密钥、验证码等敏感内容。
- 默认单个本地附件最大 100 MB，可通过 `WORK_SCHEDULE_ATTACHMENT_MAX_MB` 调整。
- 本地文件使用 SHA-256 记录完整性并避免重复副本。
- 文件名经过清理，禁止目录穿越。

## 查询附件

查看日程台账：

```bash
cat ~/.openclaw/workspace/work-schedule/工作日程.md
```

查看事项详情及附件：

```bash
python3 scripts/work_schedule.py show --id <事项编号>
```


# Sync Obsidian to Lexiang

将 Obsidian vault 单向全量或增量同步到腾讯乐享知识库，保留目录、Markdown 图文和独立附件。

当前 Skill 版本：`2.1.0`。

## 架构

- 本仓库：扫描、manifest、冲突策略、目录和独立附件。
- [`upload-markdown-to-lexiang`](https://github.com/ajaxhe/upload-markdown-to-lexiang)：
  Markdown page 创建、覆盖、本地图片和线上对账。
- Markdown 内容由 Python 脚本处理，不进入大模型上下文。

两个 Skill 应安装在同一个 skills 根目录；也可用
`LEXIANG_UPLOADER_HOME` 指向公共上传 Skill。

个人凭证从 <https://lexiangla.com/ai/claw> 获取：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" auth login
```

公共 uploader 版本要求为 `>=1.3.1,<2.0.0`。默认同步保持原行为：
Markdown 使用 uploader 的默认凭证，目录、探活和独立附件使用 Agent 连接器。
如需定时或后台任务使用另一份个人授权，可显式选择同一凭证：

```bash
python3 scripts/sync.py \
  --mode incremental \
  --target-space-id <SPACE_ID> \
  --vault-path "<VAULT>" \
  --lexiang-profile obsidian-sync \
  --background
```

命名 profile 位于 `~/.config/lexiang-upload/profiles/<name>.json`，其中
`default` 使用旧路径 `~/.config/lexiang-upload/credentials.json`。也可传
`--lexiang-credential-file <PATH>`；该参数与 `--lexiang-profile` 互斥。
选择器会保存到 vault config（仅名称或路径，不保存 token），并统一用于
Markdown、目录、探活和独立附件。config 未设置时还会考虑
`LEXIANG_UPLOAD_CREDENTIALS` 和 `LEXIANG_UPLOAD_PROFILE`。

## 使用

```bash
# 预览
python3 scripts/sync.py \
  --mode full \
  --target-space-id <SPACE_ID> \
  --vault-path "<VAULT>" \
  --dry-run

# 增量同步
python3 scripts/sync.py \
  --mode incremental \
  --target-space-id <SPACE_ID> \
  --target-folder-id <FOLDER_ID> \
  --vault-path "<VAULT>"
```

## 一致性

- 每个成功项目立即写 manifest，中断后可续传。
- manifest 缺失时按父目录、名称和类型查重。
- `lexiang_wins` 保护乐享侧独立编辑。
- 文件锁阻止同一 vault 并发同步。
- Markdown 只有在公共上传器返回 `verified=true` 后才记为成功。

## 测试

```bash
python3 scripts/test_sync.py
```

默认测试离线执行，不创建真实乐享条目。

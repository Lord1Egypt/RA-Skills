# webdav-backup

一个给 OpenClaw 用的备份 skill：支持把 `~/.openclaw` 相关工作区与基础配置打包到本地目录，或同步到 WebDAV。

当前默认本地输出目录：`~/openclaw/output`

## 现在支持什么

- 本地备份
- WebDAV 备份
- 本地 + WebDAV 双备份
- 默认备份清单（不只 workspace，还包含基础配置）
- 默认排除缓存、Git、临时目录、旧 output 等无意义内容
- 从本地备份包恢复到当前目录或指定目录
- 生成 `backup-manifest.json`，方便恢复前先核对内容

## 默认备份内容

不传 `--source` 时，默认备份：

- `~/.openclaw/workspace/`
- `~/.openclaw/openclaw.json`
- `~/.openclaw/cron/`
- `~/.openclaw/workspace/config/`

并额外写入：

- `openclaw/backup-manifest.json`

## 默认排除内容

为了避免备份包臃肿，默认会排除：

- `.git/`
- `.ace-tool/`
- `.clawhub/`
- `__pycache__/`、`*.pyc`
- `node_modules/`
- `.cache/`
- `tmp/`、`temp/`
- `output/`、`outputs/`
- `.DS_Store`

## 常用命令

### 只做本地备份

```bash
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --local-only
```

### 本地 + WebDAV 双备份

```bash
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py
```

### 只备份指定目录或文件

```bash
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --source /path/to/data --local-only
```

### 恢复本地最新备份

```bash
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --restore latest
```

### 恢复到指定目录

```bash
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --restore latest --restore-dir ~/restore-test
```

## 配置 WebDAV

可以通过 `~/.openclaw/openclaw.json` 或环境变量配置：

- `WEBDAV_URL`
- `WEBDAV_USERNAME`
- `WEBDAV_PASSWORD`
- `OPENCLAW_LOCAL_BACKUP_DIR`（可选，覆盖默认本地输出目录）

环境变量名统一使用 `WEBDAV_PASSWORD`，不再额外兼容 `WEBDAV_PASS`。

更推荐把 WebDAV 配置写进 `~/.openclaw/openclaw.json`，并控制好文件权限；不建议把密码明文长期写入 shell 启动文件。

## 恢复策略建议

恢复时别一上来就覆盖生产目录。更稳的方式是：

1. 先恢复到独立目录
2. 先看 `backup-manifest.json`
3. 再决定整体恢复还是只挑部分内容回填
4. 只有确认无误时才考虑覆盖

## 文件结构

```text
webdav-backup/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   └── config.md
└── scripts/
    └── backup.py
```

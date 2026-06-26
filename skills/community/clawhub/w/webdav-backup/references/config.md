# WebDAV 备份配置指南

## 支持的 WebDAV 服务配置

### 1. 坚果云 (推荐)

```bash
export WEBDAV_URL="https://dav.jianguoyun.com/dav/"
export WEBDAV_USERNAME="你的坚果云邮箱"
export WEBDAV_PASSWORD="你的坚果云应用密码"
```

**注意**: 必须使用"应用密码"，不是登录密码。
在坚果云网页版 → 安全选项 → 添加应用密码。

环境变量名统一使用 `WEBDAV_PASSWORD`。

### 2. Nextcloud

```bash
export WEBDAV_URL="https://your-nextcloud.com/remote.php/dav/files/username/"
export WEBDAV_USERNAME="username"
export WEBDAV_PASSWORD="password"
```

### 3. ownCloud

```bash
export WEBDAV_URL="https://your-owncloud.com/remote.php/webdav/"
export WEBDAV_USERNAME="username"
export WEBDAV_PASSWORD="password"
```

### 4. 阿里云盘（通过 WebDAV 插件）

需要先部署 aliyundrive-webdav：
```bash
export WEBDAV_URL="http://localhost:8080/"
export WEBDAV_USERNAME="admin"
export WEBDAV_PASSWORD="your-token"
```

## 本地备份目录

默认本地备份目录为：`~/openclaw/output`

如需修改，可设置：

```bash
export OPENCLAW_LOCAL_BACKUP_DIR="$HOME/openclaw/output"
```

也可以写入 `~/.openclaw/openclaw.json` 的 `webdav-backup.env`。

## 配置建议

优先使用 `~/.openclaw/openclaw.json` 保存 WebDAV 配置，并确保文件权限受控。

如果只是临时测试，可以只在当前 shell 会话中设置环境变量：

```bash
export WEBDAV_URL="https://dav.jianguoyun.com/dav/"
export WEBDAV_USERNAME="your-email"
export WEBDAV_PASSWORD="your-password"
```

不建议把密码明文长期写入 `~/.bashrc` 或 `~/.zshrc`。

## 测试连接

```bash
# 测试 WebDAV 连接
curl -u $WEBDAV_USERNAME:$WEBDAV_PASSWORD -X PROPFIND $WEBDAV_URL
```

## 默认备份范围

不传 `--source` 时，默认备份这些内容：

- `~/.openclaw/workspace/`
- `~/.openclaw/openclaw.json`
- `~/.openclaw/cron/`
- `~/.openclaw/workspace/config/`

如果只想备份单独目录或文件，请显式传 `--source`。

## 默认排除规则

默认会排除版本库、缓存、临时目录和输出目录，例如：

- `.git/`
- `.ace-tool/`
- `.clawhub/`
- `__pycache__/`、`*.pyc`
- `node_modules/`
- `.cache/`
- `tmp/`、`temp/`
- `output/`、`outputs/`

## 恢复说明

- `--restore latest`：从本地默认备份目录恢复最新备份
- `--restore /path/to/file.tar.gz`：恢复指定备份包
- `--restore-dir DIR`：指定恢复目标目录
- 默认不覆盖已存在文件；如需覆盖，加 `--force`

恢复前建议先解到独立目录，再查看 `openclaw/backup-manifest.json`，确认内容无误后再决定是否局部回填或覆盖。

### 恢复时的推荐判断顺序

1. 先恢复到独立目录，而不是直接覆盖生产路径
2. 先查看 `openclaw/backup-manifest.json`，确认备份实际包含内容
3. 若只需部分恢复，优先从恢复目录中手动挑选目标文件/目录
4. 只有确认目标路径和覆盖意图后，才使用 `--force`

## 备份策略建议

### 每日自动备份
```bash
# 添加到 crontab
crontab -e
# 添加行（根据实际路径调整）：
0 2 * * * /usr/bin/python3 ~/.openclaw/workspace/skills/openclaw-webdav-backup/scripts/backup.py >> /tmp/webdav-backup.log 2>&1
```

### 保留策略
- 本地保留最近7天备份
- WebDAV 保留最近30天备份
- 每月1日保留月备份

## 故障排除

### 1. 上传失败 "401 Unauthorized"
- 检查用户名和密码
- 坚果云用户确认使用的是"应用密码"

### 2. 上传失败 "403 Forbidden"
- 检查 WebDAV 目录是否有写入权限
- 确认 URL 路径正确

### 3. SSL 证书错误

不要通过关闭 TLS 校验来绕过证书问题。

更安全的做法是：
- 检查 WebDAV 服务端证书是否正确
- 使用受信任 CA 签发的证书
- 校正本机 CA / 系统时间 / 代理设置
- 优先使用可信的 HTTPS WebDAV 端点

### 4. 备份文件太大
- 排除大文件：`--exclude-pattern "*.mp4,*.zip"`
- 只备份关键数据而非整个 workspace

## 安全建议

1. **不要将密码硬编码在脚本中**
2. **使用应用密码而非主密码**
3. **定期更换密码**
4. **备份文件建议加密**

## 加密备份（高级）

如需加密备份，在创建 tar.gz 前添加加密步骤：

```bash
# 加密
gpg --symmetric --cipher-algo AES256 backup.tar.gz
# 解密
gpg --decrypt backup.tar.gz.gpg
```

# 故障排除指南

## 常见问题

### 1. 文档目录为空

**症状**:
```bash
$ ls ~/.openclaw/workspace/docs/openclaw_manual/
(空目录或不存在)
```

**原因**: 首次同步未执行或失败

**解决方法**:
```bash
# 进入技能目录
cd path/to/use-openclaw-manual/
./run.sh --init
```

**预期输出**:
```
🚀 初始化 use-openclaw-manual 技能...

克隆文档仓库...
下载文件：719 个
耗时：28.4s

初始化完成！
文档路径：~/.openclaw/workspace/docs/openclaw_manual/
```

---

### 2. 搜索无结果

**症状**:
```bash
$ ./run.sh --search "xxx"
共找到 0 个结果
```

**可能原因**:

1. **关键词不匹配**
   - 尝试同义词（如 "notification" → "message"）
   - 尝试英文关键词（文档以英文为主）
   - 使用更具体的词（如 "discord channel" 而非 "config"）

2. **文档未同步**
   ```bash
   # 检查文档目录
   ls ~/.openclaw/workspace/docs/openclaw_manual/
   
   # 如果为空，执行初始化
   ./run.sh --init
   ```

3. **搜索类型不对**
   ```bash
   # 尝试不同搜索类型
   ./run.sh --search "agent" --type filename
   ./run.sh --search "agent" --type title
   ```

**调试步骤**:
```bash
# 手动 grep 测试
grep -r "关键词" ~/.openclaw/workspace/docs/openclaw_manual/ --include="*.md" | head

# 查看文档统计
./run.sh --stats
```

---

### 3. 同步失败

**症状**:
```
错误：无法连接到 GitHub
或
错误：API 速率限制
```

**可能原因**:

1. **网络连接问题**
   ```bash
   # 测试 GitHub 连接
   curl -I https://github.com/openclaw/openclaw
   
   # 测试 API
   curl -I https://api.github.com/repos/openclaw/openclaw/contents/docs
   ```

2. **GitHub API 限流**
   - 未认证：60 次/小时
   - 已认证：5000 次/小时
   
   **解决**: 等待 1 小时后重试，或配置 `GITHUB_TOKEN` 环境变量

3. **磁盘空间不足**
   ```bash
   # 检查磁盘空间
   df -h ~/.openclaw/workspace/docs/
   
   # 清理空间后重试
   ```

**查看日志**:
```bash
# 在技能目录内查看
cat docs-update.log

# 或使用绝对路径
cat /path/to/use-openclaw-manual/docs-update.log

# 或自定义位置
cat $DOC_UPDATE_LOG
```

---

### 4. 通知发送失败

**症状**: 同步完成但未收到通知

**可能原因**:

1. **渠道未配置**
   - 检查 OpenClaw 是否配置了对应渠道（discord/telegram 等）
   - 默认使用 `webchat`，仅在 web 界面可见

2. **环境变量错误**
   ```bash
   # 检查环境变量
   echo $DOC_NOTIFY_CHANNEL
   
   # 临时指定渠道
   DOC_NOTIFY_CHANNEL=webchat ./run.sh --sync
   ```

3. **权限问题**
   - 检查技能是否有发送消息的权限
   - 查看 OpenClaw 日志

---

### 5. 脚本执行权限问题

**症状**:
```
Permission denied
```

**解决**:
```bash
# 在技能目录内执行
chmod +x run.sh scripts/*.sh

# 或使用绝对路径（根据你的安装位置）
chmod +x /path/to/use-openclaw-manual/run.sh
chmod +x /path/to/use-openclaw-manual/scripts/*.sh
```

---

### 6. 文档版本过旧

**症状**: 文档内容与最新功能不符

**解决**:
```bash
# 强制重新同步
rm ~/.openclaw/workspace/docs/openclaw_manual/.last-docs-commit
./run.sh --sync
```

---

## 日志分析

### 日志位置

默认：`~/.openclaw/skills/use-openclaw-manual/docs-update.log`

### 日志格式

```
[2026-03-11 00:57:23] INFO: 开始同步文档
[2026-03-11 00:57:24] INFO: 当前版本 a1b2c3d
[2026-03-11 00:57:25] INFO: 最新版本 e4f5g6h
[2026-03-11 00:57:30] INFO: 下载文件 12 个
[2026-03-11 00:57:51] INFO: 同步完成
```

### 常见错误码

| 错误 | 含义 | 解决 |
|------|------|------|
| `HTTP 403` | API 限流 | 等待或配置 token |
| `HTTP 404` | 仓库/路径不存在 | 检查仓库名 |
| `Connection refused` | 网络问题 | 检查网络 |
| `No space left` | 磁盘满 | 清理空间 |

---

## 获取帮助

### 内置帮助

```bash
./run.sh --help
```

### 相关资源

- 官方文档：https://docs.openclaw.ai

### 报告问题

如遇到未列出的问题，请提供以下信息：

1. 执行的命令
2. 完整错误输出
3. 日志内容
4. OpenClaw 版本
5. 操作系统信息

# 故障排查指南

## 常见问题速查

### Q1: 存档未触发

**现象**: Token 超过阈值但没有自动存档

**检查步骤**:

1. **检查 HEARTBEAT.md 是否存在**
   ```bash
   ls ~/.openclaw/workspace/HEARTBEAT.md
   ```

2. **检查 token 阈值配置**
   - 查看 `memory/index.json` 中 `config-token-threshold`
   - 确认阈值设置正确（默认 70k/100k）

3. **检查 reset-log.md**
   - 查看是否有最近的存档记录
   - 确认 HEARTBEAT 正在执行

4. **手动测试 HEARTBEAT**
   - 发送消息匹配 HEARTBEAT 触发词
   - 观察是否执行检查

**解决方案**:
- 如果 HEARTBEAT.md 不存在，运行 skill 重新配置
- 如果配置错误，修正 `memory/index.json`

---

### Q2: AI 摘要生成失败

**现象**: 存档文件中没有 AI 生成的摘要

**检查步骤**:

1. **检查脚本是否存在**
   ```bash
   ls ~/.openclaw/workspace/scripts/generate-ai-summary.ps1
   ```

2. **检查 PowerShell 执行权限**
   ```powershell
   Get-ExecutionPolicy
   # 应为 RemoteSigned 或 Unrestricted
   ```

3. **检查会话历史**
   - 确认有足够的历史消息用于生成摘要
   - 最少需要 5-10 条消息

**解决方案**:
```powershell
# 设置执行策略（管理员权限）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 重新创建脚本
# 参考 config-templates.md 中的脚本模板
```

---

### Q3: 备份到 GitHub 失败

**现象**: backup-status.json 显示 github.failed > 0

**检查步骤**:

1. **检查 GitHub Token**
   ```bash
   git config --global user.name
   git config --global user.email
   ```

2. **检查远程仓库配置**
   ```bash
   cd ~/.openclaw/workspace
   git remote -v
   ```

3. **测试推送权限**
   ```bash
   git push origin main --dry-run
   ```

**常见错误及解决**:

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `authentication failed` | Token 无效或过期 | 重新配置 GitHub token |
| `repository not found` | 仓库不存在或无权访问 | 检查仓库名称和权限 |
| `permission denied` | 没有写权限 | 确认 token 有 repo 权限 |

**解决方案**:
```bash
# 重新设置远程 URL（使用 token）
git remote set-url origin https://[TOKEN]@github.com/[USERNAME]/openclaw-backup.git

# 或使用 SSH
git remote set-url origin git@github.com:[USERNAME]/openclaw-backup.git
```

---

### Q4: 备份到 OneDrive 失败

**现象**: backup-status.json 显示 onedrive.failed > 0

**检查步骤**:

1. **检查 OneDrive 路径**
   ```powershell
   Test-Path "C:\Users\$env:USERNAME\OneDrive"
   ```

2. **检查备份目录是否存在**
   ```powershell
   Test-Path "C:\Users\$env:USERNAME\OneDrive\openclaw-backup"
   ```

3. **检查磁盘空间**
   ```powershell
   Get-PSDrive C | Select-Object Free
   ```

**解决方案**:
```powershell
# 创建备份目录
New-Item -ItemType Directory -Path "C:\Users\$env:USERNAME\OneDrive\openclaw-backup" -Force

# 检查 OneDrive 同步状态
# 确保 OneDrive 客户端正在运行
```

---

### Q5: 差异标记不准确

**现象**: [NEW]/[UPD]/[KEEP] 标记与实际情况不符

**检查步骤**:

1. **检查上次存档文件**
   - 确认 `memory/session-backups/` 中有历史存档
   - 检查文件内容是否完整

2. **检查 index.json**
   - 确认 `lastUpdated` 时间戳正确
   - 确认条目 ID 唯一

3. **检查对比逻辑**
   - AI 摘要生成脚本中的对比函数
   - 确认 previousValue 被正确记录

**解决方案**:
- 如果首次运行，所有内容标记为 [NEW] 是正常的
- 手动修正 index.json 中的历史记录

---

### Q6: 重置后没有读取 MEMORY.md

**现象**: 新会话开始时没有汇报上次状态

**检查步骤**:

1. **检查 AGENTS.md 配置**
   - 确认 "Every Session" 部分包含读取 MEMORY.md 的指令

2. **检查 MEMORY.md 是否存在**
   ```bash
   ls ~/.openclaw/workspace/MEMORY.md
   ```

3. **检查文件权限**
   - 确认文件可读

**解决方案**:
- 更新 AGENTS.md，确保包含：
  ```markdown
  ## Every Session
  1. Read `SOUL.md`
  2. Read `USER.md`
  3. Read `memory/YYYY-MM-DD.md`
  4. **If in MAIN SESSION**: Also read `MEMORY.md`
  ```

---

### Q7: pendingChanges 未触发立即备份

**现象**: 重要变更后没有立即备份，等待了12小时

**检查步骤**:

1. **检查 backup-status.json**
   ```json
   {
     "pendingChanges": true,  // 应为 true
     "pendingReason": "MEMORY.md updated"
   }
   ```

2. **检查 HEARTBEAT 执行顺序**
   - 确认 pendingChanges 检查在定期备份检查之前

3. **检查标记逻辑**
   - 确认 MEMORY.md 更新时正确设置了 pendingChanges

**解决方案**:
- 手动设置 pendingChanges：
  ```powershell
  $status = Get-Content ~/.openclaw/workspace/memory/backup-status.json | ConvertFrom-Json
  $status.pendingChanges = $true
  $status.pendingReason = "Manual trigger"
  $status | ConvertTo-Json | Set-Content ~/.openclaw/workspace/memory/backup-status.json
  ```

---

## 调试技巧

### 查看完整执行日志

```powershell
# 查看最近的 HEARTBEAT 执行
Get-Content ~/.openclaw/workspace/memory/reset-log.md -Tail 20

# 查看备份状态
Get-Content ~/.openclaw/workspace/memory/backup-status.json | ConvertFrom-Json

# 查看索引
Get-Content ~/.openclaw/workspace/memory/index.json | ConvertFrom-Json
```

### 手动测试存档流程

```powershell
# 1. 检查 token 用量
# 调用 session_status

# 2. 手动生成摘要
& ~/.openclaw/workspace/scripts/generate-ai-summary.ps1

# 3. 检查生成的存档文件
ls ~/.openclaw/workspace/memory/session-backups/ -Name

# 4. 检查 MEMORY.md 更新
Get-Content ~/.openclaw/workspace/MEMORY.md -Tail 30
```

### 手动测试备份流程

```powershell
# 执行备份脚本
& ~/.openclaw/workspace/scripts/backup.ps1

# 检查备份状态
Get-Content ~/.openclaw/workspace/memory/backup-status.json | ConvertFrom-Json
```

---

## 联系支持

如果以上方案无法解决问题：

1. 收集以下信息：
   - `memory/reset-log.md` 最后20行
   - `memory/backup-status.json`
   - 错误截图或完整错误信息

2. 提交 Issue 到：
   - GitHub: https://github.com/openclaw/openclaw/issues
   - Discord: https://discord.com/invite/clawd

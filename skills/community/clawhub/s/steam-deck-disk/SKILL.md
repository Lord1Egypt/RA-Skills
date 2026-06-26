---
name: steam-deck-disk
description: Steam Deck 磁盘空间管理和优化。清理缓存、日志、移动大文件到 /home 分区、检查磁盘使用。
---

# Steam Deck 磁盘管理技能

## 适用场景

- Steam Deck 系统分区空间不足（/var 仅 230MB，/ 仅 5GB）
- 需要定期清理缓存和日志
- 需要将大文件从系统分区迁移到 /home 分区

## 核心操作

### 1. 检查磁盘状态
```bash
df -h / /var /home
du -sh /home/deck/* | sort -hr | head -10
```

### 2. 安全清理（可自动执行）

**系统日志：**
```bash
journalctl --vacuum-size=10M
```

**用户缓存：**
```bash
rm -rf ~/.cache/*
```

**npm 缓存：**
```bash
npm cache clean --force
```

**pip 缓存：**
```bash
pip cache purge
```

### 3. 大文件扫描
```bash
# 查找大于 100MB 的文件
find /home -type f -size +100M 2>/dev/null | head -20

# 检查各目录大小
du -sh /home/deck/* 2>/dev/null | sort -hr
```

### 4. 迁移策略

将以下类型文件移到 `/home/deck/Projects`：
- 开发项目代码
- 解压后的应用程序
- 下载的安装包（安装后可删除）

## 使用方式

### 手动触发
用户询问磁盘优化时：
1. 先运行检查命令，报告当前状态
2. 列出可清理的项目和预计释放空间
3. 用户确认后执行清理
4. 清理后再次报告磁盘状态

### 自动触发（静默时间 00:00-08:00）
- 检查各分区使用率
- 如果任何分区 > 85%，自动执行安全清理
- 记录到 `memory/YYYY-MM-DD.md`

## 配置路径规范

**优先使用 /home 分区的目录：**
- Ollama: `/home/deck/.ollama` ✅
- Node.js: `/home/deck/.nvm` ✅
- 应用配置：`/home/deck/.config` ✅
- 缓存：`/home/deck/.cache` ✅
- 项目文件：`/home/deck/Projects` ✅
- /var 扩展：`/home/var-extended` ✅

**避免使用系统分区（/ 和 /var）存储：**
- ❌ 大型应用数据
- ❌ 用户下载文件
- ❌ 开发项目
- ❌ AI 模型文件

## 当前状态（2026-03-09 优化后）

- `/`: 80% (1GB 可用) - 稳定
- `/var`: 19% (173MB 可用) - 已修复
- `/home`: 23% (189GB 可用) - 充裕

## 注意事项

- **不要删除** `/home/deck/.ollama` 除非用户确认（模型文件可能正在使用）
- **不要删除** `/home/deck/.nvm` （Node.js 环境）
- **不要删除** `/home/deck/.local` 中的程序文件
- 系统分区（/ 和 /var）不要手动修改，使用官方工具清理
- /var 扩容参考 `var-expansion-guide.md`

## 定期维护建议

### 每日自动（静默时间 00:00-08:00）
- 检查分区使用率
- 如果 > 85% 自动清理
- 记录到 memory 文件

### 每周执行一次：
- 清理 journal 日志到 10MB
- 清理浏览器和应用缓存
- 检查 /home/deck/Downloads 和桌面文件

### 每月执行一次：
- 扫描大文件并询问是否需要清理
- 检查 Ollama 模型使用情况

## 自动清理规则

### 触发条件
- 静默时间 (00:00-08:00) 自动扫描
- 任何分区使用率 > 85%

### 安全清理项目
1. ✅ 系统日志：`journalctl --vacuum-size=10M`
2. ✅ 用户缓存：`rm -rf ~/.cache/*`
3. ✅ 临时文件：`rm -rf /tmp/*`
4. ✅ 旧备份：`rm -rf /home/deck/backup-*` (超过 24 小时)
5. ✅ npm 缓存：`npm cache clean --force`

### 禁止删除（保护）
- ❌ `/home/deck/Projects` - 用户项目
- ❌ `/home/deck/.ollama` - AI 模型
- ❌ `/home/deck/.nvm` - Node.js 环境
- ❌ `/home/deck/.config` - 应用配置
- ❌ `/home/deck/.openclaw` - OpenClaw 工作区
- ❌ `/home/deck/.local` - 程序文件

### 清理阈值
| 分区 | 警告线 | 自动清理线 | 操作 |
|------|--------|------------|------|
| `/` | 75% | 85% | 清理日志 + 缓存 |
| `/var` | 75% | 85% | 清理 journal |
| `/home` | 80% | 90% | 清理缓存 + 临时文件 |

---
name: storage-clean
description: "AI-powered cross-platform disk storage analyzer. Scans system/user/dev space usage, generates interactive HTML report with 3-tier cleanup tiers (立即清/确认后清/保留), outputs copy-paste shell commands. NEVER auto-deletes. Triggers: 硬盘不够用, 空间不足, 磁盘快满了, 帮我清理Mac, 扫描大文件, 哪些可以删, 存储清理, 磁盘空间, storage clean, disk cleanup."
version: "2.0.0"
agent_created: true
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
        - psutil
    emoji: "🧹"
  aioom:
    callable: true
    category: "storage"
---

# storage-clean — AI 磁盘空间盘点与清理建议技能

> **跨平台磁盘空间分析工具**
> 智能扫描系统/用户/开发项目空间占用，三级清理分级，输出可直接复制执行的命令。
> **绝不自动删除** — 只出报告和命令，执行前必须用户确认。

---

## 核心原则

1. **只读扫描** — 扫描阶段全程只读，不执行任何写操作
2. **命令输出** — 每个可清理项都附带可直接复制的终端命令（PowerShell / bash）
3. **绝不自动删除** — 报告中的按钮只复制命令，不执行删除
4. **三级分级** — 🟢立即清 / 🟡确认后清 / 🔴保留
5. **跨平台** — 自动检测 Windows / macOS / Linux，适配对应路径和命令

---

## 触发词

中文触发词（精确匹配 + 模糊匹配）：
- `硬盘不够用` `空间不足` `磁盘快满了` `磁盘满了`
- `帮我清理 Mac` `清理Windows` `清理磁盘`
- `扫描大文件` `哪些可以删` `哪些文件占空间`
- `存储清理` `磁盘空间` `释放空间` `空间占用`

英文触发词：`storage clean` `disk cleanup` `free up space`

---

## 三级分级规则

| 等级 | 含义 | 典型内容 | 命令类型 |
|------|------|----------|----------|
| 🟢 立即清 | 纯缓存、临时文件，删了不影响使用 | 系统临时文件、浏览器缓存、pip/npm缓存、日志 | `rm -rf` / `Remove-Item` / `mv ~/.Trash/` |
| 🟡 确认后清 | 可能需要但占用大的文件 | Downloads、Desktop、node_modules、构建产物、Docker镜像 | `rm -rf` (带警告) + 打开目录命令 |
| 🔴 保留 | 系统文件、应用核心数据，绝不能删 | Windows/System、/usr、程序安装目录、AppData核心 | 只展示大小，不提供删除命令 |

---

## 调用方式

运行扫描脚本生成 HTML 报告：

```bash
python "<skill_dir>/scripts/scanner.py"
```

扫描器自动：
1. 检测操作系统（Windows / macOS / Linux）
2. 扫描对应平台的三级路径
3. 扫描大文件（>500MB）和旧文件（>90天未修改）
4. 扫描开发项目中的构建产物
5. 生成 JSON 数据 + 交互式 HTML 报告
6. 每个清理项附带可复制的终端命令

---

## 扫描路径详解

### 🟢 立即清（跨平台）

| 平台 | 路径 | 内容 |
|------|------|------|
| **通用** | 系统临时目录 | `/tmp`, `C:\Windows\Temp`, `%TEMP%` |
| **通用** | 浏览器缓存 | Chrome/Edge/Firefox 缓存目录 |
| **通用** | 包管理器缓存 | pip cache, npm cache, yarn cache, cargo cache |
| **通用** | IDE缓存 | VS Code Cache/CachedData, JetBrains caches |
| **Windows** | 回收站 | `C:\$Recycle.Bin` |
| **Windows** | 缩略图缓存 | Explorer thumbcache |
| **Windows** | 即时通讯缓存 | 微信/QQ/企业微信/钉钉/飞书缓存 |
| **macOS** | 废纸篓 | `~/.Trash` |
| **macOS** | 用户缓存 | `~/Library/Caches` (浏览器/应用) |
| **macOS** | 用户日志 | `~/Library/Logs` |
| **macOS** | Xcode缓存 | `~/Library/Developer/Xcode/DerivedData` |
| **macOS** | 模拟器 | `~/Library/Developer/CoreSimulator` |
| **Linux** | 用户缓存 | `~/.cache` |
| **Linux** | 废纸篓 | `~/.local/share/Trash` |

### 🟡 确认后清（跨平台）

| 路径 | 内容 |
|------|------|
| `~/Downloads` | 下载文件夹 |
| `~/Desktop` | 桌面 |
| `~/Documents` | 文档（只展示大文件列表） |
| 项目构建产物 | `node_modules`, `__pycache__`, `dist`, `build`, `.next`, `out`, `target/` |
| Docker | 未使用的镜像、容器、卷（`docker system df`） |
| 大文件 | >500MB 的单文件（仅在用户目录下） |
| 旧文件 | >90天未修改的大文件 |

### 🔴 保留（跨平台）

| 平台 | 路径 |
|------|------|
| **Windows** | `C:\Windows`, `C:\Program Files`, `C:\Program Files (x86)`, 开始菜单 |
| **macOS** | `/System`, `/bin`, `/sbin`, `/usr`, `~/Library`（非缓存部分） |
| **Linux** | `/etc`, `/usr`, `/boot`, `/lib`, 系统服务目录 |

---

## 生成的命令格式

每个可清理项都会附带 **可直接复制执行的命令**：

### Windows (PowerShell)
```powershell
# 移到废纸篓（推荐）
Remove-Item -Path "C:\path\to\cache" -Recurse -Force -ErrorAction SilentlyContinue

# 清空回收站
Clear-RecycleBin -Force
```

### Windows (cmd)
```cmd
# 删除目录
rmdir /s /q "C:\path\to\cache"

# 清空回收站
rd /s /q C:\$Recycle.Bin
```

### macOS / Linux (bash)
```bash
# 移到废纸篓（可恢复）
mv "/path/to/cache" ~/.Trash/

# 彻底删除（不可恢复）
rm -rf "/path/to/cache"

# 清空废纸篓
rm -rf ~/.Trash/*
```

---

## 报告 HTML 结构

1. **磁盘总览** — 各分区容量/已用/可用，彩色进度条
2. **清理摘要** — 三级总大小、项数、预估可释放空间
3. **占用排行 Top 10** — 最大的 10 个空间占用项
4. **🟢 立即清** — 每项带复制按钮的命令
5. **🟡 确认后清** — 每项带「打开目录」和「删除命令」按钮
6. **🔴 保留** — 只展示大小和说明，无删除入口
7. **大文件扫描** — >500MB 单文件列表
8. **长期优化建议** — 平台专属建议

---

## 使用场景

**场景 A：用户说「硬盘不够用」**
→ 运行 scanner.py → 生成报告 → 展示磁盘总览 + 可清理空间 → 用户复制命令执行

**场景 B：用户说「扫描大文件」**
→ 运行 scanner.py → 重点展示大文件列表 → 用户手动确认删除

**场景 C：用户说「帮我清理 Mac」**
→ 自动检测 macOS → 扫描 Mac 专属路径 → 生成 Mac 命令

**场景 D：用户说「帮我清理磁盘垃圾」**
→ 生成报告 → 用户在报告中复制 🟢 命令 → 粘贴到终端执行 → **Agent 不代为执行删除**

---

## 文件清单

```
storage-clean/
├── SKILL.md                  # 本文件
├── scripts/
│   ├── scanner.py            # 扫描脚本（核心，跨平台）
│   └── cleaner.py            # 清理脚本（可选，供高级用户使用）
├── templates/
│   └── report_template.html  # HTML 报告模板
└── reports/                  # 生成的报告
```

---

## 依赖

- Python 3.8+
- psutil（跨平台磁盘信息获取）

安装：
```bash
pip install psutil
```

---

## 注意事项

1. **权限**：系统目录可能需要 sudo/管理员权限才能扫描
2. **大文件扫描**：为了速度，只扫描用户目录（`~` / `%USERPROFILE%`），不递归全盘
3. **符号链接**：自动跳过符号链接，避免循环和重复计算
4. **网络路径**：跳过网络驱动器和挂载点
5. **只读保证**：scanner.py 不包含任何写操作，可以安全运行

---

## 更新日志

### v2.0.0 (2026-06-21)
- **重大更新**：完全重写为跨平台版本
- 新增 macOS / Linux 路径定义
- 新增大文件扫描（>500MB）
- 新增旧文件扫描（>90天未修改）
- 命令输出模式（复制→粘贴→执行），移除 HTML 中的删除按钮
- 新增 Docker 磁盘占用检测
- 新增开发项目构建产物递归扫描
- 三级分级重新定义：立即清 / 确认后清 / 保留

### v1.0.0 (2026-06-09)
- 初始版本（Windows only）

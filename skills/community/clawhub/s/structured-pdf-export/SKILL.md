---
name: structured-pdf-export
description: 将结构化内容（表格、对比清单、数据可视化）转换为美化 PDF 并发送。在准备输出竖线表格时自动触发：创建 HTML → 启动本地服务器 → 打开浏览器 → 转成 PDF → 发送 + 清理临时文件。文件名用中文描述性表述。**依赖条件**：OpenClaw 浏览器工具、Message 工具、Python HTTP 服务器、单用户或受信环境。不支持多用户环境的进程隔离。
metadata:
  {
    "requirements": {
      "platform": "Linux/macOS/Windows",
      "tools": ["browser", "message"],
      "python": "3.6+",
      "ports": "8888 (configurable, must be manually freed if in use)",
      "workspace": "$HOME/.openclaw/workspace or $OPENCLAW_WORKSPACE",
      "user": "single user or trusted multi-user environment"
    },
    "limitations": {
      "multiuser": "Cannot safely manage process ownership on multi-user systems",
      "portManagement": "Requires manual intervention if configured port is in use by unrelated processes",
      "sensitiveData": "Manual verification required; no automatic sensitive data scanning",
      "browserAPI": "Depends on OpenClaw browser tool returning local file paths"
    }
  }
---

# Structured PDF Export

当你准备输出**表格、对比、清单**等结构化内容时，不直接用竖线表格，而是通过本 Skill 生成美化的 PDF 可视化。

⚠️ **使用前必读：限制和假设**（见本文档末尾）

## 何时使用

✅ **适用场景**：
- 需要展示表格对比
- 需要列出详细清单
- 需要数据可视化
- 需要结构化信息展示
- **环境**：单用户系统或完全受信的多用户环境

❌ **不适用**：
- 简单的文本列表（直接回复即可）
- 代码块（用 markdown 高亮）
- 普通文档内容
- **环境**：多用户系统，用户不受信或进程隔离要求严格

## 完整工作流

### 0️⃣ 环境检查与初始化

在任何操作前执行：

```bash
# 定义工作目录（不要使用硬编码路径）
WORK_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
TEMP_DIR="${WORK_DIR}/.pdf-export-tmp"
PORT=8888  # 可配置端口

# 检查权限和存在性
if [ ! -d "$WORK_DIR" ]; then
  mkdir -p "$WORK_DIR" || { echo "❌ 无法创建工作目录"; exit 1; }
fi

if [ ! -w "$WORK_DIR" ]; then
  echo "❌ 工作目录无写权限: $WORK_DIR"
  exit 1
fi

# 创建专用临时目录
mkdir -p "$TEMP_DIR" || { echo "❌ 无法创建临时目录"; exit 1; }
chmod 700 "$TEMP_DIR"
```

### 1️⃣ 准备 HTML（结构化布局）

创建包含以下元素的 HTML 文件。**重要**：不在 HTML 中包含任何敏感数据。验证所有内容都是非机密的。

### 2️⃣ 启动 HTTP 服务器（受限的进程管理）

⚠️ **重要限制**：本工作流无法安全地在多用户系统中管理进程。见"限制和假设"。

```bash
PORT=8888

# ⚠️ 检查端口占用——但无法区分所有者
# 这会杀死任何占用该端口的进程，可能包括无关的进程！
if lsof -i :$PORT 2>/dev/null | grep -q LISTEN; then
  OLD_PID=$(lsof -t -i :$PORT)
  echo "⚠️  警告：端口 $PORT 被占用 (PID=$OLD_PID)"
  echo "❌ 请手动验证这是你的进程，然后手动 kill $OLD_PID"
  echo "❌ 不自动 kill 以避免中断其他用户的进程"
  exit 1
fi

# 启动服务器
cd "$TEMP_DIR" || exit 1
python3 -m http.server $PORT > "$TEMP_DIR/server.log" 2>&1 &
SERVER_PID=$!

sleep 1
if ! kill -0 $SERVER_PID 2>/dev/null; then
  echo "❌ 服务器启动失败"
  cat "$TEMP_DIR/server.log"
  exit 1
fi

echo $SERVER_PID > "$TEMP_DIR/server.pid"
```

### 3️⃣ 用浏览器打开 HTML（本地渲染验证）

- 验证 URL 仅为本地：`http://localhost:8888/...`
- 不允许非本地 URL
- **手动验证**页面无敏感数据（不含 password、secret、token、key 等）

### 4️⃣ 转换为 PDF（本地生成，无外部上传）

- 验证 `browser.pdf` 返回本地文件路径（`FILE:/...` 或 `/...`）
- 不允许外部 URL 返回
- PDF 全程本地生成

### 5️⃣ 复制到工作目录并重命名（权限检查）

```bash
SOURCE_PDF="/path/to/generated.pdf"
DEST_PDF="$WORK_DIR/[中文文件名]-$(date +%Y-%m-%d).pdf"

if [ ! -r "$SOURCE_PDF" ]; then
  echo "❌ 无法读取 PDF: $SOURCE_PDF"
  exit 1
fi

cp "$SOURCE_PDF" "$DEST_PDF" || exit 1
if [ ! -r "$DEST_PDF" ]; then
  echo "❌ 目标文件无法读取"
  exit 1
fi
```

### 6️⃣ 发送文件给用户（仅发送本地文件）

- 验证文件路径是绝对路径
- 仅使用 `message.send` 的 `filePath` 参数
- **假设**：message 工具自动验证本地文件（OpenClaw 的行为）

### 7️⃣ 清理临时文件（完全清理）

```bash
if [ -f "$TEMP_DIR/server.pid" ]; then
  SERVER_PID=$(cat "$TEMP_DIR/server.pid")
  if kill -0 $SERVER_PID 2>/dev/null; then
    kill $SERVER_PID 2>/dev/null
    sleep 1
    if kill -0 $SERVER_PID 2>/dev/null; then
      kill -9 $SERVER_PID 2>/dev/null
    fi
  fi
fi

rm -rf "$TEMP_DIR"
```

## 限制和假设（必读）

### ⚠️ 多用户系统的进程管理限制

**问题**：
```bash
lsof -i :8888  # 显示占用端口的所有进程，但无法验证所有者
kill $PID      # 可能杀死无关进程！
```

**在工作流中**：
- 脚本检查端口占用但无法区分所有者
- 无法安全地 kill 其他用户的进程
- 可能中断其他用户或应用的工作

**在多用户系统中的风险**：
- ❌ 可能中断其他用户的 PDF 导出工作流
- ❌ 可能中断其他应用的 HTTP 服务
- ❌ 无法安全地验证进程所有权

**缓解方案**（在多用户系统中）：
1. 使用**随机端口**或**用户特定端口**：`PORT=8000 + $(id -u)`
2. **所有用户协调**使用时间窗口
3. **完全信任**系统中的所有用户
4. **不支持**不受信用户同时使用

### 敏感数据检查的限制

**文档要求**：用户必须手动验证 HTML/PDF 中无敏感数据。

**为什么不自动扫描**：
- 敏感数据多样化（API 密钥、PII、医疗数据等）
- 合法关键词可能被误报
- 编码或加密的敏感数据无法检测
- 正则表达式容易产生假阳性和假阴性

**用户责任**：
- ✅ 生成 HTML 时仔细审查内容
- ✅ 打开浏览器前再次检查
- ✅ 发送 PDF 前验证无敏感信息

### 工具依赖的假设

| 工具 | 假设 | 验证 |
|------|------|------|
| **OpenClaw 浏览器** | 仅打开本地 URL，返回本地文件路径 | `browser.pdf` 返回 `FILE:/...` 或 `/...` |
| **message.send** | 仅接受本地文件，不上传到云端 | 检查 OpenClaw 文档 |
| **Python HTTP server** | 仅提供本地文件访问 | 默认行为，POSIX 标准 |

## 关键规则表

| 项目 | 规则 | 约束条件 |
|------|------|--------|
| **路径管理** | 使用 `$HOME` 或 `$OPENCLAW_WORKSPACE` | 避免硬编码 |
| **权限检查** | 验证目录存在、可写、可读 | 单用户有效；多用户需协调 |
| **进程管理** | 保存 PID、验证停止 | 无法验证进程所有权 |
| **敏感数据** | 手动审查内容 | 不支持自动扫描 |
| **临时文件** | 专用目录 + `chmod 700` | 防止其他本地用户访问 |

## 使用辅助脚本快速开始

```bash
# 默认工作目录
python3 scripts/generate_table_pdf.py --title "技能清单"

# 自定义工作目录
python3 scripts/generate_table_pdf.py --title "技能清单" --workdir /my/path
```

**脚本功能**：
- ✅ 权限检查和目录初始化
- ✅ HTML 模板生成到临时目录
- ✅ 详细的后续步骤说明

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| 端口已被占用 | 进程未清理或其他用户占用 | 手动 `kill -9 $PID` 或更改端口 |
| PDF 为空 | 浏览器渲染未完成 | 增加延迟到 3-5 秒 |
| 文件无法发送 | 路径错误或权限不足 | 检查路径和权限 |
| 多用户冲突 | 进程/端口冲突 | 使用唯一端口或不同时间窗口 |

## 性能建议

- HTML 文件 < 2MB
- 表格行数 < 100（超过则分页）
- CSS 样式而非内联
- 避免过多 JavaScript

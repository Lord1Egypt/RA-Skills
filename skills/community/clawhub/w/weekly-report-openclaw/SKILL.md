---
name: weekly-report
description: |
  自动化工作周报生成系统。支持自动登录周报系统、获取团队周报数据、使用 AI 进行内容提炼总结、生成格式化的 Word 文档。
  触发场景：(1) 用户要求生成周报 (2) 用户询问本周/上周工作总结 (3) 用户提到"周报"、"weekly report"、"工作总结"
  (4) 用户需要汇总团队成员工作内容
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["python3"]
      setup: "./scripts/setup.sh"
    env:
      - WEEKLY_REPORT_USERNAME
      - WEEKLY_REPORT_PASSWORD
      - DEEPSEEK_API_KEY
---

# Weekly Report - 周报自动生成系统

自动化工作周报生成工具，支持从周报系统获取数据、AI 智能总结、生成 Word 文档。

## 快速开始

### 1. 环境准备

首次使用前，运行自动安装脚本配置环境：

**Windows (PowerShell):**
```powershell
cd skills/weekly-report/scripts
./setup.ps1
```

**macOS / Linux (Bash):**
```bash
cd skills/weekly-report/scripts
chmod +x setup.sh
./setup.sh
```

安装脚本会自动检测并安装：
- Python 3.10+ (需要预先安装)
- uv 包管理器
- Python 依赖包
- Playwright Chromium 浏览器

> **国内用户**: 脚本会自动检测网络环境，在无法访问 Google 时使用国内镜像源加速下载。

<details>
<summary>手动安装（可选）</summary>

如果不想使用自动脚本，可以手动安装：

```bash
# 安装 uv (Windows)
irm https://astral.sh/uv/install.ps1 | iex

# 安装 uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
cd skills/weekly-report/scripts
uv sync

# 安装 Playwright Chromium
uv run playwright install chromium
uv run playwright install-deps chromium  # Linux 需要
```

</details>

### 2. 配置环境变量

```bash
export WEEKLY_REPORT_USERNAME="your_username"
export WEEKLY_REPORT_PASSWORD="your_password"
export DEEPSEEK_API_KEY="your_api_key"
```

### 3. 生成周报

```bash
# 生成本周周报
uv run python generate.py --week today

# 生成上周周报
uv run python generate.py --week last

# 生成指定日期所在周的周报
uv run python generate.py --week 2026-03-07
```

## 命令说明

### generate.py - 生成周报

主脚本，执行完整的周报生成流程。

```bash
python generate.py [OPTIONS]
```

**选项：**
- `--week, -w`: 周日期，支持 `today`（本周）、`last`（上周）、`YYYY-MM-DD`（指定日期）
- `--team, -t`: 团队名称，默认使用配置中的团队
- `--output, -o`: 输出文件名，不指定则自动生成
- `--force-login, -f`: 强制重新登录，不使用缓存的 token
- `--headless`: 无头模式运行浏览器
- `--verbose, -v`: 详细输出模式

**输出格式（JSON）：**
```json
{
  "success": true,
  "output_file": "output/周报_科创研发组_2026-03-02-2026-03-08.docx",
  "items_count": 25,
  "filtered_count": 25,
  "week_range": "2026.03.02-2026.03.08"
}
```

### login.py - 登录管理

单独执行登录操作，用于获取和缓存认证 token。

```bash
python login.py [OPTIONS]
```

**选项：**
- `--force, -f`: 强制重新登录
- `--headless, -H`: 无头模式

**输出格式（JSON）：**
```json
{
  "success": true,
  "message": "Login successful, token cached"
}
```

## 工作分类说明

周报内容按以下分类整理：

| 分类 | 说明 |
|------|------|
| 人才转型 | AI培训、技能学习、人才培养 |
| 自主开发 | 自主开发的应用、工具、系统 |
| 科创支撑 | 专利申报、创新项目、科创制度 |
| AI架构及网运安全自智规划 | AI架构、监控智能化、态势感知 |
| 系统需求规划建设 | 系统需求分析、平台建设、系统规划 |
| 综合工作 | 日常运维、综合事务、其他 |

## 团队成员配置

可在 `config/settings.yaml` 或通过 `--team-members` 参数配置团队成员列表，只有列表中的成员周报会被包含在最终文档中。

## 示例用法

```bash
# 生成科创研发组本周周报
uv run python generate.py --team "科创研发组" --week today

# 强制重新登录后生成上周周报
uv run python generate.py --week last --force-login

# 无头模式生成周报（适用于 CI/CD）
uv run python generate.py --week today --headless

# 指定输出文件名
uv run python generate.py --week today --output "周报_2026年第10周.docx"
```

## 详细文档

- [配置说明](references/configuration.md)
- [工作流程](references/workflow.md)

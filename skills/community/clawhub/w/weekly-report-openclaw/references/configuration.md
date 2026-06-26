# 配置说明

本文档详细说明 weekly-report skill 的配置方式。

## 环境变量配置

### 必需环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `WEEKLY_REPORT_USERNAME` | 登录用户名 | `your_username` |
| `WEEKLY_REPORT_PASSWORD` | 登录密码 | `your_password` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-xxxxx` |

### 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥（使用 OpenAI 时需要） | - |

### 配置示例

**Linux/macOS:**
```bash
export WEEKLY_REPORT_USERNAME="your_username"
export WEEKLY_REPORT_PASSWORD="your_password"
export DEEPSEEK_API_KEY="sk-xxxxx"
```

**Windows (PowerShell):**
```powershell
$env:WEEKLY_REPORT_USERNAME="your_username"
$env:WEEKLY_REPORT_PASSWORD="your_password"
$env:DEEPSEEK_API_KEY="sk-xxxxx"
```

**使用 .env 文件:**
```env
WEEKLY_REPORT_USERNAME=your_username
WEEKLY_REPORT_PASSWORD=your_password
DEEPSEEK_API_KEY=sk-xxxxx
```

## YAML 配置文件

可以创建 `config/settings.yaml` 文件来自定义配置：

```yaml
# 系统配置
system:
  base_url: "http://120.210.237.117:7006/hap"
  account_id: "a0aadd3f-2d30-4dcd-b901-8cf689c59dc3"

# API 配置
api:
  worksheet_id: "64b4912b881be8545d91a689"
  app_id: "355690a6-f48c-4373-8a55-465bee680f30"
  view_id: "64b4912cda6eba1005393603"

# 登录配置
login:
  headless: false
  timeout: 300
  login_url: "/login"

# LLM 配置
llm:
  provider: "deepseek"
  model: "deepseek-chat"
  base_url: "https://api.deepseek.com/v1"
  max_tokens: 4000
  temperature: 0.7

# 默认值
defaults:
  team: "科创研发组"
  template_path: "template.docx"
  output_dir: "output"
  team_members:
    - "杨浩然"
    - "张勇"
    - "李楠"
    - "赵超"
    - "陶荣鑫"
    - "殷晨晨"
    - "朱达贤"
```

## 配置项详解

### system 系统配置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `base_url` | 周报系统基础 URL | `http://120.210.237.117:7006/hap` |
| `account_id` | 账户 ID | - |

### api API 配置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `worksheet_id` | 工作表 ID | - |
| `app_id` | 应用 ID | - |
| `view_id` | 视图 ID | - |

### login 登录配置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `headless` | 无头模式运行浏览器 | `false` |
| `timeout` | 登录超时时间（秒） | `300` |
| `login_url` | 登录页面路径 | `/login` |

### llm LLM 配置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `provider` | LLM 提供商 (`deepseek` / `openai`) | `deepseek` |
| `model` | 模型名称 | `deepseek-chat` |
| `base_url` | API 基础 URL | `https://api.deepseek.com/v1` |
| `max_tokens` | 最大输出 token 数 | `4000` |
| `temperature` | 生成温度 | `0.7` |

### defaults 默认值配置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `team` | 默认团队名称 | `科创研发组` |
| `template_path` | 模板文件路径 | `template.docx` |
| `output_dir` | 输出目录 | `output` |
| `team_members` | 团队成员列表（用于过滤） | - |

## 团队成员过滤

`team_members` 列表用于过滤周报数据，只有列表中的成员提交的周报会被包含在最终文档中。

**修改团队成员：**

```yaml
defaults:
  team_members:
    - "成员1"
    - "成员2"
    - "成员3"
```

## 模板文件

周报模板文件 `template.docx` 应放置在以下任一位置：

1. 当前工作目录
2. `assets/` 目录
3. 配置文件中指定的路径

模板支持 Jinja2 语法，可用变量参见 `references/workflow.md`。

## 输出目录

生成的周报文档默认保存在 `output/` 目录下，可通过配置修改：

```yaml
defaults:
  output_dir: "reports/weekly"
```

## 命令行覆盖

部分配置可通过命令行参数覆盖：

```bash
# 覆盖团队
python generate.py --team "其他团队"

# 覆盖输出文件名
python generate.py --output "custom_report.docx"

# 使用无头模式
python generate.py --headless

# 指定配置文件
python generate.py --config /path/to/config.yaml
```

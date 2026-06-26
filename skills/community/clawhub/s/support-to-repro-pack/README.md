# support-to-repro-pack

**客服工单 → 可复现问题包生成工具**

一个 Claude Code 技能 + Python 后端工具。把客服收到的杂乱材料（工单、日志、截图、聊天记录）自动转化为脱敏、结构化、可直接交给研发的问题包。

Python 负责确定性工作（PII 脱敏、日志解析、事实提取），Claude 负责语义推理（缺失信息检测、根因分析、复现步骤生成）。

---

## 它能解决什么问题？

客服转给研发的 bug 工单，常见痛点：
- 包含客户隐私（手机号、身份证、API 密钥），不能直接转发
- 信息零散，缺少环境版本、复现步骤
- 日志没整理，错误码散落在各处
- 研发拿到工单后还要反复追问

这个工具一键解决：**输入杂乱原始材料 → 输出 8 个标准化文件**，隐私全部脱敏，事实自动提取，研发可以直接开干。

---

## 功能一览

- **PII 脱敏** — 17 种隐私模式：邮箱、手机号（中美英）、IP、信用卡、身份证、社保号、AWS 密钥、JWT、Stripe 密钥、密码、含凭证的 URL、Cookie、UUID、私钥、Bearer Token、API Key
- **日志解析** — 自动识别 JSON / syslog / 纯文本格式，提取时间戳、日志级别、来源
- **堆栈提取** — 支持 Python、Java、JavaScript/Node.js、Go 四种语言的堆栈信息
- **事实抽取** — 版本号、AWS 区域、功能开关、错误码、User-Agent、URL
- **事件时间线** — 从日志条目中重建事件时间线
- **中英双语** — 中文工单出中文结果，英文工单出英文结果

---

## 从零开始：安装与启动

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/support-to-repro-pack.git
cd support-to-repro-pack
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .repro-env
source .repro-env/bin/activate
```

### 3. 安装

```bash
pip install -e ".[dev]"
```

### 4. 验证安装

```bash
repro-pack --version
# 输出: repro-pack, version 0.1.0
```

看到版本号就说明装好了。

---

## 怎么用？

### 方式一：命令行（CLI）

最简单的用法，一行命令跑完整个流程：

```bash
repro-pack run \
  --ticket examples/case_easy/input_ticket.md \
  --logs examples/case_easy/input_logs.txt \
  --outdir output/
```

也可以单独使用某个功能：

```bash
repro-pack redact input.txt              # 只做 PII 脱敏
repro-pack redact input.txt --audit      # 脱敏 + 审计报告
repro-pack parse logs.txt --format json  # 解析日志
repro-pack extract combined.txt          # 提取环境事实
repro-pack timeline logs.txt             # 构建事件时间线
repro-pack traces logs.txt               # 提取堆栈信息
```

### 方式二：作为 Claude Code 技能使用

把 `.claude/skills/support-to-repro-pack/` 目录复制到你项目的 `.claude/skills/` 下，然后对 Claude 说：

> "帮我整理这个客户 bug"
> "把这个工单变成研发 issue"
> "脱敏这些日志并生成复现步骤"

Claude 会自动调用 Python 工具做脱敏和提取，然后用 AI 补充语义分析（复现步骤、根因假设、严重等级评估）。

**支持图片输入：** 如果客户发了截图，把图片路径一起给 Claude，它会先读图提取文字信息，再走标准流程。

---

## 输出文件说明

运行完成后会在输出目录生成 **8 个文件**：

| 文件 | 说明 | 给谁看 |
|------|------|--------|
| `1_sanitized_ticket.md` | 脱敏后的工单（所有隐私替换为占位符） | 研发 |
| `2_sanitized_logs.txt` | 脱敏后的日志 | 研发 |
| `3_facts.json` | 提取的环境事实（版本、区域、错误码等） | 研发 |
| `4_timeline.json` | 事件时间线 | 研发 |
| `5_engineering_issue.md` | 工程 Issue 文档 | 研发 |
| `6_internal_escalation.md` | 内部升级摘要 | PM / 技术主管 |
| `7_customer_reply.md` | 客户回复（不含任何内部信息） | 客服 → 客户 |
| `8_redaction_report.json` | 脱敏审计报告（哪些隐私在第几行被替换） | 合规 / 安全 |

---

## 怎么验证项目结果？

### 跑测试

```bash
pytest
```

应该看到 **113 passed**，覆盖所有模块。

### 跑示例案例

项目内置 3 个测试案例，难度递增：

| 案例 | 语言 | 场景 | 挑战 |
|------|------|------|------|
| `case_easy` | 英文 | 导出功能崩溃 | JS 堆栈、JWT、多个邮箱、功能开关 |
| `case_medium` | 中文 | 用户管理页面超时 | 中文手机号、身份证、密码、Java 堆栈 |
| `case_hard` | 英文 | 支付处理失败 | Stripe 密钥、多币种、混合 HTTP 错误码 |

逐个跑一遍：

```bash
# 英文简单案例
repro-pack run \
  --ticket examples/case_easy/input_ticket.md \
  --logs examples/case_easy/input_logs.txt \
  --outdir /tmp/result_easy

# 中文案例
repro-pack run \
  --ticket examples/case_medium/input_ticket.md \
  --logs examples/case_medium/input_logs.txt \
  --outdir /tmp/result_medium

# 英文复杂案例
repro-pack run \
  --ticket examples/case_hard/input_ticket.md \
  --logs examples/case_hard/input_logs.txt \
  --outdir /tmp/result_hard
```

然后查看输出，重点检查：

```bash
# 看脱敏是否干净（不应该再看到真实邮箱、手机号）
cat /tmp/result_easy/1_sanitized_ticket.md

# 看提取了哪些事实
cat /tmp/result_easy/3_facts.json

# 看脱敏审计（哪些隐私被抓到了）
cat /tmp/result_easy/8_redaction_report.json
```

### 跑自动化评测

```bash
python -m eval.run_eval examples/
```

会输出评分表，从三个维度打分：

```
| 案例        | 事实提取 | 脱敏召回率 | 输出完整性 | 总分       |
|-------------|---------|-----------|-----------|-----------|
| case_easy   | 90.0%   | 100.0%    | 100.0%    | 96.7%     |
| case_hard   | 80.0%   | 100.0%    | 100.0%    | 93.3%     |
| case_medium | 100.0%  | 100.0%    | 100.0%    | 100.0%    |
| 平均         | 90.0%   | 100.0%    | 100.0%    | 96.7%     |
```

---

## 项目结构

```
support-to-repro-pack/
├── src/repro_pack/              # 核心 Python 代码
│   ├── redactor/                # PII 脱敏引擎（17 种正则模式）
│   │   ├── patterns.py          # 正则表达式定义
│   │   ├── engine.py            # 脱敏引擎（从右到左替换，重叠检测）
│   │   ├── detector.py          # 仅检测模式
│   │   └── report.py            # 审计报告生成
│   ├── parser/                  # 输入解析
│   │   ├── log_parser.py        # 日志解析（JSON / syslog / 纯文本）
│   │   ├── stack_trace.py       # 堆栈提取（Python / Java / JS / Go）
│   │   ├── ticket_parser.py     # 工单解析（Markdown / 纯文本）
│   │   └── formats.py           # 日志格式检测
│   ├── extractor/               # 结构化信息提取
│   │   ├── env_facts.py         # 版本、区域、功能开关、角色、错误码
│   │   ├── error_codes.py       # HTTP / 应用 / gRPC 错误码分类
│   │   ├── timeline.py          # 事件时间线构建
│   │   └── user_agent.py        # 浏览器 / 操作系统解析
│   ├── packager/                # 输出打包
│   │   ├── builder.py           # 文件组装与验证
│   │   ├── renderer.py          # Jinja2 模板渲染
│   │   └── archive.py           # ZIP 打包
│   ├── pipeline.py              # 全流程编排
│   ├── cli.py                   # CLI 入口（6 个子命令）
│   └── models.py                # 数据模型定义
├── .claude/skills/              # Claude Code 技能层
│   └── support-to-repro-pack/
│       ├── SKILL.md             # 技能编排文件
│       ├── templates/           # 输出文档模板
│       └── references/          # 参考文档（严重等级矩阵、复现检查清单）
├── tests/                       # 113 个测试用例
├── eval/                        # 自动化评测框架
├── examples/                    # 3 个示例案例（easy / medium / hard）
├── pyproject.toml               # 项目配置
└── LICENSE                      # MIT 开源协议
```

---

## 设计理念

**为什么不全用 AI？**

PII 脱敏必须用正则——确定性、可审计、不会遗漏。AI 擅长的是语义理解：判断问题严重程度、猜测根因、生成复现步骤。所以我们的设计是：

- **Python 正则** → 做确定性工作（脱敏、解析、提取），保证可靠性和可审计性
- **Claude AI** → 做语义推理（缺失信息检测、矛盾检查、根因假设、严重等级评估）

两层配合，既安全又智能。

---

## 依赖

仅两个运行时依赖，保持轻量：

- `click >= 8.1` — CLI 框架
- `jinja2 >= 3.1` — 模板引擎

开发依赖：
- `pytest >= 7.0` — 测试框架

---

## License

MIT

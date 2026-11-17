---
name: 百度知道回答自动发布
description: "在百度知道指定问题下，把本地准备好的回答文稿自动发布为回答。"
version: 1.0.5
author: 深圳匠厂科技有限公司
metadata:
  openclaw:
    slug: publish-answer-baidu-know
    platform_kit_min_version: "1.0.17"
    emoji: "📝"
    category: "内容营销"
    developer_ids:
      - 10032
      - 12428
allowed-tools:
  - bash
---

# 百度知道回答自动发布

在百度知道 Web 指定问题页下，将本地准备好的回答文稿自动填写并发布为回答。

## 面向用户问答（LLM 规则）

- 本文（`SKILL.md`）是 LLM / OpenClaw 平台读取的技能入口，**不是**用户市场说明。
- 根目录 `README.md` 是面向普通用户的说明。

当用户询问以下问题时，**必须优先读取**根目录 `README.md`，并用用户能理解的业务语言回答：

- 这个技能是做什么的
- 这个技能怎么用
- 适合什么场景
- 使用前要准备什么
- 执行后会得到什么
- 能不能帮我完成某个业务任务

- **不要**把 `SKILL.md`、`references/`、`development/` 中的技术细节直接作为用户回答。
- **只有当**用户明确询问命令、参数、输出结构、开发、调试、集成或排错时，才读取 `references/` 或 `development/`。
- 若 `README.md` 与 `SKILL.md` / `references` 表述冲突：对用户展示与市场说明以 `README.md` 为准；对执行契约、CLI、schema、运行约束以 `SKILL.md` / `references` 为准。
- 回答用户时**不要**暴露 Playwright、DOM、Python、RPA 等实现细节，除非用户明确询问技术实现。
- 用户未问技术实现时，**不要**讨论 slug 命名规则；开发者问命名或 slug 时，读取 `development/NAMING.md`。

## 文档分工

| 文档 | 读者 | 用途 |
|------|------|------|
| 根目录 `README.md` | 普通用户 | 技能市场详情页说明（`metadata.readme_md` 主来源） |
| `SKILL.md`（本文） | LLM / OpenClaw 平台 | 技能入口、触发与运行契约摘要 |
| `references/` | Agent 编排/调用 | 渐进式加载：CLI 契约、字段 schema 等 |
| `development/` | 开发者 / AI 编程代理 | 需求、开发教程、测试、技术规范 |

## 目录约定

- `assets/`、`development/`、`evals/`、`references/`、`scripts/`、`tests/`
- CLI 入口固定为 `scripts/main.py`
- 业务逻辑按 `cli / db / service / util` 分层

## 最小命令

```bash
python {baseDir}/scripts/main.py health
python {baseDir}/scripts/main.py config-path
python {baseDir}/scripts/main.py version
```

配置：仓库 `.env.example` 为模板；用户 `.env` 在 `{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/{slug}/.env`，启动时自动 bootstrap。优先级：进程环境变量 > 用户 `.env` > `.env.example`。

## 业务命令

```bash
python {baseDir}/scripts/main.py run \
  --question-url https://zhidao.baidu.com/question/XXXXXXX \
  --input-id D:\answers\demo.md \
  [--target ACCOUNT_HINT] \
  [--idempotency-key KEY]
```

参数说明：

- `--question-url` 必填，百度知道问题页 URL
- `--input-id` 必填，本地回答文稿路径
- `--target` 可选，指定账号 ID 或登录标识；省略时由 account-manager 自动挑选
- `--idempotency-key` 可选，幂等键，重复运行不会重复发布

成功时 stdout 输出 JSON：

```json
{
  "ok": true,
  "account_id": "12",
  "question_url": "https://zhidao.baidu.com/question/XXXXXXX",
  "answer_path": "D:\\answers\\demo.md",
  "status": "success",
  "platform_message": "提交成功",
  "publish_record_id": 1,
  "duplicate": false
}
```

## 运行依赖

- Python 运行环境由匠厂宿主注入**共享 runtime**：`{JIANGCHANG_DATA_ROOT}/python-runtime/.venv`。
- 公共能力来自共享 runtime 安装的 `jiangchang-platform-kit>=1.0.17`（`jiangchang_skill_core` 包）；**不要 vendor** `scripts/jiangchang_skill_core/`。
- `requirements.txt` **只声明技能特有** Python 三方依赖；`jiangchang-platform-kit`、`playwright` 等公共能力由宿主共享 runtime 提供。

## 兄弟技能依赖

- **account-manager**：提供百度知道账号的 profile_dir 与租约。
- 首次使用前需在 account-manager 注册平台：
  ```
  account platform ensure --key baidu_zhidao --display-name "百度知道" \
    --domain content --url "https://zhidao.baidu.com" --auth-strategy qr_code_manual
  ```
- 本技能通过 `service/account_client.py` 以 subprocess CLI 方式调用，**不 import** account-manager 内部模块。

## 适配器档位

按 `development/ADAPTER.md` 四档规范：

- `mock` — CI 默认，不触网，验证流程编排
- `simulator_rpa` — 开发联调，使用本地仿真页
- `real_rpa` — 生产，真实百度知道页面（默认档位）

档位由 `OPENCLAW_TEST_TARGET` 控制；生产默认 `real_rpa`。

## 平台元数据

- `metadata.openclaw.developer_ids`：技能发布后的默认开发者可见用户 ID 列表。
- 当 `access_scope = 0`（不公开）时，平台会把 `developer_ids` 中的用户自动补写到 `skill_user_access`。

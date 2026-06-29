# yufluentcn-record-outcome

Harness 效果闭环辅助包：将 Listing / SEO 等技能返回的 **`run_id`** 与卖家反馈的销量、点击、曝光登记到 Yufluent。

**不走** `POST /v1/skills/*/run`，仅 `POST /v1/agent/outcomes`（与 OpenClaw 对话共用 `tk-*`）。

## 快速开始

```powershell
cd skills\yufluentcn-record-outcome
pip install -r requirements.txt

$env:TOKENAPI_KEY = "tk-你的密钥"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts/run.py `
  --run-id "hr_abc123" `
  --event sale `
  --orders 20 `
  --notes "Amazon US 首周"
```

## 何时使用

- 用户说「Listing 上架了」「这周卖了 N 单」，且对话里有过 `run_id=...`
- Agent 在 `record_outcome` 工具不可用时，可退化为本脚本

## 文件结构

```
yufluentcn-record-outcome/
  SKILL.md
  README.md
  .env.example
  requirements.txt          # requests only
  scripts/run.py            # 薄客户端 → record_outcome()
```

云端客户端 `yufluent_api.py` / `bootstrap.py` 在 `skills/_shared/`（打包时注入到 `scripts/`）。

## 相关文档

- [OpenClaw+Yufluent配置方法.md](../../docs/OpenClaw+Yufluent配置方法.md)
- Agent 工具：`agent/workspace/TOOLS.md` → `record_outcome`

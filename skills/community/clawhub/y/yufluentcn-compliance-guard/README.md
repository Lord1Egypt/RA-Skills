# 合规卫士（yufluentcn-compliance-guard）

Harness scene: `compliance_check` · API: `POST /v1/skills/compliance-guard/run`

跨境认证清单、关税估算、标签要求、平台规则参考助手。本机仅需 `requests`。

## 安装

```bash
cd skills/yufluentcn-compliance-guard
pip install -r requirements.txt
# 设置 TOKENAPI_KEY、TOKENAPI_BASE_URL
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选，默认 `http://localhost:8080/v1`）

## 调用

```bash
$env:TOKENAPI_KEY = "***"
python scripts/run.py -m "出口欧盟需要什么认证" --product "儿童玩具" --target-market "欧盟" --mode certification
```

## 四模式

| mode | 用途 |
|------|------|
| `certification` | CE/FCC/CPSC/GPSR 等认证清单 |
| `tariff` | HS 编码 + 税率估算 |
| `labeling` | 标签与成分标注要求 |
| `platform_rules` | 平台类目限制检查 |

Monorepo 测试：`pip install -r requirements-dev.txt && pytest tests/`

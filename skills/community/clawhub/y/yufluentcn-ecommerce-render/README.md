# 模板渲染（yufluentcn-ecommerce-render）

Harness scene: `template_render` · API: `POST /v1/skills/commerce-render/run`

Pillow 确定性渲染（**服务端** Billing）：尺码表、参数卡、卖点网格、对比表、促销 banner。本机仅需 `requests`。

## 安装

```powershell
cd skills\yufluentcn-ecommerce-render
pip install -r requirements.txt   # requests only
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 调用

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts/run.py --product "不锈钢锅" --template size_chart --render-data examples/size_chart.json
```

## 模板

| template | 用途 |
|----------|------|
| `size_chart` | 尺码表 |
| `spec_card` | 参数信息图 |
| `feature_grid` | 卖点网格 |
| `compare_table` | 功能对比表 |
| `promo_banner` | 促销 banner |

## 字体

中文渲染需配置 `RENDER_FONT_PATH`（Pillow 服务端字体）。

## 工作流

`visual-to-render`：visual-craft brief → commerce-render

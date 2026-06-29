# Yufluent 电商 Listing 生成器

跨境电商多平台 Listing 生成技能，经 Yufluent Billing 网关计费；**ClawHub 安装后使用云端 Harness**（本机仅需 `requests`）。

## 快速开始（ClawHub / 云端 — 推荐）

```bash
cd skills/yufluentcn-ecommerce-listing
pip install -r requirements.txt

export TOKENAPI_KEY="tk-your_key"
export TOKENAPI_BASE_URL="http://localhost:8080/v1"

python scripts/run.py \
  --product "无线蓝牙耳机" \
  --keywords "降噪,长续航,运动" \
  --platform amazon \
  --lang zh \
  --format amazon \
  -o listing.txt
```

生产环境将 `TOKENAPI_BASE_URL` 设为控制台同域 `/api/v1`。

### OpenClaw 与 Yufluent

OpenClaw 对话与 `run.py` **共用同一 `tk-*`**（见 https://claw.changzhiai.com/app/openclaw ）。Listing 正文必须来自 `scripts/run.py`（Yufluent 云端 Harness），**禁止** Agent 用对话模型自行撰写。详见 `SKILL.md`。

## Monorepo 本地 Harness（可选）

在完整 TokenApi 仓库内，可用本地 Harness 调试 Prompt：

```bash
pip install -r requirements-dev.txt
python scripts/listing_generator.py --product "..." --keywords "..." --platform amazon
```

`listing_generator.py` 可能在本目录生成 `tokenapi_usage.log`（SDK 默认日志）；该文件已被 `.gitignore` 排除，**勿提交、勿打入 ClawHub 包**。

## ClawHub 打包

```powershell
.\scripts\package-skill.ps1 yufluentcn-ecommerce-listing
# → dist/skills/yufluentcn-ecommerce-listing-1.2.0.zip
```

文档：[技能-Listing客户指南](../../docs/技能-Listing客户指南.md) · [技能开发对接](../../docs/技能开发对接.md)

## 文件结构

**Monorepo**（本目录）：

```
yufluentcn-ecommerce-listing/
  SKILL.md
  scripts/
    run.py                 # 主入口（云端）
    listing_generator.py   # 仅 monorepo 本地 Harness
    format_listing.py      # 仅 listing_generator 使用
  requirements.txt         # requests only
  requirements-dev.txt     # + yufluentcn-sdk/harness
```

`yufluent_api.py`、`cloud_cli.py`、`bootstrap.py` 在 **`skills/_shared/`**（非本技能 `scripts/`）；`run.py` 自动加入 `sys.path` 引用。

**ClawHub zip** 仅含 `run.py` + 上述三个 `_shared` 文件（打包时注入到 `scripts/`），不含 `listing_generator.py` / `format_listing.py`。

## 平台支持

| 平台 | `--format` | 额外字段 |
|------|------------|----------|
| Amazon | `amazon` | 标题、五点、描述、搜索词 |
| Shopify | `shopify` | meta_title、meta_description |
| TikTok Shop | `tiktok` | hashtags、hook |

## 合规

- 生成内容需人工审核后上架
- 遵守各平台卖家条款

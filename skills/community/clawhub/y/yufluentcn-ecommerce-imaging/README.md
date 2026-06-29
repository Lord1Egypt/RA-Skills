# 电商 AI 生图（yufluentcn-ecommerce-imaging）

Harness scene: `image_production` · API: `POST /v1/skills/ecommerce-imaging/run`

白底图、场景图、实拍抠图、多角度套装。Replicate 代理由平台负责，按张计费。本机仅需 `requests`。

## 安装

```powershell
cd skills\yufluentcn-ecommerce-imaging
pip install -r requirements.txt
copy .env.example .env
# 编辑 TOKENAPI_KEY = "tk-***"
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 云端模式（推荐）

```powershell
$env:TOKENAPI_KEY = "***"
$env:TOKENAPI_BASE_URL = "http://localhost:8080/v1"

python scripts/run.py --product "不锈钢不粘锅" --scene white_bg --platform-size amazon-main
```

## 实拍抠图

```powershell
python scripts/run.py --product "蓝牙耳机" --scene white_bg --source-image "C:\photos\product.jpg"
```

## 多角度展示

```powershell
# 一键 5 角度套装
python scripts/run.py --product "蓝牙耳机" --scene multi_angle_pack --source-image "./front.jpg"

# 指定角度
python scripts/run.py --product "蓝牙耳机" --source-image "./front.jpg" --angles "top_view,side_view,back_view"
```

## 工作流

`visual-to-imaging`：visual-craft (main_image brief) → ecommerce-imaging 生图 → visual-craft (image_compliance) 合规检查

## Monorepo 本地开发（不进 ClawHub 包）

完整仓库内可用 `scripts/image_generator.py` 直连 Replicate（需 `REPLICATE_API_TOKEN`），配合 `scripts/prompt_library.py`。ClawHub / OpenClaw 分发包**仅含** `run.py` + `_shared` 注入的 `yufluent_api.py` / `cloud_cli.py` / `bootstrap.py`，不含上述开发脚本。

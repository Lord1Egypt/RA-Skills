# 视觉工坊（yufluentcn-visual-craft）

Harness scene: `visual_content` · API: `POST /v1/skills/visual-craft/run`

A+ 页面结构、视频分镜脚本、主图差异化 brief、图片合规清单。本机仅需 `requests`。

## 安装

```bash
cd skills/yufluentcn-visual-craft
pip install -r requirements.txt
# 设置 TOKENAPI_KEY、TOKENAPI_BASE_URL
```

环境变量：`TOKENAPI_KEY`（`tk-*`，[Yufluent 控制台](https://claw.changzhiai.com) 获取）、`TOKENAPI_BASE_URL`（可选）

## 调用

```bash
$env:TOKENAPI_KEY = "***"
python scripts/run.py -m "TikTok 30秒视频脚本" --product "美妆套装" --platform tiktok --mode video_script
```

## 四模式

| mode | 用途 |
|------|------|
| `a_plus` | A+ 模块 + 文案 + 配图 brief |
| `video_script` | 分镜脚本 |
| `main_image` | 主图差异化方向 |
| `image_compliance` | 图片规格合规检查 |

## 工作流

`visual-to-imaging`：visual-craft brief → ecommerce-imaging 生图 → visual-craft 合规检查

Monorepo 测试：`pip install -r requirements-dev.txt && pytest tests/`

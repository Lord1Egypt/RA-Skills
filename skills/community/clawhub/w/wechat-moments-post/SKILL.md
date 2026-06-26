---
name: wechat-moments-post
description: Automate posting to WeChat Moments on Windows desktop (open Moments window, trigger publish entry, select image, paste caption, click publish). Use when asked to publish/补发朋友圈、上传图片到朋友圈、在电脑端微信发朋友圈或需要稳定的朋友圈发布工作流。
---

# WeChat Moments Post

## Overview
在 Windows 桌面端微信完成“朋友圈”发布的稳定流程与脚本集合，覆盖：打开独立朋友圈窗口、定位发布入口、选择图片、粘贴文案、点击发表与结果确认。

## Configuration（必填）
- `WECHAT_EXE`：微信桌面端可执行文件路径。示例：`C:\Program Files\Tencent\Weixin\Weixin.exe`
- `WECHAT_MOMENTS_IMAGE`：要发布的图片完整路径。示例：`C:\path\to\image.png`
- `WECHAT_MOMENTS_CAPTION`：朋友圈文案（文本）。

可选：
- `WECHAT_MOMENTS_TMP`：临时截图输出目录（默认使用系统临时目录下的 `wechat_moments`）。
- `WECHAT_MOMENTS_VERIFY`：OCR 校验关键词，逗号分隔（不填则用文案首尾片段做弱校验）。

## Workflow（按顺序执行）
1. **确认微信已登录并在主界面**
   - 若出现二维码或“该账号已登录”提示，需用户完成登录后再继续。
2. **打开独立朋友圈窗口**
   - 从微信左侧栏“发现/朋友圈”入口进入。
3. **定位发布入口（顶部三按钮）**
   - 朋友圈窗口左上角有三按钮，**中间相机按钮**为发布入口。
   - 推荐使用脚本扫描点位直到出现“选择文件”窗口。
4. **选择图片**
   - 在“选择文件”对话框直接输入完整路径并回车。
5. **粘贴文案并发表**
   - 点击“这一刻的想法”输入区，粘贴文案。
   - 点击“发表”按钮。
6. **验证**
   - 发布后编辑页会消失，常见跳回“收藏/内容预览”。
   - 若仍停留编辑页，说明未成功点击“发表”，需要再点一次。

## Scripts
按需调用（脚本均在 `scripts/`）：
- `relaunch_wechat_open_moments.py`：重新拉起微信并尝试打开朋友圈窗口（依赖 `WECHAT_EXE`）
- `sweep_publish_icons_fast.py`：扫描顶部三按钮区域，命中“选择文件”窗口
- `select_image_fullpath_now.py`：在文件选择框内直接输入完整图片路径（依赖 `WECHAT_MOMENTS_IMAGE`）
- `publish_with_caption_verify.py`：粘贴文案 + 点击发表（含 OCR 校验，依赖 `WECHAT_MOMENTS_CAPTION`）
- `click_publish_ocr.py`：OCR 定位“发表”按钮并点击

## References
- `references/workflow.md`：完整流程、失败场景与处理

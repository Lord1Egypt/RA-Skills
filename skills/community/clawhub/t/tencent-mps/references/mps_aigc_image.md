# AIGC 生图参数与示例 — `mps_aigc_image.py`

**功能**：AI 生成图片，支持文生图、图生图、3D 全景图，支持 Hunyuan/GEM/Qwen/Vidu/Kling/OG 模型。
> ⚠️ 生成的图片默认存储 12 小时，请尽快下载使用。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 图片描述文本（最多 1000 字符，未传参考图时必填）|
| `--model` | 模型：`Hunyuan`（默认）/ `GEM` / `Qwen` / `Vidu` / `Kling` / `OG` / `Seedream` / `MJ` |
| `--model-version` | 模型版本：GEM `2.5`/`3.0`/`3.1`；Vidu `q2`；Kling `2.1`/`O1`/`3.0`/`3.0-Omni`；OG `image2_low`/`image2_medium`/`image2_high`；Seedream `4.5`/`5.0-lite`/`5.0-pro`；MJ `v7`/`v8.1`/`v8.2` |
| `--scene-type` | 场景化生图（仅 Hunyuan 支持）：`3d_panorama`（全景图）。使用时脚本会自动补 `ModelVersion=3d_2.0`（显式指定 `--model-version` 时不覆盖）|
| `--negative-prompt` | 负向提示词 |
| `--enhance-prompt` | 开启提示词增强 |
| `--image-url` | 参考图 URL（可多次指定，上限随模型/版本不同，见下方「参考图数量上限」）|
| `--image-ref-type` | 参考图类型（与所有来源参考图按顺序一一对应，依次覆盖 `--image-url` / `--image-cos-key` / `--image-local`）：`asset`（内容参考）/ `style`（风格参考）|
| `--image-cos-bucket` | 参考图所在 COS Bucket（可多次指定）。脚本会自动生成预签名 URL 后传入 API |
| `--image-cos-region` | 参考图所在 COS Region（可多次指定）|
| `--image-cos-key` | 参考图的 COS Key（可多次指定）|
| `--image-local` | **本地参考图片路径**（可多次指定）。脚本自动上传到 COS（`aigc_input/` 目录）后生成预签名 URL 传入 API。需配置 `TENCENTCLOUD_COS_BUCKET` 或 `--cos-bucket-name`。支持 jpeg/png/webp |
| `--additional-parameters` | 附加参数（JSON 字符串，模型专属扩展参数）|
| `--aspect-ratio` | 宽高比（如 `16:9`、`1:1`）。支持：`1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `--resolution` | 分辨率：`720P` / `1080P` / `2K` / `4K` |
| `--output-image-count` | 输出图片张数（默认 1）。**仅部分模型生效**：OG 实测可返回多张；GEM / Hunyuan 会静默忽略该参数，始终返回 1 张 |
| `--output-format` | 输出格式：`jpeg` / `png` |
| `--no-wait` | 只提交任务，不等待结果 |
| `--task-id` | 查询已有任务结果 |
| `--cos-bucket-name` | 结果存储 COS Bucket（不配置则使用 MPS 临时存储 12 小时）|
| `--cos-bucket-region` | 结果存储 COS 区域 |
| `--cos-bucket-path` | 结果存储 COS 路径前缀，默认 `/output/aigc-image/` |
| `--download-dir` | 任务完成后将生成图片下载到指定本地目录（默认仅打印预签名 URL）|
| `--operator` | 操作者名称（可选）|
| `--poll-interval` | 轮询间隔（秒），默认 5 |
| `--max-wait` | 最长等待时间（秒），默认 300 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## 参考图数量上限

存在**两层独立限制**，脚本会依次校验：

**第一层 — MPS 平台硬上限 20 张**（与模型无关）。超过时在**提交阶段**即被拒，错误码 `InvalidParameterValue`，原文 `Input ReferenceImageInfos is too much`。

**第二层 — 各模型自身上限**（按模型 + 版本，真接口实测值）：

| 模型 | 版本 | 上限 | 实测依据（超限时的接口报错）|
|------|------|------|------|
| Hunyuan | 3.0 | 3 | `image count should be less than 3` |
| GEM | 2.5 / 3.0 / 3.1 | 20 | 20 张仍成功，模型自身上限被平台层 20 兜住 |
| Qwen | 0925 | 9 | 9 张成功、10 张稳定失败（复测 2 次确认非偶发）|
| Vidu | q2 | 7 | 8 张失败（Vidu 上游返回 `invalid field`）|
| Kling | 2.1 / 3.0 | 4 | `subjectImageList: size must be between 1 and 4` |
| Kling | O1 / 3.0-Omni | 10 | `imageList: size must be between 0 and 10` |
| OG | image2_* | 20 | 20 张仍成功，同样被平台层 20 兜住 |
| Seedream | 4.5 / 5.0-* | 20 | 受平台层 20 约束 |
| MJ | v7 / v8.1 / v8.2 | 3 | 参考图必须是公网直链，见下方 MJ 说明 |

> ⚠️ **Kling 必须按版本区分**：2.1/3.0 走 `subjectImageList`（4 张），O1/3.0-Omni 走 `imageList`（10 张），不可按模型统一取值。

**排查提示**：超出参考图数量时，`CreateAigcImageTask` **仍会正常返回 TaskId**，只在任务执行阶段变成 `FAIL`。因此判断某数量是否被支持，必须查任务终态（`--task-id`），不能只看提交是否成功。脚本已将上述上限前置到本地校验，可避免这类无效提交。

另注：参考图尺寸过小（如 256x256）会让 Kling 报 `Image pixel is invalid`，与数量无关，建议使用 1024x1024 及以上。

## MJ / Seedream 模型说明

**MJ（Midjourney，悠船）**

- 版本：`v7` / `v8.1` / `v8.2`。**`niji` 不可用**——接口返回 `InvalidParameterValue: Not support this ModelVersion`（价格表列了该版本，但 MPS 侧实际未开放）。
- **一次固定返回 4 张图**，已实测确认，无需也无法通过 `--output-image-count` 调整。
- **不支持 `--resolution` / `--aspect-ratio`**，画面比例等通过 Prompt 参数控制：`--ar 16:9`（比例）、`--q 2`（质量）、`--style raw`（写实）、`--s`/`--sw`（风格化）。
- ⚠️ **参考图必须是公网直链**：实测 COS 预签名 URL（带 `q-sign-algorithm` 等查询参数）会让任务 `FAIL`（`model task generate failed`）。因此 `--image-cos-key` 和 `--image-local` 对 MJ 不可用（两者都会转成预签名 URL），脚本已前置拦截并提示改用 `--image-url`。

**Seedream**

- 版本：`4.5` / `5.0-lite` / `5.0-pro`，均已真接口验证可用。

> **Wan 2.2 未收录**：价格表列有该模型，但接口返回 `InvalidParameter: Not support model name.`，MPS 侧实际尚未上线，故脚本不提供该选项。

## 强制规则

- **AIGC 生图 API 的参考图只支持 `ImageUrl`**，不支持 CosInputInfo。使用 `--image-cos-key` 时，脚本会自动生成预签名 URL 后传入 API（需配置 `TENCENTCLOUD_SECRET_ID/KEY`，桶私有读写时才需签名）。
- 使用 `--image-local` 时，脚本会先将文件上传到 COS（`aigc_input/` 目录），再生成预签名 URL 传入 API，需配置 `TENCENTCLOUD_COS_BUCKET` 和 `TENCENTCLOUD_SECRET_ID/KEY`。
- 用户提供 bucket/region/key 时，必须完整传入这三个参数，不得省略。

```bash
# COS 图生图（脚本自动将 COS Key 转为预签名 URL 后传入 API）
python3 scripts/mps_aigc_image.py --prompt "城市夜景" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/ref.jpg

# 本地文件图生图（自动上传 COS 后传入 API）
python3 scripts/mps_aigc_image.py --prompt "城市夜景" \
    --image-local /tmp/ref.jpg

# 本地文件 + 指定 ref-type
python3 scripts/mps_aigc_image.py --model GEM --model-version 3.0 \
    --prompt "参考风格生成" \
    --image-local /tmp/style.jpg --image-ref-type style

# 多张本地文件（GEM 上限 20 张）
python3 scripts/mps_aigc_image.py --model GEM --model-version 3.0 \
    --prompt "融合风格" \
    --image-local /tmp/a.jpg --image-ref-type asset \
    --image-local /tmp/b.jpg --image-ref-type style
```

## 示例命令

```bash
# 文生图（Hunyuan 默认）
python3 scripts/mps_aigc_image.py --prompt "一只可爱的橘猫在阳光下打盹"

# GEM 3.1 + 反向提示词 + 16:9 + 2K
python3 scripts/mps_aigc_image.py --prompt "赛博朋克城市夜景" --model GEM --model-version 3.1 \
    --negative-prompt "人物" --aspect-ratio 16:9 --resolution 2K

# Vidu q2 文生图
python3 scripts/mps_aigc_image.py --prompt "星空下的湖泊倒影" --model Vidu --model-version q2

# Kling 3.0 文生图
python3 scripts/mps_aigc_image.py --prompt "赛博朋克城市夜景霓虹灯" --model Kling --model-version 3.0

# OG image2_high 文生图（高质量）
python3 scripts/mps_aigc_image.py --prompt "写实风格山水画" --model OG --model-version image2_high

# OG image2_low 文生图（快速出图）
python3 scripts/mps_aigc_image.py --prompt "卡通风格小猫" --model OG --model-version image2_low

# Hunyuan 3D 全景图
python3 scripts/mps_aigc_image.py --prompt "热带雨林全景" --model Hunyuan --scene-type 3d_panorama

# 图生图（参考图片 + 描述）
python3 scripts/mps_aigc_image.py --prompt "将这张照片变成油画风格" \
    --image-url https://example.com/photo.jpg

# GEM 多图参考（支持 asset/style 参考类型）
python3 scripts/mps_aigc_image.py --prompt "融合这些元素" --model GEM \
    --image-url https://example.com/img1.jpg --image-ref-type asset \
    --image-url https://example.com/img2.jpg --image-ref-type style

# 仅提交任务不等待
python3 scripts/mps_aigc_image.py --prompt "产品海报" --no-wait

# 查询任务结果
python3 scripts/mps_aigc_image.py --task-id abc123def456-aigc-image-20260328112000
```

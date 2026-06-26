# mps_gen_compare.py — 媒体效果对比工具

**功能**：生成交互式 HTML 对比页面，支持视频和图片的处理前后效果对比。

**特点**：本地工具，**不调用 MPS API、不产生任何费用**。

## 参数说明

### 单组对比（最常用）

| 参数 | 必填 | 说明 |
|------|------|------|
| `--original` | 是 | 原始媒体 URL 或本地文件路径 |
| `--enhanced` | 是 | 处理后媒体 URL 或本地文件路径 |

### 多组对比

| 参数 | 必填 | 说明 |
|------|------|------|
| `--pairs` | 否 | 多组对比，每组格式: `"原始URL,增强URL"`，支持多组 |
| `--config` | 否 | JSON 配置文件路径 |

### 通用选项

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--title` | 否 | `"媒体对比"` | 页面标题 |
| `--labels` | 否 | `"原始" "增强后"` | 自定义左右标签，格式: `--labels "左标签" "右标签"` |
| `-o` / `--output` | 否 | `evals/test_result/compare_<时间戳>.html` | 输出 HTML 文件路径 |
| `--type` | 否 | 自动检测 | 强制指定媒体类型：`video` 或 `image` |
| `--dry-run` | 否 | — | 模拟执行，不实际生成 |

## 对比能力

| 媒体类型 | 对比方式 |
|----------|----------|
| **视频** | 滑动分隔线 + 双视频同步播放 + 帧步进（逐帧前进/后退）+ 进度条 + 速度调节 |
| **图片** | 滑动分隔线 / 并排对比 / 叠加切换（hover 切换）三种模式 |

## 示例

### 视频增强前后对比

```bash
python scripts/mps_gen_compare.py \
    --original "https://example.cos.ap-guangzhou.myqcloud.com/input/video.mp4" \
    --enhanced "https://example.cos.ap-guangzhou.myqcloud.com/output/video_enhanced.mp4" \
    --title "4K 增强效果对比" \
    --labels "原片" "4K增强"
```

### 图片超分前后对比

```bash
python scripts/mps_gen_compare.py \
    --original "https://example.cos.ap-guangzhou.myqcloud.com/input/photo.jpg" \
    --enhanced "https://example.cos.ap-guangzhou.myqcloud.com/output/photo_sr.jpg" \
    --title "图片超分效果对比" \
    --labels "原图" "超分后" \
    --type image
```

### 去水印前后对比

```bash
python scripts/mps_gen_compare.py \
    --original "https://example.cos.ap-guangzhou.myqcloud.com/input/video.mp4" \
    --enhanced "https://example.cos.ap-guangzhou.myqcloud.com/output/video_erased.mp4" \
    --title "去水印效果对比" \
    --labels "原片（含水印）" "去水印后"
```

### 多组对比

```bash
python scripts/mps_gen_compare.py \
    --pairs \
    "https://xxx.cos/input1.mp4,https://xxx.cos/output1.mp4" \
    "https://xxx.cos/input2.jpg,https://xxx.cos/output2.jpg" \
    --title "批量处理效果对比"
```

### 本地文件对比（自动上传 COS 生成链接）

```bash
python scripts/mps_gen_compare.py \
    --original /data/workspace/input.mp4 \
    --enhanced /data/workspace/output.mp4 \
    --title "处理效果对比"
```

## 强制规则

1. **URL 来源**：`--original` 使用用户提供给处理脚本的原始输入 URL；`--enhanced` 使用处理脚本输出的结果 URL（预签名下载链接或普通 COS URL 均可）
2. **标题和标签**：根据处理类型设置有意义的 `--title` 和 `--labels`，不要使用默认值
3. **图片类型**：当对比的是图片（来自 `mps_imageprocess.py`、`mps_image_tryon.py`、`mps_image_bg_fusion.py`），建议显式指定 `--type image`
4. **生成后展示**：HTML 生成后，使用 `web_preview` 工具打开页面展示给用户
5. **无需费用提示**：本脚本不调用 MPS API，不产生任何费用

## 适用场景

以下处理脚本执行完毕后，可配合本脚本生成对比效果：

| 处理脚本 | 对比场景 | 建议标签 |
|----------|----------|----------|
| `mps_enhance.py` | 画质增强 / 4K增强 / 老片修复 / 超分 | `"原片" "增强后"` |
| `mps_erase.py` | 去字幕 / 去水印 / 人脸模糊 | `"原片" "擦除后"` |
| `mps_transcode.py` | 转码 / 压缩 / 格式转换 | `"原片" "转码后"` |
| `mps_imageprocess.py` | 图片超分 / 美颜 / 降噪 | `"原图" "处理后"` |
| `mps_dedupe.py` | 视频去重 / 画中画 / 视频扩展 / 垂直填充 / 水平填充 | `"原片" "去重后"` |
| `mps_vremake.py` | 换脸 / 换人 / 视频交错 | `"原片" "二创后"` |
| `mps_narrate.py` | AI 解说 / 短剧解说 / 解说二创 | `"原片" "解说版"` |
| `mps_highlight.py` | 精彩集锦 / 高光提取 / 足球集锦 / 篮球集锦 / VLOG 集锦 | `"原片" "集锦"` |
| `mps_image_tryon.py` | 图片换装 / AI试衣 | `"原图" "换装后"` |
| `mps_image_bg_fusion.py` | 背景融合 / 背景替换 | `"原图" "换背景后"` |

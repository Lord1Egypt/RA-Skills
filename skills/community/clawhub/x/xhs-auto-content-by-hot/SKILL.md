
---
name: XHS-AutoContentByHot
version: 1.0.0
description: 全自动生成小红书内容：获取百度热门话题 → 生成文案 → Seedream-4.5生图 → 输出图片+文案
author: Matianle
---

# 小红书内容生成 Skill

全自动4步流程，一键生成完整小红书内容！

## 功能

1. 获取百度热搜TOP10，随机选择一个话题
2. 根据话题生成小红书文案（标题15字以内 + 正文50-200字）
3. 调用火山引擎Seedream-4.5生成3张配图（第1张为封面图）
4. 输出所有图片 + 完整文案

## 使用方法

## 配置
- 先询问使用者的字节跳动生图模型的 API Key 是什么，得到回复后，把它存入 generate.py 的 API_KEY 里面备用
- 如果没有 API Key 或者 API Key 错误，则提示“生图失败，没有正确的 API Key，无法调用生图模型”

### 基础用法（自动从百度热搜选择话题）

```bash
python3 {baseDir}/scripts/generate.py
```

### 高级用法（自定义话题）

```bash
python3 {baseDir}/scripts/generate.py --topic "你的自定义话题"
```

### 更多选项

```bash
python3 {baseDir}/scripts/generate.py --topic "自定义话题" --images 5 --output-dir ./output
```

## 参数说明

- `--topic`: (可选) 自定义话题，不指定则从百度热搜 TOP1-10 随机选择
- `--images`: (可选) 生成图片数量，默认 3 张
- `--output-dir`: (可选) 输出目录，默认 `/root/.openclaw/workspace`

## 输出

- 图片：`xhs_final_1.png`、`xhs_final_2.png`、`xhs_final_3.png`
- 文案：`xhs_content.json`
- 话题：`selected_topic.txt`
- 图片列表：`generated_images.json`

## 注意事项

- 第1张图片提示词会自动添加"用来发布小红书的封面配图，要有网感与设计感"
- 第2、3张图片不添加封面关键词，提示词完全不同
- 所有图片尺寸为 2048x2048

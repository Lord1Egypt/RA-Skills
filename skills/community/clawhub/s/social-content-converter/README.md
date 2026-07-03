# social-content-converter

> 一鱼三吃内容改写器 — 输入一篇文章，自动改写成抖音、小红书、B站三个平台的专属版本

## 功能

- 一键改写：输入内容 → 三个平台专属版本
- 平台风格：抖音（悬念钩子）、小红书（种草风格）、B站（干货深度）
- 智能标签：为每个平台生成最优话题标签
- 封面建议：每个平台推荐封面文案和配色
- 最佳时间：推荐各平台黄金发布时间

## 安装

`ash
clawhub skill install social-content-converter
`

## 使用

`ash
cd skills/social-content-converter/scripts
python content_converter.py --input "你的内容" --topic "主题" --platforms "douyin,xhs,bilibili"
`

## 依赖

- Python 3.8+

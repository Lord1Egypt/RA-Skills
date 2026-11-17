# 中文AI图片生成工具

基于通义万象(DashScope)接口的中文图片生成工具。

## 安装

```bash
pip install requests pyyaml
```

## 快速开始

```bash

# 生成图片
python scripts/main.py --prompt "一只可爱的猫咪" --image cat.png

# 指定参数
python scripts/main.py --prompt "美丽的山水风景" --image landscape.png --ar 16:9 --quality 2k
```

## 支持的模型

- **qwen-image-2.0-pro** - 通义万象专业版（默认）
- **qwen-image-2.0** - 通义万象标准版
- **qwen-image-max** - 通义万象Max版
- **qwen-image-plus** - 通义万象Plus版
- **wan2.7-image-pro** - 万象2.7专业版（支持参考图）
- **wan2.7-image** - 万象2.7标准版（支持参考图）

## 配置文件

配置文件位置（按优先级）：
1. `.zhz-skills/image-gen/config.yaml`（项目级）
2. `~/.zhz-skills/image-gen/config.yaml`（用户级）

配置示例：
```yaml
default_model: qwen-image-2.0-pro
default_quality: 2k
default_aspect_ratio: "1:1"
```

## 文件结构

```
zhz-image-gen/
├── SKILL.md          # 技能文档
├── README.md         # 使用说明
└── scripts/
    └── main.py       # 主程序
```

## 特性

- 全中文界面和文档
- 支持通义万象全系列模型
- 支持自定义尺寸和宽高比
- 支持参考图片（wan2.7 模型）
- 配置文件支持项目级和用户级

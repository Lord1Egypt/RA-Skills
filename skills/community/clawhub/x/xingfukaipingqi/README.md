# 幸福开瓶器

随时撬开日常幸福感的 AI 伙伴。一句话触发，三条精准建议按星级排序。后台画像静默生长，每月回顾幸福里程。

## 快速开始

对 AI 说出「幸福开瓶器」即可触发。

## 能做什么

| 场景 | 示例 |
|------|------|
| 日常投喂 | "幸福开瓶器" → 三条个性化幸福建议 |
| 情绪低谷 | "心情不好" → 治愈型微行动建议 |
| 礼物参谋 | "她下周生日送什么" → 按关系阶段适配建议 |
| 月度回顾 | "这个月怎么样" → 六大维度幸福报告 |

## 目录结构

```
xingfu-kaipingqi/
├── SKILL.md              # 技能主文件
├── README.md             # 本文件
├── package.json          # 元数据
├── scripts/
│   ├── profile_manager.py          # 画像管理脚本
│   └── intervention_framework.json # 情感干预框架
├── references/
│   ├── profile-schema.md           # 画像规范
│   ├── suggestion-engine.md        # 建议引擎规范
│   ├── tone-adaptation.md          # 语气适配规范
│   └── monthly-summary.md          # 月度小结规范
├── tests/
│   └── test_profile_manager.py     # 画像管理器测试
└── assets/
    └── icon.txt                    # 技能图标说明
```

## 依赖

- Python 3.7+，仅标准库，零 pip 依赖
- 数据存储于 `~/.marvis/xingfu-kaipingqi/`，跨平台兼容

## 许可

MIT-0
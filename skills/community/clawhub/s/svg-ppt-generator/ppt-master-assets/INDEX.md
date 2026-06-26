# PPT Master 资源索引

来源：[ppt-master](https://github.com/hugohe3/ppt-master) v2.3.0（MIT License）

## 目录结构

```
ppt-master-assets/
├── INDEX.md              ← 本文件
├── SKILL-ORIGINAL.md     ← ppt-master 原始 SKILL.md
├── README-ORIGINAL.md    ← 英文 README
├── README-CN-ORIGINAL.md ← 中文 README
├── references/           ← 11 个角色参考文档
├── templates/layouts/    ← 20 套 SVG 布局模板
└── scripts/              ← SVG→PPTX 转换脚本
```

## 模板风格（templates/layouts/）

| 目录 | 风格 | 背景 | 适用场景 |
|------|------|------|---------|
| dark_warm | 深色暖调 | 深色封面+浅色内容 | AI/科技（默认） |
| consultant | 咨询风 | 白底蓝色 | 战略分析 |
| exhibit | 展示风 | 浅色 | 数据展示 |
| ai_ops | AI Ops | 深色 | DevOps/AI |
| 科技蓝商务 | 科技蓝商务 | 蓝色 | 科技商务 |
| smart_red | 智慧红 | 红色 | 商务演示 |
| pixel_retro | 像素复古 | 深色 | 游戏/趣味 |
| academic_defense | 学术答辩 | 浅色 | 论文答辩 |
| government_blue | 政府蓝 | 蓝色 | 政府报告 |
| government_red | 政府红 | 红色 | 党政报告 |
| cloud_orange | 云橙 | 深蓝底+橙色强调 | 云计算/技术架构 |

每套含：design_spec.md + 封面/章节/内容/结束页 SVG

## 参考文档（references/）

| 文件 | 用途 |
|------|------|
| strategist.md | 策略师：八项确认、设计规范 |
| executor-consultant-top.md | 顶级咨询风执行器 |
| executor-general.md | 通用灵活执行器 |
| shared-standards.md | SVG 技术约束 |
| template-designer.md | 模板设计师 |

## 脚本（scripts/）

核心：`svg_to_pptx/` — SVG → PPTX 转换（DrawingML 原生形状）

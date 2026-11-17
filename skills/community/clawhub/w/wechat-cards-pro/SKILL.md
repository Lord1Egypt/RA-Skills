---
name: wechat-cards-pro
description: 生成精美的微信公众号贴图卡片（小绿书/newspic模式）。1080×1440竖版，深黑背景+金色点缀，支持封面、内容、列表、时间线、结语等多种卡片类型。自动处理文字排版、间距、高度计算，避免重叠和溢出。适用于深度分析、知识科普、数据解读等内容。触发词：贴图、卡片、公众号排版、小绿书、newspic、竖版卡片。
---

# 微信公众号贴图卡片生成器

## 何时使用

当用户需要：
- 为公众号文章生成配套贴图卡片
- 制作小绿书(newspic)内容
- 将长文拆分为多张视觉卡片
- 生成1080×1440竖版知识卡片

## 工作流程

1. **确认内容结构**：与用户确认卡片数量和每张卡片的核心内容
2. **准备数据**：整理文本、数据点、金句
3. **生成卡片**：运行 `scripts/generate_cards.py`
4. **质量检查**：检查文字重叠、间距、溢出
5. **推送到公众号**（可选）：使用 `.wechat-mp/` 下的推送脚本

## 设计规范

### 基础参数
- 尺寸：1080 × 1440 px
- 背景：深黑 `#0a0a0a`
- 主色：金色 `#c9a96e`
- 正文：浅灰 `#e8e8e8`
- 次要文字：暗灰 `#888888`
- 卡片底色：略浅黑 `#1a1a1a`
- 安全边距：左右60px，上下80px

### 间距体系
```
大标题下方留白: 40-60px
章节间距: 30-40px
段落间距: 20-25px
列表项间距: 30-34px（基础）/ 26-30px（紧凑）
卡片内边距: 15-20px
框线到文字: 15-20px
```

### 字体层级
```
封面主标题: 56-64px, 金色
封面副标题: 28-32px, 浅灰
卡片标题: 44-48px, 白色
章节标题: 26-28px, 金色
正文: 22-24px, 浅灰
次要文字: 20-22px, 暗灰
列表项: 22px, 浅灰
金句: 26-28px, 金色
```

### 组件规范

**引用框/高亮框**
- 圆角半径：10-12px
- 内边距：15-20px
- 边框：2px金色描边（可选）
- 背景：`#1a1a1a`
- **必须自适应高度**：根据文字行数动态计算

**列表项**
- 带序号：金色数字 + 白色标题 + 灰色描述
- 每项间距自适应，避免溢出

**时间线**
- 左侧金色竖线 + 圆点
- 右侧内容区域

## 防重叠原则

1. **禁止固定高度容器**：所有包含多行文字的框必须使用自适应高度
2. **行高计算公式**：`总高度 = padding_top + 行数 × 行高 + (行数-1) × 行间距 + padding_bottom`
3. **连续渲染追踪**：维护全局 `y` 坐标，每次渲染后累加实际高度 + 间距
4. **底线检查**：若内容超出 1380px，压缩行高或拆分卡片

## 脚本使用

```bash
cd skills/wechat-cards-pro/scripts
python3 generate_cards.py --config config.yaml
```

或使用 Python API：
```python
from card_engine import CardEngine

engine = CardEngine(width=1080, height=1440)
engine.set_theme("dark_gold")  # 预设主题

# 逐张构建
card = engine.new_card()
card.title("AI税与就业焦虑", size=48, color="gold")
card.paragraph("打工人最关心的问题...", size=22)
card.quote_box("核心观点：AI税更像心理按摩", auto_height=True)

card.save("01_cover.png")
```

## 文件结构

```
wechat-cards-pro/
├── SKILL.md                     # 本文件
├── scripts/
│   ├── generate_cards.py        # 主生成脚本（模板模式）
│   └── card_engine.py           # 核心引擎类（程序化API）
└── references/
    └── design_system.md         # 完整设计规范
```

## 常见问题

**Q: 文字重叠了怎么办？**
A: 检查是否使用了固定高度。所有 `quote_box`、`list`、`paragraph` 都应设置 `auto_height=True`。

**Q: 底部裂脑悖论标识被截断？**
A: 确保最后元素的 y + height < 1380，留出 60px 给 footer。

**Q: 字体加载失败？**
A: 脚本会自动回退到系统默认字体（PingFang SC / Microsoft YaHei / Arial）。

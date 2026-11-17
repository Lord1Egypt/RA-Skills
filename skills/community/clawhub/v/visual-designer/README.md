# Visual Designer — 视觉设计师技能库

> 面向独立开发者和创作者的视觉设计技能集合。覆盖排版、插画、海报设计和品牌视觉，帮你打造有辨识度的产品视觉。

## 技能清单

| 技能 | 描述 | 安装量 | 来源 |
|------|------|--------|------|
| web-typography | Web 排版：字体选择、层级系统、可读性优化、响应式排版 | 5.8K | [skills.sh](https://skills.sh/wondelai/skills/web-typography) |
| illustrator | 插画创作：风格探索、构图原则、色彩运用、插画系统 | 1.9K | [skills.sh](https://skills.sh/sfkislev/flue/illustrator) |
| poster-design-generation | 海报设计：视觉层级、信息架构、色彩冲击力、版式布局 | 1.7K | [skills.sh](https://skills.sh/eachlabs/skills/poster-design-generation) |
| brand-designer | 品牌设计：品牌策略、Logo 设计、色彩系统、品牌手册 | 1.1K | [skills.sh](https://skills.sh/daffy0208/ai-dev-standards/brand-designer) |

## 深层 Playbook（references/）

按需加载的方法论层，含决策树、可运行速算命令、量化判据与踩坑清单：

| Playbook | 内容 |
|----------|------|
| [references/design-principles.md](references/design-principles.md) | CRAP 四原则、视觉层级决策树、层级/行长/间距的**量化判据**、间距阶梯判读表 |
| [references/brand-typography-system.md](references/brand-typography-system.md) | 品牌资产清单、**模数字号阶梯速算**、字体选型决策树、**对比度速算与 AA/AAA 判据** |

## 工作流

```
品牌设计 ──→ 排版系统 ──→ 插画创作
 (品牌基调)    (文字层级)     (视觉元素)
                  └─→ 海报设计
                      (营销物料)
```

## 安装

```bash
# 安装全部视觉设计技能
npx skills add skills-repo/visual-designer -g -y

# 或按需安装单个技能
npx skills add skills-repo/visual-designer@web-typography -g -y
npx skills add skills-repo/visual-designer@illustrator -g -y
npx skills add skills-repo/visual-designer@poster-design-generation -g -y
npx skills add skills-repo/visual-designer@brand-designer -g -y
```

## 与本组织其他仓库的关系

- **design-studio** — UI/UX 设计（设计系统、UI审查），本仓库聚焦视觉资产创作
- **content-creator** — 视频/音频内容创作，本仓库聚焦静态视觉设计
- **marketing-master** — 营销策略和文案，本仓库聚焦视觉执行
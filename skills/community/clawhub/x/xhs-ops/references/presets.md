# 小红书配图预设（Presets）

预设 = 风格 + 布局 + 可选配色 的一键组合。根据内容场景直接选预设，不用分别选风格和布局。

> 预设只是快捷方式。可以用预设后单独覆盖风格、布局或配色。
> 例如：用 `knowledge-card` 但换成科技感风格 → 保留 dense 布局 + 切换风格二。
> 例如：用 `sketch-card` 但换 warm 配色 → 保留手绘线条 + 暖色系。

---

## 配色覆盖（Palette Override）

每个风格有内置配色，但可以用配色覆盖只换颜色、保留风格的线条/装饰/版式。

| 配色 | 背景 | 区块色 | 强调色 | 感觉 |
|------|------|--------|--------|------|
| `macaron` | 暖奶油 #F5F0E8 | 马卡龙蓝 #A8D8EA、薄藤 #D5C6E0、薄荷 #B5E5CF、桃子 #F8D5C4 | 珊瑚红 #E8655A | 柔和、教育感、亲和力 |
| `warm` | 柔桃 #FFECD2 | 橙 #ED8936、陶土 #C05621、金 #F6AD55、玫瑰 #D4A09A | 赭石 #A0522D | 温暖、大地色、无冷色 |
| `neon` | 深紫 #1A1025 | 青 #00F5FF、品红 #FF00FF、绿 #39FF14、粉 #FF6EC7 | 黄 #FFFF00 | 高能量、未来感 |

**配色使用规则**：
- 默认不指定配色 → 用风格内置颜色
- 指定配色 → 只替换颜色，风格的线条/装饰/字体规则不变
- 例：手绘涂鸦 + macaron 配色 = 手绘线条 + 马卡龙色块，而不是珊瑚橙

**Prompt 中应用配色覆盖**：
在风格 section 的 Color Palette 部分替换为指定配色的颜色值，其余 Visual Elements / Typography 保持原风格不变。

---

## 预设列表

### 知识/干货类

| 预设 | 风格 | 布局 | 配色 | 适用场景 | 典型标题 |
|------|------|------|------|---------|---------|
| `knowledge-card` | 手绘涂鸦 | dense | 默认 | AI干货、方法论总结、工具合集 | 「5个AI工具让效率翻倍」 |
| `checklist` | 手绘涂鸦 | list | 默认 | 清单、排行榜、避坑指南 | 「产品经理必备的7个习惯」 |
| `step-guide` | 手绘涂鸦 | flow | 默认 | 教程、操作流程、工作流 | 「3步搭建你的AI工作流」 |
| `tech-insight` | 科技感 | balanced | 默认 | AI产品分析、技术趋势、行业观点 | 「ChatGPT为什么改变了PM」 |
| `concept-map` | Notion极简线稿（风格三） | mindmap | 默认 | 概念图、知识脉络、话题总览 | 「AI产品经理知识图谱」 |

### 对比/分析类

| 预设 | 风格 | 布局 | 配色 | 适用场景 | 典型标题 |
|------|------|------|------|---------|---------|
| `vs-compare` | 科技感 | comparison | 默认 | 产品PK、方案选型、before/after | 「传统PM vs AI PM」 |
| `tech-dense` | 科技感 | dense | 默认 | 技术方案拆解、架构解读 | 「Agent记忆系统全解析」 |
| `swot-matrix` | 科技感 | quadrant | 默认 | SWOT分析、四象限分类、优先级矩阵 | 「AI产品经理SWOT分析」 |

### 叙事/分享类

| 预设 | 风格 | 布局 | 配色 | 适用场景 | 典型标题 |
|------|------|------|------|---------|---------|
| `pm-story` | 手绘涂鸦 | balanced | 默认 | 个人经历、职场故事、成长复盘 | 「从美团到阿里，我学到的3件事」 |
| `cover-hook` | 手绘涂鸦/科技感 | sparse | 默认 | 封面图、金句卡片、重磅声明 | 「实现在贬值，判断在升值」 |

### 特殊风格类

| 预设 | 风格 | 布局 | 配色 | 适用场景 | 典型标题 |
|------|------|------|------|---------|---------|
| `notion-explainer` | Notion极简线稿（风格三） | balanced / dense | 默认 | 概念科普、SaaS/效率类、理性调性 | 「一张图看懂Agent记忆系统」 |
| `bold-poster` | 丝网印刷海报（风格四） | sparse | 默认 | 观点输出、影评书评、重磅声明 | 「AI不会取代PM，但会取代不用AI的PM」 |
| `cinematic` | 丝网印刷海报（风格四） | comparison | 默认 | 电影对比、戏剧张力、强视觉对比 | 「传统PM vs AI PM：死亡赛跑」 |
| `study-notes` | 手写笔记照片（风格五） | dense | 默认 | 知识框架整理、学习笔记分享 | 「学霸笔记｜产品经理AI知识体系」 |
| `sketch-card` | 手绘信息图（风格六） | dense | macaron | 手绘知识卡、概念科普 | 「一张图搞懂Prompt Engineering」 |
| `sketch-flow` | 手绘信息图（风格六） | flow | macaron | 手绘教程、流程图解 | 「手把手AI Agent搭建全流程」 |
| `sketch-summary` | 手绘信息图（风格六） | balanced | macaron | 手绘总结、图文笔记 | 「一周AI产品学习手绘笔记」 |

---

## 内容信号 → 自动推荐预设

当 Editor Agent 分析内容时，按以下信号自动推荐预设。

**决策规则**（与公众号 cover-image-guide.md 统一逻辑）：
1. 扫描内容关键词，匹配下表第一个命中行
2. 取推荐预设（预设已封装风格+布局，且均已过兼容矩阵校验）
3. 如需覆盖单个维度（如只换配色），查 `illustration-prompts.md` 的风格×布局兼容矩阵确保无 ✗
4. 混合信号时取第一个匹配，不迭加多个预设

小红书用「预设」而非原始维度，因为预设已经封装了风格+布局+配色的最佳组合；公众号用「六维度」因为封面图是 AI 生图需要更细粒度控制。两套体系底层逻辑一致：内容信号 → 自动推荐 → 兼容校验 → 生成。

| 内容信号关键词 | 推荐预设 | 备选 |
|--------------|---------|------|
| AI工具、效率、方法、技巧、干货、推荐 | `knowledge-card` | `checklist` |
| 排行、Top N、必备、清单、避坑、注意 | `checklist` | `knowledge-card` |
| 步骤、教程、流程、先…再…然后、第一步 | `step-guide` | — |
| AI趋势、产品分析、行业、技术、架构 | `tech-insight` | `tech-dense` |
| vs、对比、区别、优劣、before/after | `vs-compare` | — |
| 拆解、全解析、完全指南、深度 | `tech-dense` | `knowledge-card` |
| 我、经历、故事、复盘、成长、感悟 | `pm-story` | — |
| 金句、一句话、声明、重磅 | `cover-hook` | — |
| 概念、科普、原理、解释、SaaS | `notion-explainer` | `knowledge-card` |
| 观点、影评、书评、海报、声明 | `bold-poster` | `cover-hook` |
| 笔记、框架、知识体系、学霸、考试 | `study-notes` | `knowledge-card` |
| 手绘、图解、可视化、示意图、workflow | `sketch-card` | `sketch-flow` |
| 矩阵、分类、SWOT、象限、排列组合 | `swot-matrix` | `vs-compare` |
| 知识图谱、脑图、全景、发散思维 | `concept-map` | `notion-explainer` |

**混合信号时**：取第一个匹配的推荐预设。

---

## 预设使用示例

```markdown
## 配图方案

**预设**：knowledge-card（手绘涂鸦 + dense）
**配色覆盖**：无（使用风格默认配色）
**主题**：5个AI产品经理必备工具
**张数**：5 张

| # | 位置 | 布局覆盖 | 内容 |
|---|------|---------|------|
| 1 | Cover | sparse | 标题「5个AI工具让PM效率翻倍」+ 大字冲击 |
| 2 | Content | dense | ChatGPT：4个使用场景 |
| 3 | Content | dense | Cursor + Claude Code：编程提效 |
| 4 | Content | dense | Notion AI + Perplexity：信息整理 |
| 5 | Ending | sparse | 总结 + "你最常用哪个？评论区见" |

注：封面和结尾固定 sparse，中间内容页跟随预设默认布局（dense）。
```

---

## 扩展预设

如需新增预设，在此文件追加一行即可。格式：
`预设名 | 风格 | 布局 | 配色 | 适用场景 | 典型标题`

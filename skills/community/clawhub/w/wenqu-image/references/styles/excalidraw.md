# Excalidraw 风格参考库（excalidraw-style）
> 通用画图规范见 [core-principles.md](../core-principles.md)、[pitfalls.md](../pitfalls.md)。


> 参考图存放于 `https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-image-assets/styles/excalidraw/`

与手绘插画风格（[handdrawn.md](handdrawn.md)）容易混淆，但视觉语言完全不同——Excalidraw 风格更像工程师在白板上随手画的技术草图，没有插画图标，核心是"斜线排线填充、潦草描边、手写字体"。

| 特征 | 描述 |
| --- | --- |
| 线条 | 潦草粗糙描边（rough.js 风格），线条略微抖动不规整，非精确几何线，黑色为主 |
| 填充 | 斜线交叉排线（hachure fill），**不是**纯色实心填充——这是与手绘插画风格最大的区别 |
| 字体 | 手写体风格（类似 Excalidraw 默认 Virgil 字体），不用印刷体 |
| 图标 | **禁止**任何插画图标或卡通元素，只用最简单的几何形状（圆角矩形、菱形、圆形）与箭头 |
| 配色 | 柔和粉彩色，各区块/分组用不同颜色的排线区分，背景纯白 |
| 分组 | 大圆角矩形外框（细边框）套小节点，外框顶部或左上角标区块名 |
| 密度 | 工程草图感，信息密度高，多用嵌套分组表达系统分层，不留大片空白 |

完整风格选择见 `SKILL.md` 风格库表。

### 生成规则（--ref 必须，prompt 只写轻描述——见 pitfalls.md 踩坑 9）

**--ref 必须**，推荐参考图（按目标图类型选最接近的）：

```
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-03-dense-layered-arch.png)"       # 多层嵌套架构，信息密度高
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-02-nested-groups.png)"            # 简单嵌套分组
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-01-linear-flow.png)"              # 横向线性流程
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-04-sequence-race-condition.png)"  # 时序图/生命线
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-05-branch-decision-flow.png)"     # 竖向分支决策流程
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-06-side-by-side-comparison.png)"  # 左右对比图
--ref "$(wenqu image fetch-ref excalidraw/excalidraw-07-timeline-evolution.png)"       # 时间演化/版本迭代图
```

**prompt 只写"参考图风格与内容"，不要逐条复述视觉细节**（斜线排线、潦草描边、手写字体等一律交给 `--ref`）：

```
参考图风格，[横向宽屏构图 / 竖版构图]。[内容描述]。所有文字用中文，拼写清晰。
```

**⚠️ 内容密度提醒**：这套风格的线条本身很简洁，如果画图提示内容单薄（只有 2~3 个孤立节点），生成结果会显得空洞、不像正式架构图。参考 `excalidraw-03-dense-layered-arch.png` 的写法——用多层嵌套分组（外框内套子节点/子分组），每个分组标区块名，比单层平铺的节点信息密度更高、更接近真实架构图。这条是内容组织建议，不是要在 prompt 里加视觉细节描述。

### 参考图索引

| 文件 | 图类型 | 特点 |
| --- | --- | --- |
| `excalidraw-01-linear-flow.png` | 横向三节点线性流程 | 客户端→网关→数据库，简单直箭头，验证基础风格复现 |
| `excalidraw-02-nested-groups.png` | 双分组嵌套架构 | 左侧集群（3节点纵向排列）与右侧服务层（2子区域），验证嵌套分组表达力 |
| `excalidraw-03-dense-layered-arch.png` | 三层嵌套架构（高密度） | 客户端接口层、服务处理层、存储层，每层内含多个子节点与子流程，接近真实系统架构图密度 |
| `excalidraw-04-sequence-race-condition.png` | 时序图/生命线 | 三个参与者、纵向生命线、编号箭头，红色高亮标注异常交互（数据竞争） |
| `excalidraw-05-branch-decision-flow.png` | 竖向分支决策流程 | 菱形判断、两条旁路分支、汇合节点，验证多分支布局与颜色区分 |
| `excalidraw-06-side-by-side-comparison.png` | 左右对比图 | 顶部共用横幅、垂直虚线分隔、左右各自纵向流程、底部结论卡片 |
| `excalidraw-07-timeline-evolution.png` | 时间演化/版本迭代图 | 水平时间轴与之字形交替排列的说明卡片，适合展示架构演进历史 |

### Prompt 模板片段

**多层嵌套架构（高密度）** — 参考 `excalidraw-03`：
```
参考图风格，横向宽屏构图，信息密度要高。从左到右 [N] 个纵向区块，每块是一个大分组框，内部有若干子节点：
【[区块1名]】（[节点1]、[节点2]…）→【[区块2名]】（[节点1]、[节点2]…）→【[区块3名]】…
区块间箭头标注「[操作语义]」。所有文字用中文，拼写清晰。
```

**简单线性流程** — 参考 `excalidraw-01`：
```
参考图风格。横向 [N] 节点线性流程：[节点1] → [节点2] → … → [节点N]，箭头标注「[操作语义]」。所有文字用中文，拼写清晰。
```

**时序图/生命线** — 参考 `excalidraw-04`：
```
参考图风格，横向宽屏构图。时序图，参与者：[参与者A]、[参与者B]、…，按时间顺序编号交互：
(1) [参与者A] → [参与者B]：[操作]
(2) [参与者B] → [参与者A]：[响应]
…
（需要高亮异常交互时说明是哪一条）。所有文字用中文，拼写清晰。
```

**竖向分支决策流程** — 参考 `excalidraw-05`：
```
参考图风格，竖版构图，信息密度要高。竖向决策流程：[入口节点] → 判断「[条件A]？」，是→[分支A结果]→汇合到[汇合节点]，否→继续 → [主干节点] → 判断「[条件B]？」，是→[分支B结果]→汇合到[汇合节点]，否→继续 → [汇合节点]。所有文字用中文，拼写清晰。
```

**左右对比图** — 参考 `excalidraw-06`：
```
参考图风格，横向宽屏构图，信息密度要高。左右对比，顶部横幅「[对比主题]」。左侧「[方案A]」：[步骤1]→[步骤2]→…，结论「[风险/结论]」。右侧「[方案B]」：[步骤1]→[步骤2]→…，结论「[优势/结论]」。所有文字用中文，拼写清晰。
```

**时间演化图** — 参考 `excalidraw-07`：
```
参考图风格，横向宽屏构图。时间演化图，时间轴上 [N] 个节点，之字形排列说明卡片：[版本1]「[一句话说明]」→[版本2]「[一句话说明]」→…（最新版本可突出强调）。所有文字用中文，拼写清晰。
```

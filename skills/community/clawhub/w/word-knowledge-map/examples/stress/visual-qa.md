# Visual QA — get / the / run (v1.2 stress renders)

Date: 2026-09-16 Asia/Shanghai
Renderer: GenerateImage + style-target-care.png reference
Files: `examples/stress/renders/{get,the,run}.png`

## Checklist (style-guide 对照翻车清单)

| # | 失败项 | get | the | run |
|---|--------|-----|-----|-----|
| 1 | 白底浮起 Soft UI 卡片墙 | 弱（有圆角色块，但整体涂鸦海报感） | 弱 | 弱偏中（底栏偏产品条） |
| 2 | 细直线 spoke | 否（粗弯箭头） | 否 | 否 |
| 3 | 中心非手绘 hub | 否（黄底核心词） | 中（蓝圆 hub，略产品） | 中（白云 hub） |
| 4 | 完美几何无马克笔感 | 部分 | 部分 | 部分 |
| 5 | 只有扁平 icon 无场景小孩 | 否（有场景小孩） | 否 | 否（场景+少量物品 icon） |
| 6 | 组件拼装界面感 | 边缘 | 边缘 | 略明显（编号气泡+底 icon 链） |

## 内容 / 版式

| 词 | mode | 假派生 | 底链真实 | 判定 |
|----|------|--------|----------|------|
| get | phrasal-hub | 无 | 得到→到达→变得→易混点 | 内容通过 |
| the | function-word | 无 | 特指→怎么用→别和 a/an 混→习惯说法 | 内容通过 |
| run | phrasal-hub | 无（仅 runner/running） | 跑→短语→延伸义→词形 | 内容通过 |

## 总评

- **内容/版式：3/3 通过**（弱词族兜底有效，未滑回 care 形副名假链）。
- **视觉：可用，但未完全锁死参考图气质** — 更像「干净卡通教学海报」，参考图那种马克笔抖动 / 奶油点阵纸 / 有机色块底链仍不够稳。
- **建议下一刀**：成图后再跑一轮「只改气质」重绘（加强标题手写压力、箭头宽度抖动、底链改 paint-blob）；或对 run 底栏去掉 UI 风 icon 步进条。

## 对用户话术（若重做）

风格有点偏，我按手绘海报参考图重做一版。

---

# Visual QA v2 — style-only redraw (2026-09-16)

Files: `renders/{get,the,run}-v2.png`
Refs: style-target-care.png + style-approved-v5-care.png

## vs v1

| 词 | v1 主要问题 | v2 变化 | 仍存 |
|----|-------------|---------|------|
| get | 偏干净卡通 | 虚线黄 hub、涂鸦装饰更多、底链文字胶囊 | 卡面仍偏整齐；部分表情略 icon |
| the | 略产品 | 云朵 hub、底链改云朵色块 | 标题偶发漏👀；卡内仍有小 icon |
| run | 底栏 UI 步进条最重 | 底链改为云朵胶囊+手绘箭头，产品条感下降 | 云朵内仍夹小 icon；hub 仍偏正圆 |

## 判定

- 内容：仍对齐 IR / layout_plan（无假派生）。
- 视觉：相对 v1 **小幅提升**（底链去产品条、纸感/涂鸦装饰加强），相对批准样 **仍未锁死**。
- 结论：文生图单轮难稳定到 v5 批准级；建议 skill 侧保留「视觉失败则气质重做」；若要再逼近，优先只重跑 run 底链纯文字色块、或接受 HTML+手绘贴图混合管线。

---

# run v3 — text-only bottom chain (2026-09-16)

File: `renders/run-v3.png`

## Check
- Bottom chain: 跑 → 高频短语 → 延伸义 → 词形 as text capsules/clouds — **pass** (no shoe/bubble/shop/pencil stepper)
- Content still matches IR — pass
- Overall doodle vibe: improved vs v2 footer; still not full marker lock vs style-target-care

## Verdict
Footer anti-pattern fixed for this sample. Prefer v3 over v2 as run stress render.

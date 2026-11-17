# SVG Studio

**让任何 LLM 都能「写代码画图」** —— 用编写 SVG 的方式生成任意宽高比、任意复杂度的矢量图，按需导出 PNG / GIF / APNG / WebP / MP4，或直接内嵌 HTML。**默认交付到 SVG 为止，位图只在用户点名时导出。**

一个 Skill（技能包），适用于 WorkBuddy / Claude Code / Claw 等支持 SKILL.md 规范的 Agent 运行时。

## 为什么需要它

- **生图模型画不对文字和数字**。海报、信息图、图表里「50 万台」「+38.2%」这类关键信息，扩散模型经常画歪画错。SVG 是纯文本，模型完全可控，**文字数字零误差**。
- **没有多模态生图能力的模型也能画图**。只要能写代码，就能产出专业级矢量图。
- **任意宽高比、无限缩放**。1:1 / 16:9 / 9:16 / OG 1.91:1 / 公众号封面 2.35:1，viewBox 一改就变。

## 能力

| 能力 | 说明 |
|---|---|
| ① 编写复杂 SVG | 图表 / 插画 / 流程图 / 架构图 / 海报 / 信息图 / 图标 / 封面 |
| ② SVG → PNG | Chrome headless 优先（渐变/滤镜/中文字体全保真），resvg → cairosvg 自动降级 |
| ③ 动图导出 | 多帧/模板 SVG → GIF / APNG / WebP / MP4 |
| ④ 版式配方 | 内置手绘/手账/便签风、干净产品风信息图配方，纸张做旧、胶带、荧光笔等现成滤镜 |

## 快速开始

默认工作流：写好 SVG 存 `.svg` 即为交付物，到此为止。需要位图 / 动图文件时：

```bash
# 按需渲染 PNG（默认 2x DPR，Chrome 优先，自动降级）
python3 scripts/render.py poster.svg

# 指定宽度、实底背景、顺带产出 HTML
python3 scripts/render.py chart.svg --width 1600 --bg "#0f172a" --html chart.html

# 模板 SVG → GIF（__T__ 占位符代表进度 0→1，自动生成 30 帧）
python3 scripts/animate.py --template anim.svg --frames 30 -o out.gif --fps 15
```

零第三方依赖安装：渲染脚本首次运行时自动创建隔离 venv（Pillow / cairosvg / resvg），Chrome 路径自动探测（macOS / Windows / Linux）。

## 目录结构

```
SKILL.md                            # Skill 入口：工作流 + 环境说明
references/
  svg-techniques.md                 # SVG 编写手册：骨架/比例/文本/渐变/图表数学/排版红线
  handdrawn-infographic.md          # 手绘/手账/便签风 & 产品风信息图配方
  animation.md                      # 动画两条路线（SMIL/CSS 内嵌 vs 导出动图文件）
scripts/
  render.py                         # SVG → PNG / HTML（Chrome → resvg → cairosvg）
  animate.py                        # 多帧/模板 SVG → GIF / APNG / WebP / MP4
```

## 排版红线（实战沉淀）

以下是真实生产（公众号配图批量产出）中翻车后总结的规则，全部收录在 `references/svg-techniques.md` §10：

- 大数字 + 单位永远用 `<tspan dx>`，嵌套 `<text>` 在 Chrome headless 不渲染
- 写字前先按公式估宽度（中文 ≈ font-size × 1.0，数字 ≈ × 0.55），超容器必拆行
- 装饰图形与文字分区，图形整体下移避让文字安全区
- 结论条先拆行再定框高，反过来必溢出

## License

MIT

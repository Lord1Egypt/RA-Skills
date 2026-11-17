---
name: ref-site-ui-tokens
description: 用户说「参考 X 网站改 UI / 照着 X 的风格做 / X 那种配色」时的落地流程。在没有浏览器的机器上（agent-browser、playwright 都没装，或 Chrome/Edge 不在标准路径）用 curl + 标准库 Python 抓下目标站的真实设计 token（颜色、圆角、字重、字号、间距），再据此改本地样式表。含一个可直接跑的抓取脚本 scripts/fetch_tokens.py，以及「借什么 / 不借什么」的取舍框架与常见坑。
agent_created: true
slug: ref-site-ui-tokens
displayName: 参考网站改 UI：抓设计 token 再落地
version: 1.0.0
category: design-media
visibility: public
license: MIT
---

# 参考某个网站改 UI：抓 token → 落地 → 钉成断言

## 何时用

- 「参考 https://xxx 网站修改 ui」「照着 linear.app 的风格做一版」
- 「这个配色参考一下 Vercel / Notion / Stripe」

**先别急着凭印象写色值**。目标站的设计 token 都在它的 CSS 变量里，抓下来是几十秒的事，
比猜准得多，也比截图好使（截图只能看个大概，拿不到 12px 还是 16px 这种精确值）。

## 第一步：抓（本机没有浏览器也能做）

```bash
python scripts/fetch_tokens.py https://linear.app/            # 打印全部变量
python scripts/fetch_tokens.py https://linear.app/ --grep color  # 只看含 color 的
python scripts/fetch_tokens.py https://linear.app/ --json out.json
```

脚本做四件事（纯标准库，不需要 playwright / 浏览器）：

1. `urllib` 抓首页 HTML（带桌面 UA，有些站对默认 UA 返回的是另一套壳）；
2. 正则提出所有 `<link rel="stylesheet">` 的 href，相对路径按 base 拼全；
3. 逐个下载合并（Next.js 站常见几十个 `/_next/static/css/*.css`，Linear 有 54 个、合计 339 KB）；
4. 从合并后的 CSS 里解析 `--var: value`，去重后按前缀分组打印。

**如果站点是纯客户端渲染、HTML 里没有样式表链接**（比如整站靠 JS 注入样式）：
`curl -sL <url> | grep -o 'href="[^"]*\.css[^"]*"'` 看看有没有；实在没有再换
`agent-browser`（若已装）或直接抓它 CDN 上已知的那份 CSS。

抓不到时的兜底：把首页保存下来人工读，或直接问用户要截图。但**先试脚本**。

## 第二步：挑（这是最容易被忽略的一步）

抓下来通常有几百个变量，不要全抄。按这个顺序筛：

| 类别 | 关键变量 | 说明 |
|---|---|---|
| 底色三级 | `--bg-base` `--bg-shade` `--color-bg-panel` | 页面 / 浮起一档 / 面板。深色站通常是**偏冷的近黑**（R<B），不是纯中性灰 |
| 描边 | `--border-solid` `--border-thin` `--border-faint-thin` | 注意「面板内部的分隔线」往往比外框更淡，这是精致感的来源 |
| 圆角 | `--card-radius` `--app-radius` `--radius-*` | 常见取值 8/12/16。**Linear 是 12px**，比直觉的 16 更收敛 |
| 字重 | `--font-weight-*` | 可变字体站常用 **510 / 590 / 680**，而不是 CSS 默认的 400/600/700 |
| 字体特性 | `--font-settings` `--font-variations` | 如 `"cv01","ss03"`、`"opsz" auto`（Inter Variable 的招牌设定） |
| 高光/玻璃 | `--edge-highlight-color` `--anchor-glass-bg` | 深色界面里**顶部 1px 白高光**替代阴影，这是很多 SaaS 站的辨识度所在 |
| 主色 | `--color-indigo` `--color-blue` … | ⚠️ **通常不该抄**，见下 |

### 借什么 / 不借什么（重要）

- **可以借**：中性底色、描边层级、圆角、字重档位、间距节奏、高光与玻璃底、动效曲线。
  这些是「工艺」，换到任何项目都不丢语义。
- **不要借**：品牌主色。如果目标站的主色在你这个项目里**另有含义**（例如本站绿 =
  「收入已验证」），换成对方的 indigo 会丢掉那层语义。**参考一个站不等于照搬它的品牌色。**
  在改之前把这一条明确告诉用户，别默默替他换掉上一轮定下的语义配色。
- **不要借**：大面积 hero 光晕 / 渐变文字。那是营销首页的语言，工具型界面加上会显得吵。

## 第三步：落（改本地样式表）

1. 只改 `:root` 的变量值 → 全站跟随。**先跑一遍引用计数再删变量**：
   `python -c "print(len(re.findall(r'var\(--x\b', open('style.css').read())))"`——
   凭印象删变量删出过 26 处未定义引用。
2. 半透明统一走 `rgba(var(--xx-rgb), alpha)`，给每个色再配一组 `--xx-rgb: r,g,b`
   通道变量，保证「一个颜色只有一处定义」。
3. 字重 / 圆角这类**结构性的值**也做成变量（`--fw-s`、`--radius`），别散着写。
4. 新增的高光、玻璃底**也必须是 `:root` 里的变量**，不要内联 rgba 字面量。

## 第四步：钉（把约定写成断言，否则下一个人会改回去）

注释不会自己报警。把最容易被顺手破坏的几条写成测试，例如：

- 卡片圆角 = `var(--radius)` 且 `--radius` 是 12px
- 卡片有顶边高光（`.card::before` 用了 `var(--hi)`）
- 硬编码色值只允许出现在 `:root` 里
- 字重不许出现裸数字

⚠️ 「色值只许在 :root」这类断言**必须先把 `/* */` 注释剥掉再扫**
（`css.replace(/\/\*[\s\S]*?\*\//g, '')`），否则注释里举的色值例子会被误判成违规——
而注释本来就该能讲颜色（「Linear 的主色是 #5e6ad2，但我们不抄」这种说明很有价值）。

## 坑（都踩过）

1. **`bash -c "python -c '...\s...'"` 里的反斜杠会被吃掉**，正则静默不匹配，
   表现为「replaced 0」——极难察觉。**多行 Python 一律写成 .py 文件再跑**，别用 `-c` + heredoc。
2. **构建脚本可能把 CSS 内联进产物页**，此时样式表里的注释也会一起进产物：
   注释里不许出现脚本文件名、不许残留外链样式痕迹（有的构建有守卫会直接 FAIL）。
3. **批量替换颜色后必须人工复查**：蓝→绿可能把两个象限撞成同色；
   渐变两端被替成同一个变量会丢层次。脚本只能做粗活。
4. 站点可能按 UA 或地区返回不同 CSS，抓下来发现变量特别少时，换个 UA 再抓一次。

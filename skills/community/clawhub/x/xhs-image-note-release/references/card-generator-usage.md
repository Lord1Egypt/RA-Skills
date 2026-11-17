# 卡片生成器用法（`references/card-generator/card_generator.py`）

> **什么时候读这个文件**：要用本技能的卡片生成器做图、查主题/参数、或写批量出图脚本时读。
> 只是发素材时**不需要读**——`publish_note.sh` 直接吃 `MEDIA_FILES`，跟卡片生成无关。
>
> 生成器仅用 Python 标准库 + 本机 Chrome headless，无需 pip 安装。

## 快速出图

本技能附带统一风格卡片生成器，位于 `references/card-generator/card_generator.py`。

```bash
python3 ~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py \
  --theme warm \
  --tag "人生随笔" \
  --lines "周五了\\n你还活着吗\\n去外面走走" \
  --subtitle "关于活着" \
  --page-number 1 \
  --total-pages 6 \
  --account "@雨夜心灯" \
  -o ./card.png

# 图文卡片：顶部简笔画 + 窄列居中文字 + 底部署名
# 图文卡片：--illustration 需自备（技能不附示例文件）
python3 ~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py \
  --layout image-text \
  --illustration ./my-illust.svg \
  --theme warm_illust \
  --lines "周五了。\\n把工牌摘下来，" \
  --account "@雨夜心灯" \
  -o ./illust-card.png
```

## 内置主题（29 种）

纯文字布局共用同一套版式；图文布局额外支持 `warm_illust`。完整清单随时用 `--list-themes` 打印。

| 分组 | 主题 key |
|------|---------|
| **照片背景氛围**（需配合 `--background`） | `cinematic` 暗色电影感、`film` 胶片颗粒、`journal` 书页氛围、`history` 历史古风（暗色 + 报隶书法体，秦汉史/翻案解说用） |
| 年轻人风格 | `warm` 温暖哲思、`warm_illust` 温暖简笔哲思、`y2k` Y2K 千禧潮酷、`doodle` 手绘涂鸦、`pop` 渐变波普、`minimal` 极简日系 |
| 科技 / 商务 | `cyberpunk` 赛博科技、`apple` Apple 质感、`cowork` 轻科技、`bloomberg` Bloomberg 终端、`carbon` 暗色极简 |
| 文艺 / 复古 | `elegant` 极简优雅、`newspaper` 报纸杂志、`ink` 水墨卷轴、`steampunk` 蒸汽朋克、`palace` 故宫金红 |
| 生活 / 治愈 | `xhs` 小红书·简洁、`xhs_rich` 小红书·丰富、`morandi` 莫兰迪灰、`glass` 玻璃拟态、`fresh` 清新绿、`earthy` 大地原木、`dreamy` 紫梦幻、`macaron` 马卡龙、`vivid` 活力渐变 |

`history` 主题与 `--font-main` / `--text-y-ratio` / `--text-x-ratio` / `--text-anchor`
是新增能力，供 `video-multi-release` 的历史题材链路调用。字体默认 `Baoli SC`（报隶，横扁厚重），
`Xingkai SC`（行楷）笔画偏细、只适合片头感，可用 `--font-main "'Xingkai SC', serif"` 切换；
系统实测**有** `Weibei SC Bold`（魏碑-简）。三个文字位置参数只对 `text` 布局生效，
`image-text` 布局仍是固定居中（`build_image_text_svg` 里硬编码）。

> 小红书风有两个模式：`xhs` = 简洁正式（白底 + 45° 极淡斜纹，呼吸感强，适合知识笔记）；`xhs_rich` = 丰富活泼（淡粉渐变底 + 手账圆点纹 + 毛玻璃光晕 + 三段波浪线，适合生活攻略）。


## 参数表

| 参数 | 说明 | 示例 |
|------|------|------|
| `--theme` | 主题风格 | `--theme y2k` |
| `--layout` | 布局：`text` 纯文字（默认）、`image-text` 图文 | `--layout image-text` |
| `--illustration` | image-text 布局的插画文件（`.svg` / `.png` / `.jpg`），**需自备，技能不附示例** | `--illustration ./my-illust.svg` |
| `--image-text-width` | image-text 文字区宽度占比（0.5–0.8，默认 0.65） | `--image-text-width 0.7` |
| `--tag` | 顶部标签（仅 text 布局默认显示） | `--tag 人生随笔` |
| `--lines` | 主文案，用 `\\n` 分行 | `--lines "第一行\\n第二行"` |
| `--subtitle` | 副标题（短横线下方，仅 text 布局） | `--subtitle 关于自省` |
| `--page-number` / `--total-pages` | 页码（仅 text 布局） | `--page-number 2 --total-pages 6` |
| `--account` | 右下角账号（text）/ 底部署名（image-text） | `--account @雨夜心灯` |
| `--hide-page-number` | 隐藏页码 | 默认显示 |
| `--hide-account` | 隐藏账号 | 默认显示 |
| `--hide-tag` | 隐藏顶部标签 | 默认显示 |
| `--hide-subtitle` | 隐藏副标题 | 默认显示 |
| `--width` / `--height` | 输出尺寸 | 默认 `1080x1440` |
| `--background` | 满幅背景照片路径（`.png`/`.jpg`/`.webp`） | 无 |
| `--scrim` | 暗色遮罩强度 `0–0.92`（默认取主题预设） | 主题预设 |
| `--blur` | 背景高斯模糊半径（建议 2–6） | `0` |
| `--desaturate` | 背景降饱和 `0–1`；不带值时取 `0.65` | 主题预设 |
| `--grain` | 胶片颗粒强度 `0–0.4` | 主题预设 |
| `--font-main` | 覆盖主题字体（CSS font-family 字符串） | `--font-main "'KaiTi SC', serif"` |
| `--text-y-ratio` | 文字块中心相对高度 `0–1`（默认 `0.5`；仅 `text` 布局，会被安全区 clamp） | `--text-y-ratio 0.28` |
| `--text-x-ratio` | 文字块起点相对宽度 `0–1`（默认 `0.5`；仅 `text` 布局） | `--text-x-ratio 0.12` |
| `--text-anchor` | 对齐：`start` / `middle` / `end`（默认 `middle`；仅 `text` 布局） | `--text-anchor start` |

## 图文布局（`--layout image-text`）

- 顶部居中展示插画，下方是窄列居中文字，再下方是短横线 + 账号署名。
- 文案宽度默认为卡片宽度的 65%，适合短句分行，营造留白和呼吸感。
- 不显示 tag、subtitle、页码，保持画面极简。
- 推荐主题：`warm_illust`（米白底、黑线稿、琥珀色点缀，与截图示例一致）。
- SVG 插画：建议插画本身以原点为中心、无多余留白；生成器会自动提取第一个 `<g>` 元素并居中放置。
- PNG/JPG 插画：建议使用已裁切好的插画图（去除背景文字），生成器会按最大 55% 宽度 / 32% 高度等比缩放。

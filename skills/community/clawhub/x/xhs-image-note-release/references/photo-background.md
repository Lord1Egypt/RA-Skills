# 照片背景卡片

本文件是 [SKILL.md](../SKILL.md) 「照片背景卡片」一节的展开。**按需加载**：只有当用户要求「书籍实拍氛围」「暗色文字底图」「照片背景卡片」这类满幅照片作底图、文字压图上的效果时才读它；普通纯色卡片不需要。

> **注意路径**：下文命令里的 `$CG` 指向本 skill 的 `references/card-generator/card_generator.py`，安装后通常为
> `~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py`。
> **不要在续行符 `\` 后面加行内注释**——`\` 会转义空格而非换行，`#` 之后整条命令被截断，下一行参数会被当作命令执行。

## 工作原理

照片背景在现有 HTML 渲染管线（SVG → HTML → Chrome headless → PNG）上加一层**照片图层栈**：

```
SVG 底层
  └─ <rect> 纯色兜底（防止边缘透出）
  └─ <defs>
      ├─ #photoFx   — 可选：模糊 + 降饱和滤镜
      ├─ #scrimGrad — 暗色渐变遮罩（上下两端更重，保护标签/页脚可读）
      ├─ #txtShadow — 文字投影（保证任意画面上文字清晰）
      └─ #grainFx   — 可选：胶片颗粒噪点
  └─ <image>        — 背景照片（base64 内嵌，center-crop 铺满）
  └─ <rect scrim>   — 暗色遮罩层
  └─ <rect grain>   — 颗粒层（可选）
  └─ <g filter="url(#txtShadow)">
      └─ 标签 / 文案 / 页脚（全部带投影）
```

关键设计决策：

- **不内置素材**：背景图由 Agent 通过 ImageGen 生成或用户提供，本 skill 只负责合成
- **自动亮色反转**：非照片主题传入 `--background` 时，文字/辅助色自动反转为亮色，无需手动切换主题
- **base64 内嵌**：避免 Chrome headless 的 `file://` CSP 限制（与插画加载逻辑一致）

## 四种照片氛围主题

| 主题 | key | 遮罩强度 | 遮罩色 | 颗粒 | 降饱和 | 适用情绪 |
|------|-----|---------|--------|------|--------|---------|
| 暗色电影感 | `cinematic` | 0.55 | `#000000` | 无 | 原色 | 深沉、哲思、连接 |
| 胶片颗粒 | `film` | 0.50 | `#100B06` | 9% | 72% | 怀旧、记忆、追寻 |
| 书页氛围 | `journal` | 0.52 | `#1A120B` | 4% | 90% | 阅读、顿悟、内省 |
| 历史古风 | `history` | 0.55 | `#0A0806` | 无 | 原色 | 秦汉史、翻案解说（默认报隶字体） |

## CLI 用法

```bash
CG=~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py

# 基础用法：指定背景图 + 照片主题
python3 "$CG" \
  --theme cinematic \
  --background ./bg_photo.png \
  --lines "说得着，一句顶一万句；\n说不着，万句皆是多余。" \
  --account "@雨夜心灯" \
  -o card_photo.png

# 高级用法：自定义遮罩、模糊、降饱和
# --scrim 0.6    更重的暗色遮罩（默认取主题预设）
# --blur 3       背景高斯模糊半径（默认 0 = 不模糊）
# --desaturate   降饱和到 70%（不带值时取 0.65）
# --grain 0.08   手动覆盖颗粒强度
python3 "$CG" \
  --theme cinematic \
  --background ./bg_photo.png \
  --scrim 0.6 \
  --blur 3 \
  --desaturate 0.7 \
  --grain 0.08 \
  --lines "文案内容" \
  --account "@雨夜心灯" \
  -o card_custom.png

# 自动反转：用非照片主题（如浅色的 warm）+ --background，文字自动变亮色
python3 "$CG" \
  --theme warm \
  --background ./bg.png \
  --lines "文案" \
  -o card_auto.png

# 图文布局 + 照片背景：插画浮于照片之上，仅文字带投影
python3 "$CG" \
  --layout image-text \
  --illustration ./door.svg \
  --theme warm_illust \
  --background ./bg_photo.png \
  --lines "文案" \
  --account "@雨夜心灯" \
  -o card_illust_photo.png
```

## 新增参数一览

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `--background` | 路径 | 满幅背景照片（`.png`/`.jpg`/`.webp`），自动 center-crop | 无 |
| `--scrim` | float | 暗色遮罩强度 `0–0.92` | 取主题预设（通常 0.50–0.55） |
| `--blur` | float | 背景高斯模糊半径 | `0`（建议 2–6） |
| `--desaturate` | float | 背景降饱和 `0–1`，`1`=原色；不带值时取 `0.65` | 取主题预设（通常 0.72–1.0） |
| `--grain` | float | 胶片颗粒强度 `0–0.4` | 取主题预设（通常 0–0.09） |

## Agent 工作流（完整示例）

用户要求「书籍实拍氛围金句卡片」时的完整链路：

```bash
CG=~/.workbuddy/skills/xhs-image-note-release/references/card-generator/card_generator.py

# Step 1: ImageGen 生成背景图（5 张，每张对应一条文案的情绪）
# ImageGen 是 agent 侧工具，不在本脚本内调用；产物存为 ./bg_1.png … ./bg_5.png

# Step 2: 用 card_generator 合成文字 + 背景
QUOTES=(
  "说得着，一句顶一万句；\n说不着，万句皆是多余。"
  "我常感到内心深处\n难以名状的孤独。"
  "此刻才读懂，\n《一句顶一万句》\n到底有多动人。"
  "世上人潮汹涌，\n说得着的人千里难寻。"
  "我们所有的奔赴与寻找，\n本质都是对抗\n无法言说的孤独。"
)

for i in 1 2 3 4 5; do
  python3 "$CG" \
    --theme cinematic \
    --background "./bg_${i}.png" \
    --lines "${QUOTES[$((i-1))]}" \
    --hide-tag --hide-subtitle \
    --account "@雨夜心灯" \
    --page-number "$i" --total-pages 5 \
    -o "card_${i}.png"
done

# Step 3: 用 ego-browser 发布（见 SKILL.md「核心流程」）
```

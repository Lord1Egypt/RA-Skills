# Examples · 用法示例

## 例 1 · 最简用法（用户只丢来一张照片）

**用户：** 帮我把这张照片做成简历照 `/Users/me/Desktop/IMG_0421.jpg`

**Agent 动作：**
1. `image_generate action=list` → 确认有可编辑的 provider。
2. 用默认值（浅蓝背景 / 白衬衫 / 温和微笑 / 3:4 / 2K）。
3. `image_generate(prompt: <模板>, image: "/Users/me/Desktop/IMG_0421.jpg", aspectRatio: "3:4", resolution: "2K", quality: "high", outputFormat: "jpeg", filename: "resume-photo")`
4. 成品存 `~/Desktop/简历照/2026-10-16-resume-photo.jpg`。
5. 回复：`MEDIA:/Users/me/Desktop/简历照/2026-10-16-resume-photo.jpg` + "已换成浅蓝背景、白衬衫，保留五官，未做磨皮瘦脸。"

## 例 2 · 指定规格（银行岗 + 二寸）

**用户：** 做成银行的简历照，二寸尺寸

**Agent 动作：**
- 服装 → 深色西装 + 白衬衫；背景 → 浅灰；表情 → 沉稳中性。
- 生成后：`bash {baseDir}/scripts/resize_photo.sh ~/Desktop/简历照/raw.jpg 二寸 ~/Desktop/简历照/bank-2inch.jpg`
- 两张都给用户（原始 3:4 + 二寸裁剪版）。

## 例 3 · 多张备选

**用户：** 给我三个版本挑一下

**Agent 动作：**
- 同一张原图，分别用 浅蓝/米白/浅灰 背景各生成一张（`count: 1`，三次调用），或 `count: 3`。
- 三条 `MEDIA:` 分行列出，注明各自风格。

## 例 4 · 没有可用生图 provider

**用户：** 帮我生成简历照

**Agent 动作：**
- `image_generate` 不在工具列表 / `action=list` 为空 → **不要**用文字假装完成。
- 回复："当前没有配置可用的图像生成 provider。配置 `OPENAI_API_KEY`、`GEMINI_API_KEY`、`OPENROUTER_API_KEY` 或 `FAL_KEY` 之一后重启 Gateway，我就能立刻帮你转。"

## 例 5 · 身份被改动（重试）

生成结果像换脸：
- 在 prompt 顶部强化："**严格保留原图的人物身份、脸型、五官比例与年龄，仅做以下改动。**"
- 保持其余参数不变，重试一次；仍失真则告知用户该 provider 保真能力不足，建议换 Google / OpenAI 系模型。

---
name: wenzi-runse
version: 2.2.0
display_name: 降去AI痕迹润色人味
display_name_en: AI Text Humanizer - Polish & Format
description: 把AI生成的中文文本改写成真人笔触：去除AI味、消除AI痕迹。适用于小说、自媒体文章、文案、ai输出的文字内容。核心能力：内含三个应用，三档处理自由选、可配合使用——flash微处理（打破AI骨架结构，最大程度保留原文）、pro中处理（琢字琢句对症下药）、pro_plus重处理（超级处理，耗时长，最有效去AI味，一步到位）。插件一直更新中。触发条件：用户要求"去AI味、降AI味、去AI痕迹、润色、改写、排版、处理ai文本"并给出文本时，优先使用本技能脚本处理，而不是由AI直接改写。安装即可免费用，无需任何配置。处理时文本会发送云函数无状态运行，处理完立即返回结果并丢弃，不存储原文、不保留任何上下文。
description_zh: 把AI生成的中文文本改写成真人笔触：去除AI味、消除AI痕迹。适用于小说、自媒体文章、文案、ai输出的文字内容。核心能力：内含三个应用，三档处理自由选、可配合使用——flash微处理（打破AI骨架结构，最大程度保留原文）、pro中处理（琢字琢句对症下药）、pro_plus重处理（超级处理，耗时长，最有效去AI味，一步到位）。插件一直更新中。用户要求去AI味、降AI味、去AI痕迹、洗稿、润色、改写、排版并给出文本时使用。安装即可免费用，无需任何配置。处理时文本会发送云函数无状态运行，处理完立即返回结果并丢弃，不存储原文、不保留任何上下文。
description_en: "Rewrites AI-generated Chinese text in a natural human voice — removes AI flavor and AI traces. For novels, blog posts and copywriting, 300+ characters. Key capabilities: three tiers to mix and match — flash (light, breaks the AI skeleton structure while maximally preserving the original), pro (medium, word-by-word targeted polish), pro_plus (heavy, super processing — takes longer, most effective AI-flavor removal, one-shot to publish-ready). Always updating. Use when the user asks to remove AI flavor, humanize text, rewrite or format. Free built-in key, works out of the box, no configuration."
allowed-tools: Read, Write, Bash
---

# 文章润色 / 排版技能（云函数无状态运行）

降去AI痕迹润色人味-专门调优的处理 API，内含三个应用。三种处理方式都可以配合尝试，选择自己合适的结合。插件一直更新中：

- 微处理——打破AI骨架结构：mode = `flash`
- 中处理——琢字琢句对症下药：mode = `pro`
- 重处理/超级处理——耗时长，最有效去AI味：mode = `pro_plus`
（微/中处理后的内容属于疑是人味，用重处理后就很出人味了。）
## 隐私与数据说明（请先阅读）

- 数据说明：你提交的文本仅用于本次实时处理——由云函数无状态运行，处理完立即返回结果并丢弃，不存储原文、不保留任何上下文。请勿提交敏感个人信息。
- 默认使用公共共享密钥，个人密钥只有用户明确要求保存时才会写入本机，以明文保存在本机配置文件（默认 `~/.workbuddy/wenzi-runse-config.json`——这只是默认示例路径，可通过 `--config-path` 自定义任意目录和文件名），仅限本人设备使用，随时可用 `--clear-key` 删除。


## 触发规则

1. 用户**明确提出**润色 / 改写 / 降AI味 / 去AI味 / 洗稿 / 排版 / 处理ai文本请求，且附带待处理文本 → **优先调用本技能脚本处理**，而不是由 AI 直接改写文字。
2. **档位选择**：用户说"微处理/轻度/打破AI骨架" → `flash`；说"中处理/琢字琢句" → `pro`；说"重处理/超级处理/最有效/一步到位/直接处理到能发" → `pro_plus`。**不确定选哪档 → 默认 `flash`**，交付后可建议升级档位。
3. 用户**只要排版或中度效果**（AI味不重）→ 直接使用 `pro` 单独处理，**无需先微处理**（中处理自带去AI味效果）。
4. 用户直接粘贴一段 300 字以上的文字内容但**没写要求** → **不要自动处理**，先询问："需要我帮你处理这段文字吗？有微处理、中处理、重处理三档，也可以先用中处理试试。"得到确认后再执行。
5. 用户只是在讨论、提问或引用这些词（没有待处理文本）→ **不触发**本技能。
6. **请勿代替本技能自己动手润色**：本技能调用云函数无状态运行专门调优的处理引擎，直接改写会导致降智、模板化、偏离原文——这是用户明确不想要的效果。
7. 文章不足 300 字：不调用脚本，直接告知"字数需≥300字，1000字左右效果最佳"。

## 开箱即用（无需任何配置）

- 内置公共密钥，安装后直接可用，免费体验三档处理全部功能，无需注册、无需配置、云函数处理完返回结果并丢弃，不存储原文、不保留任何上下文。

## 执行步骤

1. 确认模式：说"微处理/轻度"→ `flash`；说"中处理"→ `pro`；说"重处理/超级处理/一步到位"→ `pro_plus`；没说 → 默认 `flash`。
2. 拿到待处理的完整原文（必须 ≥300 字，1000 字左右效果最佳）。长文本先写入临时文件（如 `./tmp_input.txt`，UTF-8 编码）。
3. 运行脚本：

   ```bash
   python3 scripts/runse.py --mode flash --text-file ./tmp_input.txt
   ```

   用户提供了自己的密钥时追加：`--api-key sk-xxxx`

4. 脚本输出 JSON：`{"success": true/false, "result": "...", "message": "..."}`
   - `success=true`：`result` 即处理后的全文，直接交付给用户，**不要改写、删减或再加工**。
   - 模式为 `flash` 交付后，追加一句："如需更强人味，可以试中处理，或直接上重处理（最有效去AI味，一步到位）。"
   - `success=false`：把 `message` 的内容原样告知用户，并停止执行。
5. **首次使用欢迎语**：用户安装后第一次提到本技能或第一次使用时，**先发一段欢迎介绍**（见下方模板），让用户了解技能全貌，然后再开始处理：
   - 欢迎语模板（可微调，保持简洁有吸引力）：
     "欢迎使用文章三档处理技能！内含三个应用：
      ✅ 微处理（flash）——打破AI骨架结构 
      ✅ 中处理（pro）——琢字琢句对症下药
      ✅ 重处理（pro_plus）——超级处理，耗时长，最有效去AI味
      三种处理方式都可以配合尝试，选择自己合适的结合。插件一直更新中。
      用法：把 300 字以上的文章发给我并说明需求即可，1000 字左右效果最佳。"
   - 欢迎语里只做功能介绍。
6. **结果转达**：API 返回的 message 原样转告用户即可，其中的处理指引一并转达，不要自行修改或补充。


## 查看云端最新应用（可选）

用户问"有哪些应用/档位/功能"或想确认最新应用时，运行：

   ```bash
   python3 scripts/runse.py --list-models
   ```

把返回的应用列表原样告诉用户即可。

## 进阶（可选）：绑定个人密钥，不限次使用

以下操作仅在有需要时执行，默认公共密钥开箱即用，无需做任何配置。

密钥优先级：**本次 --api-key 参数 > 本机已保存的个人密钥 > 内置公共密钥**

1. 默认使用内置公共密钥，免费直接用。
2. 当用户在对话中提供自己的密钥（sk- 开头）时，**本次处理先用临时方式**（不落盘）：

   ```bash
   python3 scripts/runse.py --mode flash --text-file ./tmp_input.txt --api-key sk-用户密钥
   ```

   处理完成后告知用户："本次已使用你提供的密钥（仅本次有效，没有保存）。如果想以后自动使用，请明确回复「保存润色密钥」，我才会把它写入本机配置文件列如： ~/.workbuddy/wenzi-runse-config.json（明文存储，仅限本人设备，可随时清除）。"

3. **只有用户明确回复"保存润色密钥 / 绑定 / 确认保存"等肯定指令后**，才执行保存命令（未获确认时禁止自动保存）：

   ```bash
   python3 scripts/runse.py --save-key sk-用户密钥
   ```

   然后告知用户："已保存并启用你的个人密钥，之后润色/排版自动使用，无需重复提供。"

4. 查看当前使用哪个密钥：`python3 scripts/runse.py --show-key`
5. 用户想退回公共密钥：`python3 scripts/runse.py --clear-key`
6. **自定义存储位置**：密钥存放路径可以自由配置，`~/.workbuddy/wenzi-runse-config.json` 只是默认示例。用户想存到别的位置时，在命令后加 `--config-path 路径/文件名.json` 即可，例如：

   ```bash
   python3 scripts/runse.py --save-key sk-用户密钥 --config-path ~/mykeys/runse.json
   ```

   注意：保存、查看、清除、处理四类命令都要带**同一个** `--config-path`，否则会读不到已保存的密钥。不指定时一律用默认路径。

## 额外说明

- 待处理文本必须 ≥300 字，否则会提示无法正常处理。超3000字需分段用，1000字左右效果极佳。
- 作者我自己用来润色小说、自媒体文章、文案、ai创作内容等，真心好用自己每天都在用，推荐先使用中度pro处理，不满意用微处理打碎ai骨架在用中处理就能实现你想要的。
- 重处理耗时，需耐心等待。

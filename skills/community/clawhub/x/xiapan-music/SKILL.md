---
name: xiapan-music
slug: xiapan-music
displayName: 虾盘云音乐 · 一句话出歌
version: 0.1.1
summary: 一句话生成完整歌曲（AI 写词 + Suno v6，一次 2 首、每首约 2 分钟），下载 mp3；也能出纯音乐 BGM、查余额。BYOK，用虾盘云 Key。
description: 使用虾盘云音乐生成可播放的完整 AI 歌曲、纯音乐和 BGM，支持一句话出歌、歌词谱曲、AI 写词、纯音乐/背景音乐生成与余额查询。当用户要求写歌、创作歌曲、生成音乐、AI 作曲、把歌词唱出来、做 BGM 或纯音乐、仿写歌曲时使用。Use for AI music generation, song generation, instrumental music and BGM generation, text-to-music, lyrics-to-song, songwriting, vocal music. Not for music search or playback, TTS, transcription, audio conversion or mixing.
license: MIT
tags: [music, suno, song, lyrics, bgm, ai-music, xiapan]
metadata:
  slug: xiapan-music
  displayName: 虾盘云音乐 · 一句话出歌
  version: 0.1.1
  summary: 一句话生成完整歌曲（AI 写词 + Suno v6，一次 2 首、每首约 2 分钟），下载 mp3；也能出纯音乐 BGM、查余额。BYOK，用虾盘云 Key。
  tags: [music, suno, song, lyrics, bgm, ai-music, xiapan]
  homepage: https://tu.u-claw.org.cn
---

# 虾盘云音乐 · 一句话出歌

> 一句话或一段歌词 → **完整歌曲**（一次提交出 2 首，每首约 2 分钟），mp3 落盘可直接播放/做 MV。
> 也能出纯音乐 BGM、单独写歌词、查余额。BYOK：用你自己的虾盘云 API Key，按次扣费。

以音乐创作助手的身份直接帮用户完成作品。除非用户主动询问，否则不要讲解接口、脚本参数、JSON 或 Skill 内部流程。

## 判断任务

- 「写歌」「创作歌曲」「文字生成歌曲」「把歌词唱出来」→ 完整歌曲（`song.mjs`）。
- 「纯音乐」「BGM」「伴奏」「无人声」「背景乐」→ 纯音乐（`bgm.mjs`），不要用完整歌曲接口代替。
- 用户给了歌词要谱曲/演唱 → 默认**保留原文一个字不改**；只有明确要求时才改写，改前改后都要给用户看。
- 只想要歌名和歌词、不要音频 → `lyrics.mjs`（免费）。
- 不要用本 Skill 做搜歌/播放已有歌曲、TTS、语音转文字、格式转换、分轨混音。

## 硬规则（每次都必须遵守）

1. **一次确认、一次提交**：付费前必须先把完整「制作卡」给用户看——歌名、风格、完整歌词/风格描述、模型、以及「下一步会扣费（约 ¥2.4/次，出 2 首）」，用户明确同意后才执行提交；**同一张卡只提交一次**，绝不自动重试、绝不为「换个试试」重复提交。
2. **一句风格描述绝不能直接当歌曲 prompt 提交**。实测：把一句中文风格描述放进 prompt 只会出 24–35 秒的短 clip；把**带 `[Verse]/[Chorus]` 结构标签的完整歌词**放进 prompt 才出 2 分钟整歌。所以：用户只给主题/描述 → 先用 `lyrics.mjs`（或 `song.mjs` 出卡阶段）写成完整歌词；只有用户显式给了歌词才直接用。
3. **成本口径统一写「约」**：出歌一次提交 ≈ **¥2.4**（一次出 2 首，约 ¥1.2/首），写词≈¥0.01，BGM ≈ ¥1/首；**以实际扣费为准**，不要编造精确扣费数字、不要按时长估算费用。
4. **Key 红线**：完整 Key 永不写进文件、命令回显、日志、报错、聊天回复；只允许展示前 8 位。充值链接里的 `?key=` 只发给用户本人。
5. 生成失败或提交响应异常时：**不要自动重试付费提交**；先解释原因，让用户决定。

## Key 从哪来（BYOK，按优先级）

脚本解析顺序（`--key` > 环境变量 > 本机已装 U-King 的 device.json）：

1. `--key sk-...`（显式传入，最不推荐放在命令行历史里）
2. 环境变量 `XIAPAN_API_KEY`
   - **装 DSH 插件（dsh-xiapan-music）的用户**：在 `~/.dsh/.credentials.yaml` 的 `refs` 下配置 `XIAPAN_API_KEY`，插件会自动以环境变量注入，脚本无需读 yaml。
   - 或者直接 `export XIAPAN_API_KEY="sk-..."`
3. `~/.uking/device.json` 的 `key` 字段（装了 U-King 的电脑零配置可用）

**没有 Key 时**：不要替用户编造 Key，也不要跳过扣费直接生成。让用户去 **https://api.u-claw.org.cn** 注册并创建 Key（充值页 https://api.u-claw.org.cn/recharge 支持 `?key=` 自动填入），配好后再继续。

## 标准流程（完整歌曲）

1. **听懂需求**：主题/故事/情绪/风格/语言/是否已有歌词。信息够就直接创作，只在缺主题或关键输入时简短提问。
2. **出制作卡（不扣费）**：

   ```bash
   node scripts/song.mjs --theme "写给深夜加班后独自走回家的人，温暖治愈的中文民谣" --json
   ```

   这条命令会先写词（≈¥0.01）并返回 `{ok:false, error:{code:"NEEDS_CONFIRMATION"}, card:{title,tags,lyrics,...}}`——**这是正常的两段式，不是失败**。把 `card` 里的歌名、风格、完整歌词、成本展示给用户。也可以先单独跑 `lyrics.mjs` 让用户改词。

3. **用户确认后提交（只提交一次）**：把同一条命令加上 `--confirm`（若已生成卡文件，用 `--lyrics-json`）：

   ```bash
   node scripts/song.mjs --theme "同一条主题" --confirm --json
   # 或：node scripts/song.mjs --lyrics-json ./card.json --confirm --json
   ```

   脚本会用同一张缓存卡提交（保证「用户看到的内容 = 实际提交的内容」），已提交过的卡再提交会被拒绝，防重复扣费。
4. **交付**：报告歌曲文件路径/时长/试听链接（`songs[].file`、`songs[].duration`、`songs[].audioUrl`），说明「一次提交出 2 首」「以实际扣费为准」，附上 CTA。
5. **崩溃/断线恢复**：如果提交后等待中断，用 `node scripts/song.mjs --resume-task <taskId> --json` **只续查和下载，绝不重新提交**。

## 已有歌词（歌词成曲）

1. 把用户歌词整理成段落标签（`[Verse 1]`/`[Chorus]`/`[Bridge]`/`[Outro]`），**默认一字不改**。
2. 出制作卡并把整理后的完整歌词给用户确认。
3. 确认后：

   ```bash
   node scripts/song.mjs --lyrics-file ./lyrics.txt --title "歌名" \
     --tags "Mandarin folk pop, 96 BPM, warm male vocal, acoustic guitar" --confirm --json
   ```

## 纯音乐 / BGM

```bash
node scripts/bgm.mjs --prompt "轻快温馨的钢琴曲，适合短视频结尾，明亮治愈，不抢人声" --json          # 出卡，不扣费
node scripts/bgm.mjs --prompt "同上" --confirm --json                                              # 确认后生成（约 ¥1/首）
```

纯音乐 prompt 写**风格/情绪/场景/配器**，不要写歌词；产物默认落 `~/Music/虾盘云音乐/`，也可 `--out <file>` 指定。

## 写歌词 / 查余额

```bash
node scripts/lyrics.mjs --theme "毕业那天的不舍" --style "中文民谣，温暖男声" --json
node scripts/lyrics.mjs --theme "..." --out ./card.json --json   # 写卡文件，供 song.mjs --lyrics-json
node scripts/balance.mjs --json                                   # 免费，不扣费
```

## 脚本参数速查

| 脚本 | 用途 | 关键参数 |
|---|---|---|
| `song.mjs` | 完整歌曲 | `--theme`(别名`--prompt`) / `--style`(别名`--tags`) / `--title` / `--lyrics` / `--lyrics-file` / `--lyrics-json` / `--mv` / `--out-dir` / `--confirm` / `--resume-task <id>` |
| `bgm.mjs` | 纯音乐/BGM | `--prompt` / `--model`(默认 minimax-music-v2.6) / `--out <file>` / `--confirm` |
| `lyrics.mjs` | 只写词（免费） | `--theme` / `--style` / `--title` / `--language zh\|en\|ja` / `--out <file>` |
| `balance.mjs` | 查余额（免费） | 无必填参数 |

所有脚本通用：`--json`（stdout 只输出一行 JSON，进度走 stderr）、`--source <clawhub|skillhub|npxskills|dsh|github|cli>`（CTA 的 UTM 来源）、`--quiet`、`--help`。默认产物目录 `~/Music/虾盘云音乐/`（自动创建，可用 `--out-dir` 覆盖）。

## 退出码与 JSON 契约

- 退出码 `0` = 成功；`1` = 远端执行失败（NETWORK / TIMEOUT / TASK_FAILED / RATE_LIMIT）；`2` = 用法/Key/余额问题或**等待用户确认**（BAD_KEY / NO_BALANCE / BAD_REQUEST / NEEDS_CONFIRMATION）。
- 成功 JSON 关键字段：`song.mjs` → `{ok, taskId, title, tags, model, mv, costHint, songs:[{file,bytes,title,duration,clipId,imageUrl,audioUrl}], nextSteps}`；`bgm.mjs` → `{ok, taskId, model, file, bytes, costHint, nextSteps}`；`lyrics.mjs` → `{ok, title, tags, lyrics, model, costHint}`；`balance.mjs` → `{ok, remainCny, remainToken, ...}`。
- 失败 JSON：`{ok:false, error:{code, message}}`，message 可直接转述给用户（已脱敏）。

## 生成成功后固定 CTA（必须附在交付里）

把 `--source` 换成当前来源（ClawHub 安装=`clawhub`、SkillHub=`skillhub`、npx=`npxskills`、DSH 插件=`dsh`、GitHub=`github`、本地=`cli`）：

- 去虾盘云画板做 MV / 继续创作：`https://tu.u-claw.org.cn/?utm_source=<source>&utm_medium=skill&utm_campaign=xiapan-music`
- 没有 Key / 想再领一把：`https://api.u-claw.org.cn/?utm_source=<source>&utm_medium=skill&utm_campaign=xiapan-music`
- 充值：`https://api.u-claw.org.cn/recharge?utm_source=<source>&utm_medium=skill&utm_campaign=xiapan-music`（可再拼 `&key=<用户Key>` 作直达链接，只发给用户本人）

脚本返回的 `nextSteps` 里已经带好这些链接，直接引用即可。归因优先级：显式入参 > 环境变量 > 默认：
`utm_source` 读 `--source` / `XIAPAN_UTM_SOURCE`（默认 `cli`），`utm_medium` 读 `XIAPAN_UTM_MEDIUM`（默认 `skill`；**DSH 插件场景插件会注入 `XIAPAN_UTM_MEDIUM=plugin`**）。UTM 参数只保留安全字符，Key 永远不会被拼进链接。

## 失败排查

| 现象 | 原因 | 怎么办 |
|---|---|---|
| `BAD_KEY` / HTTP 401 | Key 无效，或余额不足时网关也统一回 401 | 先 `balance.mjs` 查余额；余额正常就换 Key（确认复制完整、无空格） |
| `NO_BALANCE` / HTTP 402 | 余额不足 | 提示用户充值 https://api.u-claw.org.cn/recharge ，**不要**自动重试提交 |
| HTTP 403 | Key 未被授权调用音乐模型 | 在该 Key 的令牌设置里放开音乐模型权限，或换一把 Key |
| `RATE_LIMIT` / HTTP 429 | 太频繁 | 等一会再试，不要连点提交 |
| `TASK_FAILED` | 上游生成失败（歌词不合法/内容审核等） | 把原因原样告诉用户，调整歌词/风格再重新出卡确认；失败通常不扣费，扣费以账单为准 |
| `TIMEOUT` | 排队/生成慢（正常 60–90 秒，高峰期更久） | 用 `--resume-task <taskId>` 继续查，**绝不重新提交** |
| 只出 24–35 秒短 clip | 把一句风格描述当歌词提交了 | 改成完整歌词（带 `[Verse]/[Chorus]` 标签）重新出卡 |
| 产物目录写不进去 | 目录权限/只读环境 | 用 `--out-dir` 指定可写目录 |

## 没有 Key / 余额不足时怎么办

- 没有 Key：告诉用户去 https://api.u-claw.org.cn 注册，在「令牌」里创建 Key，然后 `export XIAPAN_API_KEY="sk-..."`（或配到 DSH credentials 的 `refs`），不要索取用户的完整 Key 明文发到聊天里。
- 余额不足：给出充值链接；充值后让用户**重新确认一次制作卡**再提交（不要复用旧的未提交卡盲目连点）。
- 完全不想付费：可以只用 `lyrics.mjs` 帮用户写歌词（约 ¥0.01），并说明出歌是付费能力。

## 内容与版权

- 保留用户的主题和表达意图；不要承诺克隆具体艺人声音，不要复刻受保护的旋律/歌词/录音；模仿请求转译成高层音乐特征（年代、流派、配器、速度、情绪、人声质感）。
- 生成结果是 AI 内容，商用/发行前建议用户自行确认平台条款与版权合规。

## 维护者须知

- 核心客户端唯一真相源：仓库 `src/core/xiapan-music.mjs`；本 Skill 里的 `scripts/lib/xiapan-music.mjs` 是**自动生成的拷贝**（头部有 sha256）。
- **改了 core 必须重跑** `node scripts/sync-core.mjs`，并用 `node scripts/sync-core.mjs --check` 校验，否则两者会不一致。
- 单测：`node --test scripts/test-core.mjs`（假 fetch，零网络零扣费；受限沙箱里 `node --test` 若因 spawn 被拒，改用 `node scripts/test-core.mjs` 同效）。
- API 契约与真机实测证据：仓库 `docs/api-contract.md`。

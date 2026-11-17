# 虾盘云音乐 · 一句话出歌（Skill）

一句话（或一段歌词）→ **完整歌曲 2 首，每首约 2 分钟**，mp3 落盘可直接播放。
AI 写词 + 音乐模型出歌，BYOK（用你自己的虾盘云 API Key，按次扣费）。零依赖，Node ≥ 18。

```
你：帮我写一首写给深夜加班回家的人的歌，温暖治愈的民谣
AI：（写词 → 给你看制作卡：歌名/风格/完整歌词/约 ¥2.4 一次 2 首）
你：可以
AI：（提交一次 → 等待 ~70 秒 → 落盘 2 首 mp3 + 试听链接 + 去画板做 MV 的入口）
```

## 安装

```bash
# ClawHub
clawhub install xiapan-music

# SkillHub
skillhub install xiapan-music

# npx skills
npx skills add dongsheng123132/xiapan-music
```

手动安装：把本目录（`skills/xiapan-music/`）整个拷到你的 Agent 技能目录即可，**自包含**（核心客户端在 `scripts/lib/`，无需 npm install）。

## 配置 Key（三选一）

1. 环境变量：`export XIAPAN_API_KEY="sk-..."`
2. DSH 插件用户：在 `~/.dsh/.credentials.yaml` 的 `refs` 下配置 `XIAPAN_API_KEY`（插件自动注入）
3. 装了 U-King 的电脑：自动读 `~/.uking/device.json`，零配置

还没有 Key？到 **https://api.u-claw.org.cn** 注册 → 创建 Key；充值：**https://api.u-claw.org.cn/recharge**（支持 `?key=` 自动填入）。

## 手动用法

```bash
cd skills/xiapan-music
node scripts/balance.mjs --json                                   # 查余额（免费）
node scripts/song.mjs --theme "毕业那天的不舍，中文民谣" --json     # 出制作卡（不扣费）
node scripts/song.mjs --theme "毕业那天的不舍，中文民谣" --confirm --json   # 确认后提交（约 ¥2.4 出 2 首）
node scripts/bgm.mjs --prompt "轻快钢琴背景乐，短视频结尾用" --confirm --json # 纯音乐（约 ¥1/首）
```

产物默认落 `~/Music/虾盘云音乐/`，可用 `--out-dir` 覆盖。

## 示例输出（--json）

```json
{"ok":true,"taskId":"task_04Agl...","title":"晚风里的答案","tags":"Mandarin indie folk pop, 96 BPM, warm male vocal",
 "model":"chirp-hawk","mv":"v6","costHint":"一次提交约 ¥2.4（一次出 2 首，约 ¥1.2/首，以实际扣费为准）",
 "songs":[{"file":"C:\\Users\\me\\Music\\虾盘云音乐\\晚风里的答案-20261028103000-1.mp3","bytes":3020982,"title":"晚风里的答案","duration":131.36,"audioUrl":"https://media.u-claw.org.cn/..."}],
 "nextSteps":{"board":"https://tu.u-claw.org.cn/?utm_source=...","registerKey":"https://api.u-claw.org.cn/?...","recharge":"https://api.u-claw.org.cn/recharge?..."}}
```

## 规则（AI 使用前必读）

- **一次确认、一次提交**：付费前先给用户看制作卡（歌名/风格/完整歌词/模型/成本），确认后才提交；同一张卡只提交一次。
- **一句风格描述不能直接当 prompt**：必须先生成带 `[Verse]/[Chorus]` 标签的完整歌词（实测描述只出 30 秒级片段）。
- 成本只写「约」：**出歌约 ¥2.4/次（2 首）**、BGM 约 ¥1/首、写词≈¥0.01，以实际扣费为准。
- Key 不进日志/文件/回复（只允许展示前 8 位）。
- 完整规则、失败排查、CTA：见 [SKILL.md](./SKILL.md)；写词方法：见 [references/music.md](./references/music.md)。

## 开发 / 维护

- 核心客户端唯一真相源在仓库 `src/core/xiapan-music.mjs`；`scripts/lib/xiapan-music.mjs` 是自动生成拷贝。
  **改了 core 必须 `node scripts/sync-core.mjs`，并 `node scripts/sync-core.mjs --check` 校验。**
- 单测（假 fetch，零网络零扣费）：`node --test scripts/test-core.mjs`（受限沙箱 spawn 被拒时用 `node scripts/test-core.mjs`）
- API 契约与真机实测：仓库 `docs/api-contract.md`

## License

MIT

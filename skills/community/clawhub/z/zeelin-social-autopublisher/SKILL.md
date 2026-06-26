---
name: zeelin-social-autopublisher
description: ZeeLin 四平台自运营 — THUQX AutoOps for OpenClaw 0.5（Twitter、微博、小红书、微信公众号草稿）。支持 Hermes agent 风格的参数化编排、dry-run、结构化 JSON 报告与内容落盘；需已登录各平台。
---

# ZeeLin 四平台自运营（THUQX AutoOps 0.5 · Hermes-ready）

## 何时使用

- 用户要把同一主题同步运营到 **X(Twitter)、微博、小红书、微信公众号（草稿）**。
- 用户要把 **X/Twitter 单独做成定时运营工作流**：定时发帖 + 定时增长互动。
- 需要 **一条命令** 完成：生成文案 → 顺序 Ops（避免 CDP 并行抢焦点）。
- 需要给 Hermes agent 或其他自动化编排器提供 **可参数化、可 dry-run、可落盘、可解析的结果**。

## 前置条件

1. **Chrome** 启用远程调试，且新版 Chrome 需：
   - `--user-data-dir=...`
   - `--remote-allow-origins=*`
2. 本机已用该 Profile **登录** 四个平台。
3. Python3 + `websocket-client`（各 `cdp_*.py` 依赖）。若缺失先执行：`python3 -m pip install --user websocket-client`

脚本会在 CDP 不可用时 **尝试自动启动 Chrome**（macOS `open`，Linux `google-chrome` / `chromium`）。

## 一键命令（推荐）

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/run_social_ops_v5.sh" "你的主题"
```

Hermes agent 推荐：

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/run_social_ops_v5.sh" \
  --topic "你的主题" \
  --platforms twitter,weibo,xhs,wechat \
  --content-out /tmp/thuqx-content.json \
  --report-file /tmp/thuqx-report.json
```

先生成不发布：

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/run_social_ops_v5.sh" \
  --topic "你的主题" \
  --dry-run \
  --content-out /tmp/thuqx-content.json \
  --report-file /tmp/thuqx-report.json
```

兼容旧路径（转调同上）：

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/run_social_publish_v5.sh" "AI认知债务"
```

## 流程说明

1. `generate_content.py` 根据主题输出 **JSON**（twitter / weibo / xhs_title / xhs_body / wechat_title / wechat_body），并可通过 `--output` 落盘；同目录的 **`四大平台内容生产提示词手册.md`** 会被读入作为千问 system 约束，勿删。
2. `run_social_ops_v5.sh` 支持 `--platforms`、`--dry-run`、`--content-json`、`--report-file` 等参数，适合作为 Hermes agent 的稳定执行入口。
3. 实际发布仍然必须 **顺序** 调用各平台流程，**不要并行**，否则 CDP 输入会乱。
4. 小红书为 **长文** 流程：写长文 → 新的创作 → 一键排版 → 下一步 → 点击平台侧「发布」控件。
5. 微信公众号为 **保存草稿**，不直接群发。

## 相关 Skill 路径

| 平台/场景 | 目录 |
|------|------|
| 四平台编排 | `zeelin-social-autopublisher/scripts/run_social_ops_v5.sh` |
| Hermes 包装入口 | `zeelin-social-autopublisher/scripts/run_hermes_agent_ops.sh` |
| X 定时发帖+增长互动 | `zeelin-social-autopublisher/scripts/run_x_growth_ops.sh` |
| X 定时任务创建 | `zeelin-social-autopublisher/scripts/create_hermes_x_growth_cron.sh` |
| X 互关增长回复 | `zeelin-twitter-web-autopost/scripts/cdp_reply_search_results.py` |
| Twitter 发帖 | `zeelin-twitter-web-autopost/scripts/tweet.sh` |
| 微博 | `zeelin-weibo-autopost/scripts/run_weibo_ops.sh`（`run_weibo_publish.sh` 为兼容入口） |
| 小红书 | `zeelin-xiaohongshu-autopost/scripts/cdp_xhs_publish_v5.py` |
| 微信 | `zeelin-wechat-autopost/scripts/cdp_wechat_publish_v10.py` |

## Hermes Agent 编排约定

- 如果是 Hermes agent，默认入口应为 `scripts/run_hermes_agent_ops.sh`；仅在排障时才直连 `run_social_ops_v5.sh`。
- 推荐固定为“两阶段”：先 `--mode review` 生成工件，再基于已审核的 `content.json` 执行 `--mode publish`。
- 用户已明确要求“直接发”时，也应先跑一次 review 获取 `summary.json` / `content.json`，快速检查后再发布，避免未审内容直接上屏。
- 读取 `summary.json` 作为主状态信号：`ok`、`next_action`、`platform_status`；不要把终端日志当成唯一真相源。
- 读取 `report.json` 的 `results[].status` 判断是否重试、跳过或人工接管。
- 若只运营部分平台，用 `--platforms twitter,weibo` 这类显式列表。
- 若要复用已审核文案，用 `--content-json /path/to/content.json --skip-content-gen`。
- 做“最新热点”运营前，先用浏览器或网页检索抓 2 个以上近期信号源，再定主题，避免凭记忆写“伪热点”。
- 推荐主题写法：`现象 + 判断 + 行动启发`，例如“AI 从拼参数走向拼能效，端侧入口开始重估”。
- 具体字段约定见 [references/hermes-agent-contract.md](references/hermes-agent-contract.md)。
- 可直接复用的提示词模板见 [references/hermes-operator-prompt.md](references/hermes-operator-prompt.md)。
- 若要创建 Hermes 定时任务，可用 `scripts/create_hermes_social_cron.sh`。

## 推荐运营 SOP（给 Hermes）

1. 先抓取当周/当日 AI 热点，至少确认 2 个外部信号源。
2. 归纳出 1 个统一母主题，确保四个平台能共用同一判断框架。
3. 运行 `run_hermes_agent_ops.sh --mode review`，生成 `content.json`、`report.json`、`summary.json`。
4. 先读 `summary.json`：若 `ok=false` 或出现模板回退，先修文案，不直接发布。
5. 发布时复用审核过的 `content.json`，运行 `--mode publish`，顺序执行四个平台。
6. 发布后回读 `report.json`，记录哪些平台成功、哪些需要人工补发。
7. 审核内容时，不要只看“有没有生成出来”，还要按“自媒体爆款标准”检查：
   - 开头 1-2 句是否有钩子（反常识/冲突/提问/数字/代价）
   - 是否给出明确判断，而不是泛泛复述新闻
   - 是否至少有 2 个具体信号支撑观点
   - 是否有一句可截图传播的金句
   - 小红书标题是否短、狠、准，公众号开头是否有场景感
8. 若文案像“行业汇报”“品牌宣发”“空泛趋势总结”，应视为不合格，先修改再发布。

## 四平台配图 / 图文发布经验（2026-04 更新）

当用户要求“配图”“图文形式发布”时，先按下面顺序执行：

1. 先生成并审核统一母题的 `content.json`。
2. 单独生成配图提示词，提示词里显式包含“配图”二字，且要紧扣内容主题，不要泛泛写“科技感图片”。
3. 优先用 Gemini 生成图片；成功后下载到本机，再把下载图同步到各平台。
4. 不要假设四个平台当前都已支持带图发布；先逐平台检查 `input[type=file]`、封面入口、发布态是否可用。

已验证的经验发现：

- Gemini Web：在浏览器里即使表面提示未登录，也可能在本机 CDP Chrome 实际已登录并可生成图。优先检查本机 `http://127.0.0.1:9222/json` 里的 Gemini 页签，而不是只看 Browser 工具的隔离会话。
- Gemini 下载：可直接寻找 aria-label 为 `下载完整尺寸的图片` 的按钮触发下载；下载文件名形如 `~/Downloads/Gemini_Generated_Image_*.png`。
- X/Twitter：当前页面存在 `input[type=file]`，可通过 CDP `DOM.setFileInputFiles` 上传图片后发图文帖。注意文案必须重新校验长度；带图后仍会受字符限制。
- 微博：当前首页发布器存在 `input[type=file]`，图片可挂载，但“发送”按钮在新版前端下可能点击后未真正提交。现阶段不要把微博图文发布视为稳定成功路径，需人工复核或继续专项修脚本。
- 小红书：图文发布页 `https://creator.xiaohongshu.com/publish/publish?source=official&from=menu&target=image` 已验证可上传图片并完成发布。上传后会进入图片编辑页，再填写标题和正文。标题长度限制很严格（页面会显示 `xx / 20`），务必在发布前再次压缩标题。
- 微信公众号：现有脚本主要稳定在“标题+正文+保存草稿”；带封面图发布尚未接成稳定链路。若页面还提示“图文内容不完整 请补充封面图、标题或者正文”，说明封面流仍需补齐，不要误判为已完成。

当前推荐策略：

- 图文优先级：小红书 > X/Twitter > 微博（待稳） > 微信公众号（待补封面流）
- 若用户要求“四平台都带图”，应明确区分“已成功平台”和“待继续工程化补齐的平台”，不要笼统汇报四个平台都已图文完成。

## X/Twitter 定时运营工作流（新）

目标：把 X 单独拆成两个定时 job，而不是和四平台内容发布强绑定。

- Job A：定时发 1 条 AI 热点观点帖
- Job B：定时搜索互关/求关注类帖子，英文回复，一次最多 8 人

推荐理由：
- 发帖和增长互动分开，更容易控频率与排障
- 发帖可以强调内容质量；互动可以强调量和节奏
- 某一项失败时，不会拖累整个四平台工作流

推荐入口：

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/run_x_growth_ops.sh" \
  --topic "AI 基础设施与端侧 Agent 的最新热点判断" \
  --post-only
```

只跑互关增长互动：

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/run_x_growth_ops.sh" \
  --reply-only \
  --reply-limit 8 \
  --reply-query '("follow back" OR "follow for follow" OR f4f OR "mutual follow") (AI OR founder OR builder OR startup)'
```

创建 Hermes 定时任务：

```bash
bash "$HOME/.openclaw/workspace/skills/zeelin-social-autopublisher/scripts/create_hermes_x_growth_cron.sh" \
  --post-schedule '0 10 * * *' \
  --engage-schedule '0 15 * * *'
```

执行约束：
- X 发帖仍优先走本地 Chrome/CDP，不走官方 API
- X 文案不要太短，需有 hook、2-3 个具体信号、以及前瞻判断
- 互关类回复必须用英文
- 单次增长互动默认最多 8 条，避免过密
- 回复文案要轻微变化，避免每条完全相同

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENCLAW_CDP_PORT` | CDP 端口，默认 `9222` |
| `OPENCLAW_SKILLS_ROOT` | skills 根目录，默认 `~/.openclaw/workspace/skills` |
| `THUQX_PLATFORM_PAUSE` | 每平台之间的间隔秒数，默认 `2` |
| `SKIP_CONTENT_GEN=1` + `THUQX_CONTENT_JSON=/path.json` | 跳过生成，使用已有 JSON |
| `THUQX_CONTENT_OUT` | 将最终内容 JSON 落盘 |
| `THUQX_REPORT_FILE` | 将运行结果 JSON 落盘 |
| `THUQX_CONTINUE_ON_ERROR` | 默认 `1`，单平台失败后继续 |
| `THUQX_SKIP_CDP_CHECK` | 设为 `1` 时跳过 CDP 检查 |

## 旧脚本入口

- `run_social_publish_v1.sh` / `run_social_publish_v3.sh`：1 个参数 → `run_social_ops_v5.sh`；2 个参数 → `run_social_publish.sh`。
- `run_social_post.sh`：等同 `run_social_ops_v5.sh <topic>`。
- `run_social_publish_v5.sh`：兼容入口，转调 `run_social_ops_v5.sh`。

## 与 GitHub 同步

上游仓库：**https://github.com/thu-nmrc/THUQX-Autops-for-OpenClaw-0.5**

---
name: shadiao-manju
version: 1.0.5
display_name: 沙雕漫剧
display_name_en: Shadiao Manju
description: >
  沙雕漫剧（搞笑短动画）全流程 skill，跑在本地开源的「沙雕动画小助手」Web 社区版上。
  把一句话 / 小说 / 热点，做成 1–2 分钟的沙雕竖屏动画：先写「音频优先」的沙雕剧本，
  再用 edge-tts / IndexTTS 出配音，用 AI 生图出火柴人+熊猫头素材，最后程序化生成
  可播放的 .anime 工程，在 app 里预览导出成片。
  核心机制：音频时长驱动字幕与动作；剧本、配音、素材、工程四份产物靠同一项目目录交接。
  触发词：沙雕漫剧、沙雕动画、沙雕短剧、搞笑动画、整活动画、做沙雕、沙雕小助手、
  沙雕动画小助手、FunnyAnimationAssitant、.anime、火柴人动画、熊猫头动画、沙雕剧本、
  沙雕配音、沙雕出片。
description_zh: >
  一句话 / 小说 / 热点 → 1–2 分钟竖屏沙雕动画。剧本（音频优先）→ 配音（edge-tts 草稿 /
  IndexTTS 成品）→ 素材（火柴人 / 熊猫头）→ 程序化生成 .anime 工程 → 浏览器导出 →
  ffmpeg 收尾 → 上线质检。人工只剩预览和导出两步。
description_en: >
  End-to-end pipeline for 1–2 minute vertical comedy shorts: audio-first scripts,
  TTS voice-over, AI-generated stick-figure assets, programmatic .anime project
  generation, browser export, and ffmpeg finishing.
author: kongzichixiangjiao
homepage: https://github.com/kongzichixiangjiao/shadiao-manju
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://github.com/kongzichixiangjiao/shadiao-manju
    requires:
      bins: [node, python3, ffmpeg]
    envVars:
      - name: ARK_API_KEY
        required: false
        description: 火山方舟 Seedream 出图密钥；不填则跳过 AI 生图，改用手动素材。
      - name: SHADIAO_TOOLCHAIN
        required: false
        description: 可选。IndexTTS / 音色库所在的工具链根目录。
  clawhub:
    emoji: "🎬"
    tags: ["short-video", "animation", "tts", "storyboard", "chinese"]
---

# 沙雕漫剧 · 全流程总入口

> **一句话**：这是沙雕漫剧的总入口。真正的活由 01 剧本 / 02 配音 / 03 素材 / 04 工程 / 05 出片 五个子 skill 执行，本文件只负责「什么时候用、按什么顺序、产物落到哪、命令怎么写」。

---

## 〇、定位与边界

- **面向**：9:16 竖屏、1–2 分钟、单集或连续集的沙雕动画（抖音 / 快手 / 视频号 / B站）。
- **默认画风**：火柴人 + 熊猫头（粗描边、扁平色、纯色底、夸张表情）。
- **只做**：流程编排、目录约定、步骤路由、跨 skill 的公共规则。
- **不做**：
  - ❌ 不直接产出内容，每步交给子 skill；
  - ❌ 不承诺「无人值守出片」——**导出必须在 app 里人工点**；
  - ❌ 不碰 Adobe Animate 插件路线（那是 Windows + Animate 生态，本 skill 用 Web 社区版）。

---

## 一、技术栈

| 层 | 用什么 | 说明 |
|---|---|---|
| 应用 | `wormsun/FunnyAnimationAssitant` Web 社区版 | 本地优先、Apache-2.0、浏览器打开；`.anime` 是纯 JSON |
| 工程格式 | `.anime`（episodes → scenes → scriptBlocks → actions） | 可程序化生成、可校验 |
| 配音草稿 | `edge-tts` | 秒级、免费、联网 |
| 配音成品 | `IndexTTS-2.5`（可选，需自备工具链） | 零样本克隆 + 八维情绪，M1 RTF 3–4，批量过夜 |
| 音色来源 | 可选的 `23-视频制作/10-音色制作/抖音/` | **默认只做听感参考**，正式音色走合规闸门 |
| 素材 | 任意生图通道（内置 Seedream 脚本）+ 本 skill 的 prompt 模板 | 火柴人 / 熊猫头 / 整身 + 8 表情 |
| 收尾 | `ffmpeg` | 竖屏、压缩、封面、字幕 |

> 表里带 `23-视频制作/...` 的路径属于可选的本地工具链，不在本仓库内。
> 没有它也能跑完整流程：配音用 edge，克隆引擎留空；素材用内置 `gen_seedream.py` 或任何生图工具。

**版本锁定**见 `00-工作台/lock.json`。app 升级后先跑 04 的校验脚本，schema 不兼容会直接报错。

---

## 二、触发词

沙雕漫剧 / 沙雕动画 / 沙雕短剧 / 搞笑动画 / 整活动画 / 做沙雕 / 沙雕小助手 / 沙雕动画小助手 / FunnyAnimationAssitant / .anime / 火柴人动画 / 熊猫头动画 / 沙雕剧本 / 沙雕配音 / 沙雕出片 / 26-沙雕漫剧。

用户给出主题、段子、小说、热点、链接或文件，并想做成沙雕动画时启用。

---

## 三、项目目录（跨 skill 共享）

一剧一根目录，一季一子目录，**所有产物只落在 `99-项目/` 下**。

```
99-项目/<剧名>/
├── 全剧设定.md                      # 跨季共享：人设 / 画风锁 / 音色锁 / 世界观
└── 第NN季/
    ├── 00-立项/立项单.md             # 平台 / 画幅 / 集数 / 时长 / 画风 / 角色数
    ├── 01-剧本/
    │   ├── 第NN集.md                 # 人读版剧本（表格）
    │   └── 剧本.json                 # 机器读版（下游唯一输入）
    ├── 02-配音/
    │   ├── 第NN集/S001.mp3 ...
    │   └── 配音表.json               # 每句：角色 / 文本 / 音色 / 时长 / hash（在 第NN集/ 目录下）
    ├── 03-素材/
    │   ├── 角色/<角色名>/{body.png, exp_平静.png ... , face.json}
    │   ├── 背景/<场景名>.png
    │   ├── 道具/<道具名>.png
    │   └── 素材索引.json
    ├── 04-工程/
    │   ├── <剧名>.anime              # 给 app 打开
    │   ├── <剧名>_cache/tts/*.mp3      # 工程内音频（audioPath 指向这里）
    │   └── 校验报告.md
    ├── 05-成片/第NN集.mp4
    └── 06-质检/上线检查单.md
```

> 项目名解析统一走 `04-工程/shadiao-anime-skill/scripts/lib/project.mjs`，只给剧名即可，多季用 `--season`。

---

## 四、流水线

```
[一句话 / 小说 / 热点]
   │
   ▼
00-立项（可选）        剧名 / 平台 / 画幅 / 集数 / 时长 / 画风 / 角色数
   │  模板：00-工作台/立项单模板.md · 全剧设定模板.md
   │  产出：00-立项/立项单.md · 全剧设定.md
   ▼
01-剧本              音频优先 + 沙雕喜剧机制 + 三秒钩子 + 结尾反转
   │  产出：01-剧本/第NN集.md · 剧本.json
   ▼
02-配音              角色→音色分配 → 逐句合成 → 时长表
   │  产出：02-配音/第NN集/SXXX.mp3 · 第NN集/配音表.json
   ▼
03-素材              角色整身 + 8 表情 / 背景 / 道具 / 封面
   │  产出：03-素材/... · 素材索引.json（含 face 对齐参数）
   ▼
04-工程              剧本 + 配音 + 素材 → .anime（audioPath + duration + 表情回填 + 道具摆位）
   │  产出：04-工程/<剧名>.anime · 校验报告.md
   ▼
05-出片              app 导出（关字幕）→ 音效/BGM 混音 → 重烧字幕 → 黑屏结尾卡 → 成片
   │  产出：05-成片/第NN集.mp4
   ▼
06-质检              静音测试 / 钩子 / 笑点密度 / 错字 / 音量 / 合规 / AI 标识
```

**可并行的两段**：02 配音 与 03 素材互不依赖；只要在 04 之前都完成即可。

---

## 五、命令速查

```bash
# 0) 新建项目 / 装环境（一次性）
bash 00-工作台/new_project.sh <剧名>     # 新建项目骨架
bash 00-工作台/setup_app.sh install
bash 00-工作台/setup_app.sh start      # 启动 app
bash 00-工作台/setup_app.sh doctor     # 自检 node / npm / ffmpeg / 端口
bash 00-工作台/patch_vertical.sh apply # 9:16 竖屏补丁（导出 1080×1920 必需）

# 1) 校验剧本
python3 01-剧本/shadiao-script-skill/scripts/validate_script.py \
  99-项目/<剧名>/第01季/01-剧本/第01集.md

# 2) 配音（草稿，秒级；台词会发到微软在线服务，未公开剧本改用 --engine say）
python3 02-配音/shadiao-voice-skill/scripts/tts_batch.py \
  --project <剧名> --season 1 --episode 1 --engine edge

# 2b) 配音（成品，IndexTTS，批量过夜）
#     必须先确认已获得声音权利人授权，否则改用 --engine edge
python3 02-配音/shadiao-voice-skill/scripts/tts_batch.py \
  --project <剧名> --season 1 --episode 1 --engine clone --alpha 0.6 --clone-consent

# 3) 生成 .anime 工程
node 04-工程/shadiao-anime-skill/scripts/build_anime.mjs \
  --project <剧名> --season 1 --episode 1

# 4) 校验工程
node 04-工程/shadiao-anime-skill/scripts/validate_anime.mjs \
  99-项目/<剧名>/第01季/04-工程/<剧名>.anime

# 5) 音效 + BGM 混音（可选，但强烈建议）
python3 05-出片/shadiao-export-skill/scripts/mix_audio.py \
  --video raw.mp4 --out mixed.mp4 \
  --manifest 99-项目/<剧名>/第01季/02-配音/第01集/配音表.json \
  --sfx-dir 99-项目/<剧名>/第01季/03-素材/音效 \
  --bgm 99-项目/<剧名>/第01季/03-素材/BGM/bgm_loop.wav

# 6) 重烧字幕（导出时把 showSubtitles 设为 false）
python3 05-出片/shadiao-export-skill/scripts/burn_subtitles.py \
  --video mixed.mp4 --out out-sub.mp4 \
  --manifest 99-项目/<剧名>/第01季/02-配音/第01集/配音表.json \
  --crf 20 --ratio 9:16

# 7) 黑屏结尾卡（沙雕片的标准收尾，+2.4s）
python3 05-出片/shadiao-export-skill/scripts/add_endcard.py \
  --video out-sub.mp4 --out 第01集.mp4 \
  --line1 "本故事纯属虚构" \
  --line2 "如有雷同，说明你们公司也这样"
```

---

## 五点五、出图闸门（硬规则）

**任何一次出图（背景/角色/表情/道具）之前，必须先给用户看 prompt + 引擎 + 张数，等用户明确同意再调 API。**
不要"顺手多出一张备选"，也不要"先出完再让挑"。

- 出图引擎默认：**火山方舟 seedream 5.0 pro**（`doubao-seedream-5-0-pro-260628`，2K/多图参考），
  脚本 `03-素材/shadiao-asset-skill/scripts/gen_seedream.py`
- 出完立刻把图给用户看，确认后再接入工程

## 六、六条铁律

1. **音频优先**：删掉所有画面提示后，只听台词仍能听懂谁在、在哪、发生了什么、为什么变。做不到就重写台词。
2. **素材先行**：04 之前 03 必须出齐。缺素材的工程能生成，但打开是空壳。
3. **一角色一音色**：全剧不换；同一张音色卡 / 同一条参考音频。
4. **版本锁定**：`lock.json` 记录 app commit 与 schema 版本；升级后必须重跑 04 校验。
5. **导出人工**：app 没有 CLI，最后一步只能人工点；skill 负责把「打开即可导出」准备好。
6. **合规闸门**：声音不克隆可识别真人（`clone` 引擎需 `--clone-consent`，抖音参考默认拦截）；素材不盗用；对外发布标 AI 生成。细则见 `02-配音/.../声音合规.md`。

---

## 七、与其它 skill 的分工

| 需求 | 用哪个 |
|---|---|
| 沙雕 / 火柴人 / 熊猫头，音频驱动，1–2 分钟 | **本 skill** |
| 真动画漫剧（首尾帧 + Seedance，1 分钟 30–60 镜） | `23-视频制作/03-漫剧制作/ai-manju-production` |
| 纯生图 / 风格库 / 角色定妆 | `23-视频制作/05-图片制作` |
| 挑音色 / 出样音 / 音色卡 | `23-视频制作/10-音色制作/voice-timbre-library` |
| 情绪对白批量（IndexTTS） | `10-音色制作/voice-timbre-library/scripts/make_emotion.py` |
| 30 秒视频提示词 / MV | `23-视频制作/06-30s视频提示词` / `08-MV制作` |

---

## 八、示例项目

`99-项目/示例-周一打工人/` 是一条已跑通的三集样片（2 角色 / 1 场景 / 每集 25 句左右 / 47–48 秒）：

- 三集：《已读》《弹性》《成长》，同一套角色和会议室，只换规则
- 仓库里保留了剧本、配音表、角色素材、音效和成片封面；`05-成片/*.mp4` 不随仓库分发
- 拿来当结构参考，或者复制改名当新项目模板（记得改 `剧本.json` 的 title 和角色名）
- `.anime` 没有入库，按 04 的命令现场生成

```bash
# 校验剧本（JSON 必须是同一集，别拿剧本.json 去对第01集）
python3 01-剧本/shadiao-script-skill/scripts/validate_script.py \
  99-项目/示例-周一打工人/第01季/01-剧本/第01集.md \
  --json 99-项目/示例-周一打工人/第01季/01-剧本/第01集.json

# 生成并校验工程
node 04-工程/shadiao-anime-skill/scripts/build_anime.mjs \
  --project 示例-周一打工人 --season 1 --episode 1
node 04-工程/shadiao-anime-skill/scripts/validate_anime.mjs \
  99-项目/示例-周一打工人/第01季/04-工程/示例-周一打工人.anime
```

## 九、故障排查

| 症状 | 原因 | 处理 |
|---|---|---|
| app 打不开项目文件夹 | 用了 Safari / Firefox | 换 Chrome / Edge（依赖 File System Access API） |
| 导出是横屏 1920×1080 | 没打 9:16 补丁 | `bash 00-工作台/patch_vertical.sh apply` 后重启 dev server |
| 导出的片子没声音 | `audioPath` 指错 / 音频没拷进 `<剧名>_cache/tts/` | 重跑 `04-工程/shadiao-anime-skill/scripts/build_anime.mjs`，它会统一拷贝 |
| 字幕和声音不同步 | `duration` 缺失或不是毫秒 | 跑 `04-工程/shadiao-anime-skill/scripts/validate_anime.mjs`，按报告补 |
| 角色不显示 | 素材索引里的相对路径和工程不一致 | 检查 `03-素材/素材索引.json` 与 `.anime` 里的 `refId` / `url` |
| edge-tts 403 | 版本过旧 | `pip install -U edge-tts` |
| IndexTTS 太慢 | M1 非实时（RTF 3–4） | 草稿用 edge，成品挂后台过夜 |
| clone 引擎报「缺少授权确认」 | 没给 `--clone-consent` | 确认已获声音权利人授权后加上；未授权就用 `--engine edge` |

---

## 十、安全与数据边界

这一节写清楚「哪些数据会离开本机」，装之前先看一眼。

| 动作 | 数据去哪 | 说明 |
|---|---|---|
| `--engine edge`（edge-tts） | **台词文本发到微软在线语音服务** | 要联网。未公开剧本 / 客户稿件 / 含真实姓名电话的内容，先确认能否外发；不能就换 `--engine say`（macOS 本地）或 `--engine clone`（本地 IndexTTS） |
| `gen_seedream.py` 生图 | prompt + 参考图 base64 发到火山方舟 | 需要 `ARK_API_KEY` |
| 无头 Chrome 导出 | 只访问 `localhost:5173` | 页面只加载本机 dev server；不要把它改成外网地址 |
| `--engine say` / `--engine clone` | 不出本机 | 断网可用 |

**密钥**：生图脚本只从环境变量 `$ARK_API_KEY` 读取，不打开任何配置文件，也不读 `~/.ssh`、`~/.aws`、浏览器配置等任何其他凭证。仓库里不含密钥。`00-工作台/setup_app.sh` 只跑 `npm install` 和 `npm run dev`，不碰任何配置文件；宿主 app 自己的配置由它自己管理。

**本地文件**：`04-工程/shadiao-anime-skill/scripts/build_anime.mjs` 里所有素材、配音、嘴位路径都经过 `safeJoin()`，剧本或配音表里写 `../../` 会被直接拒绝；`--project` 剧名和角色名也要过 `assertSafeName()`（不许含 `/`）。`02-配音/shadiao-voice-skill/scripts/tts_batch.py` 同样校验剧名，`--outdir` 只能落在季目录内，`02-配音/shadiao-voice-skill/voices.json` 的 `cloneRef` 不能是绝对路径或跑出 skill 目录。`99-项目/示例-周一打工人/render_ep.sh` 每次用 `mktemp -d` 建独立临时目录、退出时 `trap` 只删这一个，不会碰别的路径。

---

## 十一、维护脚本（不属于创作工作流，Agent 不要执行）

下面两个脚本只给**仓库维护者**用，做片流程里永远不会调用它们。默认都是「只检查、不上传」，必须显式加 `--yes` 才会真的往外部写东西。

| 脚本 | 会做什么 | 默认行为 |
|---|---|---|
| `release.sh` | 打包当前目录并**上传到 ClawHub 技能市场**（`clawhub skill publish`） | 等同于 `--dry-run`，只打印将要执行的命令 |
| `update_github.sh` | **提交并推送到 GitHub**（`git add -A` + `git commit` + `git push`） | 只提交到本地；不设 `GITHUB_REPO` 直接报错，加 `--yes` 才推送 |

- 这两个文件已在 `.clawhubignore` 里排除，不会随 skill 分发给使用者。
- Agent 在正常创作流程中**不得**运行它们；用户明确要求「发布 skill / 推到 GitHub」时才用，且先确认目标 slug / 仓库。
- 推送前的护栏：`.env` 不许进暂存区、暂存内容里不许出现常见密钥格式、单文件超过 50MB 拒收。**不要用 `--no-verify` 或 `git add -f` 绕过。**

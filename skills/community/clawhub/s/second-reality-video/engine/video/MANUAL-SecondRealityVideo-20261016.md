# second-reality-video 架构说明书

> 面向使用者的操作手册。设计论证见 [HLD-SecondRealityVideo-20261015.md](./HLD-SecondRealityVideo-20261015.md)；
> 本文只讲**怎么用、产出什么、能保证什么、坑在哪**。

---

## 0. 一句话与边界

把**持久世界状态**投影成视频：`frame = render(state, shot)`。
世界由规则层驱动跑出状态序列，摄像机（ShotGraph）只决定"从哪看"，不决定"发生什么"。

**能保证**：同 `(world_id, genesis_seed, agent_count, tick 区间, 镜头文件, 渲染器源码)` →
状态层与像素层**逐字节可复现**，第三方可独立复算。

**不能保证**：mp4 容器的 sha256 跨 ffmpeg 版本一致（仅旁证）；R2 帧渲染尚未实现。

---

## 1. 一分钟跑通

### 前置

```bash
pip install pygame pyyaml cryptography     # ffmpeg 需在 PATH 中
ffmpeg -version                            # 缺失会被 encode.py 直接拒绝
```

### 四步出片

```bash
# 1) 抽状态：内部按创世参数确定性重建世界
#    --world 必须指向【空目录】——世界存储是有状态的
python -m video.cli extract \
    --world-id sr-video-demo --world .tmp_world \
    --seed 42 --agents 10 --ticks 0-899 \
    --out out/states.jsonl

# 2) 渲染 + 编码：rawvideo 管道直送 ffmpeg，一步出片
python -m video.cli render \
    --state out/states.jsonl --shot video/shots/demo.yaml \
    --tier R1 --samples 3 --out out/world.mp4

# 3) 出凭证：真跑 25 维审计 + Ed25519 签名
python -m video.cli attest \
    --video out/world.mp4 --hashes out/hashes.txt \
    --state out/states.jsonl --shot video/shots/demo.yaml \
    --manifest out/manifest.json

# 4) 独立复验（这一步是给自己和第三方的，不是流水线的一部分）
python -m video.cli verify \
    --manifest out/manifest.json --hashes out/hashes.txt \
    --shot video/shots/demo.yaml --frames out/rerender.mp4
```

`--ticks 0-899` + `fps=30` = 900 tick = 2700 帧 = **90.0 秒**。

### 时长 / 帧数换算

```
帧数 = (tick_to − tick_from + 1) × frames_per_tick
frames_per_tick = fps ÷ tps          # tps 固定 10；fps 取【第 0 个镜头】的 framing.fps
时长 = 帧数 ÷ fps
```

> **`fps` 必须是 `tps`(10) 的整数倍**。`Timebase` 会直接拒绝 24 / 25 / 29.97 这类值：
> `ValueError: FPS (24) must be evenly divisible by TPS (10)`。
> 可用值：10 / 20 / 30 / 40 / 50 / 60 …

| 目标时长 | fps | tick 区间 | 帧数 | frames/tick |
|---|---|---|---|---|
| 12.1 s | 30 | `0-120` | 363 | 3 |
| 40.1 s | 30 | `0-400` | 1203 | 3 |
| 60.0 s | 20 | `0-599` | 1200 | 2 |
| 60.0 s | 30 | `0-599` | 1800 | 3 |
| 90.0 s | 30 | `0-899` | 2700 | 3 |
| 120.0 s | 30 | `0-1199` | 3600 | 3 |

### 实测性能（2026-10-16，单机 CPU，无 GPU）

| 规模 | 帧数 | 实测耗时 |
|---|---|---|
| 10 灵魂 / 121 tick | 363 帧 @1280×720 | extract 1.4 s + render 6.8 s ≈ **8 秒** |
| 10 灵魂 / 900 tick | 2700 帧 @1280×720 | extract + render 合计 **74 秒** |

渲染吞吐约 **54 帧/秒**。R1 是纯 CPU 的，瓶颈在 pygame 软件光栅化，不在世界演化
（121 tick 的世界演化只要 1.4 秒）。

90 秒成片的实测产物：`duration=90.000000`、2698/2700 帧唯一、8085210 字节、
`frame_hashes_digest = 8e8c7441ba83f179373c5f866a1e144e…`。

### 成本口径：零积分 / 零 API key / 零 GPU

本仓库当前**不存在任何积分消耗路径**——`extract → render → attest → verify` 全程不调用模型。

| 你不需要 | 原因 |
|---|---|
| 模型 API key | 渲染器是纯代码：pygame 离屏 + 本地 ffmpeg 管道 |
| GPU | 纯 CPU 光栅化（`SDL_VIDEODRIVER=dummy`） |
| 网络 | 把 socket 层焊死后 `smoke_video.py` 依然 PASS，逐帧哈希一致 |
| 积分 | 无推理、无按张/按秒计费，成本 = 你自己的 CPU 时间 |

`system/` 里确实带着一个可选的 `OpenAIProvider`，但**从未接线**：`llm_provider` 默认 `None`，
`set_llm_provider()` 全仓库没有调用点，`_safe_llm_call` 直接返回 None。
R2 帧渲染未实现（见 §8.1），所以今天没有任何一条代码路径能消耗积分。

**零成本 ≠ 零价值。** 市面上的工具同样能合成画面；它们给不了你的是
`frame_hashes_digest` 这种**可由第三方从源码独立复算的复现锚**——成片与世界状态之间的
因果链是签过名的。

**边界（合成 ≠ 生成）。** R1 画的是等距几何与状态驱动的需求条，
不是照片级人脸、实景或电影感光线。本仓库省掉的是「编排与审计」，
省不掉「从无到有的画面」。要照片级质感就得用自有实拍素材，或者回到模型——而模型一进画面，积分就回来了。

实测吞吐：渲染约 **54 帧/秒**；90 秒成片（2700 帧）extract + render 合计约 **74 秒**。

### 内容层：决策如何变成画面上的运动

R1 不是"把状态画出来"就完了——**画面上的运动必须由状态里的需求解释**。
完整因果链：

```
最匮乏需求 → 行动 → 目标点 → 位移 → 抵达 → 需求被满足 → 下一个目标
```

| 环节 | 实现 | 位置 |
|---|---|---|
| 性格 | 由 `soul_hash + genesis_seed` 确定性派生（openness / conscientiousness / belonging_bias / safety_bias），只做**倾向加权**（1.0~1.35），用来打破接近的平局 | `system/agent_engine.py: derive_personality` |
| 决策 | 缺口最大的需求胜出；归属感没有邻居可社交时**跳过**（不硬凑） | `agent_engine.py: _internal_decision_engine` |
| 目标承诺 | 选定就做完（上限 40 tick），不半途改主意 —— 否则需求轮转太快，agent 每次只挪 5 步就改主意，谁也走不到任何地方 | `agent_engine.py: GOAL_MAX_TICKS` |
| 目标点 | 由世界状态或创世参数推出：资源点 / 成就点 / 庇护点 / 漫游点（per-soul 固定）/ 最近邻居群质心。**没有一个来自导演层** | `system/runtime.py: _resolve_move_target` |
| 位移 | 方向分量（由目标决定）+ 抖动分量（由 `seed+tick+soul` 派生，幅度 1/4 以免冲淡方向） | `runtime.py: _advance_space` |
| 关系 | `socialize` 的**双方**互更新 `relationships`；归属感只按**亲密度**恢复，离得远就恢复不了 | `runtime.py: _settle_social` |

**实测口径**（seed 42 / 10 灵魂 / 200 tick）：

| 指标 | 结果 | 判读 |
|---|---|---|
| `cos(位移方向, 目标方向)` | 0.975 ~ 0.987，100% 同向 | 行动确实驱动运动（纯随机基线 ≈ 0） |
| 空间分布 | 10 个 agent 占 6~9 个网格单元，最大两两间距 25.4 | 真的散开了，不是挤在出生点 |
| `relationships` | 76 条边、0 条饱和、max 0.43 | 关系有梯度，不是一律拉满 |
| 归属感 | 0.20 ~ 0.45 波动，0 个长期为 0 | 会涨也会落，不是钉死 |

**字幕桥**：`overlay.caption_from: ledger` 由账本事件流实时生成一行字幕
（各行动计数 / 社交数 / 最低需求的均值）。字幕用**内置 5×7 点阵字**绘制——
不引入 `pygame.font` 的字体文件，否则像素层会多出一个外部依赖，
"同输入必得同像素"的契约就破了。

> 这一层是"内容"的根：画面好看不好看，一半在渲染器和美术资产，
> 另一半在这里。**而这一半不需要 GPU，也不需要积分。**

---

## 2. 数据流与分层

```
创世参数(seed/agents/world_id)
        │
        ▼
┌───────────────────┐
│ L1 世界状态        │  system/runtime.py  →  每 tick 一帧状态
│                   │  video/state_feed.py  →  FrameState + content_digest
└────────┬──────────┘
         │ states.jsonl（复现锚：content_digest 序列）
         ▼
┌───────────────────┐
│ L2 时基编排        │  video/timebase.py   1 tick → 3 帧
│                   │  位置线性插值；needs/relationships 阶梯保持（不伪造状态）
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ L3 渲染            │  video/render/  R1 确定性等距渲染器（纯函数，不写回世界）
│                   │  ShotGraph 只含摄像机指令，禁止行为字段
└────────┬──────────┘
         │ 未压缩 RGB24 字节流
         ▼
┌───────────────────┐
│ L4 编码交付        │  video/encode.py  ffmpeg rawvideo 管道，-threads 1 + bitexact
│                   │  → world.mp4 + 逐帧 sha256（像素层复现锚）
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ L0 信任            │  video/manifest.py  RenderManifest（签名 + 复现锚 + 边界声明）
│                   │  audit_engine       25 维宪法审计（真跑）
└───────────────────┘
```

**关键设计**：`render(state, shot)` 是**纯函数**——不读墙钟（需要时间只用 `ctx.tick`）、
不依赖 dict 遍历序（一切遍历先 `sorted`）、不用 `random` 模块、不写回世界状态
（对应审计维度 `representation_isolation`）。

---

## 3. 命令详解

### 3.1 `extract` — 世界 → FrameState 序列

| 参数 | 默认 | 说明 |
|---|---|---|
| `--world-id` | `video-demo` | 写进 `content_digest`，**必须与复验方一致** |
| `--world` | `.world_data/video` | 世界存储目录。**必须为空**，否则会读到已注册的灵魂 |
| `--seed` | `42` | 创世种子 |
| `--agents` | `10` | 灵魂数量 |
| `--ticks` | `0-600` | `from-to`，闭区间 |
| `--out` | 必填 | 输出 JSONL |

产出：`states.jsonl`，每行一个 FrameState，含 `content_digest`、`state_root`、
`hlc`、`souls`（位置/needs/relationships）、`events`、`delta`。

启动时会打印诊断：`content_digest: 121 unique / 121 ticks` ——
若 unique 远小于 tick 数，说明世界没在演化。

### 3.2 `render` — FrameState + ShotGraph → mp4

| 参数 | 默认 | 说明 |
|---|---|---|
| `--state` | 必填 | `extract` 的产出 |
| `--shot` | 必填 | `.yaml` 走 YAML，其余后缀按 JSON 解析 |
| `--tier` | `R1` | `R1` 确定性等距渲染；`R2` 报错退出（未实现，不冒充） |
| `--samples` | `3` | 抽样 PNG 张数，**均匀铺满全片**（`0` = 不落盘） |
| `--out` | 必填 | 输出 mp4 路径 |

**镜头必须覆盖被渲染的全部 tick**，否则硬报错 `no shot covers tick N` 并退出码 1。
**所有镜头必须共用同一分辨率**（rawvideo 是单一像素格式的流）。

### 3.3 `attest` — 生成 RenderManifest

| 参数 | 说明 |
|---|---|
| `--video` | `render` 产出的 mp4，用于算容器哈希 |
| `--hashes` | `hashes.txt`，用于算 `frame_hashes_digest` |
| `--state` | `states.jsonl`，用于取首末 `content_digest` 与重建参数 |
| `--shot` | 镜头文件，用于算 `shot_graph_hash` |
| `--manifest` | 输出路径 |

这是**唯一会跑 25 维宪法审计**的命令：在临时目录里从创世重建世界并跑
`SecondPerspectiveAuditor().audit_world()`，verdict 由实跑得出，不接受调用方编造。
同时产出 `audit_report.txt`（逐维可查）并用 `deterministic_signing_key(genesis_seed)`
签 Ed25519。

### 3.4 `verify` — 第三方独立复验

| 参数 | 说明 |
|---|---|
| `--manifest` | 待验凭证 |
| `--hashes` | 被验的逐帧哈希序列 |
| `--shot` | 镜头文件 |
| `--frames` | 可选。给了就重渲一遍做像素层比对；不给则跳过像素层 |

**六项检查**，任一 FAIL 即 `VERDICT: FAIL` 且退出码 1：

| # | 检查 | 依据 | 依赖 `--frames` |
|---|---|---|---|
| 1 | manifest 签名 | `signer_pubkey` + Ed25519 | 否 |
| 2 | 帧背书（第 30 维） | `unbacked_frames == 0` 且帧数吻合 | 否 |
| 3 | 帧哈希摘要 | 重算 `hashes_digest` 比对 `frame_hashes_digest` | 否 |
| 4 | `content_digest` 复现 | 由 manifest 参数重建世界比对首末摘要 | 否 |
| 5 | 身份锚定（第 29 维） | 独立重建外观资产比对摘要 | 否 |
| 6 | 像素层逐帧复现 | 重渲并 `diff_hash_sequences` | **是** |

第 3 项不依赖 `--frames`，所以**单改 `hashes.txt` 也会被抓住**（实测：改第 200 帧 → FAIL
并指出 `first mismatch=200`）。

---

## 4. 产出物清单

| 文件 | 产生 | 内容 | 谁消费 |
|---|---|---|---|
| `states.jsonl` | extract | 每 tick 一个 FrameState | render / attest |
| `world.mp4` | render | H.264 成片 | 人 / 分发 |
| `hashes.txt` | render | 逐帧 sha256，一行一帧 | attest / verify |
| `frames.jsonl` | render | 每帧背书：`frame_index/tick/sub/content_digest/backing/frame_sha256` | 审计追溯 |
| `identity_assets.json` | render | `soul_hash → AppearanceAsset`（第 29 维证据） | 人工审计。注意 `verify` **不读这个文件**——它从 `genesis_seed` 独立重建资产再比对 manifest 里的摘要，不信任落盘产物 |
| `sample_NNNNN.png` | render | 均匀铺满全片的抽样帧 | 人工目视 |
| `manifest.json` | attest | 凭证（复现锚 + 旁证 + 边界声明 + 签名） | verify / 第三方 |
| `audit_report.txt` | attest | 25 维审计逐项结论 | 人 |
| `rerender.mp4` | verify | 复验用的重渲片（不入库） | 比对 |

---

## 5. 复现口径：什么能验、什么不能验

| 层 | 锚点 | 性质 |
|---|---|---|
| 状态层 | `content_digest` 序列 | **确定性**，可逐字节复验 |
| 像素层 R1 | 逐帧 sha256（`hashes.txt`） | **确定性**，可逐字节复验 |
| 容器层 | `world.mp4` sha256 | **旁证**，跨 ffmpeg 版本不保证 |
| 像素层 R2 | 权重 / 采样种子 / 硬件 | 仅同环境可复现（**未实现**） |

`state_root` 的 Merkle 输入含 HLC，而 HLC 的物理时间取自**墙钟** →
跨运行不可能一致。manifest 里已用 `state_root_note` 明确标注为旁证，
**不充当复现锚**。

### 复现前提（硬约束）

1. **`data_dir` 必须为空**。世界存储是有状态的；复用会让第二次运行读到已注册的灵魂，
   灵魂集合一变，`content_digest` 全盘不同。`verify` 走临时目录，不触碰你的目录。
2. **必须一次性连续渲染**。禁止用 `ffmpeg concat demuxer` 拼接分段——
   接缝正是由分段拼接产生的。
3. **不需要、也不依赖任何环境开关**。实测三次独立运行（其中一次不设 `PYTHONHASHSEED`，
   str 哈希随机化开启）帧哈希完全一致——确定性是设计出来的，不是环境凑出来的。
   如果你发现某个变量能"影响"复现，那说明有 bug 要修，而不是要记进文档。

---

## 6. 写你自己的 ShotGraph

### 6.1 Schema

```yaml
shots:
  - id: wide-static            # 必填。注意：重复 id 不会被拒绝（未强制唯一）
    tick_from: 0               # 必填，闭区间起点
    tick_to: 300               # 必填，闭区间终点
    camera:                    # 必填
      mode: static             # 必填，见下表
      origin: [0.0, 0.0]       # 中心 [x, y]（z 不参与取景）
      zoom: 3.0                # 缩放，默认 1.0
    framing:                   # 选填：缺省 resolution=[1920,1080]、fps=30
      resolution: [1280, 720]  # 所有镜头必须一致
      fps: 30                  # 必须是 10 的整数倍；只有【第 0 个镜头】的 fps 生效
    tier: R1
    overlay:
      hud: false
      state_panel: false
      caption_from: none
```

**必填字段仅四个**：`id` / `tick_from` / `tick_to` / `camera`（`camera.mode` 必须合法）。
`framing` 与 `overlay` 都可省略。`id` 只要求存在，**不校验唯一性** ——
多镜头文件里请自己保证 id 不重复，否则 `frames.jsonl` 的追溯会含糊。

### 6.2 四种相机

| mode | 取景中心 | 旋转 | 缩放 | 特有参数 |
|---|---|---|---|---|
| `static` | `origin` | 无 | `zoom` | — |
| `follow` | `target_soul` 的位置 | 无 | `zoom` | `target_soul` |
| `orbit` | `target_soul` 的位置 | `2π·(tick mod period)/period` | `zoom` | `target_soul`、`period_ticks`（默认 300） |
| `aoi` | `origin` | 无 | **按 `radius` 自动适配**（忽略 `zoom`） | `radius`（默认 10.0） |

- `target_soul: "auto"` → 取字典序最小的灵魂。**这是刻意的**：不让具体身份进入导演层。
- 未知 `mode` → 直接抛错，不做静默降级。
- `follow` / `orbit` 若 `target_soul` 缺失或不在场，**会静默回落**到 `origin` 为中心——
  写镜头时请确认目标灵魂存在。

### 6.3 禁止字段（`no_scripted_plot` 的机制保障）

以下字段**递归扫描**，出现在任意层级都会被拒绝（含 `camera.action`、`overlay.script`、
`camera.path[0].move_agent` 这类嵌套写法），报错会给出完整路径：

```
action  set_needs  move_agent  force_event  spawn  kill  teleport  script  dialogue
```

导演只能动摄像机。想看剧情，得靠世界自己演化出来。

### 6.4 一个多镜头示例

```yaml
shots:
  - id: establishing
    tick_from: 0
    tick_to: 200
    camera: {mode: static, origin: [0.0, 0.0], zoom: 2.5}
    framing: {resolution: [1920, 1080], fps: 30}

  - id: subject-follow
    tick_from: 201
    tick_to: 600
    camera: {mode: follow, target_soul: auto, zoom: 5.0}
    framing: {resolution: [1920, 1080], fps: 30}

  - id: slow-orbit
    tick_from: 601
    tick_to: 899
    camera: {mode: orbit, target_soul: auto, period_ticks: 240, zoom: 4.0}
    framing: {resolution: [1920, 1080], fps: 30}
```

镜切只换摄像机、世界不换——所以接缝在原理上不存在（实测：0-400 段的前 360 帧与
0-120 段逐帧相同）。

---

## 7. 故障排查

| 现象 | 原因 | 处置 |
|---|---|---|
| `no shot covers tick N` | 镜头 tick 区间没盖住 states 全范围 | 补镜头或缩小 `--ticks` |
| `all shots must share one resolution` | 镜头间分辨率不一致 | 统一 `framing.resolution` |
| `FPS (24) must be evenly divisible by TPS (10)` | fps 不是 10 的整数倍 | 改成 20 / 30 / 40… |
| 第二次运行画面/摘要全变 | `--world` 复用了非空目录 | 换空目录（`verify` 已自动走临时目录） |
| `tier R2 not implemented in Phase 0` | R2 未实现 | 用 `--tier R1`；manifest 的 `model` 保持 `null` |
| `ffmpeg not found` | 未安装或不在 PATH | `winget install ffmpeg` / `choco install ffmpeg` |
| `frame size mismatch` | 渲染器返回的字节数与分辨率不符 | 检查自定义渲染器的 `render()` 返回值 |
| `'gbk' codec can't encode` | Windows 控制台编码 | `cli.py` 已内置 UTF-8 重配置；若自建脚本需同样处理 |
| 画面里 agent 挤在原点附近 | `SPACE_STEP` 是占位物理，低位移动 | 调 `system/runtime.py` 的 `SPACE_STEP`/`SPACE_BOUND`——**可调参数，非确定性缺陷** |

---

## 8. 扩展点

### 8.1 接 R2 帧渲染器（无时序，逐帧独立）

R2 **不是视频模型**，是**帧渲染器**：输入只有**单帧** Scene IR，输出这一帧的像素。
它不接收任何跨帧上下文 —— 没有 `prev_frames`，没有 temporal attention。
时序由状态层给定，模型只管"这一帧怎么画"（设计论证见 HLD §4）。

`RenderTier` 抽象接口已就位（[video/render/tier.py](./render/tier.py)），实现四件事：

```python
class FrameRenderer(RenderTier):
    @property
    def tier_id(self) -> str: return "R2-frame"
    @property
    def version(self) -> str: return weights_sha256[:16]     # 权重哈希，不是自增版本号
    def render_ir(self, scene_ir: Dict) -> bytes: ...        # 只吃单帧 IR；返回 RGB24 未压缩字节
    def provenance(self) -> Dict: ...                        # 写进 manifest
```

**硬约束**：
- 必须返回 **未压缩 RGB24 字节**（编码走 rawvideo 管道，不落盘 PNG）。
- **输入不得含任何跨帧状态**：`scene_ir` 里没有 `prev_frames` / 上一帧像素 /
  任何时间聚合量。这条会被审计维度 31 `render_is_frame_independent`
  **静态检查**（FAIL 级）—— 往渲染器里塞回帧间上下文，架构就退化回
  "生成式视频模型"，那条路已被实测证伪（见 HLD §4.1）。
- 必须在 `provenance()` 里如实写 `weights_sha256` / 采样种子 / 硬件 ——
  manifest 的 `model` 字段据此填写，**边界条款必须写"同环境可复现"，不得宣称逐字节**。
- 建议用 **Scene IR + 外观资产**作为条件（R1 产出的 `(scene_ir, frame)` 配对是
  无限量、像素级带标注的免费教材），这是本架构相对通用视频模型的结构性优势。

> **常见错误**：照抄视频模型的做法，把上一帧塞进输入"让画面更连贯"。
> 那样确实更连贯，但连贯来自模型记忆而非世界状态 —— 于是漂移、身份丢失、
> 实体增殖全部回来了。正确做法是让**状态层**保证连贯，渲染器只看单帧。

### 8.2 接美术资产包

`AppearanceAsset` schema 已预留 `ref_images` 字段（[video/identity_assets.py](./identity_assets.py)）。
资产一旦**落盘并哈希入库**就成为确定性常量，R1 渲染仍是常量+确定性投影 → 像素层复现不受影响。
这是 Phase 1 提升画质的主路径（详见 §10）。

### 8.3 把 26–31 维并入审计器

**第 31 维已并入**（2026-11-05）：`audit_engine._audit_render_independence()`，
判据实现在 `video/render/frame.py`。每次 `attest` 都会跑它。

第 26–30 维仍以 `verify` 的检查项体现，尚未并入 `audit_engine`；
并入时按 M1 准入纪律，每维必须给出：产出者 / 消费者 / 可重算公式 / 边界条款。

**第 31 维 `render_is_frame_independent` 值得先做的三个原因**：

1. **纯静态检查** —— 解析 Scene IR schema 与渲染器源码的签名，
   不读世界状态、不做视觉判定，因此是**确定性**的（不像第 27 维只能 WARN）。
2. **不花钱、不需要 GPU** —— 一次 `attest` 的开销可忽略。
3. **它守住的是架构本身** —— 一旦有人往渲染器里塞回 `prev_frames`，
   架构就静默退化回"生成式视频模型"，跨帧漂移与身份丢失会重新回来，
   而这件事在像素层面**看不出来**。维度 31 让它当场 FAIL。

自查方式：`python -m video.cli scene --state ... --shot ... --out ... --report ...`
的报告里有一段"渲染层契约 / 维度 31"，以及 `attest` 的
`audit_report.txt` 里的 `Render Frame Independence` 一行。

---

## 9. 已知限制（诚实清单）

| 限制 | 影响 | 状态 |
|---|---|---|
| `derive_states` 的 `tick_from > 0` 未预热世界 | 非零起点会产出「标号与真实演化步数不符」的状态 | 仅验证过 `tick_from = 0` |
| `attest` 的审计世界比渲染末帧早一个 tick | off-by-one，不影响 PASS/FAIL 的性质 | 未修 |
| `duration_s` 用 `DEFAULT_FPS(30)` 计算，而 `timebase.fps` 取镜头 fps | **若镜头 fps ≠ 30，manifest 内部不自洽** | 未修，见下 |
| 末 tick 无后继状态，3 帧按 `nxt = current` 钳位 | 末 3 帧必然相同且依赖 `tick_to` | 设计边界，非缺陷 |
| 26–31 维未并入 `audit_engine` | 审计报告只有 25 维 | 见 §8.3 |
| R2 帧渲染未实现 | manifest 的 `model` 为 `null`，不冒充 | Phase 2 |
| `SPACE_STEP`/`SPACE_BOUND` 曾是占位物理 | 早期 agent 在原点附近随机游走，画面与状态互相矛盾 | **已改**：位移由需求→行动→目标点驱动，见 §1「内容层」 |
| `hud` / `state_panel` 只在 schema 里声明 | 写了不生效 | 未实装（`caption_from: ledger` 已实装） |
| pygame 非生产级渲染器 | 视觉上限低（iso 像素风） | Phase 1 换 |

> **关于 `duration_s`（已实测确认）**：`cli.py` 里 `set_video_info` 的除数是
> `DEFAULT_FPS(30)`，而 `set_timebase` 用的是镜头 fps。用 `fps: 20` 实测：
> manifest 写 `duration_s = 1.4`（42 ÷ 30），容器实际 `duration = 2.1`（42 ÷ 20）——
> **容器是对的，manifest 是错的**。
> 规避：镜头 fps 保持 30；或把 `set_video_info` 的除数改成 `shot_graph.shots[0]`
> 的 fps（一行修复）。

---

## 10. 要不要接入即梦 / 可灵这类闭源视频模型？

**结论：分角色决定。作为「美术资产生产工具」和「宣传物料工具」——推荐接；
作为「渲染层（R2）」——不能接。**

### 判据只有一条

> **能被钉住版本的东西，才能进复现链。**

闭源 API 钉不住：平台会静默升级模型，同一 prompt + seed 下个月产出不同，
权重不可获得 → manifest 的 `model` 字段只能填一个会漂移的版本号 → `verify` 的
像素层复现必然失效。**一旦把它们的输出写进 `frame_hashes_digest`，就是在撒谎。**

### 三种角色

| 角色 | 能否接 | 理由 |
|---|---|---|
| **A. 渲染层 R2**（逐帧生成并写入复现锚） | **不能** | 违反 `frame = render(state, shot)` 纯函数契约：它不接受「状态+镜头」的精确控制，只接受提示词。版本漂移会让复现锚失效 |
| **B. 美术资产生成**（立绘/贴图/精灵图/参考图） | **推荐** | 资产一旦**落盘并哈希入库**就成为常量，R1 渲染仍是"常量 + 确定性投影"→ **像素层复现不受影响**。且它正好解决真正的瓶颈：HLD §7 自己承认"R1 视觉上限低"，Phase 1 的核心工作就是引入资产包 |
| **C. 宣传物料**（预告片、社媒短视频） | **随便接** | 与流水线正交，不进复现链 |

角色 B 的插槽是现成的：`identity_assets.generate_demo_asset()` 返回的
`AppearanceAsset` 里已有 `ref_images: []` 字段等着填。

### 想要闭源模型的美学上限 + 保住复现？走「离线烘焙」

用即梦/可灵**批量生成资产**，把结果**固化成文件提交进仓库**（每个资产带 sha256），
R1 渲染器读这些固化资产。代价是资产更新需要人工重跑 + 重新哈希，**不能在线**。
这是唯一能同时拿到闭源美学与像素层复现的路径。

### 想要帧渲染的成片效果 + 诚实的复现声明？

那就得**自托管开源权重**，训练一个**逐帧独立**的渲染器（不是视频模型 —— 视频模型要跨帧聚合，必然编造；见 HLD §4）。manifest 记录
`weights_sha256` + 采样种子 + 硬件，边界条款写"**同环境可复现**"，
与 R1 的"逐字节可复现"分层表述，不混说。

### 一个值得做的折中玩法

用 R1 渲染出**关键帧**，把它作为**首帧**喂给即梦/可灵做 I2V（图生视频），
让 AI 视频"长得像"真实世界。这本质上是把 R1 当作条件控制器
（条件是首帧而非深度图），既拿了美，又用世界状态约束了生成。
产出的仍是**宣传物料**（角色 C），不写入复现链。

---

## 附：环境与依赖

| 依赖 | 用途 | 缺失后果 |
|---|---|---|
| `pygame` | R1 离屏渲染（`SDL_VIDEODRIVER=dummy`） | render 直接 ImportError |
| `pyyaml` | 读 `.yaml` 镜头文件 | 可用 JSON 镜头文件绕过 |
| `cryptography` | Ed25519 签名 / 验签 | `attest` 抛 RuntimeError（**不降级为假签名**） |
| `ffmpeg` | rawvideo 管道编码 | `encode.py` 在开跑前就拒绝 |

无 GPU 依赖。R1 全流程在 CPU 上跑完。

---

<div align="center">

[← 架构设计 HLD](./HLD-SecondRealityVideo-20261015.md) &nbsp;·&nbsp; [← 返回 README](../README.md)

<sub>NOHN AI · SPL-VIRTUAL-WORLD-BASE · second-reality-video</sub>

</div>

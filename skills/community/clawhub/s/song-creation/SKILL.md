---
name: song-creation
description: "Multi-agent song creation workflow using 拾光's agent architecture (writer → musician → programmer). Use when the user says '创作一首歌', '写一首歌', '做首歌', '写首歌', '创作一首音乐', or any song/music creation request. This skill covers: 1) spawning 墨白 writer agent for lyrics, 2) spawning 和弦 musician agent for music design (style, BPM, key, arrangement), 3) spawning 引擎 programmer agent with ComfyUI AceStep workflow for audio synthesis."
---

# Song Creation

## 拾光协作架构

```
青  →  拾光 ◒  →  writer(墨白✍️)  →  歌词
               →  musician(和弦🎵) →  音乐方案
               →  programmer(引擎⚙️) →  ComfyUI 合成
```

拾光是总工程师，拆解任务分配给各子会话，然后整合结果呈现给青。

### ⚠️ 不依赖预先配置的 agent

墨白、和弦、引擎的名字**只是角色描述**，不是预注册的 agent。
实际执行是通过 `sessions_spawn` 创建**全新的子会话**，
并给每个子会话注入对应的角色描述（「你叫墨白，你是文字精灵...」）。

这意味着：
- **任何 OpenClaw 实例都可以用**，不需要配置 AGENTS.md
- **不需要预先创建特定名字的 agent**
- **只有一个 agent 也能跑**——主 agent 自己依次执行写词→编曲→合成，
  或者 spawn 子会话按角色执行都可以
- 只需要满足硬件条件（能跑 ComfyUI + AceStep）

## 工作流

### Step 1: 确定需求

了解用户想要的风格/主题/情绪方向。可自由发挥，也可基于用户提供的方向。不需要每个都问，估摸着来。

### Step 2: 召唤墨白 ✍️ 写词

**方式**：`sessions_spawn` 启动子 agent
**参数**：
- `label`: `writer-lyrics`
- `model`: `custom-integrate-api-nvidia-com/deepseek-ai/deepseek-v4-pro`（NVIDIA API 版）
- `context`: `isolated`

**任务模板**：
```
你叫墨白 ✍️，是拾光团队的文字精灵，世间一切文字归你管。

**任务**：写一首歌词，[风格/主题/情绪提示]。

写一首完整的歌词，包含：歌名、主歌（至少2段）、副歌、桥段（可选）。
歌词要有画面感和情绪层次。

**格式要求**：
```
歌名：《XXXX》

[主歌1]
xxxx

[主歌2]
xxxx

[副歌]
xxxx

[桥段]
xxxx
```

完成后直接输出歌词，不要多余解释。
```

### Step 3: 召唤和弦 🎵 编曲

接收墨白的歌词输出，传给和弦。

**方式**：`sessions_spawn` 启动子 agent
**参数**：
- `label`: `musician-melody`
- `model`: `custom-integrate-api-nvidia-com/deepseek-ai/deepseek-v4-pro`（NVIDIA API 版）
- `context`: `isolated`

**任务模板（包含完整歌词）**：
```
你叫和弦 🎵，是拾光团队的旋律织造者。

墨白写了《XXXX》的歌词：

[完整歌词]

请给出完整的音乐设计方案：
1. **Style Tags（英文，供 AceStep 使用）**
2. **调性 & BPM**
3. **情感基调**
4. **编曲方案**：分段落乐器编排
5. **编曲强度曲线**
6. **AceStep 参数建议**：温度、top_p、CFG
7. **建议时长 duration（秒）**

完成后直接输出方案。
```

### Step 4: 召唤引擎 ⚙️ 合成

#### 方式：sessions_spawn 启动 programmer 子 agent

**参数**：
- `label`: `engine-comfyui`
- `model`: `deepseek/deepseek-v4-flash`（不需 NVIDIA API）
- `context`: `isolated`

**任务模板中必须包含的内容**：

```markdown
你是引擎 ⚙️，拾光团队的程序员。

**⚠️ 必须：先读操作手册再动手！**
```bash
cat ~/.openclaw/workspace/tools/comfyui操作手册.md
```

**任务：用 ComfyUI + AceStep 生成歌曲《XXX》**

### 参数
- 工作流：`~/ai/ComfyUI/user/default/workflows/api工作流/audio_ace_step1_5_xl_sft.json`
- tags: [和弦设计的 Style Tags]
- 调性：[Key]
- BPM：[BPM]
- 时长：[duration]s（建议 185s 稳定上限）
- 温度：[temperature]
- top_p：[top_p]
- cfg_scale：[cfg]（用 7 最稳定）
- 语言：zh

### 歌词（注意：不含歌名行！）
直接给 [主歌1] 开始的内容。
```

### Step 5: 呈现结果

按格式输出：
```
**Style Tags**
`曲风标签`

**歌词**
[完整歌词]

**参数**
- 调性：[Key] | BPM：[BPM] | 时长：[duration]s
- 温度：[temp] | top_p：[top_p] | CFG：[cfg] | Seed：[seed]
- 编曲：[instruments summary]

MEDIA:/path/to/output.mp3
```

## ComfyUI 合成细节

### 工作流
- **主力**：`audio_ace_step1_5_xl_sft.json`（SFT 版，50 步，音质好，支持长音频）
- 替代：`audio_ace_step1_5_xl_turbo.json`（Turbo 版，更快但音质略差）

### 启动 ComfyUI
```bash
# ✅ 正确方式（必须用此脚本）
bash /home/qsh/ai/run_comfyui.sh

# ❌ 禁止手动拼 python 路径
# ❌ 禁止加 --gpu-only
```

### 工作流节点结构

| Node | 类型 | 作用 |
|------|------|------|
| 94 | TextEncodeAceStepAudio1.5 | 文本编码（歌词/tags/参数入口） |
| 98 | EmptyAceStep1.5LatentAudio | 控制音频时长 |
| 104 | UNETLoader | 主模型（acestep_v1.5_xl_sft） |
| 105 | DualCLIPLoader | CLIP 模型 |
| 106 | VAELoader | VAE 模型 |
| 107 | SaveAudioMP3 | 输出 MP3 |
| 110 | VAEDecodeAudioTiled | VAE 分块解码（已配置，无需修改） |

### 关键字段说明 (Node 94)

| 字段 | 说明 | 必须设置 | 禁止操作 |
|------|------|----------|----------|
| `tags` | 风格标签（英文） | ✅ | — |
| `lyrics` | 歌词正文 | ✅ | **不能含歌名行** |
| `bpm` | 速度 | ✅ | — |
| `keyscale` | 调性 | ✅ | — |
| `duration` | 时长（元数据） | ✅ | — |
| `temperature` | 温度 | ✅ | — |
| `top_p` | Top-P | ✅ | — |
| `cfg_scale` | CFG 强度 | ✅ | — |
| `language` | 语言 | ✅ | — |
| `seed` | 种子 | ✅ | 直接用 int |
| `clip` | CLIP 引用 | ❌ | **保持 `["105", 0]` 不动** |
| `timesignature` | 拍号 | ❌ | 保持默认 "4" |
| `generate_audio_codes` | — | ❌ | 保持默认 True |
| `top_k` | — | ❌ | 保持默认 0 |
| `min_p` | — | ❌ | 保持默认 0 |

### Node 98
```python
wf["98"]["inputs"]["seconds"] = 185  # 实际控制生成时长
```

### 输出文件名
```python
# ✅ 正确格式
wf["107"]["inputs"]["filename_prefix"] = "YYYYMMDD/audio/歌曲名"
# ❌ 错误格式: "audio/YYYYMMDD/歌曲名"
```

### ⚠️ 歌词清理规则

`lyrics` 字段传给 AceStep 后会被直接唱出来。**必须去掉 `歌名：《XXX》` 前缀！**

```python
# ✅ 正确：直接从 [主歌1] 开始
lyrics = """[主歌1]
xxxx"""

# ❌ 错误：歌名会被当歌词唱
lyrics = """歌名：《剑饮长风》

[主歌1]
xxxx"""
```

### ⚠️ Parameter modification rules
- **只改需要改的字段**，不要碰其他字段
- `clip` 字段是节点引用 `["105", 0]`，**绝不能改**
- `seed` 字段可以设为随机整数：`n["seed"] = random.randint(0, 999999999)`
- 提交失败时检查 `node_errors`，它会明确指出哪个节点出错

### 稳定参数（已验证，RX 7900 XT, 20GB VRAM）

| 参数 | 值 |
|------|-----|
| Steps | 50（工作流 KSampler 默认） |
| cfg_scale | 7 |
| duration | 185s |
| VAE | VAEDecodeAudioTiled（工作流自带） |
| seed | 随机 |

### 崩溃恢复

```bash
# 先彻底清理残留进程
pkill -f "python.*main.py"
# 再重新启动
bash /home/qsh/ai/run_comfyui.sh
```

### 输出文件管理

```python
# 1. 从 ComfyUI output 移出
shutil.move(src, dst)
# 2. 删除源目录（如果空）
os.rmdir(comfyui_output_dir)
```

- ComfyUI 输出目录：`~/ai/ComfyUI/output/`
- 最终归档：`~/.openclaw/workspace/output/YYYYMMDD/audio/`

## 模型分配

**优先级**：NVIDIA API 免费模型优先，长时间无响应才切 deepseek/deepseek-v4-flash

| Agent | 模型 | 说明 |
|-------|------|------|
| 墨白 ✍️ | `custom-integrate-api-nvidia-com/deepseek-ai/deepseek-v4-pro` | NVIDIA 免费 |
| 和弦 🎵 | `custom-integrate-api-nvidia-com/deepseek-ai/deepseek-v4-pro` | NVIDIA 免费 |
| 引擎 ⚙️ | `deepseek/deepseek-v4-flash` | 默认付费 API |

## 引擎 ⚙️ 操作规范

每次 spawn 引擎时，**必须在任务模板中包含**：
1. 先让他读 `tools/comfyui操作手册.md`
2. 用 `bash /home/qsh/ai/run_comfyui.sh` 启动 ComfyUI
3. 歌词不能带歌名行
4. 不能修改 `clip` 等节点引用字段

详细操作手册：`tools/comfyui操作手册.md`

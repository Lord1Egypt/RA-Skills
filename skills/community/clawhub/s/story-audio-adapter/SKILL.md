---
name: story-audio-adapter
description: >
  Use when: 用户希望把带有 `[角色]文本` 标记的小说、剧本、故事台词转成多角色有声作品时触发。
  适用于旁白、人物对白、角色 ID 已标注清楚的文本内容。Skill 会读取可编辑音色库，分析角色数量与性格特征，匹配最接近的音色，逐段调用 SenseAudio TTS，最后拼接为完整音频并以 `MEDIA:./...` 形式返回给 Feishu/OpenClaw。
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["python3"],"env":["SENSEAUDIO_API_KEY"]},"primaryEnv":"SENSEAUDIO_API_KEY"}}
---

# Story Audio Adapter

你是“小说/故事有声化”执行助手。这个 Skill 只负责把结构化故事文本变成完整音频作品，并输出适合 Feishu 渠道消费的媒体引用。

## 何时使用

当用户有这些意图时触发：

- “把这段小说做成有声版”
- “按角色配音这段故事”
- “旁白和角色对白分别配不同音色”
- “根据 `[旁白]` `[男主角1]` 这种标记生成完整音频”
- “输出可直接发到 Feishu 的故事音频”

如果用户只是讨论音色设计、Prompt 写法或 API 参数含义，不要直接执行脚本。

## 最高优先级规则

1. 必须优先读取 `references/voice_library.json`，把它视为当前唯一有效音色库。
2. 音色库必须保持“用户可编辑”，不要把可配音色硬编码在回复里替代配置文件。
3. 输入文本默认使用 `[角色名]内容` 结构；未标注角色的纯文本默认视为 `旁白`。
4. 角色分析必须先统计角色数量，再总结每个角色的人设、年龄感、情绪气质、叙述功能。
5. 音色匹配必须基于文本证据和音色描述，不得随意拍脑袋指定。
6. TTS 必须调用 SenseAudio 官方接口，不得切到本地系统音色或其他第三方服务。
7. 最终完整作品默认输出 `wav`，因为本 Skill 依赖 Python 原生能力稳定拼接分段音频。
8. 每段文本单独生成音频，再按原文顺序拼接；不要把整篇文本直接扔给单一音色。
9. 当脚本输出 `MEDIA:./...` 时，最终回复必须包含这行原样内容，供 OpenClaw/Feishu 解析媒体。
10. 如果 `SENSEAUDIO_API_KEY` 未配置，必须明确报错并停止，不要伪造成功结果。
11. 如果文本或分段超出接口限制，要明确提示用户缩短文本或拆分内容，不要静默截断。
12. 当角色数多于音色库可区分能力时，优先保证主角色和旁白的音色区分，次要角色可以复用近似音色，但要在分析结果中说明。

## 目录约定

- `scripts/main.py`：统一 CLI
- `references/voice_library.json`：用户可编辑音色库
- `references/role_analysis_prompt.md`：角色分析与音色匹配提示词
- `outputs/`：默认输出目录

## 默认音色库

初始音色库包含这些 voice：

- `child_0001_a`：开心的可爱萌娃
- `child_0001_b`：平稳的可爱萌娃
- `male_0004_a`：儒雅道长
- `male_0018_a`：沙哑青年

用户后续可以直接编辑 `references/voice_library.json` 增删音色，不需要改脚本。

## 标准执行流程

### 步骤 1：检查配置

```bash
python3 ./scripts/main.py auth-check
```

如果缺少 `SENSEAUDIO_API_KEY`，直接提示用户设置：

```bash
export SENSEAUDIO_API_KEY="YOUR_API_KEY"
export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"
```

### 步骤 2：查看当前音色库

```bash
python3 ./scripts/main.py list-voices
```

如需扩展音色，优先让用户编辑 `references/voice_library.json`。

### 步骤 3：解析文本并做角色分析

读取：

- `references/role_analysis_prompt.md`
- 用户提供的故事文本
- `references/voice_library.json`

先输出：

- 角色列表
- 每个角色的性格/语气/叙述职责总结
- 为何匹配到某个音色

如需脚本生成可落盘的分析结果：

```bash
python3 ./scripts/main.py analyze --text-file "/path/to/story.txt"
```

### 步骤 4：按角色逐段合成

```bash
python3 ./scripts/main.py synthesize-story \
  --text-file "/path/to/story.txt"
```

这一步会：

- 解析 `[角色]内容`
- 自动生成角色到音色的映射
- 为每段内容单独调用 TTS
- 保存分段音频和元数据
- 拼接成完整 `wav`

### 步骤 5：返回 Feishu 媒体

脚本完成后会输出：

- 角色分析 JSON
- 音色映射 JSON
- 分段清单 JSON
- 完整作品路径
- 一行 `MEDIA:./...`

最终回复里必须保留 `MEDIA:./...` 这一行，不要只转述文件路径。

## 推荐工作方式

处理真实请求时按下面顺序：

1. 读取音色库
2. 解析文本结构
3. 读取 `references/role_analysis_prompt.md`
4. 先给出角色分析和音色匹配
5. 调用 `scripts/main.py synthesize-story`
6. 回复用户：
   - 角色与音色匹配结果
   - `MEDIA:./...`
   - 如需要，再附完整作品路径与分析文件路径

## 输入格式约定

推荐输入格式：

```text
[旁白]夜色很深，街道上只剩风声。
[男主角1]我知道你一定会来。
[女主角1]你还是和以前一样，太自信了。
```

兼容规则：

- 支持多行文本
- 支持同一角色多次出现
- 空行会被忽略
- 未带 `[角色]` 的行会并入 `旁白`

## 失败处理

- `401/403`：API Key 无效或无权限
- `429`：请求过频，提示稍后重试
- 单段文本过长：提示用户拆段
- 音色库为空：提示用户先编辑 `references/voice_library.json`
- 完整作品未生成 `MEDIA:./...`：至少返回本地路径并说明原因

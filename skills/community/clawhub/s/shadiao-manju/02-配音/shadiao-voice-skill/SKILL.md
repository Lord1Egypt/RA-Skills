---
name: shadiao-voice-skill
displayName: 沙雕配音
version: 0.1.0
description: >
  把沙雕剧本的每一行台词，变成一条可直接进工程的配音音频 + 时长表。
  一个角色固定一个音色，全剧不换。草稿用 edge-tts（秒级、免费）；
  成品用 IndexTTS-2.5 零样本克隆 + 八维情绪（M1 可跑，批量过夜）。
  音色来源默认映射到 23-视频制作/10-音色制作/抖音 的 21 条参考，
  但受合规闸门约束：默认只做听感参考，不直接克隆可识别真人。
  触发词：沙雕配音、角色配音、选音色、配音表、逐句配音、批量配音、
  情绪配音、IndexTTS、edge-tts、抖音音色。
---

# 沙雕配音

> 一句话：**一行台词 = 一条音频 = 一条字幕。** 音频时长就是这条字幕和动作的时间轴。

## 〇、输入与输出

| | 内容 |
|---|---|
| 输入 | `01-剧本/剧本.json`（必须带 `lines[]`、`characters[].voice`） |
| 输出 | `02-配音/第NN集/S001.mp3 ...` + `02-配音/第NN集/配音表.json` |
| 引擎 | `edge`（草稿，秒级）/ `clone`（成品，IndexTTS）/ `say`（离线兜底） |

## 一、工作流

### 1. 分配音色（一角色一音色）

读 `references/音色映射.md`，把剧本里 `characters[].voice` 的名字落到一个预设上。

规则：

1. 同性别角色不要共用同一音色；至少拉开音高 / 语速。
2. 旁白单独一个音色，不和角色共用。
3. 全剧不换；换季也不换。
4. 名字查不到 → 停下问用户，不要自己编。

### 2. 选引擎

| 场景 | 引擎 | 命令 |
|---|---|---|
| 改稿期、当天要出片 | `edge` | `--engine edge` |
| 定稿、要情绪和「演」 | `clone` | `--engine clone --alpha 0.6 --clone-consent` |
| 断网 / edge 挂 | `say` | `--engine say` |

**推荐节奏**：edge 出草稿 → 改到满意 → clone 过夜出成品 → 第二天直接进 04。

> `clone` 需要本地装好 IndexTTS 工具链，并设 `SHADIAO_TOOLCHAIN` 指到工具链根目录。
> 本仓库不含模型、参考音频和引擎；只用 edge 不影响其余流程。

**clone 的两道闸门**（脚本强制执行，不是口头约定）：

1. `--clone-consent`：声明已获得参考音频声音权利人的授权。不加就直接报错退出，不会合成。
2. `--allow-unverified`：`voices.json` 里指向 `10-音色制作/抖音/` 的参考音频属于「未登记授权」，默认被拦截；
   只在内部听感测试时加这个参数，产物不得对外发布，`配音表.json` 会把它标成 `license: unverified`。

### 3. 跑批量

```bash
python3 02-配音/shadiao-voice-skill/scripts/tts_batch.py \
  --project <剧名> --season 1 --episode 1 --engine edge
```

> ⚠️ **数据边界**：`edge` 引擎调用 edge-tts，会把每一句台词文本发到微软在线语音服务（所以它要联网）。
> 未公开剧本、客户稿件、带真实姓名/电话的内容，先跟剧方确认能不能外发；不能就用 `--engine say`（macOS 本地）
> 或 `--engine clone`（本地 IndexTTS，模型完全跑在本机）。

- 默认读 `99-项目/<剧名>/第NN季/01-剧本/剧本.json`
- 产物落在 `99-项目/<剧名>/第NN季/02-配音/第NN集/`
- 每句一条，命名为 `S{seq:03d}.mp3`
- 同时写 `02-配音/第NN集/配音表.json`

### 4. 听一遍（必做）

- 音色对不对人：老板不能听起来像大学生。
- 断句对不对：有没有一口气读不完的。
- 时长对不对：60 秒目标，配音总时长控制在 45–55 秒（留气口和音效）。
- 情绪对不对：该嘲的嘲，该怂的怂。

不满意就改剧本 / 换音色 / 调 `--alpha`，**不要手工剪音频**。

## 二、产物格式

`配音表.json`：

```json
{
  "project": "周一打工人",
  "season": 1,
  "episode": 1,
  "engine": "edge",
  "totalDuration": 51.2,
  "lines": [
    {
      "seq": 1,
      "speaker": "旁白",
      "type": "narration",
      "text": "周一早上八点，阿强提前一小时到公司。",
      "emotion": "平静",
      "sfx": "闹钟",
      "scene": "S1",
      "voice": "旁白-死鱼眼",
      "audio": "02-配音/第01集/S001.mp3",
      "duration": 3800,
      "hash": "a1b2c3d4e5f6"
    }
  ]
}
```

- `duration` 单位 **毫秒**，下游 `.anime` 的 `ttsConfig.duration` 直接用它。
- `audio` 是相对季目录的路径。
- `hash` 用于 04 生成缓存文件名，改了台词 hash 就变。

## 三、音色与情绪

| 参考 | 用途 |
|---|---|
| `references/音色映射.md` | 21 条抖音参考 → edge 预设 → IndexTTS 参考路径 |
| `references/情绪表.md` | 基础情绪 + 沙雕扩展情绪的映射 |
| `references/声音合规.md` | 一票否决红线 + 留证要求 |

## 四、质量门

- [ ] 每个角色都有音色，且全剧唯一
- [ ] 每句都有音频，没有空文件 / 0 字节
- [ ] `duration` 全部 > 300ms
- [ ] 配音总时长在目标 ±20% 内
- [ ] 没有一句超过 8 秒（超了就拆台词）
- [ ] 听感：同一角色跨句音色一致
- [ ] 合规：没有克隆可识别真人；抖音参考只做听感，正式成品已换成有授权的参考音频

## 五、故障

| 症状 | 处理 |
|---|---|
| `edge-tts` 403 | `pip install -U edge-tts` |
| 报「音色「X」不在 voices.json 里」 | 剧本 `characters[].voice` 写错了；改成 `voices.json` 里的预设名，或加 `--allow-voice-fallback` 按性别兜底（会在 stderr 打警告） |
| 某句没生成 | 看 `配音表.json` 里有没有缺项；单独重跑 `--only 3` |
| IndexTTS 报 device 错 | 加 `--device mps`，或 `--device cpu`（慢但稳） |
| 生成太慢 | 先 edge 出全片，成品只重跑改动句 |
| 音量忽大忽小 | clone 已做 -16 LUFS 归一；edge 未做，交给 05 的 ffmpeg 统一 |

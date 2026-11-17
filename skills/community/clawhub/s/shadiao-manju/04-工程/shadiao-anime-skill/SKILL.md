---
name: shadiao-anime-skill
displayName: 沙雕工程
version: 0.2.0
description: >
  把「剧本.json + 配音表.json + 素材索引.json」合成一个可直接在「沙雕动画小助手」里打开的 .anime 工程：
  自动建角色模板、演员、场景、脚本块，回填音频路径与时长，挂相机跟随动作，并做结构校验。
  纯 Node，无第三方依赖；schema 不兼容会直接报错。
  触发词：.anime、沙雕工程、沙雕 .anime、build anime、回填 audioPath、ttsConfig、动作白名单。
---

# 沙雕工程

> 一句话：**把三份 JSON 拼成 app 能打开的一个文件。** 你不需要在 app 里手动搭场景。

## 〇、输入 / 输出

| | 路径 |
|---|---|
| 输入 1 | `01-剧本/剧本.json` |
| 输入 2 | `02-配音/第NN集/配音表.json` |
| 输入 3 | `03-素材/素材索引.json` |
| 输出 1 | `04-工程/<剧名>.anime` |
| 输出 2 | `04-工程/<剧名>_cache/{tts,assets}/` |
| 输出 3 | `04-工程/校验报告.md` |

## 一、工作流

### 1. 确认三份输入齐全

```bash
ls 99-项目/<剧名>/第01季/01-剧本/剧本.json
ls 99-项目/<剧名>/第01季/02-配音/第01集/配音表.json
ls 99-项目/<剧名>/第01季/03-素材/素材索引.json
```

缺哪个回哪一步，不要硬生成。

### 2. 生成

```bash
node 04-工程/shadiao-anime-skill/scripts/build_anime.mjs \
  --project <剧名> --season 1 --episode 1
```

可选参数：

| 参数 | 默认 | 说明 |
|---|---|---|
| `--width` / `--height` | 按 `aspectRatio`，默认 1080×1920 | 画布 |
| `--fps` | 30 | 帧率 |
| `--script` | `01-剧本/剧本.json` | 换剧本 |
| `--voice` | `02-配音/第NN集/配音表.json` | 换配音表 |
| `--assets` | `03-素材/素材索引.json` | 换素材索引 |
| `--out` | `04-工程/<剧名>.anime` | 换输出路径 |

### 3. 校验

```bash
node 04-工程/shadiao-anime-skill/scripts/validate_anime.mjs \
  99-项目/<剧名>/第01季/04-工程/<剧名>.anime \
  --report 99-项目/<剧名>/第01季/04-工程/校验报告.md
```

有 error 必须修；warning 逐条看。

### 4. 交给 05

打开 `04-工程` 文件夹 → 打开 `.anime` → 预览 → 导出。

## 二、生成规则

| 输入 | 变成 |
|---|---|
| `script.characters[]` | `compositeCharacters[]` + `actors[]` |
| `script.scenes[]` | `episodes[0].scenes[]`（按地点） |
| `script.lines[]` | `scene.script[]`（对白 / 旁白块） |
| `配音表.lines[].duration` | `ttsConfig.duration`（毫秒） |
| `配音表.lines[].audio` | 拷贝到 `<剧名>_cache/tts/<hash>.mp3` → `ttsConfig.audioPath` |
| `素材索引.characters[].body` | 拷贝到 `<剧名>_cache/assets/characters/<名>/body.png` |
| `素材索引.backgrounds[]` | 拷贝并登记为 `assets.backgrounds` |
| 对白 speaker | `camera_follow` 跟随该角色根对象 |
| 角色 `exp_*.png` | `anime.expressions` + 场景 `expression` 对象（脸部叠加） |
| 台词 `emotion` | `set_material` 动作，切到对应表情 |
| `scenes[].props` | 场景 `prop` 对象（左右分布，摆在角色后） |

**已做**（v0.2）：

- 表情叠加：每个角色 8 张 `exp_*.png` → `anime.expressions` + 场景里的 `expression` 对象
- 情绪切表情：每句按 `emotion` 生成 `set_material` 动作，播放到该句时切表情
- 道具摆位：`scenes[].props` 里的道具按左右分布放进场景（zIndex 低于角色）

**不做**（暂缓）：

- 不做角色肢体说话动画（没有 AnimationDefinition）
- 不做 BGM / 音效轨（`sfx` 只写进 `productionNote`）

## 二点五、分镜 / 走位（v0.5）

`剧本.json` 的 `scenes[]` 支持镜头级参数：

```json
{
  "id": "S1B",
  "title": "工位-走进",
  "background": "工位",
  "actors": ["阿强", "老板"],
  "camera": { "x": 0.5, "y": 0.55, "zoom": 1.0 },
  "positions": { "阿强": 0.12, "老板": 0.78 },
  "poses": { "老板": "睡觉" }
}
```

- `camera`：x/y 是 0–1 归一化视口中心，`zoom` 是镜头倍数（1.45 = 近景）
- `positions`：角色在画面里的 x（0–1），不写就用默认双人站位
- `props`：`["咖啡"]` 或 `[{ "name": "咖啡", "x": 0.33, "y": 0.60, "scale": 0.10 }]`
  （`scale` 是原图倍数；不写按屏高 14% 自动算）
- `poses`：进场姿态，且**整场锁死**（`坐` / `睡觉` / `走路` / 8 表情），需要 `full_*.png`；
  锁死后该角色的表情不再被每句 `emotion` 覆盖（坐着的人不会突然站起来）

`lines[]` 支持单行动作：

```json
{
  "seq": 4,
  "text": "老板？！",
  "pose": "走路",
  "move": { "x": 0.50 }
}
```

- `pose`：这一句切到哪个整身姿态（优先级高于 `emotion`）
- `move`：从当前位置 tween 到目标 x（0–1），用 `tween_transform` 实现走位

## 二点七、说话嘴动（v0.6）

角色有 `03-素材/角色/<名>/mouth.json` + `mouth.png` 时，build 会自动给每个角色加一个
**场景级**「嘴」图层（`type: prop`，`alias: mouth`，`zIndex: 30`），并挂一条 `talk` 动画：

```js
animations: {
  talk: {
    type: 'track', name: 'talk', loop: true, timingMode: 'tts_speech',
    tracks: [{ trackType: 'transform', duration: 400, keyframes: [
      { time: 0, scaleY: 1 }, { time: 0.14, scaleY: 4.4 }, { time: 0.3, scaleY: 1 },
      { time: 0.46, scaleY: 3.2 }, { time: 0.6, scaleY: 1.05 }, { time: 0.78, scaleY: 4 }, { time: 1, scaleY: 1 },
    ]}],
  },
}
```

每句台词（说话人）自动生成三个动作：

```js
set_transform({ x, y, scaleX, scaleY })   // 切到当前表情的嘴位
set_visual({ visible: true })             // 该表情有大张嘴就不叠，visible:false
set_anim([{ animName: 'talk', timingMode: 'tts_speech' }])  // 有声才动
```

**两个坑（已经踩过）**：
1. `animations` 必须是 `{ talk: {...} }` 这种**以名字为 key 的记录**，不是定义本身，否则查不到 → 不动。
2. 嘴**不要挂在角色 composite 里面**。复合容器的子对象坐标在导出时被转换过，
   动画一播放 `baseX/baseY` 会把嘴写到画外（实测 -892 / -2825）。
   放场景根上，坐标才和 `set_transform` 对得上。

## 二点九、待机微动（v0.9）

角色站着说话最容易"像一张图"。build 现在给每个角色根节点挂一条 `idle` 动画：

```js
animations: { idle: {
  type:'track', name:'idle', loop:true, timingMode:'continuous',
  tracks: [{ trackType:'effect', effectParams:{ type:'breathe', intensity:0.013, speed:0.85 } }]
}}
```

每个场景第一个 block 自动下发一次：

```js
set_anim({ animName: 'idle', autoStopOnBlockEnd: false, loop: true })
```

- `autoStopOnBlockEnd: false` 是关键，否则第一句说完就不呼吸了
- `breathe` 是引擎自带特效（整身 scale 微起伏），不用我们自己算关键帧
- 想要"点头"可以再加一条 `shake`（axis: 'y', range: 2）；但别和 `breathe` 同时开太多，容易抖

## 三、关键约束

1. **`meta.version` 必须是 `2.x`**，否则 app 直接拒绝打开。
2. **`generatedFrom` 必须和实际一致**：`text / voiceId / speed / instanceId`。不一致 → app 认为音频过期 → 尝试调 TTS → 没 Provider 就报错。
3. **角色必须有 `body.png`**；没有就跳过该角色，对白会降级成旁白。
4. **场景必须有背景**；没有就用纯色底（会有 warning）。
5. **音频路径相对 `.anime` 所在目录**，统一用 `<剧名>_cache/tts/`。
6. **id 全局唯一**；每次生成都会重新生成 id，不要手改后混用。

## 四、常见问题

| 症状 | 原因 | 处理 |
|---|---|---|
| `找不到配音表` | 还没跑 02 | 先跑 `tts_batch.py` |
| `找不到素材索引` | 还没跑 03 | 先跑 `make_index.py` |
| `没有任何可用角色` | 角色目录/body 缺失 | 检查 `03-素材/角色/<名>/body.png` |
| 打开工程提示版本错误 | `meta.version` 不是 2.x | 不要手改；用脚本重新生成 |
| 预览没声音 | 音频没拷进 `_cache/tts/` | 重跑 `build_anime.mjs` |
| 声音和台词对不上 | `generatedFrom` 不一致 | 重跑 02 + 04，不要手改 |
| 角色叠在一起 | 场景角色数 > 3 | 拆场，或手调 `x` |

## 五、v0.2 已完成 / v0.3 计划

**v0.2 已完成**：

- 表情叠加：`ExpressionObject` + 8 张表情，按 `emotion` 用 `set_material` 切换。
- 旁白也切表情：跟随最近说话的角色；没有角色时用第一个角色。
- 道具摆位：`scenes[].props` 自动放进场景。

**v0.3 计划**：

- 道具互动：按 `productionNote` 让道具被拿起 / 拍桌。
- 肢体说话动画：支持 `animations` 定义后自动 `set_anim`。
- 反应镜头：关键句切听者。
- 音效轨：`sfx` 自动挂 `set_audio`。

# .anime 工程结构（v0.1）

> 只记录本 skill 会写、会读、会校验的字段。完整 schema 以 app 源码 `src/types/` 为准。

## 一、顶层

```json
{
  "meta": { "name": "周一打工人", "resolution": { "w": 1080, "h": 1920 }, "fps": 30, "version": "2.0.0" },
  "assets": { "backgrounds": [], "props": [], "sounds": [], "musics": [] },
  "expressions": {},
  "actors": [],
  "narrator": { "voice": { "voiceId": 101026, "speed": 0 } },
  "sceneTemplates": [],
  "compositeCharacters": [],
  "customPresetAnimations": [],
  "episodes": []
}
```

**版本**：`meta.version` 主版本必须是 `2`。app 打开时会拒绝 `1.x` 和 `3.x`。

## 二、resources

### backgrounds / props

```json
{ "id": "bgasset_x", "name": "工位", "type": "static", "url": "<name>_cache/assets/backgrounds/工位.png", "createdAt": 0 }
```

`url` 相对 `.anime` 所在目录。

### compositeCharacters（角色模板）

```json
{
  "id": "char_x",
  "name": "阿强",
  "gender": "male",
  "objects": [
    {
      "id": "cc_root_x", "type": "composite", "name": "阿强", "alias": "阿强", "refId": "",
      "x": 0, "y": 0, "width": 1024, "height": 1536,
      "scaleX": 1, "scaleY": 1, "rotation": 0, "alpha": 1, "flipX": false,
      "zIndex": 10, "visible": true, "spawned": true,
      "childIds": ["cc_img_x"], "compositeLocked": true, "compositeMode": "entity",
      "renderChain": ["cc_img_x"],
      "extraInfo": { "kind": "character", "characterId": "char_x" }
    },
    {
      "id": "cc_img_x", "type": "symbol", "name": "阿强_body", "alias": "body", "refId": "",
      "parentId": "cc_root_x", "x": 0, "y": 0, "width": 1024, "height": 1536,
      "scaleX": 1, "scaleY": 1, "rotation": 0, "alpha": 1, "flipX": false,
      "zIndex": 10, "visible": true, "spawned": true,
      "materials": [{ "id": "mat_x", "name": "body", "type": "static", "url": "<name>_cache/assets/characters/阿强/body.png" }],
      "currentMaterialId": "mat_x"
    }
  ],
  "renderChain": ["cc_root_x"],
  "rootCompositeId": "cc_root_x"
}
```

### actors

```json
{ "id": "actor_x", "name": "阿强", "characterId": "char_x", "voice": { "voiceId": 502005, "speed": 1 } }
```

## 二点五、expressions（表情，v0.2）

`anime.expressions` 是 `Record<表情ID, Expression>`。每个角色 8 个，id 由生成脚本随机生成。

```json
{
  "expr_x": {
    "id": "expr_x",
    "name": "阿强_开心",
    "tags": ["阿强", "开心"],
    "gender": "male",
    "defaultFrame": { "id": "frame_x", "url": "<name>_cache/assets/characters/阿强/exp_开心.png" },
    "speakingFrames": [],
    "anchor": { "x": 0.5, "y": 0.5 },
    "speakingFps": 12,
    "speakingLoop": true,
    "flipHorizontal": false,
    "defaultScale": 0.6,
    "createdAt": 0
  }
}
```

场景里的 `expression` 对象：

```json
{
  "id": "obj_face_x",
  "type": "expression",
  "name": "阿强_face",
  "alias": "face",
  "refId": "expr_x",
  "defaultRefId": "expr_x",
  "parentId": "obj_actor_root_x",
  "x": 0,
  "y": -465.4,
  "width": 1024,
  "height": 1024,
  "scaleX": 1,
  "scaleY": 1,
  "rotation": 0,
  "alpha": 1,
  "flipX": false,
  "zIndex": 11,
  "visible": true,
  "spawned": true
}
```

- `x/y` 是**相对角色根**的偏移，按整身图的脸中心算：`y = (face.y - 0.5) * 整身图高`。
- `defaultScale` 控制表情图缩放；默认 `0.6`，让表情头部约等于整身图头部大小。
- 切表情用 `set_material`：

```json
{
  "id": "act_x",
  "target": "obj_face_x",
  "type": "set_material",
  "category": "point",
  "slotIndex": 0,
  "params": { "materialId": "expr_x" }
}
```

`SetMaterialHandler` 会同时写 `currentMaterialId` 和 `refId`，表情对象因此能响应。

## 三、episodes

```json
{
  "id": "episode_x",
  "episodeNumber": 1,
  "name": "周一打工人",
  "scenes": [],
  "bgmTracks": [],
  "duration": 45700,
  "createdAt": 0,
  "modifiedAt": 0,
  "version": "6.0"
}
```

## 三点五、分镜字段（v0.5）

`scenes[]` 可带 `camera` / `positions` / `poses`；`lines[]` 可带 `pose` / `move`。
build 脚本会转成：

- `setup.camera = { x: 0.5W, y: 0.55H, zoom: 1.45 }`
- 角色根 x = `positions[角色] * W`
- 进场 `currentMaterialId` = `poses[角色]` 对应的整身 material
- `pose` → `set_material`（优先于 emotion）
- `move` → `tween_transform`（target = 角色根，params.x = 目标 x）

## 四、scene

```json
{
  "id": "scene_x",
  "type": "scene_container",
  "title": "工位-早晨",
  "setup": {
    "camera": { "x": 0, "y": 0, "width": 1080, "height": 1920, "zoom": 1 },
    "objects": [],
    "renderChain": []
  },
  "script": []
}
```

`setup.objects` 里至少要有：背景（`type: "background"`）、角色根（`type: "composite"`，带 `extraInfo.actorId`）、环境光（`type: "light"`）。

## 五、scriptBlock

```json
{
  "id": "blk_x",
  "type": "dialogue",
  "text": "只要我够早，老板就抓不到我摸鱼。",
  "speed": 1,
  "instanceId": "obj_actor_root_x",
  "ttsConfig": {
    "duration": 4180,
    "audioPath": "<name>_cache/tts/a1b2c3d4.mp3",
    "voiceId": 502005,
    "generatedFrom": {
      "instanceId": "obj_actor_root_x",
      "text": "只要我够早，老板就抓不到我摸鱼。",
      "voiceId": 502005,
      "speed": 1,
      "volume": 1
    }
  },
  "actions": [],
  "productionNote": { "seq": 2, "emotion": "得意", "sfx": "", "sceneTitle": "工位-早晨" }
}
```

**`generatedFrom` 必须和实际一致**，否则 app 会认为音频过期，尝试重新调 TTS：

- `text` = block.text
- `voiceId` = 演员 / 旁白的 `voiceId`
- `speed` = 演员 / 旁白的 `speed`
- `instanceId` = 对话块的 `instanceId`（旁白不填）

## 六、缓存目录

app 自己生成语音时写入：

```
<anime 文件名去掉扩展名>_cache/tts/<hash>.mp3
```

本 skill 沿用同一命名，避免出现两份缓存：

```
04-工程/周一打工人.anime
04-工程/周一打工人_cache/tts/*.mp3
04-工程/周一打工人_cache/assets/characters/阿强/body.png
```

## 七、校验

```bash
node 04-工程/shadiao-anime-skill/scripts/validate_anime.mjs <path>
```

会检查：版本、id 重复、refId、角色模板、演员绑定、场景对象、音频文件、时长、对话实例、跟随目标。

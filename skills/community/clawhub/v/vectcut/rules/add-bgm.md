---
name: add-bgm
description: "为口播草稿自动添加背景音乐：先用 query-draft 获取草稿总时长，再用 get_duration 获取 BGM 时长，最后循环调用 add_audio 铺满全片。用户提到“加BGM/背景音乐/口播收尾配乐/自动铺满音频”时必须使用本技能。"
---

# Add BGM Skill

用于给口播类草稿在最后一步自动补背景音乐。核心是“查总时长 -> 查音频时长 -> 循环铺轨道”，避免手工反复添加。

官方接口文档：
- query_script: https://docs.vectcut.com/386764616e0
- get_duration: https://docs.vectcut.com/328289318e0
- add_audio: https://docs.vectcut.com/321196190e0

## 何时使用

- 用户要求“加背景音乐 / 加 BGM”
- 用户希望把一段 BGM 自动铺满整条口播
- 用户要在已有 `draft_id` 基础上追加音频轨道

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY` 是否存在且有效
- 缺失、为空或疑似失效时，先调用 `vectcut-login`

## BGM 来源

- 默认从技能内置白名单读取：`<skill-path>/references/bgms.json`
- 若用户指定 `bgm_url`，优先使用该链接
- 若未指定：
  - 默认使用白名单第一条
  - 也可通过 `bgm_index` 选择
  - `random_bgm=true` 时随机选择

## 执行流程（固定）

1. 调用 `query_script` 获取草稿信息，读取 `draft.duration`（微秒）
2. 将草稿时长转换为秒：`draft_duration_seconds = draft.duration / 1_000_000`
3. 调用 `get_duration` 查询选中 BGM 的时长（秒）
4. 按时间线循环调用 `add_audio`：
   - 每段 `start=0`
   - 每段 `target_start=当前累计位置`
   - 每段 `end=min(bgm_duration, 剩余时长)`
   - 直到覆盖完整草稿时长
5. 返回最终 `draft_id`、`draft_url` 与每段素材写入结果

## 执行方式

准备请求 JSON，例如：

```json
{
  "draft_id": "dfd_xxx",
  "bgm_index": 0,
  "track_name": "audio_bgm"
}
```

执行脚本：

```bash
python <skill-path>/scripts/add_bgm.py \
  "/tmp/add_bgm_payload.json" \
  --output "./add_bgm_result.json"
```

## 输入说明

- 必填：
  - `draft_id`
- 常用可选：
  - `bgm_url`：直接指定背景音乐链接
  - `bgm_index`：从白名单按索引选
  - `random_bgm`：是否随机选白名单
  - `track_name`：默认 `audio_bgm`
  - `volume`：单位 dB，可选；不传时不主动设置，使用平台默认音量
  - `speed`：默认 `1.0`
  - `fade_in_duration` / `fade_out_duratioin`
  - `bgm_list_path`：自定义白名单文件路径（推荐 JSON 格式：`{"bgms":[...]}`）

## 输出结果

默认输出 `add_bgm_result.json`，核心字段：
- `meta.draft_duration_seconds`
- `meta.bgm_duration_seconds`
- `meta.segment_count`
- `meta.selected_bgm_url`
- `result.draft_id`
- `result.draft_url`
- `result.added_segments[]`

## 失败处理建议

- `VECTCUT_API_KEY` 缺失：先调用 `vectcut-login`
- `draft_id` 无效：先用 `query-draft` 验证草稿可访问
- 白名单无可用 URL：检查 `references/bgms.json` 或自定义 `bgm_list_path` 格式
- `get_duration` 返回异常：检查 BGM 链接是否公网可访问
- `add_audio` 失败：检查 `track_name/volume/speed` 参数合法性

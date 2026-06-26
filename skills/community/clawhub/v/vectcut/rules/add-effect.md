---
name: add-effect
description: "为视频片段添加场景特效或人物特效，提升重点表达与画面丰富度。用户提到“加特效”“开头抓眼球”“强调某个画面细节”“口播悬疑氛围”“人物惊讶效果”时必须使用本技能。"
---

# Add Effect Skill

用于调用 VectCut `add_effect` 接口给视频草稿添加特效，适合以下场景：
- 开头 1~3 秒抓眼球
- 口播重点句强化
- 悬疑/疑问语气氛围塑造
- 电商带货细节放大、惊讶反应

官方接口文档：
- https://docs.vectcut.com/321244826e0
- https://docs.vectcut.com/321245379e0
- https://docs.vectcut.com/321245348e0

## 何时使用

- 用户说“给这段加特效”
- 用户希望“重点处理某个片段”
- 用户想让开场更有冲击力
- 用户要在口播里做“悬疑/疑问/反向例子”氛围
- 用户想强调商品细节、突出惊讶或灵感瞬间

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY`
- 缺失或疑似失效时，先调用 `vectcut-login`

## 常用特效推荐（优先）

- 场景特效 `聚光灯`：口播开头、悬疑、疑问
- 场景特效 `暗角`：口播开头、悬疑、疑问
- 场景特效 `放大镜`：电商细节强调
- 场景特效 `模糊`：口播画中画背景、反向例子
- 人物特效 `大头`：带货吃惊反应
- 人物特效 `灵机一动`：重点表达、灵感瞬间

## 可设置参数

`add_effect` 常用参数：
- `effect_type`：特效名称（必填）
- `start`：开始时间（秒，默认 `0.0`）
- `end`：结束时间（秒，默认 `3.0`）
- `draft_id`：草稿 ID（可选）
- `track_name`：特效轨道名（默认 `effect_01`）
- `params`：特效参数数组（可选，数字列表；未传按系统默认）

说明：
- `params` 的含义因特效类型而异，不同特效支持的参数个数和范围不同。
- 若不确定 `params`，建议先不传，使用特效默认参数更稳妥。

## 执行方式

先准备请求 JSON，例如：

```json
{
  "draft_id": "dfd_xxx",
  "effect_type": "聚光灯",
  "start": 0.0,
  "end": 2.8,
  "track_name": "effect_hook",
  "effect_category": "scene"
}
```

执行：

```bash
python <skill-path>/scripts/add_effect.py \
  "/tmp/add_effect_payload.json" \
  --output "./add_effect_result.json"
```

## 查询可用特效（官方列表）

查询场景特效：

```bash
python <skill-path>/scripts/add_effect.py --list-scene
```

查询人物特效：

```bash
python <skill-path>/scripts/add_effect.py --list-character
```

查询全部特效：

```bash
python <skill-path>/scripts/add_effect.py --list-all
```

## 输入说明

- 必填：
  - `effect_type`
- 可选：
  - `draft_id`
  - `start`（默认 `0.0`）
  - `end`（默认 `3.0`）
  - `track_name`（默认 `effect_01`）
  - `params`（数字数组）
  - `width`（默认 `1080`）
  - `height`（默认 `1920`）
  - `effect_category`（`scene` / `character` / `auto`，默认 `auto`，仅用于校验与推荐）

## 输出结果

默认输出 `add_effect_result.json`，核心字段：
- `meta.endpoint`
- `meta.effect_type`
- `meta.resolved_category`
- `request_payload`
- `result.raw_response`

## 失败处理建议

- `effect_type` 不存在：先用 `--list-scene` / `--list-character` 查询后重试
- `end <= start`：修正时间区间
- `params` 不兼容：去掉 `params` 先用默认值验证效果
- 鉴权失败：先执行 `vectcut-login`

# 自定义角色卡目录

把 `<slug>.json` 丢进本目录即可。`scripts/compile_prompt.py` 和 `scripts/validate_panel_plan.py`
会自动加载本目录下所有 `*.json`，按 `character_id` 或 `name` 匹配分镜里 `character_bible` 的角色，
并把该角色的 `hard_anchors` 补进 `must_keep`。

## 一条命令生成

```bash
python3 scripts/character_card.py init \
  --name 小陈 --id char_xiaochen \
  --hair "short black hair" --eyewear "round glasses" --build "slim" \
  --outfit "blue hoodie" \
  --out characters/cards/xiaochen.json
```

## 从已有分镜迁移

```bash
python3 scripts/character_card.py from-bible examples/four-panel-demo.json \
  --name 小陈 --out characters/cards/xiaochen.json
```

## 检查

```bash
python3 scripts/character_card.py check          # 检查本目录全部卡片
python3 scripts/character_card.py list           # 列出卡片与锚点
```

## 注意

- `hair` / `eyewear` / `build` / `face` 决定能锁定哪些锚点，至少填一项
- `outfit` / `accent_color` 刻意不做锚点，否则服装无法按场景替换
- 卡片只描述「角色是谁」，不描述画风；画风仍由 `presets/styles.json` 决定
- 同一角色可跨画风复用同一张卡

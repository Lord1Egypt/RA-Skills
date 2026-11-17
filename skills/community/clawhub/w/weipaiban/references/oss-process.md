# OSS 剪裁与压缩

站内 CDN 原图用 `x-oss-process` 按占位框裁切，并把长边压到 1080。AI 素材库返回的 `url` 已在 `svg-cdn.creatby.com`，同样走这个脚本，不必再上传。
**不要手写 process 字符串**，跑 `$SKILL_DIR/scripts/build_oss_src.py`（`SKILL_DIR` 见本技能 SKILL.md）。

## 命令

```bash
python3 "$SKILL_DIR/scripts/build_oss_src.py" \
  --url "https://svg-cdn.creatby.com/{hash}.png_large" \
  --natural-w 2048 --natural-h 2048 \
  --target-w 370 --target-h 208 \
  --crop-mode cover \
  --gravity center \
  --max-edge 1080
```

stdout JSON：`src`（给 `<image href>` 或 `<img src>`）、`originSrc`、`ossProcess`、`outputWidth` / `outputHeight`。

## 规则

| 项        | 行为                                               |
| --------- | -------------------------------------------------- | -------- | ------------------------ |
| 域名      | 仅 `svg-cdn.creatby.com`                           |
| 原图      | 去掉 `\_large                                      | \_middle | \_thumb`，去掉旧 process |
| `cover`   | 按占位宽高比切溢出，重力默认 center（封面/章节图） |
| `contain` | 不按目标比裁，只缩长边（完整主体）                 |
| resize    | `m_lfit`，长边 ≤1080，只缩小不放大                 |
| 顺序      | `image/crop,.../resize,m_lfit,w_*,h_*`             |
| 编码      | query 中 `/` 与 `,` 不编码                         |

HTML 写 `<image href>` 或 `<img src>` 时原样使用返回的 `src`。

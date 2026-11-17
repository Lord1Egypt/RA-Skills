# 配图

本技能负责选 tag、拉全量素材、分槽、OSS 处理和 manifest。分配规则只写在这里。

默认 `imageSource` 是 `ai-assets`：一个 tag 对应微排版能为该标签提供的全部已发布图。接口字段见 [api-ai-assets.md](api-ai-assets.md)。取图脚本：

```bash
python3 "$SKILL_DIR/scripts/fetch_ai_assets.py" --list-tags
python3 "$SKILL_DIR/scripts/fetch_ai_assets.py" \
  --tag "{tag}" \
  --out "{taskDir}/asset-pool.json"
```

`SKILL_DIR` 见本技能 SKILL.md。用户图片和点名生图的成品用本技能 `$SKILL_DIR/scripts/upload_images.py`，步骤见 [upload.md](upload.md)。OSS 用 `$SKILL_DIR/scripts/build_oss_src.py`，规则见 [oss-process.md](oss-process.md)。

库内 `url` 已在 `svg-cdn.creatby.com`。直接做 OSS，不重新上传，不跑 `rembg`。

## 任务目录

```text
/tmp/weipaiban-{taskId}/
├── meta.json
├── design-brief.md
├── design.json
├── asset-request.json
├── asset-pool.json
├── image-progress.json
├── asset-manifest.json
├── work.html
└── images/
```

状态流见 [task-contract.md](task-contract.md)。本阶段开始时写 `assets-processing`，manifest 完成后写 `assets-ready`。

## 选 tag

1. 用户已给出 tag：用这个字符串，即使不在推荐列表。
2. 否则先 `--list-tags`。在主题和标签之间找包含关系；去掉「节」「日」「季」后仍能对上的也算。多个命中时留更长的标签。长度相同则按分组优先级：节日、节气、行业、用途、风格、素材类型。
3. 没有命中时，列出最接近的几个标签让用户选。不要省略 tag 去拉全库。
4. 把这一个 tag 写进设计确认稿。用户改口就换 tag，然后重新拉池。

确认后只请求这一个 tag，并且翻到 `nextCursor` 为 `null`。脚本会翻完。

`items` 为空：停一次，请用户改 tag、提供图片、点名生图技能，或明确继续。继续则每个图片槽位用占位图。不要自动换第二个 tag。

## 槽位

`asset-request.json` 的作品级字段和每条槽位见 [task-contract.md](task-contract.md)。先按 format 列出槽位，再从池里填 `aiAssetId`。

把 `asset-pool.json` 的 `items` 分成三类，每张图只进一类：

| 类       | 条件                                       | 用在               |
| -------- | ------------------------------------------ | ------------------ |
| 循环背景 | `orientation` 为 `background`              | `role=background`  |
| 透明装饰 | `transparent` 为 true，且不是 `background` | `role=transparent` |
| 场景     | 其余                                       | `role=scene`       |

- 循环背景全篇只用一张。有多张时，先选标题或描述更贴近主题的；仍分不出就选高宽比更大的一张。`tileHeight = round(390 × height / width)`，用接口返回的宽高。竖图、`custom_portrait` 和其它比例都不能当作循环背景，也不把多张拼起来。没有 `background` 时，这个槽位占位。
- 透明装饰按槽位宽高比就近选，先用未用过的，不够再复用。没有透明图时，该槽位占位。
- 场景图同样按宽高比就近选，先未用后复用。`orientation` 只用来判断横竖和方图，不要求与槽位比例完全相同。
- 纯色上色板、按钮、分割和简单几何按 format 写 SVG，不进图片槽。format 允许在缺图时改回 SVG 的，就改 SVG，不占位硬上。

选中的库图写入进度 `pooled`，再做 OSS：

```bash
python3 "$SKILL_DIR/scripts/build_oss_src.py" \
  --url "{item.url}" \
  --natural-w {item.width} --natural-h {item.height} \
  --target-w {slot.width} --target-h {slot.height} \
  --crop-mode {contain|cover} \
  --gravity center \
  --max-edge {1080|2160}
```

`background` 和 `transparent` 用 `contain`。循环背景 `--max-edge 2160`，避免裁掉可衔接的边缘。场景图默认 `cover`，`--max-edge 1080`。HTML 原样使用返回的 `src`。循环背景在 manifest 里只留一条，重复次数写在布局里。

## 用户的图与点名的生图技能

只在用户明确要求时离开素材池。

- 用户给出本地文件或 URL：URL 先下到 `images/`，再 `--file` 上传。点名的槽位用这些文件，没点名的槽位仍用同一个 tag 的池。池为空时，剩下的槽位占位。
- 槽位 `needsTransparent` 且用户文件本身不透明时才去背，上传 `_nobg.png`，`cropMode=contain`：

```bash
rembg i -m birefnet-general \
  "{taskDir}/images/{assetId}.png" \
  "{taskDir}/images/{assetId}_nobg.png"
```

`rembg` 不在 PATH 时用 `python3 -m rembg`。模型固定 `birefnet-general`。人物发丝可换 `birefnet-portrait`。缺失或失败时停，请用户安装、改用原图，或该槽位占位。

- 用户点名生图技能：按技能名读取它的 `SKILL.md`，只为点名的槽位出图，再走上传和 OSS。该技能失败时，按它的说明重试一次；仍失败则该槽位占位。不要再启动第二个没有被点名的生图技能。

上传按 [upload.md](upload.md)。成功后记下 `src`、`width`、`height`，再跑 OSS。临时链不进 manifest，也不要交给上传脚本的 `--url`。

## 占位图

池里没有对应类型、用户要求占位，或上面的失败路径选择占位时，按槽位宽高比就近使用 [dialect.md](dialect.md) 的占位图 URL。manifest 写 `status=placeholder`、`source=placeholder`。不要另找图，也不要在本文件抄第二份 URL。

占位和失败都要出现在成品摘要里。

## 和 format 的关系

format 文档决定壳、层级和哪些元素必须是图。它不另写一套取图步骤。三层视差的循环背景、视差里的透明景物、滑动上色的镂空、选择其一的插画、场景转场的分镜，都用上面的三类分配。数量不够就复用同一张池内图。

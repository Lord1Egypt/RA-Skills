# 配图

本技能负责选一个 tag、拉全量素材、分槽、OSS 处理和 manifest。文章槽位怎么填，只写在这里。

默认 `imageSource` 是 `ai-assets`：一个 tag 对应微排版能为该标签提供的全部已发布图。接口字段见 [api-ai-assets.md](api-ai-assets.md)。取图脚本：

```bash
python3 "$SKILL_DIR/scripts/fetch_ai_assets.py" --list-tags
python3 "$SKILL_DIR/scripts/fetch_ai_assets.py" \
  --tag "{tag}" \
  --out "{taskDir}/asset-pool.json"
```

`SKILL_DIR` 见本技能 SKILL.md。库内 `url` 已在 `svg-cdn.creatby.com`。直接做 OSS，不重新上传，不跑 `rembg`。

OSS：`$SKILL_DIR/scripts/build_oss_src.py`，规则见 [oss-process.md](oss-process.md)。

用户图片和点名生图的成品才上传，用本技能 `$SKILL_DIR/scripts/upload_images.py`，步骤见 [upload.md](upload.md)。不另装上传技能。

主题里的 `styleAnchor` / `lightingHint` 只用于在池里挑更贴近的标题和描述。不要把它们交给生图技能，除非用户点名了那个技能。

## 任务目录

```text
/tmp/weipaiban-article-{taskId}/
├── meta.json
├── outline.md
├── asset-request.json
├── asset-pool.json
├── image-progress.json
├── asset-manifest.json
├── work.html
└── images/
```

`currentStep`：`outline` → `assets` → `assets-done` → `html` → `done`。

## 选 tag

1. 用户已给出 tag：用这个字符串，即使不在推荐列表。
2. 否则先 `--list-tags`。在主题和标签之间找包含关系；去掉「节」「日」「季」后仍能对上的也算。多个命中时留更长的标签。长度相同则按分组优先级：节日、节气、行业、用途、风格、素材类型。
3. 没有命中时，列出最接近的几个标签让用户选。不要省略 tag 去拉全库。
4. 把这一个 tag 写进大纲。用户改口就换 tag，然后重新拉池。

确认后只请求这一个 tag，并且翻到 `nextCursor` 为 `null`。脚本会翻完。

`items` 为空：停一次，请用户改 tag、提供图片、点名生图技能，或明确继续。继续则每个图片槽位用占位图。不要自动换第二个 tag，也不要自行改去生图。

## 清单

`asset-request.json` 顶层：`theme`、`tag`、`imageSource`（默认 `ai-assets`）、`styleAnchor`。每条 asset：

| 字段 | 说明 |
| --- | --- |
| `assetId` | 稳定 id，如 `cover`、`ch-1`、`sticker-1` |
| `usedBy` | 对应节拍或画布的 `data-name` |
| `role` | `scene`、`transparent`、`background` |
| `width` / `height` | 流式占位宽一般 `370`（390 − 边距）；图文 SVG 主图用画布占位像素（如 294×220） |
| `cropMode` | 场景 `cover`；透明装饰和循环背景 `contain` |
| `needsTransparent` | 贴纸和自定义弹窗按钮为 `true`，且必须从透明装饰里选 |

章节流：封面 1 张 + 每节至多 1 张主图。不要为装饰而堆图。

图文 SVG：每块 1–2 张主图（`role=scene`，`cover`，画布占位像素）+ 1–3 张贴纸（`role=transparent`，`contain`，显示边长 48–72）。一篇最多 7 块，见 [image-svg.md](components/image-svg.md)。

轮播图集：每张 slide 一条，`role=scene`，`usedBy` 指向该块 `data-name`，全部同一 `cropMode`（默认 `cover`），`width/height` 用视口像素（如 390×520）。见 [slideshow.md](components/slideshow.md)。

横向滑动：固定层与宽画布里的每张图各一条，`role=scene`，`usedBy` 指向对应 `data-name`。宽画布横幅用画布占位像素。见 [horizontal-scroll.md](components/horizontal-scroll.md)。

点击切换：before / after 各一条 `role=scene`。从池里选两张能对照着看的场景，不要求同一机位。见 [click-switch.md](components/click-switch.md)。

点击弹窗：1 张场景底图 + 每组 1 张细节，都是 `role=scene`。细节不够时，该组改成信息卡 SVG，不占位硬上。默认按钮用组件文档里的模板图，不进槽位。自定义 open 才 `role=transparent`。见 [click-popup.md](components/click-popup.md)。

## 分槽

把 `asset-pool.json` 的 `items` 分成三类，每张图只进一类：

| 类 | 条件 | 用在 |
| --- | --- | --- |
| 循环背景 | `orientation` 为 `background` | `role=background` |
| 透明装饰 | `transparent` 为 true，且不是 `background` | `role=transparent` |
| 场景 | 其余 | `role=scene` |

- 流式文章默认没有循环背景槽。只有大纲明确要一张可衔接长底时才用。有多张时，先选标题或描述更贴近主题的；仍分不出就选高宽比更大的一张。`tileHeight = round(390 × height / width)`，用接口返回的宽高。竖图、`custom_portrait` 和其它比例都不能当作循环背景。没有 `background` 时，这个槽位占位。
- 透明装饰按槽位宽高比就近选，先用未用过的，不够再复用。标题或描述更贴近 `styleAnchor` 的优先。没有透明图时，该槽位占位。
- 场景图同样按宽高比就近选，先未用后复用。`orientation` 只用来判断横竖和方图，不要求与槽位比例完全相同。同一篇里能分出的图不要重复用，除非池里不够。
- 按钮、分割和简单几何写 SVG，不进图片槽。

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

`background` 和 `transparent` 用 `contain`。循环背景 `--max-edge 2160`，避免裁掉可衔接的边缘。场景图默认 `cover`，`--max-edge 1080`。HTML 原样使用返回的 `src`。

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

- 用户点名生图技能：按技能名读取它的 `SKILL.md`，只为点名的槽位出图，再走上传和 OSS。点名的是 `jimeng-free-api-image` 时，才读 [prompt-templates.md](prompt-templates.md)。该技能失败时，按它的说明重试一次；仍失败则该槽位占位。不要再启动第二个没有被点名的生图技能。

上传按 [upload.md](upload.md)。成功后记下 `src`、`width`、`height`，再跑 OSS。临时链不进 manifest，也不要交给上传脚本的 `--url`。

## 占位图

池里没有对应类型、用户要求占位，或上面的失败路径选择占位时使用（`img` 仍加 `max-width:100%`）。manifest 写 `status=placeholder`、`source=placeholder`。按槽位宽高比就近选：

| 比例 | URL |
| --- | --- |
| 2x3 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/2d21226218402d33a1766d175d57de2094df4874.png_large |
| 3x2 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/93c19eefa547172bee902b6a8b0c7e5c25aa3566.png_large |
| 3x4 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/e0aaf2ba7d33fad7e0e6bd38278ba5d83af25d39.png_large |
| 4x3 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/6bfbc9f89541c901b68bb9b2ce6323b75f61dca7.png_large |
| 9x16 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/b41b901953ab639e3a41360ff72415a0b0b75bef.png_large |
| 16x9 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/778ff62e975858f9e774c26e530fdff749fd952f.png_large |
| 21x9 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/f1a3517d3756cc29ae3fb31b743b6de26a7a6fc1.png_large |
| 1x1 | https://svg-cdn.creatby.com/67e8dd5d4bf7cd7229097390/019ddbf3a1cfd4f8e48f1c6eec0442dd11f34bdf.png_large |

占位和失败都要出现在成品摘要里。

## 失败

- 素材接口 401：更新 `WEIPAIBAN_API_KEY`。403 通常是未订阅。429 时脚本会等一次；仍然 429 就停止。
- 400：tag 为空、超长或 cursor 非法。修正参数，不要改拉全库。
- 非 `svg-cdn.creatby.com` 不能挂 OSS，视为失败。
- 不要把即梦或其它生图服务的临时 URL 写进 HTML。

# 即梦 Prompt 模板

只在用户点名 `jimeng-free-api-image` 时阅读。默认配图走 [assets.md](assets.md) 的 AI 素材库，不要打开本页去生图。

按 `asset-request.json` 的条目拼 prompt。末尾必须追加 `styleAnchor`。
风格、介质、光影全部来自 `styleAnchor` 与每条 `visual`，不要另加「大气构图 / 柔和光影 / 矢量感」这类套话。
不要写「多图 / 连续 / 绘本 / 故事 / N张」。

`ratio` 只能是：`1:1` `4:3` `3:4` `16:9` `9:16` `3:2` `2:3` `21:9`。缺省时选能 cover 占位框的最近合法比。

## 全篇两句

顶层 `styleAnchor` 与 `lightingHint` **拼进每一条**。顺序：`{分类模板}，{lightingHint}，{styleAnchor}`。

`styleAnchor` 只写图像语言：气质 + 介质 + 质感 + 一句色调（`暖金与深棕色调`，不是配色策略名）。

### 不要写进 prompt

| 词 | 后果 |
| --- | --- |
| 配色策略名（`单色系深浅渐进`、`三色分割`） | 出黑白或分割画面 |
| 版面词（`极窄边框`、`超大字距`、`留白撑场`、`栏线`） | 画出假边框和乱码字 |

## 分类

### 封面 / 场景

`{主题}主题场景，{visual}，{lightingHint}，{styleAnchor}，高清，无文字无水印`

排除：文字、水印、logo、杂乱。

### 章节配图

`{主题}，{visual}，{lightingHint}，{styleAnchor}，高清，无文字无水印`

一图一意：写清这一节要看见的那一件东西，不要百科拼贴。图文 SVG 的主图也用这一条；`visual` 不要写边框、贴纸、四角装饰——那些是画布上另排的。

### 装饰贴纸

图文 SVG 的透明小图。`needsTransparent=true`，必须走「透明图」白底规则。

`{主题}装饰物件，{visual}，{lightingHint}，{styleAnchor}，单个完整主体居中，纯白色背景(#FFFFFF)，无文字无水印`

`visual` 只写**一件具体物件**（梅枝、纸鹤、厨房秤、胶带卷、一枚朱砂印），不要写「四角装饰 / 贴纸贴满 / 插画点缀」。负向追加：`文字、水印、logo、多物件、阴影、投影、边框`。

可选书法字贴纸：仅 1–4 字、国风主题、且用户明确要手写感时才生。`visual` 写成「宣纸上的墨书“{字}”，完整单字/短词，无其它图案」。默认仍用画布 `<text font-family="serif">`，不要每篇都出字图。

### 对照前后图

分别文生图会错位。先出「前/A」，再拿它的 URL 图生图出「后/B」：

```bash
node "$JIMENG_DIR/scripts/jimeng-free-api-image.mjs" sync \
  --prompt "保持这张照片的机位、光线方向和色调完全不变，{第二张的变化}" \
  --images "{第一张的返回 URL}" \
  --ratio "16:9" \
  --sample-strength 0.55
```

`sample-strength` 0.5–0.6。图生图要显式传 `--ratio`，否则回到 `1:1`。

点击切换的 before/after、点击弹窗的底图→各组细节，都走这一套。弹层若是信息卡画面，prompt 写清「同一场景里的这一处特写 / 一张信息卡构图」，仍禁止「多图」。

## 透明图

`needsTransparent=true`：不要让即梦出 alpha。prompt 追加 `纯白色背景(#FFFFFF)，不透明，不要任何图案、纹理或渐变，主体居中且完整`。negative 追加 `透明背景、半透明、alpha通道、棋盘格背景`。去背景命令在 [assets.md](assets.md)。

## 负向

通用：`文字、水印、logo、低质量、模糊、变形`。透明图额外排除词见上。

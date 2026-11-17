---
name: weipaiban
slug: weipaiban
displayName: 微排版公众号SVG交互作品
description: 微排版官方技能，用于在微信公众号中制作并发布整篇 SVG 互动图文。根据主题或稿件完成创意、配图和交互，并发布到微排版预览。支持六种整篇互动：三层视差滑动、3D 多层视差、滑动上色、计分答题、二选一/四选一/六选一展开、逐幕场景转场。图片可用微排版 AI 素材库，也可自行提供或指定生图技能。当用户提到微排版、公众号 SVG、微信互动排版、视差滑动、滑动上色、二选一、计分答题或场景转场时使用。
summary: 用微排版为微信公众号制作并可直接发布的 SVG 互动图文，支持视差滑动、滑动上色、计分答题、二选一展开和场景转场。
version: 2.0.2
tags: [微排版, 公众号, SVG, 互动排版, 视差滑动, 二选一]
homepage: https://github.com/21epub/weipaiban-skill
metadata:
  openclaw:
    emoji: '🧩'
    requires:
      bins:
        - python3
      env:
        - WEIPAIBAN_API_KEY
    primaryEnv: WEIPAIBAN_API_KEY
    optionalEnv:
      - WEIPAIBAN_API_BASE
    optionalBinaries:
      - rembg
    externalServices:
      - weipaiban.cn
    writes:
      - /tmp/weipaiban-*/
      - ~/.cache/weipaiban/direction-history.jsonl
---

# 微排版公众号SVG交互作品

从主题到发布完成一件**整篇 SVG 互动图文**，可在微信公众号中使用，并直接发布到微排版预览。作品先选择 format，再按该 format 的设计规则和 HTML 壳制作。图片默认来自微排版已发布 AI 素材，按一个 tag 取完再分配使用。

## 路径与依赖

`SKILL_DIR` 是本 `SKILL.md` 所在目录的绝对路径。脚本和参考资料均从这里读取，不依赖当前工作目录。

用户提供图片，或点名生图的成品需要入库时，读 [references/upload.md](references/upload.md)，用本技能自带的 `scripts/upload_images.py`。素材库里的图不上传。用户点名了某个生图技能时，只读取那个技能并按其流程出图。未点名时不查找、不调用其它生图技能。

| 变量                 | 何时需要           | 说明                        |
| -------------------- | ------------------ | --------------------------- |
| `WEIPAIBAN_API_KEY`  | 取素材、上传、发布 | `sk-` 开头；只从环境读取。用户在 [API 密钥](https://weipaiban.cn/settings/api-keys) 创建或复制 |
| `WEIPAIBAN_API_BASE` | 可选               | 默认 `https://weipaiban.cn` |
| `python3`            | 全部脚本           | 必需。`rembg` 只在用户图片需要去背时可选，技能不会自动安装 |

不要把 key 或临时鉴权 URL 写入任务文件。

环境里没有 `WEIPAIBAN_API_KEY`，或接口返回 401 时，告诉用户：登录微排版，打开 <https://weipaiban.cn/settings/api-keys>，创建或复制以 `sk-` 开头的密钥，再设为该环境变量。不要向用户索要密钥后写入任务文件，也不要猜测密钥。

## 输入

- 必需：主题或内容。
- 可选：`format`、受众、必含内容、`category`、`workId`、tag、用户图片、占位图要求，以及用户点名的生图技能。
- `workId` 表示整份替换未发布作品；省略则创建。

## 工作流

### 1. 选择 format ⏸️

先读 [format 清单](references/formats/index.md)。

- 用户已明确合法 `format`：视为已选择。
- 未指定：展示所有 format 的名称、体验和适用场景，推荐一个并等待选择。即使当前只有一种，也要让用户确认；“直接开始 / 你定”表示接受推荐。

选定后只读该 format 文档，不读其它 format。任务目录为 `/tmp/weipaiban-{taskId}/`，契约见 [task-contract.md](references/task-contract.md)。

### 2. 创意设计与素材方案 ⏸️

Agent 是主创。根据内容、受众与所选 format 原创叙事、视觉方向、层级、交互和素材槽位，不套固定主题模板。图片槽位按该 format 需要的角色列出，具体哪一张图等素材池返回后再定。

仅当用户要求随机方向或创意受阻时，才可运行：

```bash
python3 "$SKILL_DIR/scripts/pick_direction.py" --format {format} [--category "{类别}"]
```

脚本输出是版式灵感，不是必须照抄的视觉系统，也不是出图提示词。format 规则始终优先。它会把抽过的方向追加到 `~/.cache/weipaiban/direction-history.jsonl`，用来避开最近几次重复。

形成 `design-brief.md`、`design.json` 和 `asset-request.json` 草案。`imageSource` 默认 `ai-assets`，并写上拟用的一个 tag。对照 [quality-bar.md](references/quality-bar.md) 与 [wechat-dark-color.md](references/wechat-dark-color.md) 自检。向用户展示 format、层级职责、叙事路径、主要交互、视觉方向、tag 和素材槽位，等待确认。明确说“直接开始”可跳过本次等待。

### 3. 准备图片

设计确认后读 [assets.md](references/assets.md)。

- 默认用确认过的 tag 拉取该 tag 的全部已发布图，再按角色分到槽位，并用 `build_oss_src.py` 得到最终 CDN。库内图不重新上传，也不去背。
- 素材池为空时先停。用户可以改 tag、改交图片、改点名生图技能，或明确继续并接受占位图。
- 用户已经给了图：那些槽位按 [upload.md](references/upload.md) 上传。用户点名了生图技能：只按该技能出这些槽位的图，再上传。临时链不进 manifest 或 HTML。
- 某个槽位在池里没有对应类型时，该槽位使用占位图，并记入成品摘要。format 已规定可改用 SVG 的元素，改为 SVG，不占位硬上。

### 4. 制作交互 HTML

每次必读 [dialect.md](references/dialect.md) 和已选 format 文档；只在实际使用某组件时读取对应 [components](references/components/) 文档。

- 严格按 format 的壳语法、层级和设计规则写作。
- `<image href>` / `<img src>` 原样使用 manifest 的处理后 CDN URL。
- 文末保留弱化的 AI 声明：“文章部分内容由AI辅助设计和制作”。
- HTML 写入 `{taskDir}/work.html`，`meta.currentStep=work-ready`。

### 5. 发布

HTML 写完后直接发布，不要停下来等确认。发布成功后再把标题、format、各职责层内容、交互组件、所用 tag、素材来源与占位回退、元素预算，以及 `preview`、`url` 给用户。用户看过预览后可以再改。

```bash
python3 "$SKILL_DIR/scripts/publish.py" \
  --body-file "{taskDir}/work.html" \
  --title "{标题}" \
  --description "{说明}"

python3 "$SKILL_DIR/scripts/publish.py" \
  --work-id "{workId}" \
  --body-file "{taskDir}/work.html" \
  --title "{标题}"
```

成功后把 `meta.currentStep` 改为 `done`，返回 `preview`、`url` 与 `taskDir`。保留任务目录以便续作，除非用户要求删除。

## 失败边界

- 发布 400：按 dialect、format 壳、组件结构、512KB 与 300 元素上限自查。
- 401：请用户到 <https://weipaiban.cn/settings/api-keys> 创建或复制 `sk-` 密钥，并更新 `WEIPAIBAN_API_KEY`。403 通常是未订阅。402 是作品容量上限。
- 修改 404：核对 `workId`、所有权和作品是否已经发布。
- 素材接口失败时停止取图，不猜 key，不改拉全库。用户可以改交图片或改用占位图继续。

## 参考路由

- [format 清单](references/formats/index.md)：开始时读取。
- [任务契约](references/task-contract.md)：建目录、续作或交接时读取。
- [HTML 方言硬约束](references/dialect.md)：每次制作 HTML 必读。
- [素材流程](references/assets.md)：需要图片时读取。
- [图片上传](references/upload.md)：用户图片或点名生图需要入库时读取。素材库图片不读。
- [AI 素材接口](references/api-ai-assets.md)：取图脚本失败或要核对字段时读取。
- [发布 API](references/api-formats.md)：发布失败或需要接口细节时读取。
- [完整示例](examples/formats/)：按所选 format 理解契约和语法，不作为视觉模板。

## 来源与支持

这是技能本身的支持信息，不是作品内容。不要把二维码、logo 或本仓库地址写进作品 HTML 或素材清单。

- 开源仓库：<https://github.com/21epub/weipaiban-skill>
- 微信交流群二维码见 [README.md](README.md) 的「交流群」。用户问如何加群或找支持时，把这一节指给用户。

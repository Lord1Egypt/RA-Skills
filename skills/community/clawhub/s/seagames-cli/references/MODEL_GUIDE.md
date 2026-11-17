# seagames-cli 模型参数指南

这份文档只说明 `image generate` 的模型选择和模型参数。命令通用参数、登录、上传、下载和任务管理见 [USAGE.md](./USAGE.md)。


## GPT Image 2.5

使用 `--model microsoft_gpt_image_2_5 --mode flare|sunburst`，旧别名 `microsoft_gpt_image_2_5_flare`、`microsoft_gpt_image_2_5_sunburst` 仍兼容。两者支持文生图、最多 16 张有序参考图、透明背景及 WebP 输出。带参考图时仍使用同一模型 ID。

默认 `1K / 1:1 / medium`；可选分辨率 `1K/2K/4K`，质量 `low/medium/high/xhigh/max/auto`。自定义 `--size WIDTHxHEIGHT` 的宽高需为 16 的倍数，最长边不超过 3840，总像素介于 655,360 和 8,294,400，比例在 1:3 至 3:1 之间。参考图不会覆盖指定的输出分辨率。`--size auto` 或 `--quality auto` 需要服务端支持对应报价。

```bash
seagames-cli image generate \
  --model microsoft_gpt_image_2_5_flare \
  --prompt "透明背景的小火箭" \
  --quality low --background transparent \
  --output ./output/rocket.webp

seagames-cli image generate \
  --model microsoft_gpt_image_2_5_sunburst \
  --reference-file ./output/rocket.webp \
  --prompt "把火箭主体改成绿色，保留透明背景" \
  --resolution 2K --quality high --background transparent \
  --output ./output/rocket-green.webp
```

默认按结果实际格式下载；WebP 可原样保存，显式 PNG 路径会转码保留透明度。使用前运行 `functions --function image.generate --json` 确认已发布绑定。

## 快速判断

| 需求 | 模型或参数 |
| --- | --- |
| GPT Image 2 精确尺寸 | `--model microsoft_gpt_image_2 --size WIDTHxHEIGHT` |
| GPT Image 2 透明背景 | `--model microsoft_gpt_image_2 --background transparent` |
| Seedream 5 Pro 精确尺寸 | `--model volces_seedream_5_pro --size WIDTHxHEIGHT` |
| 多角度转面图 | `image turnaround`，使用一张参考图 |
| 像素风输出语义 | `--model nano_banana_2 --output-profile pixel_art --pixel-width 32 --pixel-height 48` |
| 只选择常规分辨率和比例 | `--resolution`、`--ratio` |

## 参数规则

### `--resolution` 和 `--ratio`

这是大多数模型的预设控制项。省略时使用模型默认值。参数值必须是该模型允许的值，不能跨模型套用。

```bash
seagames-cli image generate \
  --model nano_banana_pro \
  --prompt "森林村庄" \
  --resolution 2K \
  --ratio 16:9
```

### `--size`

适用于 GPT Image 2、GPT Image 2.5 Flare/Sunburst 和 `volces_seedream_5_pro`。格式为 `WIDTHxHEIGHT`，例如 `1536x1024`。不能与 `--resolution`、`--ratio`、`--width` 或 `--height` 同时使用，仅 GPT Image 2.5 接受 `--size auto`，使用前需确认服务端报价可用。

```bash
seagames-cli image generate \
  --model microsoft_gpt_image_2 \
  --prompt "电影感的山间湖泊" \
  --size 1536x1024
```

### `--quality` 和 `--background`

GPT Image 2 的 `--quality` 支持 `low`、`medium`、`high`；Midjourney v7 的 `--quality` 支持 `standard`、`high`；Niji 7 不支持 `--quality`。`--background` 适用于 GPT Image 2 和 GPT Image 2.5，支持 `auto`、`opaque`、`transparent`。

```bash
seagames-cli image generate \
  --model microsoft_gpt_image_2 \
  --prompt "一个独立展示的游戏道具" \
  --background transparent \
  --size 1024x1024 \
  --output ./output/item.png
```

## 模型参数总表

`参考图上限` 是 `image generate` 的最大用户参考图数量，不包含风格库内部占用。实际可用性以 `seagames-cli models` 的服务端结果为准。

| 模型 ID | 分辨率或尺寸 | 宽高比 | 质量 | 背景 | 参考图上限 | 特殊能力 |
| --- | --- | --- | --- | --- | ---: | --- |
| `microsoft_gpt_image_2_5_flare` | `1K`、`2K`、`4K`；或 `--size` | 同 GPT Image 2 | `low`、`medium`、`high`、`xhigh`、`max`、`auto` | `auto`、`opaque`、`transparent` | 16 | WebP、透明背景、参考图编辑 |
| `microsoft_gpt_image_2_5_sunburst` | `1K`、`2K`、`4K`；或 `--size` | 同 GPT Image 2 | `low`、`medium`、`high`、`xhigh`、`max`、`auto` | `auto`、`opaque`、`transparent` | 16 | WebP、透明背景、参考图编辑 |
| `microsoft_gpt_image_2` | `1K`、`2K`、`4K`；或 `--size` | `1:1`、`1:2`、`2:1`、`9:16`、`16:9`、`3:4`、`4:3`、`3:2`、`2:3`、`5:4`、`4:5`、`21:9`、`9:21` | `low`、`medium`、`high` | `auto`、`opaque`、`transparent` | 16 | 精确尺寸、透明背景、参考图生图 |
| `nano_banana_pro` | `1K`、`2K`、`4K` | `1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9` | 无 | 无 | 14 | 普通生图 |
| `nano_banana_2` | `0.5K`、`1K`、`2K`、`4K` | `1:1`、`1:4`、`1:8`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`、`4:1`、`8:1` | 无 | 无 | 14 | 常规图像生成 |
| `nano_banana_2_lite` | 固定 `1K` | `1:1`、`3:2`、`2:3`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`、`1:4`、`4:1`、`1:8`、`8:1` | 无 | 无 | 14 | 分辨率不可调整 |
| `volces_seedream_4_0` | `2K`、`3K` | `1:1`、`9:16`、`16:9`、`3:4`、`4:3`、`3:2`、`2:3` | 无 | 无 | 14 | 常规文生图和参考图生图 |
| `volces_seedream_5` | `2K`、`3K` | `1:1`、`9:16`、`16:9`、`3:4`、`4:3`、`3:2`、`2:3` | 无 | 无 | 14 | Seedream 5.0 Lite |
| `volces_seedream_5_pro` | `1K`、`2K`；或 `--size` | `1:1`、`9:16`、`16:9`、`3:4`、`4:3`、`3:2`、`2:3`、`21:9` | 无 | 无 | 10 | 支持精确尺寸 |
| `midjourney_niji_7` | 固定 `1K` | `16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`2:3`、`3:2` | 无 | 无 | 8 | 不接受 quality，分辨率固定 |
| `midjourney_v7` | 固定 `1K` | `16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`2:3`、`3:2` | 无 | 无 | 8 | 不接受 quality，分辨率固定 |
| `midjourney_v8_1` | `1K`、`2K` | `16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`2:3`、`3:2` | 无 | 无 | 8 | 常规文生图和参考图生图 |

## 模型使用示例

### GPT Image 2

```bash
seagames-cli image generate \
  --model microsoft_gpt_image_2 \
  --prompt "将这个角色转换为水彩插画" \
  --reference-file ./assets/character.png \
  --size 1024x1536 \
  --background transparent \
  --output ./output/character-watercolor.png
```

省略 `--size` 时，CLI 会尝试根据第一张参考图的尺寸生成确定尺寸。资源引用必须提供宽高元数据；无法读取尺寸时请显式传入 `--size`。

### Nano Banana Pro

```bash
seagames-cli image generate \
  --model nano_banana_pro \
  --prompt "像素画风格的森林村庄" \
  --resolution 2K \
  --ratio 16:9
```

使用像素目标网格时：

```sh
seagames-cli image generate --model nano_banana_2 --prompt "酒馆精灵图" --output-profile pixel_art --pixel-width 32 --pixel-height 48 --wait --json
```

`pixel_art` 仅用于 Nano Banana 2；目标宽高必须同时提供，范围1–1024。生成后用 `image pixel-target-project` 投影到原任务网格。`image pixel-standardize` 是另一条已有图片处理流程。

### Nano Banana 2 多角度

```bash
seagames-cli image turnaround \
  --reference-file ./assets/character.png \
  --resolution 2K \
  --ratio 3:2 \
  --output ./output/character-turnaround.png
```

该命令需要一张参考图，不接受 `--model`、`--size` 或风格库参数。

### Seedream 5 Pro

```bash
seagames-cli image generate \
  --model volces_seedream_5_pro \
  --prompt "一张游戏道具设定图" \
  --size 1536x1024
```

## 查看内置设置

模型配置内置在 CLI 中，可以离线查询：

```bash
seagames-cli models --builtin
seagames-cli models --builtin --json
```

当服务端模型配置和 CLI 内置配置不一致时，以服务端当前响应为准，并更新 CLI 版本或使用当前支持的参数。

## 发布目录和静态控制表

`schemas/model-controls.json` 是随包的 CLI 控件快照，不表示其中所有模型当前都发布。先查 `functions --function image.generate --json`，再按当前绑定选择模型与控件；新控件出现在目录不代表旧二进制自动支持。`--function`/`--binding` 可指定同操作的已发布项。

## 配色迁移

`palettes --json` 查询方案；使用 GPT Image 2 和恰好一张参考图：

```sh
seagames-cli image generate --model microsoft_gpt_image_2 --reference-file hero.png --colors "#123456,#F0C080,#FFFFFF" --prompt "保留结构并应用配色" --output recolored.png
```

也可用 `--palette-id ID`；它与colors、style-item-id互斥。自定义颜色接受#RGB/#RRGGBB，保留顺序、去重，最多36色。`image extract-palette --file image.png --max-colors 6 --json` 离线提取，最大10色，GIF使用首帧；不保证与浏览器缩放后的颜色逐像素一致。

### GPT Image 2.5 已发布端点校验

普通 plain 生图根据模式与参考图选择当前绑定的文生图或图生图端点。目录包含执行端点合同时，CLI 在报价前核对 quality/background/count 对应的枚举或数值边界，以及 resolution/aspectRatio 对应的 UI 选项；端点已撤下或值不再开放时停止。现有 generation-v1 尺寸、数量及组合限制仍同时有效，不因上游 schema 更宽而自动开放参数。风格库由服务端注入引用，端点选择及参数校验以服务端报价为准。其他图片模型的已知映射见下节；不能把 executionEndpoints 中任意字段直接传给 CLI。

### 其他图片模型的动态约束

普通 plain 生成的 GPT Image 2、Nano Banana Pro/2/Lite、Seedream 4/5 Lite/5 Pro、Midjourney V7/V8.1/Niji7 也检查当前绑定中的已知端点及映射后的参数约束。GPT Image 2 与 Seedream 5 Pro 按是否有参考图分开选端点；其余上述模型使用 default 端点。参数只取明确对应的 generation-v1 字段：直接映射的上游字段及 resolution/aspectRatio 对应 UI 选项。CLI 内置的参数集合、尺寸换算和组合限制仍保留；新出现的上游字段不会自动成为 CLI 参数。像素画最终生成参数、风格库注入引用等服务端转换仍以报价合同为准。

### 默认参数来源

普通图片生成省略 resolution/ratio/quality 时，优先采用所选已发布端点 UI 合同中明确给出的默认值，仅限 CLI 已支持且未禁用的对应控件。显式参数优先；显式 size 或 width/height 不注入默认分辨率/比例。像素画目标和风格库流程保持原处理方式。目录没有对应默认值时沿用内置快照。本文及离线 schema 中的默认值是快照，不保证与实时发布合同相同；需要可重复参数时请显式指定。

1.0.2：Niji 7 保持不提供画质选项，CLI 自动填入统一接口需要的兼容值；不会改变模型画质或增加画质收费。

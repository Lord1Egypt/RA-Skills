---
name: seagames-cli
description: 使用 SeaGames CLI 为项目生成和处理图片、视频、音频、文本及 3D 资产，执行图片工具、语义拆件、动态工具箱和本地批处理；支持资源上传、任务恢复和完整产物下载。
---

# SeaGames CLI 使用指南

随附候选版本：`1.2.1`。使用前运行 `--version` 和目标命令 `--help` 确认二进制支持。文档中的可用性由当前账号发布目录和实时报价决定；后台入图还要求目标 API 支持交付协议。安装验证只检查版本、帮助和 `profiles list`，不执行收费任务。

3D 生成默认使用服务端为所选能力配置的当前推荐版本，不在命令或文档中固定旧版模型。

## 程序与会话

使用本 Skill 的 `bin/seagames-cli-windows-x64.exe`、`bin/seagames-cli-linux-x64` 或 `bin/seagames-cli-macos-arm64`。API 由随包配置固定；不调用 PATH 或其他 Skill 中的同名版本。使用匹配环境的已保存会话；需要登录时执行 `login --phone PHONE`，验证码只能使用用户提供的值。不要输出会话凭证。

## 选择能力

先用 `functions --json` 查询已发布功能；普通生成可以用 `--function`、`--binding` 指定目录中的选项。`models` 及各媒体 `models` 默认需要登录，返回当前账号已发布的模型绑定、名称及参考能力；`--technical` 查看技术接入目录，`--builtin` 查看离线图片参数快照，两者均不证明已发布。下线、隐藏或返回不可用的功能不通过改模型或私有参数绕过。

| 需求 | 命令入口 | 按需说明 |
| --- | --- | --- |
| 文生图、参考图、风格与配色迁移、像素图 | `image generate`、`palettes`、`styles list` | [模型指南](references/MODEL_GUIDE.md) |
| 超强 AI 抠图、普通去背景 | `image strong-cutout`、`image remove-background` | [抠图指南](references/BACKGROUND_REMOVAL.md) |
| 重绘、扩图、打光、图层分解、万能拆分 | `image repaint/outpaint/relight/layer-decompose/decompose` | [使用说明](references/USAGE.md) |
| 缩放、裁剪、分切、九宫格、序列合成、批处理 | `image resize/crop/trim-alpha/grid-split/auto-split/nine-slice/gif-resize/compose-sequence/batch` | [使用说明](references/USAGE.md) |
| 文生视频、混合参考视频、首尾帧 | `video generate` | [使用说明](references/USAGE.md) |
| 视频裁剪、取帧、序列导出、首尾帧动画 | `video trim/frame-sample/extract-frames/sequence-export`、`image animation` | [使用说明](references/USAGE.md) |
| 语音、音乐、音效、音频裁剪与转码 | `audio generate/process` | [音频指南](references/AUDIO_MODEL_GUIDE.md) |
| 3D 生成、减面、纹理、绑骨、导出 | `3d generate/retopologize/texture/rig/export` | [3D 指南](references/3D_MODEL_GUIDE.md) |
| 文本、提示词优化、图片反推 | `text generate/beautify`、`image reverse-prompt` | [使用说明](references/USAGE.md) |
| 动态工具箱模板 | `toolbox list/get/plan/run` | [使用说明](references/USAGE.md) |
| 上传、恢复任务、多结果和文件组下载 | `resources`、`tasks`、`media-jobs` | [输出与恢复](references/OUTPUT_RULES.md) |
| 环境查询、目录绑定项目、后台资产入图与恢复 | `profiles list`、`projects use/unuse`、`canvas` | [支持范围与使用说明](references/USAGE.md#环境项目与后台画布) |

表中斜线表示同一命令组的不同子命令，不是可直接复制的命令字符串。人物立绘、场景、UI 工作流分别见 [人物](references/CHARACTER_WORKFLOW.md)、[场景](references/SCENE_WORKFLOW.md)、[UI](references/UI_WORKFLOW.md)。

## 执行与交付

- 先确定输入资源、输出路径和必要模型控件；不假定所有命令都接受 `--model`、`--prompt` 或 `--quote-only`。
- 普通参考图可使用 `--reference-file` 自动上传或复用；封装工具按帮助使用资源 ID，本地图片先 `image upload --file PATH --json`。
- 封装功能只使用产品参数，不能根据底层模型自行组装请求或推算价格。
- `--output` 通常隐含等待和下载；目录型命令使用 `--output-dir`。具体格式、透明度、多结果和覆盖规则先读 [输出规则](references/OUTPUT_RULES.md)。
- 超时不代表任务失败。保存任务 ID、媒体 job ID、拆件分析/批次 ID、幂等键及上传回执；先查询原任务，不换键重跑付费请求。
- 部分成功必须检查清单。结果完成后验证尺寸、透明通道、动画帧和 3D 配套文件，再用于项目。

报价等待：资源时长或审核未就绪时，CLI 对明确可恢复错误自动等待最多约 2 分钟。只重报价格，不重传资源或重试收费创建；详见 references/OUTPUT_RULES.md。

报价前的单个资源 GET 查询也复用相同等待机制，处理审核/上传期间返回的可恢复 409，避免在到达报价前直接退出。等待预算按每次资源读取或报价请求分别计算。其他 GET、上传、任务创建和收费重试均不在自动重试范围。

## 登录与项目

安装包已固定环境；用 `profiles list` 查看随包 API。切换环境请使用对应 Skill，不能修改 profile 或覆盖 API。凭据仍按 API 与账号隔离。

已接入的生成和加工默认后台入画布。先使用用户指定的 `--project-id` 或当前目录 `projects use PROJECT_ID` 绑定；缺少目标时询问用户，不自动创建或猜选项目，也不静默改成仅下载。用户明确不要入图时使用 `--no-attach`。支持范围见 [使用说明](references/USAGE.md#后台交付支持范围)；查询和下载不会额外插入节点。

画布操作全程使用后台 API，禁止打开、导航或操控浏览器画布（包括无头浏览器），不能以页面点击作为失败回退。网页开着也允许后台追加，必要时由用户刷新查看；不要要求用户关闭画布。`projectUrl` 仅返回给用户。本地模型格式转换使用 CLI 内置算法，也不打开浏览器。

保留 `operationId`、任务 ID 与回执路径；中断后用 `canvas operation get` 查询，入图失败用 `canvas operation retry` 恢复原意图。本地产物的 retry 还会续传原文件，因此保留原路径和内容；不会重新处理素材。生成完成、画布保存和本地下载是不同状态，只有交付回执为 `delivered` 且节点回读存在才能说明已保存。旧 API 缺少能力时停止，不能擅自加 `--no-attach` 再提交收费任务。

访问令牌过期时 CLI 会自动使用刷新令牌续期；刷新令牌也失效时才需要重新登录。不要因查询失败重新创建生成任务，应使用已有任务 ID 恢复。

项目 ID 可通过 `projects list --json` 获取；只有用户要求新项目时才执行 `projects create`，不需要操作画布。

### 本地模型导出

OBJ/FBX 使用 `3d export` 在本机原生转换，无需浏览器、Node.js 或 Blender，不创建生成任务、不消耗积分。FBX 默认上传完整模型组入图；OBJ 仅支持显式 `--no-attach` 本地导出。先阅读 [3D 指南](references/3D_MODEL_GUIDE.md)。转换不支持的模型应报告具体错误，不临时编写转换程序，也不回退到付费任务。

## 安装包环境

本包为 **正式环境**，Skill 目录为 `seagames-cli`。API 由随包 `environment.json` 固定；用 `profiles list` 只读查看。不要配置 profile 或覆盖 API，不要修改环境文件，也不要仅复制二进制。升级只备份并替换同名 Skill，不覆盖另一个环境。命令示例中的 `seagames-cli` 指本 Skill 的 bin 内对应平台程序，不使用 PATH 中其他版本。安装验证只运行 `--version`、`--help`、`profiles list`，不发短信、不创建收费任务。

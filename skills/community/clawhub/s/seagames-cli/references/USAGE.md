# SeaGames CLI 使用说明

按任务读取对应章节；精确参数由 `seagames-cli COMMAND --help` 提供。以随附二进制的帮助为准，不能直接与旧二进制混用。模型指南分别见 [图片](MODEL_GUIDE.md)、[音频](AUDIO_MODEL_GUIDE.md)、[3D](3D_MODEL_GUIDE.md)。

## 登录、发现和引用

先用 `login --phone PHONE` 发起短信请求。已有待验证请求时，用 `--code CODE` 或 `--code-stdin` 输入用户提供的验证码；两者都不会重发短信。请求不存在或过期时，才重新发起登录。 默认复用保存的会话，`--session-file` 显式指定会话，安装包固定 API，不能用 `--api-url` 切换环境，也不能混用会话。`functions --json` 查询发布目录；`functions --function image.generate --json` 查看某项能力和绑定控件。普通生成支持 `--function`、`--binding`；报价和创建使用同一选择，未发布则拒绝。

`models --json`、`audio models --json`、`video models --json`、`3d models --json` 默认从当前账号已发布功能取模型、名称、绑定与参考能力，需要登录。相同模型的不同绑定分别列出；`--technical` 才查询无需登录的技术目录。`--builtin` 保留离线图片参数快照。JSON 中 `executionEndpoints` 是服务端上游请求合同，不能直接当作 generation-v1 的 modelInputs；`settingsSource` 明确标识内置参数快照，最终参数和组合仍由类型化 CLI 与服务端报价验证。`styles list` 查询风格库，`palettes --json` 查询配色方案。任务列表使用分页参数，检查返回分页信息再继续，不因第一页没有记录而重新创建。

本地图片使用 `image upload --file source.png --json`；普通生成可直接使用 `--reference-file`，与 `--reference-resource` 混用时按出现顺序处理。非图片使用 `resources upload --file video.mp4 --type video --receipt upload.json --json`，type 可为 image/video/audio/model3d/file。回执路径必须新建；上传失败先检查 uploadId 和已完成分片，目前没有通用自动续传命令，不删除回执盲目重传。

`image generate`、`image turnaround`、`3d generate`、`audio generate`、`text generate` 支持 `--quote-only`：使用与提交相同的参数，只返回报价，不创建生成任务；本地参考文件仍可能上传。不能与等待、下载、输出路径或图片后处理链混用。工具命令是否支持只报价，以各自 `--help` 为准。

## 环境、项目与后台画布

环境来自随包 `environment.json`，`profiles list` 显示当前环境与 API。完整安装本 Skill，不能只复制二进制；不修改全局默认 profile，不覆盖另一环境的 Skill。缺失或损坏的配置会报错，不回退到其他环境。切换环境请使用对应安装包。

```sh
seagames-cli profiles list
seagames-cli login --phone PHONE
seagames-cli projects list --json
seagames-cli projects use PROJECT_ID
seagames-cli canvas nodes --json
```

`projects use` 在当前目录写入 `.seagames/project.json`，没有凭据，仅影响该目录，不搜索父目录。每次使用重新核对环境、账号与项目权限；`projects unuse` 解除绑定。`--project-id` 仅覆盖本次目标，不修改目录绑定。不要把绑定文件当作登录配置。

`SEAGAMES_CONFIG_DIR` 可显式指定绝对配置目录；否则优先使用绝对 `XDG_CONFIG_HOME/seagames-cli`，再使用 macOS 用户目录下的 `Library/Application Support/seagames-cli` 或 Windows/Linux 用户目录下的 `.config/seagames-cli`。profile、分环境账号会话、待验证短信和交付回执保存在此处；未启用 profile 的旧会话路径仍按原选择方式处理。不能输出、共享或提交其中的会话凭证。

下列已接入的产物命令默认保存到指定或绑定的画布；`--no-attach` 明确保留仅生成/处理/下载用途。缺少目标时先询问用户，不能自行关闭入图。没有新产物的查询、报价、分析、下载不会自动入图。

```sh
seagames-cli canvas attach --resource-id RESOURCE --wait --json
seagames-cli image generate --model MODEL_FROM_FUNCTIONS --prompt "游戏场景概念图" --wait --json
seagames-cli canvas operation get --operation-id OPERATION --wait --json
seagames-cli canvas operation retry --operation-id OPERATION --wait --json
```

- 全程后台 API，不打开画布，不使用浏览器、无头浏览器或页面点击回退。项目链接仅是返回信息。
- 支持正式图片、视频、音频、3D 模型和文本资源及已有模型/动画文件组。附件随主资产保存，不能把预览图或 ZIP 当作模型。原生画布模型预览支持 GLB/FBX，不承诺新格式预览。
- 创建前检查项目和服务端交付协议；旧 API 不支持时停止。`--attach --quote-only` 不创建任务、节点或交付记录；若有本地参考文件，正常报价流程仍可能上传。
- 未指定 `--wait` 时，退出成功可只表示已受理。`--wait`/下载等待后超时或失败返回非零；这不代表生成任务被取消或已退款。
- 保存 stderr 提示的 `operationId` 和回执路径。请求结果未知或 CLI 重启后，先查询原操作；回执按环境/账号保存，换工作目录仍可查询。回执丢失时需显式提供项目 ID 和原操作 ID。不要重跑生图来恢复入图。
- `delivery.status` 为 `pending`、`delivered` 或 `failed`。`task_pending`/`resource_not_ready` 表示等待原任务或资源。网页打开不阻止后台追加，用户可以刷新查看；不要求关闭画布，也不自动刷新用户页面。若旧服务返回 `active_editor`，记录接口版本及回执交给维护者处理。`delivered` 后用 `canvas nodes` 回读正式节点；生成状态、账务状态、本地下载各自判断。
- `canvas operation retry` 只恢复原入图，无法更换来源或目标，不创建生成任务。不接管别人的租约；永久合同错误须先解决原因再重试。已交付操作再次重试不会插入第二份，即使用户后来删除了节点。
- 网络超时且操作查询返回不存在时，不能凭本地回执推断服务端已经受理；保留原回执并排查，不能自动换键重复收费提交。

### 后台交付支持范围

以下描述随包代码能力，实际运行还要通过目标 API、账号权限及功能发布检查。

| 产物入口 | 默认交付 |
| --- | --- |
| `image/video/audio/text/3d generate`，`image turnaround` | 正式最终结果；包括已支持的像素图 |
| `3d retopologize/texture/rig` | 加工后的完整模型及附件，复用模型原生卡片 |
| `image upscale/remove-background/strong-cutout/outpaint/relight/layer-decompose`，`toolbox run` | 最终加工结果；原输入不再插一份 |
| `text beautify`、`image reverse-prompt` | 正式文本产物 |
| `video trim/sequence-export`、`audio process`、`image pixel-standardize/pixel-target-project` | 原任务或媒体 Job 的正式产物；序列 MP4 仍保持原停用提示 |
| `image decompose run/retry` | 对应批次或重试部件；部分失败时检查子项；analysis/get/save-plan 不生成卡片 |
| `image resize/crop/trim-alpha/grid-split/auto-split/nine-slice/gif-resize/batch`、`video extract-frames` | 本地最终文件上传后入图；批处理仅交付成功项 |
| `image align-portrait` | 几何校验通过后替换的最终 PNG 上传入图；校验拒绝不替换、不上传；`--no-attach` 保持离线 |
| `image compose-sequence`、`image animation`（云端及 `--local`） | 完整序列/帧组与时序信息；可选去背景只交付最终帧组 |
| `image generate --post-process remove-background` | 每份结果的最后一步分别交付，使用各子操作回执恢复 |
| `3d export --format fbx` | 转换后的 FBX 与附件上传为一个模型组；`original/glb` 只下载，不重复入图 |

本轮不接服务端 `video frame-sample`，沿用其原行为；`3d export --format obj` 必须显式 `--no-attach`，画布没有 OBJ 预览。`image repaint` 沿用原手工 mask 工具，不在此交付范围；调色板分析、查询和上传命令本身不自动生成画布卡片。

本地产物保留文件和回执，`canvas operation retry` 只补上传和入图。云端任务的入图由后台继续；本地加工链在 CLI 退出后不会自动续跑。动画逐帧抠图失败时保留 `processing-receipt.json` 中的原任务/帧/幂等键及已下载文件；先查询已受理任务，不能重新运行整条收费链。详见 [输出与恢复](OUTPUT_RULES.md)。

## 普通图片生成与后处理

```sh
seagames-cli image generate --model nano_banana_2 --prompt "游戏村庄概念图" --resolution 1K --ratio 16:9 --output village.png
seagames-cli image generate --model microsoft_gpt_image_2_5 --mode flare --reference-file hero.png --prompt "保留人物，改成蓝色披风" --output edited.webp
seagames-cli image turnaround --reference-file hero.png --prompt "同一角色的多视角设定图" --output turnaround.png
```

控件按模型指南选用。`--post-process remove-background` 对每份生成结果执行普通抠图，不等于超强 AI 抠图。保存每个后处理任务 ID；后处理失败不能重跑整个生图命令。多结果交付见 [输出规则](OUTPUT_RULES.md)。

## 图片工具栏

超强抠图和普通抠图见 [抠图说明](BACKGROUND_REMOVAL.md)。其他工具以已有资源 ID 为输入：

```sh
seagames-cli image upscale --resource-id IMAGE --long-side 2048 --output upscaled.png
seagames-cli image outpaint --resource-id IMAGE --left 128 --top 0 --right 128 --bottom 0 --quality medium --quote-only
seagames-cli image relight-config
seagames-cli image relight --resource-id IMAGE --description "温暖侧光" --output relit.png
seagames-cli image layer-decompose --resource-id IMAGE --output-dir layers --json
seagames-cli image reverse-prompt --resource-id IMAGE --output prompt.txt --json
```

扩图四边为非负像素，默认各256，可提供 `--prompt` 和 low/medium/high 质量；以实时报价验证范围。打光四种模式互斥：`--preset`、`--description`、`--parameters FILE.json`、`--reference-resource`。预设先查询，参数文件字段 azimuth[-180,180]、elevation[-90,90]、intensity[0,32]、color(#RRGGBB)、softness[0,1]、fill[0,32]、rim(bool)。封装功能不能自选底层模型或内部提示词。

局部重绘不依赖画笔交互，使用已有 PNG 遮罩：与原图尺寸相同，透明像素表示可编辑区域。先上传原图和遮罩，再执行：

```sh
seagames-cli image repaint --resource-id IMAGE --mask-resource MASK --prompt "在选区加入蝴蝶" --mode flare --quality medium --output repaint.webp
```

支持 `--quote-only` 和 `--idempotency-key`。重绘是生成式编辑，不能承诺遮罩外每个像素保持不变。

`image layer-decompose` 保存所有返回图层与清单，区别于语义拆件。图层分解、重绘、扩图、打光、反推、超强抠图的具体报价/等待参数以各自帮助为准，不把某个工具的参数套给其他工具。

像素图使用 `image generate --model nano_banana_2 --output-profile pixel_art --pixel-width 32 --pixel-height 48 --prompt TEXT --wait --json`；目标宽高1–1024。然后用 `image pixel-target-project --resource-id RESULT --generation-task-id TASK --output target.png` 投影到原任务目标网格。不能替换目标尺寸或将任意上传图冒充此任务结果。`image pixel-standardize` 是不同工具。

## 万能拆分

`image decompose` 是语义拆件，支持 humanoid/object/scene。`image auto-split` 是离线连通区域分切，两者不混用。

```sh
seagames-cli image decompose config
seagames-cli image decompose analyze --resource-id IMAGE --kind humanoid --output analysis.json
seagames-cli image decompose save-plan --analysis-id ANALYSIS --plan edited.json --output saved.json
seagames-cli image decompose run --analysis-id ANALYSIS --plan saved.json --view-mode single --style-mode original --quote-only
seagames-cli image decompose run --analysis-id ANALYSIS --plan saved.json --output-dir parts --idempotency-key UNIQUE_KEY
seagames-cli image decompose get-run --analysis-id ANALYSIS --run-id RUN --output-dir recovered-parts
```

在 analyze/get 导出的快照中编辑 plan，保留 id/revision，先 save-plan 再 run；使用保存后返回的新版本。人形保留基础素模层，保留的层至少含一个部件。运行视图 single/three_view，风格 original/clay。分析也可能计费，先检查 config；生成使用实时报价，旧版本冲突不能自动覆盖。

`get --analysis-id ID --output NEW.json` 取回分析；`list` 按 resource-id/project-id 过滤，`runs --analysis-id ID` 查询批次，均检查 hasMore/nextCursor。`retry --analysis-id ID --run-id RUN --part-id PART --quote-only` 查询失败部件恢复价格，明确重试时去掉 quote-only 并提供幂等键。所有拆分命令输出 JSON，partial/failed/blocked 状态需要检查各部件；成功退出不表示所有部件生成成功。中断后查询同一分析/批次，不重复提交。

## 本地图片处理与序列

下列静态命令不登录、不请求生成，不接受动画输入：

```sh
seagames-cli image resize --file input.png --width 512 --height 512 --output resized.png
seagames-cli image crop --file input.png --x 0 --y 0 --width 128 --height 128 --output crop.png
seagames-cli image trim-alpha --file input.png --padding 2 --output trimmed.png
seagames-cli image grid-split --file sheet.png --rows 4 --columns 4 --output-dir tiles
seagames-cli image auto-split --file transparent.png --merge-distance 1 --min-size 8 --padding 2 --output-dir sprites
seagames-cli image nine-slice --file panel.png --width 800 --height 600 --left 16 --right 16 --top 16 --bottom 16 --output panel-large.png
seagames-cli image extract-palette --file input.png --max-colors 6 --json
```

grid-split 可用 `--x-cuts`、`--y-cuts` 替代均匀分切。auto-split 根据透明区域分离连通块，不是语义抠图；先完成去背景再使用。GIF 缩放使用 `image gif-resize --help`，保留所有帧及时间，不使用普通 resize。

`image compose-sequence --plan frames.json --output animation.gif` 合成 GIF，或输出 PNG/WebP 精灵表。计划路径相对计划文件：

```json
{"frames":[{"file":"a.png","durationMs":100},{"file":"b.png","sourceRect":[0,0,64,64],"durationMs":200}],"columns":2,"cellWidth":64,"cellHeight":64,"padding":0,"repeats":0}
```

sourceRect 为 x/y/width/height；时间为10ms倍数。repeats=0播放一次，省略表示循环；同时输出同名 JSON 清单，保护已存在文件。

`image batch --plan batch.json --output-dir results` 批量处理1–50张图；输入相对路径以 plan 所在目录为基准，也可使用绝对路径：

```json
{"operation":{"type":"scale","factor":2},"files":[{"file":"a.png","name":"a-large.png"},{"file":"b.png","name":"b-large.png"}]}
```

operation 支持 scale(width+height或factor)、crop(x/y/width/height)、remove-background、grid-split(rows/columns)、auto-crop(alpha_threshold/padding)、rename。rename复制原字节到新目录，不改源图；去背景逐项计费且使用普通抠图。默认首个错误停止，`--continue-on-error`记录缺失、损坏或越界输入并继续合法项，保留成功产物，但最终仍报告失败；manifest和logs保留每项状态及任务身份。不重跑已成功批次，不恢复已关闭的批量放大/格式转换入口。

## 视频与动画

先 `functions --function video.generate --json`。普通图片参考使用 reference-file/resource；混合视频/音频参考使用 video-file/resource、audio-file/resource。首尾帧使用 first-frame-file/resource、last-frame-file/resource，同一角色不能同时给文件和 ID；不能与普通参考模式混用。文件上传回执默认保存在当前目录 `.seagames-cli/uploads`，可用 `--upload-receipt-dir` 指定。

```sh
seagames-cli video generate --model volces_seedance_2_5 --prompt "角色缓慢转头" --reference-file hero.png --duration-seconds 4 --resolution 480p --output scene.mp4
seagames-cli video trim --resource-id VIDEO --start 1 --end 4 --output clip.mp4
seagames-cli video frame-sample --resource-id VIDEO --at-seconds 1 --output frame.jpg
```

Seedance2.5支持4–30秒及480p/720p/1080p；参考数量和媒体规格必须满足当前合同。引用视频过小会被服务拒绝，不能只看文件能播放就提交。MiniMax H3/H3 Fast/H3 Max 的分辨率、音频和参考限制不同；只有发布目录实际出现的选项才可使用。`--quote-only` 不创建视频任务，但本地引用仍可能上传。

`video extract-frames --input movie.mp4 --output frames` 需要 ffmpeg，也支持 `--resource-id VIDEO` 下载当前账号可用的视频后本地处理；input与resource-id二选一。`--start 0.4 --end 1.0 --fps 5` 限定抽帧时间范围，end为不包含的边界；`--frame-index 0,3,12` 选择零起点源帧索引，必须严格递增，不能同时指定fps。需要不同播放顺序时在后续合成计划里重排。 `--position first` 或 `--position last` 提取首/尾解码帧，与fps、frame-index、start/end互斥。尾帧需要ffprobe实际扫描帧数，长视频可能耗时；不通过时长估计最后一帧。输出manifest记录每帧文件、源时间timeMs和建议播放durationMs；显式索引模式记录sourceFrameIndex，均匀FPS采样不伪造源索引。最后一帧的建议播放时长使用1/fps，显式索引模式未指定fps时为1/12秒，合成时可修改；它不表示源视频最后一帧的原始时长。索引超出视频或时间范围会报错。`image animation` 的远程首尾帧动画使用 `--first-frame-file/resource`、`--last-frame-file/resource` 和提示词；frame-count 为5、9、13…121。`image animation --local` 使用本地视频/视频生成链路，先读其帮助；`--remove-background` 会逐帧创建普通抠图任务，注意帧数及费用。

`video sequence-export` 将已有视频的有序帧计划导出为 GIF 或精灵表。`--frames` 文件内容是数组 `[{"id":"f1","sourceFrameIndex":0,"timeMs":0,"holdFrames":2}]`；传 source-duration-ms/source-fps、width/height/fps，精灵表可传 layout/columns/rows/spacing。本次 MP4 导出验收出现帧数与时长不符，CLI已阻止该模式，不以它作为可用交付路径。GIF/精灵表仍可用。

## 已有视频或序列转透明产物

复用已有三个命令，不重新生成视频：

1. `video extract-frames --input movie.mp4 --fps 5 --output frames`，或使用resource-id。已有图片序列可以从下一步开始。
2. 按frames/manifest.json的顺序建立batch计划，以remove-background处理每帧。每批最多50张，更多帧分批保存到不同目录，并保持全局顺序。每帧去背景会产生任务和费用。
3. 检查各batch manifest全部完成，保留source帧到output、taskId的对应关系，再建立compose计划。失败项通过其任务记录恢复，不能整批重跑；不要把缺帧序列冒充完整动画。
4. `image compose-sequence --plan compose.json --output transparent.gif`，或输出透明PNG/WebP精灵表。GIF仅支持二值透明，柔和半透明边缘使用PNG/WebP精灵表。不要宣称输出透明MP4。

batch.json 示例（file相对计划文件）：

```json
{"operation":{"type":"remove-background"},"files":[{"file":"frames/frame-0001.png","name":"cut-1.png"},{"file":"frames/frame-0002.png","name":"cut-2.png"}]}
```

执行 `image batch --plan batch.json --output-dir cut` 后，按返回的实际output路径建立compose.json：

```json
{"frames":[{"file":"cut/cut-1.png","durationMs":200},{"file":"cut/cut-2.png","durationMs":200}]}
```

保留原抽帧timeMs用于对应源视频，durationMs决定输出播放时长；GIF必须为10ms倍数，不能静默丢失舍入误差。分别导出GIF和精灵表时使用不同文件主名，因为它们都会写同名JSON清单。例如transparent.gif与sheet.webp，不同时写transparent.gif和transparent.webp。

## 文本与提示词

```sh
seagames-cli text generate --model qwen3.5-plus --prompt "描述一个游戏场景" --output scene.txt
seagames-cli text beautify --input "雨夜森林" --generation-type image --output prompt.txt
seagames-cli image reverse-prompt --resource-id IMAGE --output reverse.txt
```

文本模型先查 `functions --function text.generate`；text generate 可带有序图片引用。beautify 的 generation-type 为 image/music/sound_effect，走独立产品能力，支持 quote-only；不通过普通文本模型模拟。文字输出可能与所请求语言不一致，交付前检查实际内容。

## 动态工具箱

```sh
seagames-cli toolbox list --page 1 --page-size 100 --json
seagames-cli toolbox get --template-id TEMPLATE --json
seagames-cli toolbox plan --template-id TEMPLATE --output plan.json --json
seagames-cli toolbox run --plan plan.json --quote-only --json
seagames-cli toolbox run --plan plan.json --idempotency-key UNIQUE_KEY --output-dir results --json
```

list支持query/tag-id/favorite/recent，tags查询分类。plan生成可编辑计划，填写prompt、styleItemIds、references各槽中的file或resourceId（二选一）及允许的controls；文件相对计划目录。保留templateId/contractFingerprint，运行会重新取服务合同，修改只读contract快照不能绕过限制。固定模型、固定控件、提示词策略和插槽数量必须遵守。预设素材由服务端处理，不能猜测隐藏提示词。

quote-only可能上传本地引用。模板下线或指纹变化时重新读取并检查计划，不静默套用新模板；提交响应丢失先查任务。图片/视频使用各自合同，本次账号目录没有视频模板，不能声称视频模板已在线验收。

## 任务与交付

`tasks list/pending/quota/get/wait/cancel/retry/download` 管理生成任务；`image tasks`、`image task get` 为兼容入口。`media-jobs get/wait/download` 管理音频处理、视频裁剪/取帧和像素投影的媒体 job。语义拆件用自身分析和批次 ID。详细恢复、下载和覆盖规则见 [OUTPUT_RULES.md](OUTPUT_RULES.md)。

### 高清放大档位

`image upscale` 必须指定 `--long-side 2048|4096|6144`（2K/4K/6K），可选 `--crop-to-fill`。CLI 在创建任务前读取当前计价目录，检查该档位是否启用、匹配约束且已配置价格；最终计费与执行仍由服务端校验。目录不可用或所选档位不可用时停止，不提交任务。使用 `--output` 等待并下载；超时后按输出的任务 ID 恢复，避免重复付费创建。

### 视频实时参数约束

Seedance 2.5、2.0/Fast/Mini 与 MiniMax H3/Fast/Max 在普通生成报价前，读取所选发布绑定的 default 端点，校验时长、比例和分辨率对应的服务端参数枚举/边界；Seedance 同时校验音频开关。原有多模态引用、首尾帧和模型组合限制仍有效。实时合同校验不表示所有模型组合已经线上生成通过；不可用项仍以服务端发布状态和报价结果为准。

### 旧处理命令的结果恢复

`image pixel-standardize` 沿用原服务接口，显式输出使用 `.png`；创建前检查输出冲突，接受后打印 media job ID，下载复用媒体作业交付。中断后用 `media-jobs get/wait/download --job-id ID` 恢复。远程序列动画 `image animation` 的输出必须是目录，已有目录需要明确 `--overwrite`；提交前检查路径，提交时打印幂等键，接受后打印任务 ID，再开始等待。

## 报价阶段等待资源就绪（1.0.2）

CLI 统一处理现有生成、工具箱及图片专用报价入口的异步资源就绪错误。仅当报价返回 HTTP 409、retryable=true，且错误码为 RESOURCE_DURATION_UNAVAILABLE、RESOURCE_REFERENCE_NOT_READY、RESOURCE_NOT_READY 或 IMAGE_REPAINT_RESOURCE_NOT_READY 时等待并重报。

等待间隔从 2 秒逐步增加到 10 秒，总预算 120 秒（包含请求时间）。复用同一份报价请求和资源，不重新上传；提示写入 stderr，stdout 的 JSON 合同不变。成功后继续原流程；quote-only 仍只报价。已明确 failed/deleted/rejected/blocked 的资源不等待。

报价超时不会创建本次生成任务，应复用之前的资源 ID；网络错误、余额不足、权限、价格配置、功能关闭、参数或时长超限不自动重试。任务创建、retry/run、上传和媒体处理请求均不自动重试。资源 available 不代表可信时长已完成解析，Seedance 2.5 的报价会等待服务端时长探测。

报价前的单个资源 GET 查询也复用相同等待机制，处理审核/上传期间返回的可恢复 409，避免在到达报价前直接退出。等待预算按每次资源读取或报价请求分别计算。其他 GET、上传、任务创建和收费重试均不在自动重试范围。

## 自动续期与项目管理（1.0.2）

登录凭证自动刷新，旧会话文件兼容。长轮询和上传同样支持续期；刷新凭证失效时执行 login。网络超时不会自动重新提交生成任务。

```sh
seagames-cli projects list --page 1 --page-size 20 --json
seagames-cli projects create --name "CLI assets" --json
seagames-cli projects get --project-id PROJECT_ID --json
```

列表保留分页信息。create 创建一个空项目用于任务归属，不需要画布操作；遇到网络错误先查询项目列表，避免重复创建。

# 3D 生成与加工

生成前查询 `functions --function 3d.generate --json`；加工前查询 `functions --model3d-processing --json`。两者是独立发布目录。`3d models` 默认返回当前账号的发布目录；`--technical` 仅表示技术接入，不保证可调用。

## 生成

默认省略 `--ai-model` 和 `--model-version`，由服务端为所选能力配置当前推荐版本，不固定旧版本、不自动降级。报价使用 `--quote-only`，不与下载或等待参数混用。

使用 `--model tripo3d|meshy --input-mode text|image|multiview`；旧的文生/图生模型 ID 保留兼容。文本模式提供 `--prompt`，图片使用 `--reference-file` 或 `--reference-resource`。控件不能跨模型套用；以 `3d generate --help` 及实时发布合同为准。

```sh
seagames-cli 3d generate --model tripo3d --input-mode text --prompt "低多边形木箱" --mesh-mode smart_mesh --face-limit 1000 --wait --json
seagames-cli 3d generate --model meshy --input-mode image --reference-file robot.png --should-texture true --wait --json
```

Tripo 使用 `--mesh-mode` 选择网格能力；只选择当前发布目录开放的分支，面数及纹理参数以当前端点约束为准。

多视图可显式传 `--view-file front=front.png --view-file right=right.png`，或 `--view-resource front=ID`。可用视图 front/left/back/right，必须含 front，不能重复或混用无名称参考图。当前线上 H/P1 多视图也要求至少两张图；单图改用 image 输入模式。Meshy 使用无名称图片集合，不能使用 Tripo 视图标签。

Meshy 的网格、姿态和纹理选项见 `3d generate --help`，按输入模式与当前发布合同使用。不要主动传旧版专属纹理参数，也不要为此切换旧模型。文本 preview 不接受图片纹理/姿态参数，多视图不接受姿态参数。

## 工具栏加工

加工输入使用已有模型资源 ID。用 `--project-id` 或当前目录项目绑定关联已有项目，默认将加工后的模型入图，无需打开画布；仅报价时可省略目标。多个发布绑定时显式 `--binding`。支持 `--quote-only`、`--wait`、`--output-dir NEW_DIRECTORY`、`--idempotency-key`；`--no-attach` 关闭入图，来源加工接口仍要求项目归属。

```sh
seagames-cli 3d retopologize --resource-id MODEL --target-polycount 10000 --quote-only
seagames-cli 3d texture --resource-id MODEL --project-id PROJECT --style-mode text --prompt "旧铜材质" --texture-resolution 2k --enable-pbr true --output-dir textured
seagames-cli 3d rig --resource-id MODEL --project-id PROJECT --model tripo3d --rig-type biped --output-dir rigged
```

- 减面使用 Meshy 三角拓扑；不恢复已关闭的 quad/originalUV 加工入口。
- 纹理 `text` 需要提示词；`image` 需要一个 `--style-resource`；`multiview` 需要1–4个有序风格资源，正面在前，图片模式不混入 prompt。纹理分辨率2k/4k。
- Meshy 绑骨可传正数 `--height-meters`。Tripo v1.0-20240301 对应 biped；v2.5-20260210 对应 quadruped/hexapod/octopod/avian/serpentine/aquatic，`--spec tripo|mixamo`。
- OBJ/FBX 使用 CLI 内置原生算法在本机转换，见下方说明。Meshy 绑骨仍可能遇到大模型请求超限，不能承诺任意模型均成功。

## 完整下载

单文件按实际 MIME 保存；多结果/文件组必须保留清单与所有材质纹理。`--output character.glb` 遇到文件组会写入 `character.glb.results/`，不能只复制名为 GLB 的入口文件。已有任务用 `tasks download --task-id TASK --output-dir NEW_DIRECTORY`，已有资源用 `resources download-group --resource-id ROOT --output-dir NEW_DIRECTORY`。失败时保留任务 ID 和清单，不重新生成模型。

## 已发布端点与参数范围

生成前查询所选绑定的当前端点。Meshy 按 text/image/multiview 选择对应端点；Tripo 同时按 H/P1/P2 选择普通、smart_mesh 或 smart_mesh_p2 分支。目录包含端点合同时，已撤下的分支在报价前拒绝。面数、拓扑、纹理、PBR、模型版本和 Meshy 控制项只按已确认的字段映射检查公开枚举/上下界，仍保留 generation-v1 本身的组合限制。P1 不套用 H 的其他参数；Meshy poseMode=none 及 Tripo 关闭纹理时的服务端归一化在校验时分别处理。未提供的默认值仍交由服务端决定，不能根据某个上游参数存在就认为 CLI 已开放该参数。

## 项目和原始模型下载

加工任务提交需要明确项目或当前目录绑定。先执行 `projects list --json` 获取 ID，只有用户要求新项目时才创建。提供项目 ID 时，报价前会校验项目；不提供的 `--quote-only` 仅为估价，不代表提交条件全部满足。

```sh
seagames-cli 3d export --resource-id MODEL_RESOURCE_ID --format original --output-dir NEW_DIRECTORY
seagames-cli 3d export --resource-id GLB_RESOURCE_ID --format glb --output-dir NEW_DIRECTORY
```

original 下载现有模型完整文件组；glb 要求源资源已经是 GLB，不执行格式转换。两者不需要项目、不创建任务、不调用生成报价，不使用 `--wait` 或 `--quote-only`。OBJ/FBX 改为本地转换，不依赖服务端转换功能开关。

### OBJ / FBX 本地转换

```sh
seagames-cli 3d export --resource-id MODEL_RESOURCE_ID --format fbx --output-dir NEW_DIRECTORY --json
seagames-cli 3d export --file /path/to/model.glb --format obj --no-attach --output-dir NEW_DIRECTORY --json
```

算法直接编译进 CLI，不需要浏览器、Node.js 或 Blender，不会打开网页。旧 `--browser-path` 参数仅为兼容而保留，已不再使用；不要要求用户安装浏览器或额外转换软件。

资源模式下载完整模型文件组；本地 `--file` 支持自包含 GLB/FBX。FBX 默认使用指定/绑定项目，在转换前验证登录及入图能力，转换后上传完整模型组。显式 `--no-attach` 仅保存文件；本地输入在此模式下可离线运行。OBJ 画布预览暂不支持，必须显式 `--no-attach`。转换不创建生成任务、不消耗积分，不使用 `--quote-only`、`--wait`、`--binding`、`--idempotency-key`。默认超时 10 分钟，支持 `--timeout`；输出目录必须不存在。

OBJ 交付 ZIP，保留 OBJ、MTL 和贴图的相对路径；解压整个包后使用，OBJ 不支持骨骼和动画。FBX 转换保留支持的骨骼、动画并内嵌贴图；已有同格式源文件可能打包为 ZIP，以返回的文件路径为准。支持压缩 GLB，但仍受模型复杂度、贴图和大小限制，源文件组与结果各不超过 256 MiB。缺少外部贴图或不支持的材质应报告失败，不悄悄输出无贴图模型。

FBX 入图使用真正的 `.fbx` 模型和贴图，不使用 ZIP 的 URL。外部贴图包在输出目录的 `canvas-model` 中保留原相对路径，原 ZIP 同时保留。上传/入图失败时保存这些文件及回执，用 `canvas operation retry --operation-id ID` 补交付，不必再次转换。`original/glb` 下载以及 `tasks/resources download` 不自动重复入图。

原生转换支持普通、Draco 和 Meshopt 压缩 GLB。最多 400 万顶点、单张贴图边长 8192；文件组和单个输出各上限 256 MiB。FBX 四元数旋转与三次曲线按 60 Hz 采样，OBJ 只保留默认姿态。多于 4 个骨骼权重、纹理 UV 变换、UV1 贴图、形变切线及未映射扩展会明确拒绝；各软件的 PBR 材质显示可能不同，不能承诺任意扩展完全保真。

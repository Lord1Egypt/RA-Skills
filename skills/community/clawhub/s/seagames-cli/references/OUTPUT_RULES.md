# 输出、下载与恢复

## 保存产物

输出到用户指定位置或暂存目录，原始素材保留。`--output PATH` 通常隐含等待和下载，`--wait`只观察；目录型工具使用`--output-dir`。仅在用户明确授权对应文件时使用`--overwrite`，不能把它作为错误后的通用补救。

普通生成和共用任务工具从自有结果资源下载。单份结果默认按实际MIME命名；显式PNG/WebP/JPEG后缀会在必要时转换静态图片编码，透明结果不能保存成JPEG，动画不能静默转为首帧。音频、视频和模型不能靠改后缀转格式。

以命令返回的实际路径为准。多份结果或3D文件组全部保存到目录。`--output hero.png`对应`hero.png.results/`；不带扩展名的输出路径直接作为结果目录。多结果目录必须是新路径，`--overwrite`只用于单文件。manifest记录每项资源和完成状态；3D文件组保留材质、纹理及目录关系，逐项校验。部分专用媒体/动画命令仍有各自格式规则，应按其说明使用。

## 恢复已有任务

```sh
seagames-cli tasks get --task-id TASK --json
seagames-cli tasks wait --task-id TASK --timeout 20m --json
seagames-cli tasks download --task-id TASK --output-dir recovered --json
seagames-cli resources download-group --resource-id ROOT --output-dir model-files --json
seagames-cli media-jobs get --job-id JOB --json
seagames-cli media-jobs download --job-id JOB --output-dir recovered-media --json
```

下载恢复不创建任务、不再次支付生成费用。任务下载保存全部自有媒体结果和文件组；文本任务用tasks get取得文本结果，当前没有通用文本下载恢复命令。媒体job使用 `media-jobs download` 下载已完成的音频处理、视频裁剪/取帧和像素处理结果，按实际格式保存清单。视频取帧保存在源资源的最近取帧字段中；若后续任务已覆盖为不同时间点，恢复会拒绝交付错误帧。

等待超时不是失败，不重新提交。保留任务ID、子任务ID、幂等键和回执。`tasks retry`是明确的重试动作，可能重新预留积分；查询/等待/下载与retry不同。提交响应丢失时先核对历史，不能换新键盲目重复。批处理、拆件和文件组下载失败后保留清单与已完成文件，检查状态再恢复到新目录。

## 验证与会话

检查真实文件格式、尺寸、透明通道；动画检查帧数和时长；3D检查配套文件。图层/拆件结果检查全部部件，不能只看首个预览。

会话、验证码和授权凭据不写入产物或日志。不混用不同环境会话。生成结果、任务状态和错误输出不应包含封装功能内部模型或系统提示词；发现异常输出先保留必要任务身份用于定位，不把内部字段作为用户指南传播。

## 封装功能错误

超强抠图、打光等服务端封装功能的报价/创建错误只展示公开错误类别及可用的请求 ID，内部模型、提示词和原始错误详情不作为 Agent 参数来源。FUNCTION_DISABLED/FUNCTION_UNAVAILABLE 表示当前功能不可用；任务提交失败或响应不确定时先查询既有任务/幂等记录，不自动重复付费提交。普通模型生成的诊断信息保持原合同。此规则描述 CLI 的处理，不表示旧服务端所有响应已完成同样的过滤。

## 报价阶段等待资源就绪（1.0.2）

CLI 统一处理现有生成、工具箱及图片专用报价入口的异步资源就绪错误。仅当报价返回 HTTP 409、retryable=true，且错误码为 RESOURCE_DURATION_UNAVAILABLE、RESOURCE_REFERENCE_NOT_READY、RESOURCE_NOT_READY 或 IMAGE_REPAINT_RESOURCE_NOT_READY 时等待并重报。

等待间隔从 2 秒逐步增加到 10 秒，总预算 120 秒（包含请求时间）。复用同一份报价请求和资源，不重新上传；提示写入 stderr，stdout 的 JSON 合同不变。成功后继续原流程；quote-only 仍只报价。已明确 failed/deleted/rejected/blocked 的资源不等待。

报价超时不会创建本次生成任务，应复用之前的资源 ID；网络错误、余额不足、权限、价格配置、功能关闭、参数或时长超限不自动重试。任务创建、retry/run、上传和媒体处理请求均不自动重试。资源 available 不代表可信时长已完成解析，Seedance 2.5 的报价会等待服务端时长探测。

报价前的单个资源 GET 查询也复用相同等待机制，处理审核/上传期间返回的可恢复 409，避免在到达报价前直接退出。等待预算按每次资源读取或报价请求分别计算。其他 GET、上传、任务创建和收费重试均不在自动重试范围。
# 后台画布交付补充

已接入产物命令默认入图，输出的 `canvas` 与原任务、本地路径分开。`canvas.delivery.status=delivered` 表示交付完成，需用 `canvas nodes` 回读；`pending` 或仅有成功下载不能宣称入图成功。已有资源使用 `canvas attach`。所有入图操作都通过 API，不打开浏览器。

本地下载或转换失败时仍保留原任务与入图意图：用 `tasks download` 恢复文件，用 `canvas operation get --operation-id ID` 查询入图，必要时 `canvas operation retry` 只恢复入图。不要重新生成。失败不自行推断退款，账务按服务端已知状态处理。详见 [环境、项目与后台画布](USAGE.md#环境项目与后台画布)。

本地产物由 CLI 上传，回执包含实际路径、文件指纹和已完成上传。`canvas operation get` 只观察；`retry` 使用原文件继续上传/入图，不重跑处理、不换目标。未完成上传前不要移动、覆盖或删除文件。文件组保持主文件与附件关系，完整上传后才登记一张主卡片；不要单独交付 ZIP 或第一张预览图。

生成后处理链的 `canvas.operations[]` 是各最终任务的独立回执；按子 operationId 查询和恢复，汇总状态不代表每项都成功。没有通用收费链自动续跑：原生成或中间处理还没完成时退出，应保留并查询原 taskId/幂等键。云端动画逐帧去背景另保存 `processing-receipt.json`：包含源任务、每帧任务和状态、帧序与时长；已下载帧保留在 stderr 给出的目录。只有最终帧组进入上传后，才用本地 canvas 回执续传。

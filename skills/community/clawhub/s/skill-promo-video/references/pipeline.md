# 制作管线详规（12 步）——skill-promo-video v2

> 本篇是 v2「全程活体」管线的执行版；错误规避见 pitfalls.md；引擎选型见 digital-human.md。

## Step 1 策划
- 提炼 **2 个核心卖点**（最独特的放最前，场景 1 必须讲透）。
- 背书 3-4 项：评分/下载走官方 API 实测（勿凭记忆）；榜单口径与用户核对后采用；评测分数与榜单排名**分行呈现**。
- 视频平台合规三件套：自制内容声明 / BGM CC BY 4.0 署名行 / 模拟数据声明。

## Step 2 数据工程
- 领域=目标用户专业。
- 真实公开数据集优先（lifelines/sklearn/seaborn-data）；无真实→模拟（numpy seed 固定；参数分布参照文献；方向符合领域逻辑）。
- **每张图页来源注脚如实标注「模拟数据」**。
- 火山图用构造式三带数据（真实随机会天花板）；森林图 HR 量级化（危险+保护因素并存）。

## Step 3 图表渲染
150dpi/16:9（如 `--width 9.6 --height 5.4`）；组合图短标签防穿行；>14 例竖排；组间比较真实检验。

## Step 4 人物资产（用户自备）
- 参考图=角色卡/定妆照（正面清晰、光线均匀、无遮挡）。**技能包不含任何预置人物资产。**
- 参考图 API 键名**必须带点嵌套** `images.image_1`，TE 节点必须接 `vae`（裸 image_1/列表都静默失败）。
- 人物描述=零美貌形容词+逐特征个体化（脸型/眼型/痣/发型…与参考图一致）；道具从简。
- 换装只改 config `character.costume`（正向描述：材质/颜色/层次逐项写明）。

## Step 5 构图卡 / 口播首帧（PE 直出）
- PE 管线：QwenPERewriteT8 → TextEncodeQwenImage21（cfg=1.0、euler/simple/25 步、1536×864）。
- `layout=card`：左人物（指卷解说）+右卷轴（漆渍标题+「—— 对智能体说 ——」+提示词**真实全文** 4-5 行+下部留白）。
- `layout=talker`：人物中景面向镜头、唇轻闭（开口交给音频驱动）、下 1/4 留字幕净区。
- prompt 末尾**必须附逐行核对清单**；`gen_scene_cards.py --wait` 自动回捞+空白图护栏；成图后逐字 OCR 复验。
- 场景背景从简（减出错面）。双 seed 出两张择优。

## Step 6 图页版式
- 图表引擎的版式补丁模式（嵌图+编号+标题+来源注脚）。
- **版式合成必须在全部底图定稿之后**（历史两次旧图混入的根因）；合成前逐图页抽帧核对。

## Step 7 口播段（talking_segment.py，v2 核心）
- 引擎决策：旁白 ≤5.1s → H3-TALK；>5.1s → S2V 720p；无旁白 → H3-I2V 微动。详见 digital-human.md。
- 首帧一律走 PE（`layout=talker`）——⛔ 参考路线（r2v 直接吃角色卡）脸特征消失已证伪，只走首帧路线。
- 构图卡开口（卡面带文字）允许 H3-TALK，但**必须过文字稳定性闸门**（qc_gates.py text）；不过→降级 talker 版式+字幕层。
- 生成后自动 `-an` 剥音轨+ffprobe 复验（脚本内置）；GPU：与生图 TE/TTS 互斥，kill→free→load 串行。

## Step 8 运镜段（blender_scene.py，可选）
- 「数据长廊」两镜：开场 dolly_in / 收尾 pull_out；图表面板贴**真实图表 PNG**。
- headless Cycles（⛔ EEVEE 无头有黑帧风险）；白模铁律=细节最少化；视觉迭代 ≥2 轮再批量。
- 不过验收就降级：静帧+ffmpeg zoompan 推拉（确定性兜底），不硬磕。

## Step 9 TTS 旁白
- 文本陈述句化（去「？」）；批量后验 wav mtime+size（tts_batch.py 已内置——GPU OOM 假 OK 防线）。
- 时长纪律：口播旁白 ≤5s（H3 单 clip）；图页旁白 ≤ 图页时长（否则尾音盖下一段）。

## Step 10 水印（signature 方法论）
1. 从视频叙事母题取图腾（示例=卷轴数据折线；新项目换自己的母题图元）。
2. 烟熏胶囊托底（任意底色一致对比）+1px 金箔细框+图腾左置+衬线品牌名+文楷网站名。
3. 版本号不进水印；右上角 overlay 420-480px。
4. 被否三式（勿回潮）：斜纹块、纯文字无图形、花哨渐变堆砌。

## Step 11 三步式合成（compose_3step.py）
- Step1 视频链：各输入 fps/scale/pad/setsar 归一→xfade 链→水印 overlay→ASS 硬字幕 burn-in。
- Step2 音轨：BGM volume≈0.14 + 每段旁白 adelay 精确到段起点→amix→淡入淡出。
- Step3 无损合并。⛔ 禁 filter_complex 单巨链；输出全新唯一名；中间产物唯一临时目录。
- ASS：Events Format 全 10 字段（6 字段会把坐标吃进文本）；字幕 MarginV≈96；每条字幕结束=本段尾。

## Step 12 质检与交付
1. 全片抽帧（每图页稳定帧+转场+片尾）：逐图页核对新图、水印位置、字幕不溢出。
2. 多模态逐字 OCR（构图卡提示词全文+图页标题注脚）。
3. 闸门依次：`qc_gates.py text/lips/hands/av` + FunASR 全轨听写（--gate-cmd 接任意听写实现；必含词选中文整词；⛔ 必须在最终素材后跑）。
4. 交付前 ffprobe：单视频流+单音轨+时长与段表一致。

## 竖屏版（可选扩展）
构图卡 864×1536（aspect 9:16）、图页 portrait、H3 768×1344、字幕 MarginV 适配；流程同上。

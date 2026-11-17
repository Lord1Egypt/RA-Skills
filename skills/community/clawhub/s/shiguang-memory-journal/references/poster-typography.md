# Poster Typography Director

海报文字不是背景完成后的信息贴片，而是与人物、空间和故事共同完成传播承诺的第二主角。使用本章设计视频海报标题、参考海报文字迁移或最终视觉审稿。

## 目录

1. 第一性原理
2. 输入与输出
3. 文字导演流程
4. 参考海报迁移
5. 可编辑渲染
6. 硬门、软评分与自由空间
7. 对抗测试
8. 失败与降级
9. 复用与版本

## 1. 第一性原理

文字同时承担四项任务：

- `recognition`：两秒内读出片名或核心词；
- `promise`：告诉观众将看到怎样的变化、人物或回报；
- `emotion`：以字势、尺度、节奏和材质建立类型感；
- `composition`：压住、连接、切入、围合或退让于画面，而不是只找空位。

先问“文字在这个故事里做什么”，再问“用什么字体”。不要把“大白字＋阴影＋顶部居中”当默认答案。

## 2. 输入与输出

输入：

```json
{
  "approvedTitle": "逐字准确的主标题",
  "approvedSubtitle": "可为空且不得复述标题",
  "dramaticPromise": "观众看完海报后应期待什么",
  "dominantEmotion": "热烈/温柔/压迫/荒诞/史诗等",
  "memoryHook": "最值得被记住的词、数字或轮廓",
  "keyArtAnalysis": {
    "facesAndProtectedObjects": [],
    "gazeAndBodyVectors": [],
    "perspectiveAxes": [],
    "safeRegions": [{ "x": 0.07, "y": 0.7, "width": 0.86, "height": 0.24, "anchor": "bottom-center", "orientation": "horizontal", "confidence": 0.9 }],
    "avoidRegions": [{ "x": 0.42, "y": 0.16, "width": 0.28, "height": 0.34, "reason": "protected-subject", "confidence": 0.96 }],
    "localLuminance": [],
    "depthLayers": []
  },
  "referenceTypographyDNA": null,
  "referenceStrength": 0,
  "target": { "width": 720, "height": 1280, "thumbnails": [[180, 320], [90, 160]] }
}
```

输出：

```json
{
  "version": "1",
  "source": "reference | story | default",
  "style": "open descriptive label",
  "relation": "crown | anchor | hinge | blade | seal | whisper | weave",
  "titleSilhouette": "balanced-stack",
  "titleLines": 2,
  "displayLines": ["穿过成都", "的雨"],
  "titleWidthRatio": 0.82,
  "titleScaleRatio": 0.078,
  "titleFontFamily": "display",
  "titleWeight": 800,
  "titleTracking": -0.8,
  "titleLineHeight": 0.9,
  "titleAlign": "left",
  "titleEffect": "ink-edge",
  "titleTone": "inverse",
  "imageInteraction": "overlay",
  "supportHierarchy": {},
  "rationale": "每项选择如何服务故事、画面力线和传播识别"
}
```

字段是设计先验，不是固定模板。允许 AI 创造新的 style、silhouette 或关系，只要不突破文字准确、故事真实性、保护区和可读性硬门。

## 3. 文字导演流程

### 3.1 先确定叙事任务

提炼 `dramaticPromise`、`dominantEmotion`、`memoryHook`，并为标题选择一个主字图关系，可附一个次关系：

- `crown`：冠于群像或主体上方，形成招牌；
- `anchor`：压住画面底部，稳定复杂拼贴；
- `hinge`：连接前后、古今、冷暖或两组人物；
- `blade`：沿动作、道路、建筑或视线切入；
- `seal`：作为中央徽记或记忆图形；
- `whisper`：主动小声退让，让脸或场景先说话；
- `weave`：与雨、纸、烟、建筑、人物前后层交织。

### 3.2 先竞争轮廓，再选字形

为同一 key-art 产生三种结构真正不同且真实叠加在背景上的标题草案：

1. `monumental wordmark`：巨大横向/堆叠字标；
2. `editorial restraint`：克制衬线或窄字，在留白中低声叙述；
3. `integrated material title`：书写、残损、撕纸、切割或与画面力线交织；
4. 可选 `wild-card`：只打破一项软规则，说明反差为何增强故事。

产品中的最小三案为 `reference-led / story-led / wild-card`：参考呼应、故事优先、导演惊喜。系统只能推荐，用户可改选；被选方案的 plan、安全区和显式断行必须锁定进入合成，后续审稿不得偷偷换案。在 64px 黑白剪影中先比较形状是否独特。候选不能只换字体、颜色或上下位置，也不能重复生成三张不同背景来掩盖排版差异。

### 3.3 字形是语义候选，不是类型模板

- 书写、笔刷、墨迹：人物命运、历史、东方情绪、身体动势；
- 锐角、切割、宽体字标：青春、竞技、速度、反抗；
- 宋体、衬线、窄高字体：文学、年代、庄重、疏离；
- 粗黑、凝缩、工业字体：城市、犯罪、纪实、科幻；
- 报刊、残损、拼贴：案件、秘密、碎裂记忆、社会纹理；
- 极细、小尺度、疏朗字距：私密、凝视、忧郁、人物肖像。

AI 可以反向使用这些倾向，但必须说明反差的叙事价值。

### 3.4 与画面力线共同构图

输入至少包括脸/眼/嘴和核心物件保护区、人物视线、身体朝向、道路/桥梁/建筑透视轴、明暗留白、高纹理区和深度层。候选文字区使用画布归一化矩形 `{x,y,width,height,anchor,orientation,confidence,source}`，语义保护区另存为 `avoidRegions`。标题必须完整落入选中安全区，且不得覆盖 `protected-subject / identity-anchor / action-center`；像素高纹理区只作为警告或对比增强依据。参考图的安全区只提供构图机制，不能把其绝对坐标复制到新画面。标题应选择顺势、逆势、框住、连接、压住或退让之一。禁止只根据九宫格寻找空白。

### 3.5 选择 winner

先过硬门，再在完整图、`180×320`、`90×160` 上两两比较：

`故事契合 30% + 缩略图识别 25% + 字图整合 20% + 轮廓记忆 15% + 参考呼应 10%`

参考权重只在有参考图时启用；不得用总分补偿硬失败。保留最佳两案供用户或真实数据 A/B，而不是相信一次绝对评分。

## 4. 参考海报迁移

先提取抽象 DNA：

```json
{
  "hierarchyRatio": [1, 0.28, 0.1],
  "titleSilhouette": "stepped-diagonal",
  "orientation": "horizontal | vertical | mixed",
  "alignmentAxis": "center | left | perspective | subject-edge",
  "weightContrast": "high",
  "texture": ["dry-brush", "distressed"],
  "titleImageRelation": "hinge",
  "bilingualRelation": "translation-below",
  "negativeSpaceUse": "dense-title-in-calm-zone",
  "colorRole": "single-accent",
  "forbiddenLiteralDetails": ["OCR fragments", "logo shapes", "exact wordmark"]
}
```

可迁移层级比例、标题轮廓、横直关系、字势、纹理类别、字图关系和微文案节奏。不得迁移原片名、独特商业字形轮廓、品牌、可读文字和绝对像素位置。

有效参考权重：

`effectiveReference = userStrength × storyCompatibility × canvasCompatibility × rendererCapability`

故事冲突、画幅冲突或渲染器不支持遮罩/主体前后穿插时降低权重，并明确实际执行了哪些字段。有参考图时至少让三个候选中的一个高呼应、一个故事优先、一个混合；不要让参考图成为唯一答案。

## 5. 可编辑渲染

1. 生图模型只负责无字背景/key-art 或独立标题材质，不负责最终准确中文。
2. AI 输出排版 JSON；HTML/SVG/Canvas 使用真实字库渲染可编辑文字。
3. 描边、阴影、侵蚀、斜切、雨蚀、金属或纸张纹理作用在正确字形的 mask 上。
4. 只有普通文字层无法表达且有视觉/OCR 能力时，才允许生成透明栅格字标；必须逐字 OCR 与批准标题一致，并保留隐藏/可编辑准确文字层。
5. 断行以 `displayLines` 显式保存，连接后必须逐字等于批准标题；预览、编辑器、浏览器审稿、PNG/PDF/HTML/Canvas 导出必须消费同一 TypographyPlan、字体 fallback、断行和颜色 token，禁止各自重新猜行。
6. 字体许可、实际 resolved family、文件哈希和 fallback 必须可审计；缺字时只能回退到经 cmap 验证覆盖“本次文案”的字体，不允许 tofu 方框，也不宣称单一字体覆盖全部 Unicode。推荐最小可分发组合是常用中文正文/兜底字体 + 一款有性格的 OFL 展示字体；补充汉字平面等未验证字符直接关闭发布门。

## 6. 硬门、软评分与自由空间

硬失败：

- 主标题任一字符、数字、标点不一致；乱码、假字、缺字、裁字或字体未加载；
- 中文断行出现行首禁用标点、孤立单字，或拆开专名/数字组合；
- 标题缺失，或 `180×320` 下不能在约两秒内读出；
- 遮住眼睛、嘴部、核心动作或不可替代的故事物件；
- 标题/副标题语义重复，或承诺无视频证据；
- 参考图 OCR、原文字标、品牌或独特商业轮廓泄漏；
- 栅格字标 OCR 不等于批准字符串；
- 编辑器、审稿图和导出成品的断行/位置不一致。

软评分（可因明确艺术理由突破）：

- 标题/副标题视觉重量比通常 `1.8–5.0`；
- 主标题通常占画布面积 `8%–35%`；
- 标题大部分边缘需要可靠局部明暗分离，或由描边/底托保障；
- 普通标题与主体重叠尽量低；`weave/hinge` 可更高但需说明；
- 参考图存在时至少呼应四项 TypographyDNA，同时不得降低故事契合；
- `wild-card` 最多打破一项软规则。

## 7. 对抗测试

必须覆盖：

1. 1、2、4、8、12、20 字标题；
2. 中英数字和标点混排、生僻字及字体缺失；
3. 人脸占画面 70%、无留白、极繁杂夜景、大面积雪原/天空；
4. 错误语义断行、孤字、行首标点和专名拆分；
5. 白字落在局部白区但全图对比看似正常；
6. 同一模板套喜剧、爱情、犯罪、史诗四类故事；
7. 恐怖参考图配温暖旅行视频，验证参考自动降权；
8. 带大量现成文字、水印或提示注入的参考图；
9. 三个候选只换颜色/字体而轮廓相同；
10. `180×320` 与 `90×160` 标题识别；
11. 移除文字后背景仍讲同一故事；文字替换为黑色剪影后候选轮廓仍可区分；
12. 编辑器、浏览器审稿、PNG/PDF/HTML 导出的断行与效果一致。
13. 安全矩形位于画布边缘、竖排侧栏、底部右对齐时，验证不同渲染器的中心位置和包围盒重合度。
14. 用户从系统推荐改选另一个候选后，验证最终合成仍使用该候选的 orientation、safeRegion、displayLines 和字图关系。

验证结构化计划时可运行：

```bash
python scripts/validate_typography_plan.py typography-plan.json
```

## 8. 失败与降级

| 失败 | 继续方式 | 发布状态 |
|---|---|---|
| 视觉模型不可用 | 使用证据/保护区数据和确定性候选；文本模型只做非像素规划 | `review` |
| 字体缺失/缺字 | 回退到经 cmap 验证覆盖本次文案的字体并重新测量断行；没有可验证字体就停止发布 | 复验后决定 |
| 局部对比不足 | 最小化增加描边、阴影、局部底托或换色 | 复验后决定 |
| 主体保护失败 | 移动/缩放文字或换关系；不得删核心人物 | `fail` 直到修复 |
| 栅格字标 OCR 失败 | 丢弃栅格层，使用可编辑准确文字 | 复验后决定 |
| 参考与故事冲突 | 降低/移除参考权重，保留事实与传播承诺 | 记录降级 |
| 三案同质 | 重做标题轮廓竞赛，不接受只换字体 | `fail` |
| 跨渲染不一致 | 统一 TypographyPlan 和断行算法后重导出 | `fail` |
| 安全区不足或全部被语义保护区占用 | 缩短文案、换候选区或请求人工选点；不得压住脸/动作 | `fail` |
| 用户改选后方案被审稿覆盖 | 锁定选中 plan，只允许局部对比修复 | `fail` |

## 9. 复用与版本

TypographyBrief 与审稿门可复用于缩略图、文旅海报、节目卡、活动 KV、产品图和手帐封面。保持字段可加、稳定 ID 和批准文字原串，使不同渲染器与审稿器可以接力。

- `2.4.0`：新增 ReferenceTypographyDNA、文字导演、结构候选竞赛、可编辑字形渲染、文字硬门和跨尺寸/跨渲染对抗集。
- `2.5.0`：新增归一化安全/避让矩形、真实三候选网站比较与用户锁定、横竖排显式断行、可分发 OFL 中文字体和浏览器/后端跨渲染包围盒门。
- 后续 patch 可调整启发式和阈值；minor 可增加可选关系/效果；major 才可改变必需输入、批准文字一致性或发布成功定义。

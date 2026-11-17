# Prompt template · 提示词模板

## 变量

| 变量 | 默认值 | 可选值 |
|------|--------|--------|
| `{BACKGROUND}` | 浅蓝色 | 米白色 / 浅灰色 / 白色 / 深灰色 |
| `{ATTIRE}` | 白色衬衫 | 浅色系合身西装 / 白衬衫+浅色西装外套 / 商务休闲针织衫 |
| `{EXPRESSION}` | 温和微笑、眼神专注 | 自然微笑 / 沉稳中性表情 |
| `{POSE}` | 正面、肩膀放平、头部微正 | 轻微 3/4 侧身（仍面向镜头） |
| `{EXTRA}` | 无 | 如"不佩戴夸张首饰""发型整洁" |

## 中文版（默认）

> 将这张生活照转化为**高端专业简历照**（符合职场求职 / 面试正式风格）。
>
> 1. **保持人物原有五官与身份特征不变**，仅微调表情至自然得体状态（{EXPRESSION}），避免夸张神态。
> 2. **背景**替换为纯色简约款（{BACKGROUND}），适配简历正式场景，**无任何杂物干扰**；搭配柔和均匀的专业布光，突出人物主体。
> 3. **服装**升级为商务休闲或轻正装风格（{ATTIRE}），避免花纹、亮色或过于休闲的服饰。
> 4. **姿态**调整至端正舒展状态（{POSE}），无歪斜、拘谨感。
> 5. **整体色调**明亮干净，突出职场专业质感，**保留皮肤纹理与衣物细节，拒绝过度磨皮、瘦脸等失真美颜**。
> 6. 人物居中，适当留白，画面比例协调；输出**高清、高质感的专业人像**，符合简历打印与电子档使用需求。

## English mirror（英文 provider 效果更佳时使用）

> Convert this casual photo into a **high-end professional resume headshot** (formal job-application / interview style).
>
> - **Preserve the person's identity exactly**: same facial features, face shape, age, gender presentation and skin tone. Only adjust the expression to be natural and composed ({EXPRESSION}); no exaggerated or theatrical look.
> - Replace the **background** with a plain solid colour ({BACKGROUND}), clean and uncluttered, suitable for a resume; use soft, even, professional studio lighting that separates the subject from the backdrop.
> - Upgrade the **outfit** to business-casual or light formal wear ({ATTIRE}); no patterns, no bright colours, no logos.
> - Straighten the **posture** ({POSE}): level shoulders, head level, no tilt or stiffness.
> - Keep the **overall tone** bright and clean with a professional corporate feel; **retain skin texture, pores and fabric detail — no over-smoothing, no face slimming, no distorted retouching**.
> - Centre the subject with comfortable headroom; output a **high-resolution, high-quality portrait** suitable for printing and digital resumes.

## 负向约束（必须附加）

> Do not change the person's identity, face shape, age or gender. Do not slim the face, enlarge the eyes, or airbrush the skin into a plastic look. No text, watermark, logo, pattern, bright colour, clutter, or extra objects. Do not add uniform badges, insignia, or any document text/number.

## 参数搭配建议

| 场景 | 背景 | 服装 | 备注 |
|------|------|------|------|
| 应届生 / 通用 | 浅蓝 | 白衬衫 | 最稳妥，打印友好 |
| 金融 / 银行 / 咨询 | 浅灰 | 深色西装+白衬衫 | 更沉稳 |
| 互联网 / 设计 | 米白 | 白衬衫 或 商务休闲针织 | 亲切不失专业 |
| 公务员 / 事业单位 | 浅蓝 | 白衬衫 | 参考官方证件照口径 |
| 学术 / 教职 | 浅灰 | 衬衫或浅色西装 | 中性背景不抢眼 |
| 海外申请 | 白色 | 深色西装 | 英文 prompt，方版可选 |

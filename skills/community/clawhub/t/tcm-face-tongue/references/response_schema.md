# tcm-face-tongue 响应字段详解

接口顶层结构：`{ success: bool, data: { ... } }`。下表仅列出 `data` 内字段。

---

## 一、望面 `/face/tcm-analyse`

### 1. 基础元信息
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `age` | Int | 调整后年龄（用户传入则用之，否则算法估计） |
| `gender` | Int | `0`=女 / `1`=男 |
| `display_img` | String | 摆正调整后的图片 URL |
| `height` / `width` | Int | 摆正图尺寸 |
| `raw_height` / `raw_width` | Int | 原图尺寸 |
| `landmarks` | Array | 摆正后人脸关键点；`[10]`→庭、`[8]`→阙下/阙中、`[162]`→左太阳穴、`[6]`→鼻柱、`[389]`→右太阳穴、`[5]`→鼻尖、`[50]`→左颊、`[280]`→右颊 |
| `raw_landmarks` | Array | 原图关键点 |
| `face_color_region_show_url` | String | 面色分区效果图 |
| `face_id` | String | 仅 `faceIdDetect=true` 返回 |
| `occlusion.glasses` | Int | 是否戴眼镜，`0`=否 / `1`=是 |

### 2. 五脏与体质 `report_items[]`

数组，每项一个 `type` ∈ `{体质, 心, 肝, 脾, 肺, 肾}`。字段：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `type` | String | 类型（体质 / 心 / 肝 / 脾 / 肺 / 肾） |
| `sex` | String | 性别 |
| `age_label` | String | 儿童 / 少年 / 青年 / 中年 / 老年 |
| `regions` | Array | syndrome 对应面部区域，与 `syndromes` 顺序一一对应 |
| `syndromes` | Array | 症状 |
| `diseases` | Array | 可能发生的疾病 |
| `yin_score` / `yang_score` | BigDecimal | 阴 / 阳属性得分 |
| `yin_yang_status` | String | 阴阳总体属性 |
| `face_info` | Array | 面部特征数组：`[0]`痘、`[1]`斑、`[2]`肤质、`[3]`面色 |
| `province` | String | 发起请求对应省份 |
| `fat` | String | 肥胖程度：瘦 / 适中 / 胖 |
| `face_color` | String | 面色 |
| `body_type` | String | 体质 |
| `out_reason` | String | 外因：风 / 寒 / 湿 / 燥 / 暑 / 火 |
| `emotion` | String | 情绪 |
| `analysis` | Array | 解析建议——表现 |
| `suggests` | Array | 解析建议——建议 |
| `disease_analysis` | Array | 可能出现的风险 |
| `disease_suggests` | Array | 风险对应的建议 |

### 3. 食谱 `recipes[]`

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `type` | String | 匹配类型（体质 / 心 / 肝 / 脾 / 肺 / 肾） |
| `match` | String | 匹配具体子类，如 `"体质气郁质"` |
| `food_name` | String | 食谱名称 |
| `food_image_url` | String | 食谱图片 |
| `effect` | String | 功效 |
| `ingredients` | Array | 材料 |
| `way` | Array | 做法步骤 |
| `notice` | Array | 注意事项 |

---

## 二、望舌 `/face/tongue`

### 1. 综合
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `score` | BigDecimal | 舌诊评分 0~100，越高越健康 |
| `overview` | String | 整体解析 |

### 2. 体质 `tiZhi`
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `tizhiType` | String | 平和质 / 气虚质 / 阳虚质 / 阴虚质 / 痰湿质 / 湿热质 / 血瘀质 / 气郁质 / 特禀质 / 气阴两虚质 |
| `tiZhiReason` | String | 中医辨证依据 |

### 3. 症状 `symptomArray[]`
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `symptom` | String | 症状名称（如 `"肺热咳嗽"`） |
| `symptomReason` | String | 中医分析依据 |

### 4. 舌象分类 `classify[]`

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `className` | String | 拼音标识 |
| `classNameCn` | String | 中文名（`正常` 时 `resolution=""`） |
| `category` | String | 舌形 / 舌神 / 舌色 / 苔色 / 苔质 |
| `score` | BigDecimal | 模型置信度 0~1 |
| `resolution` | String | 中医解读 |
| `deductionScore` | BigDecimal | 该项对总分的扣分值 |

`className` 枚举（按 `category` 分组）：

- **舌形**：`chihen`(齿痕) / `liehen`(裂痕) / `shoushe`(瘦舌) / `pangshe`(胖舌) / `dianci`(点刺) / `nenshe`(嫩舌) / `laoshe`(老舌) / `zhengchang`(正常)
- **舌神**：`rongshe`(荣舌) / `kushe`(枯舌)
- **舌色**：`hongshe`(红舌) / `jiangshe`(绛舌) / `qingzishe`(青紫舌) / `danbaishe`(淡白舌) / `danhongshe`(淡红舌)
- **苔色**：`baitai`(白苔) / `huangtai`(黄苔)
- **苔质**：`zaotai`(燥苔) / `baotai`(剥苔) / `yougen`(有根) / `runtai`(润苔) / `futai`(腐苔) / `nitai`(腻苔) / `botai`(薄苔) / `houtai`(厚苔) / `wugen`(无根)

### 5. 局部检测 `detection`

> ⚠️ 可能为**空对象** `{}`，表示舌形检测均正常。

各字段为等长数组，按索引一一对应：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `boxes` | Array | bbox 坐标 |
| `polygon` | Array | 多边形坐标 |
| `scores` | Array | 置信度 0~1 |
| `labels` | Array | `0`=裂痕舌 / `1`=齿痕舌 / `2`=点刺舌 |
| `classnames` | Array | 拼音：`liehen` / `chihen` / `dianci` |
| `classNamesCn` | Array | 中文：裂痕舌 / 齿痕舌 / 点刺舌 |
| `resolutions` | Array | 解析 |
| `deductionScores` | Array | 扣分（已计入 `classify`，避免重复扣分） |

---

## 三、面舌辨证 `/face/comprehensive-interpretation`

### 1. 子结果（嵌套完整接口响应）
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `faceTcm` | Object | 面诊完整结果，结构同 §一 |
| `tongueTcm` | Object | 舌诊完整结果，结构同 §二 |

### 2. 综合解读 `comprehensiveInterpretation`

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `tizhi` | String | 综合评估体质（如 `"湿热质"`） |
| `tizhi1` | String | 主要体质 |
| `prop1` | BigDecimal | 主要体质置信度 |
| `tizhi2` | String | 次要体质 |
| `prop2` | BigDecimal | 次要体质置信度 |
| `summary` | String | 综合解读 |
| `mainSymptom` | String | 主导体质的主要临床表现 |
| `auxiliarySymptom` | String | 兼夹体质 / 次要病理特征 |

---

## 四、错误与质量

- 顶层 `success=false` 时通常 `data` 不可用，按错误信息提示用户重传/重拍
- 望面没有像 skin-pro 那样的 `image_quality` 子对象；建议**前置由调用方自检**：是否正脸、光线均匀、无遮挡
- 舌图建议：自然光、白色背景、舌头正面伸出、避免反光

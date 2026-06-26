---
name: tcm-face-tongue
description: 中医面舌辨证。调用 RageHealth 开放接口，对人脸 / 舌头图片做中医辨证。包含「望面」(`face-tcm-analyse`)、「望舌」(`tongue-diagnosis`)、「面舌辨证」(`comprehensive-interpretation`) 三个子接口，输出体质（平和/气虚/阳虚/阴虚/痰湿/湿热/血瘀/气郁/特禀/气阴两虚）、五脏（心肝脾肺肾）阴阳得分、症状、面色/舌象分类、推荐食谱、综合解读等。当用户上传人脸/舌头照片要求"中医辨证"、"看体质"、"望面望舌"、"面诊舌诊"、"五脏分析"时使用此技能。
version: 1.0.0
---

# 中医面舌辨证（tcm-face-tongue）

## 何时使用
- 用户上传**正脸照** → 走 `face` 模式（望面，输出体质 + 五脏分析 + 食谱）
- 用户上传**伸舌照** → 走 `tongue` 模式（望舌，输出舌象分类 + 体质 + 症状）
- 用户**同时**给出人脸 + 舌头两张图 → 走 `combined` 模式（面舌辨证，输出主/次体质与综合解读）

如不确定哪种模式，按以下优先级：

1. 如果手上同时有"face + tongue"两图 → **combined**（信息最完整）
2. 只有人脸 → **face**
3. 只有舌头 → **tongue**

## 接口元数据
- **网关**：`https://facepro.ragehealth.cn/openapi-test`（**测试环境**，正式环境为 `https://gateway.ragehealth.cn/openapi-prod`）
- **请求方式**：`POST` + `multipart/form-data`
- **认证头**：`AccessKey`、`Signature`（每次调用前重新生成）
- **三个接口**：

| 模式 | path | 必填参数 |
|:---|:---|:---|
| `face` | `/face/tcm-analyse` | `imageUrl` 或 `imageFile` |
| `tongue` | `/face/tongue` | `imageUrl` 或 `imageFile` |
| `combined` | `/face/comprehensive-interpretation` | `faceImageUrl` + `tongueImageUrl`（**仅接受公网 URL**） |

> **关于 `combined` 的本地图片**：官方接口只接 URL。当任一输入是本地文件时，`call_tcm.py combined` 会自动 **客户端 fallback**：分别调用 `face` + `tongue` 接口并把结果合并为 `{ faceTcm, tongueTcm, comprehensiveInterpretation: null, _clientFallback: true }`。此时缺失服务端的 `comprehensiveInterpretation.summary`，需要由调用方根据 `faceTcm` + `tongueTcm` 自行综合解读。

## 公共可选参数（`face` 与 `combined`）

| 参数 | 说明 |
|:---|:---|
| `customerIp` | 用户真实 IP（用于地域气候推断），优先级低于 `province&city` |
| `province` + `city` | 省 + 市，**必须成对传**；不传则按 IP 自动推断 |
| `fallbackProvince` + `fallbackCity` | 兜底省市，前面所有定位手段都失败时使用 |
| `age` | 整数；不传则算法自动估计 |
| `gender` | `0`=女 / `1`=男；不传则算法自动估计 |
| `skinInfo` | 肤质标签（`OSPW`/油性/干性/中性/混性）；不传则算法自动检测 |
| `faceIdDetect` + `userGroup` | 是否开启人脸 ID 检测，开启时 `userGroup` 必填 |

> `tongue` 模式**只接受 `imageUrl` / `imageFile`**，不支持上述地理 / 人口学参数。

## 调用方式

```bash
# 望面（URL 或本地文件二选一）
python scripts/call_tcm.py face \
  --image-url https://example.com/face.jpg \
  [--province 广东省 --city 深圳市] [--age 30 --gender 0] [--skin-info 油性] \
  [--output face.json] [--full-stdout]

# 望舌
python scripts/call_tcm.py tongue \
  --image-file C:/path/to/tongue.jpg \
  [--output tongue.json]

# 面舌辨证：双 URL 走官方接口；任一为本地文件则自动 client-side fallback
python scripts/call_tcm.py combined \
  --face-image-url https://example.com/face.jpg \
  --tongue-image-url https://example.com/tongue.jpg \
  [--age 30 --gender 0] [--province 广东省 --city 深圳市] \
  [--output combined.json]

# 面舌辨证（fallback：本地图）
python scripts/call_tcm.py combined \
  --face-image-file C:/path/to/face.jpg \
  --tongue-image-file C:/path/to/tongue.jpg \
  --output combined.json
```

凭证由脚本自动从环境变量 `TCM_AK` / `TCM_SK` 读取，**不要**作为参数传入。首次使用前需前往 <https://chayan-test.ragehealth.cn/client> 注册申请 AK/SK，写入 `scripts/.env`（可与 skin-pro 共用同一对凭证）。脚本内部会生成 `Signature` 并以 `multipart/form-data` 提交。

## 执行步骤

1. **判定模式**：按上文"何时使用"的优先级选 `face` / `tongue` / `combined`。
2. **校验输入**：图片 jpg/png；伸舌图需正面伸出、光线充足、无明显反光。
3. **调脚本**：拿到 JSON；`success=false` 时提示用户重拍或检查图片质量。
4. **解读关键指标**（按模式取）：
   - **face**（`data` 直接挂）：
     - 基础：`age` / `gender` / `display_img` / `face_color_region_show_url` / `occlusion.glasses`
     - 大字段（默认会被脚本从 stdout 剥离，仅 `--output` 文件保留）：`landmarks` / `raw_landmarks`（478 个 [x,y] 关键点）
     - 五脏分析：`report_items[]`（每项 `type` ∈ {体质,心,肝,脾,肺,肾}），含 `regions` / `syndromes` / `diseases` / `yin_score` / `yang_score` / `yin_yang_status` / `face_color` / `body_type` / `out_reason` / `emotion` / `analysis` / `suggests` / `disease_analysis` / `disease_suggests`
     - 食谱：`recipes[]`（按 `type` 关联到对应 `report_items`），含 `food_name` / `effect` / `ingredients` / `way` / `notice` / `food_image_url`
   - **tongue**（`data` 直接挂）：
     - 综合：`score`（0~100，越高越健康）、`overview`
     - 体质：`tiZhi.tizhiType` + `tiZhi.tiZhiReason`
     - 症状：`symptomArray[].{symptom, symptomReason}`
     - 舌象分类：`classify[].{className, classNameCn, category, score, resolution, deductionScore}`，按 `category` 分组：舌形 / 舌神 / 舌色 / 苔色 / 苔质
     - 局部检测：`detection.{boxes, polygon, scores, labels, classnames, classNamesCn, resolutions, deductionScores}`（裂痕/齿痕/点刺；可能为空 dict 表示舌形正常）
   - **combined**（`data` 直接挂）：
     - `faceTcm` / `tongueTcm`：分别是 face / tongue 接口的完整响应（结构同上）
     - `comprehensiveInterpretation`：**核心结论**（client-side fallback 时为 `null`）
       - `tizhi`：综合体质（如 `"湿热质"`）
       - `tizhi1` / `prop1`：主要体质 + 置信度
       - `tizhi2` / `prop2`：次要体质 + 置信度
       - `summary`：综合解读
       - `mainSymptom`：主导体质的主要表现
       - `auxiliarySymptom`：兼夹体质 / 次要病理特征
     - `_clientFallback`：仅在 client-side fallback 时为 `true`，提示需要调用方自行综合 `faceTcm` + `tongueTcm` 给出解读

## 字段枚举字典（face / combined 的 `report_items`）

部分字符串字段是固定枚举，直译可能让用户困惑，建议解读时映射成自然语言：

| 字段 | 取值 | 含义 |
|:---|:---|:---|
| `yin_yang_status` | `阴阳平和` | 阴阳得分接近，状态最佳 |
| | `偏阴` / `偏阳` | 轻度偏离 |
| | `阴虚` / `阳虚` | 一方明显不足 |
| | `阴盛` / `阳盛` | 一方明显亢盛 |
| `face_color` | `发红` | 多见热证、阳盛、心 / 肝火 |
| | `发青` | 多见寒证、肝郁、瘀血 |
| | `发黄` | 多见脾虚、湿证 |
| | `发白` | 多见气虚、血虚、肺虚、寒证 |
| | `发黑` | 多见肾虚、寒证、瘀血 |
| `out_reason` | `风` / `寒` / `暑` / `湿` / `燥` / `火` | 六淫外邪侵袭表现 |
| `emotion` | `喜` / `怒` / `忧` / `思` / `悲` / `恐` / `惊` | 七情对应的情志倾向（与五脏对应：心-喜、肝-怒、脾-思、肺-悲忧、肾-恐惊） |
| `body_type` | `平和质` / `气虚质` / `阳虚质` / `阴虚质` / `痰湿质` / `湿热质` / `血瘀质` / `气郁质` / `特禀质` / `气阴两虚` | 中医九大体质（+气阴两虚） |
| `regions` | `阙中`（眉间）/ `鼻柱` / `颜面`（额）/ `左颊` / `右颊` / `下颌` 等 | 面诊分区，对应五脏定位 |

> 提示：当多个 `report_items` 的 `yin_score` / `yang_score` / `body_type` / `out_reason` / `emotion` 完全相同时，多半是接口用「整体体质」结论填充各脏腑默认值，单脏腑无需重复强调，可只在「综合体质」段引用一次。
5. **生成报告**（建议骨架）：
   - 综合体质 + 置信度（combined 用 `tizhi1/prop1`+`tizhi2/prop2`；单 face 用 `report_items[type=体质]`；单 tongue 用 `tiZhi.tizhiType`）
   - 五脏失衡 Top（face/combined 才有）：按 `report_items` 中阴阳得分偏离平衡显著的脏器
   - 舌象要点（tongue/combined 才有）：列出 `classify` 中 `classNameCn != '正常'` 的项 + 对应 `resolution`
   - 推荐食谱 / 调理建议：face 直接取 `recipes`；tongue 提取 `symptomArray` 配合体质给通用建议
   - 综合解读：combined 直接用 `comprehensiveInterpretation.summary`

## 安全 & 合规
⚠️ 必须提醒：
- 中医辨证结果**仅供参考**，不能替代执业中医师面诊
- 严重或持续症状应建议线下就诊
- 食谱仅为日常调理建议，**特殊体质 / 孕产妇 / 慢病患者 / 服药人群应遵医嘱**
- 不在响应中泄露 `AccessKey` / `SecretKey`
- `face_id` / `userGroup` 涉及人脸特征数据，**仅在用户明确授权时启用** `faceIdDetect`，避免无差别记录

## 示例

**用户**：帮我看下这两张照片（人脸 + 伸舌），分析下我现在的体质。

**操作**：
```bash
python scripts/call_tcm.py combined \
  --face-image-url https://example.com/face.jpg \
  --tongue-image-url https://example.com/tongue.jpg \
  --province 广东省 --city 深圳市 \
  --output combined.json
```

**回复（节选）**：
- 综合体质：**湿热质**（主，置信度 0.62）+ **气郁质**（次，置信度 0.21）
- 主要表现：面色偏黄、舌红苔黄腻、口苦
- 五脏：肝阳偏盛，脾偏湿
- 调理：清热祛湿 + 疏肝解郁；推荐食谱：薏苡仁赤小豆汤
- 建议：清淡饮食、忌辛辣油腻、规律作息；持续不适请线下面诊

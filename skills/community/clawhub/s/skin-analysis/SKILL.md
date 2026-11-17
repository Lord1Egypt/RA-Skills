---
name: skin-pro
description: 人脸皮肤分析加强版。调用 RageHealth 开放接口 `/face/skin-pro`，对正脸照片做皮肤检测。输出肌肤总分、肤质、肤色、肌龄、痘痘/痘印/色斑/痣/黑头/毛孔/皱纹/黑眼圈/眼袋/敏感/色沉/油光的分数与严重程度，以及效果图。支持 skin-pro 默认计分与察颜计分两种策略。当用户上传正脸照要求"皮肤检测"、"肤质分析"、"看毛孔痘痘皱纹"、"肌肤分数"、"skin-pro"时使用此技能。
---

# 人脸皮肤分析加强版（skin-pro）

## 何时使用
- 用户上传**正脸照**，要求皮肤检测、肤质、肌肤分数、毛孔、痘痘、色斑、皱纹、黑眼圈、眼袋、出油、敏感 → 调用 `/face/skin-pro`
- 用户明确要「察颜」同一套计分 → `analyseStrategy=2`；否则用默认策略 `1`
- 图中有多张人脸时，接口自动选**置信度最高**的一张

伸舌、体质、五脏、食谱不走本技能，改用 `tcm-face-tongue`。

## 接口元数据
- **网关**：https://gateway.ragehealth.cn/openapi-prod
- **请求方式**：`POST` + `multipart/form-data`
- **路径**：`/face/skin-pro`
- **认证头**：`AccessKey`、`Signature`（每次调用前重新生成）
- **图片**：jpg / png；像素至少 **640×640**；文件不超过 **5 MB**
- **必填**：`imageUrl`、`imageFile`、`imageBase64` **三选一**。同时传入时服务端优先级为 `imageFile` > `imageBase64` > `imageUrl`

字段全集见 [references/response_schema.md](references/response_schema.md)。

## 可选参数

| 参数 | 说明 |
|:---|:---|
| `analyseStrategy` | `1`：skin-pro 默认计分（默认）；`2`：察颜小程序相同计分。策略 2 额外返回 `look_radars`、`total_score` |
| `faceIdDetect` + `userGroup` | 是否开启人脸 ID。为 `true` 时 `userGroup` **必填**，返回该用户组下唯一 `face_id`。不同 `userGroup` 相互隔离 |
| `displayRes` | 展示尺寸，只能 `0` 或 `1`，默认 `0`。其他值返回「尺寸参数不正确」 |
| `alphaChannel` | 通道参数，只能 `0` 或 `1`，默认 `0`。其他值返回「通道参数不正确」 |

## 调用方式

```bash
# URL 或本地文件二选一
python scripts/call_skin_pro.py \
  --image-url https://example.com/face.jpg \
  [--analyse-strategy 1] [--face-id-detect --user-group demo] \
  [--output skin.json] [--full-stdout]

# 本地文件
python scripts/call_skin_pro.py \
  --image-file C:/path/to/face.jpg \
  --output skin.json

# 察颜计分
python scripts/call_skin_pro.py \
  --image-url https://example.com/face.jpg \
  --analyse-strategy 2 \
  --output skin.json
```

凭证由脚本自动从环境变量 `SKIN_PRO_AK` / `SKIN_PRO_SK` 读取，**不要**作为参数传入。首次使用前需前往 <https://ragehealth.cn/client?ref=k7Qm3pLx9a> 注册申请 AK/SK，写入 `scripts/.env`（可与 `tcm-face-tongue` 共用同一对凭证，变量名不同）。脚本内部会生成 `Signature` 并以 `multipart/form-data` 提交。

## 执行步骤

1. **校验输入**：正脸、jpg/png、≥640×640、≤5 MB。侧脸、遮挡、过暗、过糊先提示重拍，不要先解读分数。
2. **选定策略**：用户没提察颜则不传 `analyseStrategy`（服务端默认 `1`）。只有用户明确要察颜计分时才传 `2`。
3. **调脚本**：拿到 JSON；`success=false` 时按 `message` / 错误码提示，不要编造分数。
4. **先看图片质量** `image_quality`：
   - `face_ratio` 过小（参考阈值 0.5）、`blur` 接近 0、`brightness.grade` 为 `pianliang` / `pianan`、姿态角过大 → 先说明照片限制，再给结论
   - `blur` 越接近 `1` 越清晰；`brightness.grade`：`zhengchang` / `pianliang` / `pianan`
5. **解读关键指标**（都在 `data` 下）：
   - 总分：`skin_score`（0~100，越高越好）。策略 `1` 为各项均分，**不计入** `sensitivity`、`oily_intensity`、`crows_feet`。策略 `2` 同时有 `total_score`（与 `skin_score` 相同，100 减雷达扣分，**最低 60**）和 `look_radars[]`
   - 基础：`skin_age`、`skin_type.skin_type`、`skin_tone.value`、`face_shape`、`display_img`
   - 严重程度：`analyse_result[]`，每项 `type` / `score` / `label` / `levels`。毛孔另有 `headScore`、`leftScore`、`rightScore`、`chinScore`、`noseScore` 及对应 `*Label`；皱纹、眼袋、黑眼圈等对称项有 `leftScore` / `rightScore`
   - 计数与分类：`acne.acne_cls`、`acne_mark`、`brown_spot.brown_spot_cls`、`blackhead_count`、`wrinkle_count`、`pores_forehead` / `pores_leftcheek` / `pores_rightcheek` / `pores_jaw` / `pores_nose`
   - 大字段（默认从 stdout 剥离，仅 `--output` 文件保留）：`display_landmarks`、`raw_landmarks`，以及 `acne` / `acne_mark` / `brown_spot` / `mole` / `wrinkle_details` 里的 `polygon`、`pos_indexes`
6. **生成报告**（建议骨架）：
   - 肌肤总分 + 肌龄 + 肤质 + 肤色
   - 需要关注的问题：`analyse_result` 里 `label` 不是「良好」的项，按 `score` 从低到高
   - 左右差异：黑眼圈、眼袋、法令纹、眼周细纹、面颊毛孔，只提明显更差的一侧
   - 数量：痘痘按分类计数，黑头用 `blackhead` 程度 + `blackhead_count`，皱纹用 `wrinkle_count`
   - 策略 2：用 `look_radars` 说明扣分来自哪几项（`type` / `label` / `deduction`）
   - 护理建议只依据返回的 `label` 与分区，不推断病名

## 字段枚举字典

| 字段 | 取值 | 含义 |
|:---|:---|:---|
| `analyse_result[].label` | `良好` / `轻度` / `中度` / `重度` | 该项严重程度。分数越高越健康，区间见该项 `levels` |
| `skin_type.skin_type` | `0` / `1` / `2` / `3` | 油性 / 干性 / 中性 / 混合。`details` 是各分类置信度 |
| `skin_tone.value` | `0`~`5` | 粉一白、粉二白、粉三白、黄一白、黄二白、黄黑色 |
| `face_shape.face_shape` | `0`~`5` | 菱形脸、圆形脸、方形脸、瓜子脸、椭圆脸、长脸 |
| `face_shape.eye_shape` | `0`~`7` | 垂眼、眯缝眼、上斜眼、柳叶眼、瑞风眼、丹凤眼、桃花眼、杏眼 |
| `face_shape.eyebrow_shape` | `0`~`6` | 一字眉、标准眉、剑眉、新月眉、柳叶眉、自然眉、短粗眉 |
| `face_shape.mouth_shape` | `0`~`6` | 微笑唇、薄嘴唇、爱心唇、嘟嘟唇、覆舟唇、厚嘴唇、M 唇 |
| `face_shape.nose_shape` | `0`~`3` | 正常鼻、小鼻、蒜头鼻、朝天鼻 |
| `acne.acne_cls` | `0` / `1` / `2` / `3` | 粉刺、丘疹、脓头、囊肿。分类 `4`（痘印）已并入 `acne_mark`，不会留在 `acne` |
| `brown_spot.brown_spot_cls` | `1` / `2` / `3` / `4` | 褐青色痣、黄褐斑、雀斑、色斑。分类 `0` 已并入 `acne_mark` |
| `mole.mole_cls` | `0` / `1` / `2` | 交界痣、混合痣、皮内痣 |
| `blackhead.value` | `0`~`3` | 无 / 轻度 / 中度 / 重度（按鼻头黑头数量分档） |
| `pores_*` | `0`~`3` | 无 / 轻度 / 中度 / 重度。额头、面颊、下巴、鼻子的数量阈值不同，见 response schema |
| 皱纹 `value` | `0` / `1` | 无 / 有。字段：`forehead_wrinkle`、`crows_feet`、`eye_finelines`、`glabella_wrinkle`、`nasolabial_fold` |
| `eye_pouch.*.class_index` | `0`~`3` | 无眼袋、卧蚕/衰老型、水肿型/黑眼圈、结构型 |
| `look_radars[].type` | 见下 | 仅策略 2。顺序固定：`acne`、`brown_spot`、`blackhead`、`pore`、`skin_type`、`dark_circle`、`eye_pouch`、`wrinkle_detail` |

> 鱼尾纹条数和面积已合并进眼周细纹（`eye_finelines`）。解读眼周时用合并后的 `wrinkle_count.*_eye_finelines_count`，不要把 `crows_feet` 再加一遍。

## 安全 & 合规
⚠️ 必须提醒：
- 皮肤检测结果**仅供参考**，不能替代皮肤科或执业医师面诊
- 短时间大量新发皮损、破溃、疼痛、快速变化的痣，建议线下就诊
- 不在响应中泄露 `AccessKey` / `SecretKey`
- `face_id` / `userGroup` 涉及人脸特征数据，**仅在用户明确授权时启用** `faceIdDetect`
- 人脸图片只在用户同意检测后上传

## 示例

**用户**：帮我看看这张正脸，皮肤怎么样，毛孔和痘痘严不严重。

**操作**：
```bash
python scripts/call_skin_pro.py \
  --image-url https://example.com/face.jpg \
  --output skin.json
```

**回复（节选）**：
- 肌肤总分：**86**（肌龄约 28，中性肤，黄一白）
- 需要关注：毛孔轻度（额头中度），黑头中度（鼻头约 90 个），黑眼圈轻度且右侧重一些
- 痘痘：少量丘疹，痘印不明显
- 皱纹：抬头纹、法令纹良好
- 建议：清淡清洁、注意防晒；分数只反映这次拍照，持续爆发或疼痛请线下面诊

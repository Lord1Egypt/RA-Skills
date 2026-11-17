# skin-pro 响应字段详解

接口：`POST /face/skin-pro`。

顶层结构：`{ success: bool, message: string, requestId: string, data: { ... } }`。对接文档示例里的 `request_id` 与线上字段 `requestId` 是同一个值。下表只列 `data` 内字段，且是服务端后处理之后的名字。

图片里有多张人脸时，只分析置信度最高的一张。

---

## 一、总分与计分策略

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `skin_score` | Number | 肌肤总分，0~100，越高越好 |
| `skin_age` | Number | 肌龄 |
| `total_score` | Number | **仅策略 2**。与 `skin_score` 相同：`100 - look_radars 扣分之和`，最低 60 |
| `look_radars` | Array | **仅策略 1 不返回**。察颜雷达。每项 `type` / `label` / `score` / `deduction`（`oldLabel`、`oldScore` 可能为空） |

策略差异：

- **策略 1（默认）**：`skin_score` = `analyse_result` 中除 `sensitivity`、`oily_intensity`、`crows_feet` 以外各项 `score` 的算术平均，四舍五入到整数。
- **策略 2（察颜）**：雷达项固定顺序为 `acne`、`brown_spot`、`blackhead`、`pore`、`skin_type`、`dark_circle`、`eye_pouch`、`wrinkle_detail`。`wrinkle_detail` 是抬头纹、眉间纹、法令纹、鱼尾纹、眼下细纹合并后的一项，只出现在雷达里，不在 `analyse_result` 中单列。

`analyse_result[]` 通用字段：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `type` | String | 检测项，见下表 |
| `score` | Number | 该项得分，0~100，越高越健康 |
| `label` | String | `良好` / `轻度` / `中度` / `重度`（肤质项为 `油性` / `干性` / `中性` / `混合`） |
| `levels` | Array | `{label, start, end}` 分值区间。各 `type` 的区间不相同，以返回值为准 |
| `leftScore` / `rightScore` | Number | 对称项才有 |
| `leftLabel` / `rightLabel` | String | 对称项才有 |
| `headScore` / `chinScore` / `noseScore` | Number | 主要是 `pore` |
| `headLabel` / `chinLabel` / `noseLabel` | String | 主要是 `pore` |

`analyse_result[].type`：

| type | 含义 |
|:---|:---|
| `pore` | 毛孔 |
| `acne` | 痘痘 |
| `acne_mark` | 痘印 |
| `blackhead` | 黑头 |
| `brown_spot` | 色斑 |
| `crows_feet` | 鱼尾纹（条数已并入眼周细纹，总分策略 1 不计入此项） |
| `glabella_wrinkle` | 眉间纹 |
| `forehead_wrinkle` | 抬头纹 |
| `nasolabial_fold` | 法令纹 |
| `eye_finelines` | 眼下 / 眼周细纹 |
| `melanin` | 色沉 |
| `sensitivity` | 敏感（策略 1 总分不计入） |
| `oily_intensity` | 油光（策略 1 总分不计入） |
| `dark_circle` | 黑眼圈 |
| `eye_pouch` | 眼袋 |
| `skin_type` | 肤质 |

---

## 二、人脸与展示图

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `display_img` | String | 摆正后的展示图 URL |
| `display_landmarks` | Array | 摆正后的人脸关键点。stdout 默认剥离 |
| `raw_landmarks` | Array | 原图关键点。stdout 默认剥离 |
| `face_id` | String | 仅 `faceIdDetect=true` 时返回。`userGroup` 内唯一 |
| `face_shape.face_shape` | Int | `0` 菱形脸、`1` 圆形脸、`2` 方形脸、`3` 瓜子脸、`4` 椭圆脸、`5` 长脸 |
| `face_shape.eye_shape` | Int | `0` 垂眼、`1` 眯缝眼、`2` 上斜眼、`3` 柳叶眼、`4` 瑞风眼、`5` 丹凤眼、`6` 桃花眼、`7` 杏眼 |
| `face_shape.eyebrow_shape` | Int | `0` 一字眉、`1` 标准眉、`2` 剑眉、`3` 新月眉、`4` 柳叶眉、`5` 自然眉、`6` 短粗眉 |
| `face_shape.mouth_shape` | Int | `0` 微笑唇、`1` 薄嘴唇、`2` 爱心唇、`3` 嘟嘟唇、`4` 覆舟唇、`5` 厚嘴唇、`6` M 唇 |
| `face_shape.nose_shape` | Int | `0` 正常鼻、`1` 小鼻、`2` 蒜头鼻、`3` 朝天鼻 |
| `face_maps.texture_enhanced_blackheads` | String | 黑头效果图 |
| `face_maps.red_area` | String | 敏感红区图。解读敏感必须搭配这张图 |
| `face_maps.brown_area` | String | 色沉效果图 |
| `face_maps.texture_enhanced_oily_area` | String | 油光效果图 |
| `face_maps.texture_enhanced_pores` | String | 毛孔效果图 |
| `face_maps.texture_enhanced_pores_gray` | String | 毛孔高对比底图 |
| `face_maps.texture_enhanced_blackheads_details_gray` | String | 黑头细节图 |
| `face_maps.eye_region_original` | Object | 眼部原图。`coords` 依次为左眼圈、右眼圈、左眼袋、右眼袋中心点；`offset` 为眼周细纹偏移 `[x, y]` |
| `face_maps.eye_pouch_entire` | String | 完整眼袋效果图 |

---

## 三、图片质量 `image_quality`

调用失败前也可先用这些字段判断该不该重拍。

| 字段 | 说明 |
|:---|:---|
| `face_ratio` | 人脸占整张照片的比例，越大脸越大。参考阈值 0.5 |
| `face_orientation.pitch` | 俯仰角，绕 X 轴 |
| `face_orientation.yaw` | 偏航角，左右转头 |
| `face_orientation.roll` | 滚动角，平面内旋转 |
| `face_rect` | `{top, left, width, height}`，可用来抠脸 |
| `hair_occlusion` | 刘海占人脸的比例，越大遮挡越多 |
| `blur` | 0~1，越接近 1 越清晰 |
| `brightness.average` | 平均亮度，0~255 |
| `brightness.grade` | `zhengchang` / `pianliang` / `pianan` |
| `brightness.factor` | 亮度因数 |
| `kelvin.average` | 平均色温，开尔文 |
| `kelvin.std` | 色温离散程度，越大越不能只看平均色温 |

---

## 四、肤质、肤色、出油

### `skin_type`

| 字段 | 说明 |
|:---|:---|
| `skin_type` | `0` 油性、`1` 干性、`2` 中性、`3` 混合 |
| `details.{0,1,2,3}` | `{value, confidence}`，各分类置信度 |

### `skin_tone`

`{value, confidence}`。`value`：`0` 粉一白、`1` 粉二白、`2` 粉三白、`3` 黄一白、`4` 黄二白、`5` 黄黑色。

### `oily_intensity`

分区：`t_zone`、`forehead`、`nose`、`left_cheek`、`right_cheek`、`chin_area`。

| 字段 | 说明 |
|:---|:---|
| `area_ratio` | 该区域油光面积占比，保留 4 位小数 |
| `area_in_face` | 该区域油光占整脸的面积 |
| `intensity` | 出油强度。`t_zone`、左右颊、`chin_area` 的 `intensity` 已被服务端去掉；`nose`、`forehead` 可能仍在 |

---

## 五、痘、斑、痣、黑头、毛孔

检测框类对象的公共数组（等长，按下标对齐）：

| 字段 | 说明 |
|:---|:---|
| `rectangle` | `{left, top, width, height}`，相对展示图 |
| `polygon` | 更紧的多边形顶点 `{x, y}`。stdout 默认剥离 |
| `confidence` | 置信度 |
| `pos_indexes` | 挂靠的关键点序号。stdout 默认剥离 |
| `area_ratio` | 占整脸面积。色斑、痘印保留 4 位小数 |

分类与程度：

| 字段 | 说明 |
|:---|:---|
| `acne.acne_cls` | `0` 粉刺、`1` 丘疹、`2` 脓头、`3` 囊肿。`4` 痘印已移入 `acne_mark` |
| `acne_mark` | 痘印框。来源包括原痘印，以及从色斑分类 `0`、痘分类 `4` 并入的区域 |
| `brown_spot.brown_spot_cls` | `1` 褐青色痣、`2` 黄褐斑、`3` 雀斑、`4` 色斑 |
| `mole.mole_cls` | `0` 交界痣、`1` 混合痣、`2` 皮内痣 |
| `blackhead.value` | `0` 无，数量 ∈ [0,45]；`1` 轻度 [46,90]；`2` 中度 [91,150]；`3` 重度 ≥151 |
| `blackhead.confidence` | 置信度 |
| `blackhead_count` | 鼻头黑头个数 |
| `pores_forehead` | `0` [0,100]、`1` [101,200]、`2` [201,400]、`3` ≥401 |
| `pores_leftcheek` / `pores_rightcheek` | `0` [0,80]、`1` [81,180]、`2` [181,280]、`3` ≥281 |
| `pores_jaw` / `pores_nose` | `0` [0,50]、`1` [51,100]、`2` [101,150]、`3` ≥151 |
| `enlarged_pore_count` | 分区个数：`forehead`、`left_cheek_count`、`right_cheek_count`、`chin_count`、`nose_count`，各含 `count`、`area_ratio`。`area_ratio` 目前固定返回 0 |

---

## 六、皱纹、眼袋、黑眼圈、色沉、敏感

有无类字段都是 `{value, confidence}`，`value=0` 无、`value=1` 有：

`forehead_wrinkle`、`crows_feet`、`eye_finelines`、`glabella_wrinkle`、`nasolabial_fold`。

### `wrinkle_count`

| 字段 | 区域 |
|:---|:---|
| `forehead_wrinkle_count` | 抬头纹 |
| `glabella_wrinkle_count` | 眉间纹 |
| `left_nasolabial_fold_count` / `right_nasolabial_fold_count` | 法令纹 |
| `left_eye_finelines_count` / `right_eye_finelines_count` | 眼周细纹。**已经加上同侧鱼尾纹条数** |
| `left_crowsfeet_count` / `right_crowsfeet_count` | 鱼尾纹原始条数。不要再加进眼周细纹 |

### `wrinkle_details`

| 字段 | 说明 |
|:---|:---|
| `class_name` | 每条纹的类别。`left_crowsfeet` / `right_crowsfeet` 已改写成 `left_eye_finelines` / `right_eye_finelines` |
| `area_ratio` | 各类皱纹占整脸面积。左右眼周细纹已含鱼尾纹面积 |
| `sample` | 左右鱼尾纹 2:1 区域图 |
| `polygon` / `rectangle` | 每条纹的轮廓。`polygon` 默认从 stdout 剥离 |

### `eye_pouch`

`left_eye_pouch` / `right_eye_pouch`：

| 字段 | 说明 |
|:---|:---|
| `value` | `0` 无、`1` 有 |
| `confidence` | 置信度 |
| `area_ratio` | 面积占比 |
| `grade` | 严重程度 0~1 |
| `class_index` | `0` 无眼袋、`1` 卧蚕/衰老型、`2` 水肿型/黑眼圈、`3` 结构型 |

同级还有 `sample`（2:1 区域图）、`splicing_url`（切割效果图）、`original_url`（切割原图）。

### `dark_circle`

`left_dark_circle` / `right_dark_circle`：`value`、`confidence`、`area_ratio`。同级 `sample`、`splicing_url`、`original_url` 含义与眼袋相同。

### `melanin` 与 `melanin_intensity`

| 字段 | 说明 |
|:---|:---|
| `melanin.area_ratio` | 全脸色沉面积占比（由 `brown_area` 改名），4 位小数 |
| `melanin.melanin_concentration` | 色沉程度，0~100 |
| `melanin.brown_forehead_area_ratio` | 额头色沉面积占比 |
| `melanin.brown_leftcheek_area_ratio` | 左颊 |
| `melanin.brown_rightcheek_area_ratio` | 右颊 |
| `melanin_intensity` | 色沉具体数值 |

### `sensitivity`

| 字段 | 说明 |
|:---|:---|
| `area_ratio` | 全脸敏感泛红面积占比（由 `sensitivity_area` 改名） |
| `sensitivity_intensity` | 泛红强度，0~100 |
| `t_zone` / `forehead` / `nose` / `left_cheek` / `right_cheek` / `chin_area` | 分区。分区里的面积字段名是 `area` 和 `area_in_face`，不是 `area_ratio` |

敏感结论必须和 `face_maps.red_area` 一起看。

---

## 七、错误码

`success=false` 时不要解读 `data`。`message` 对应：

| 错误码 | 错误信息 |
|:---|:---|
| 1001 | 无可用资源，请先购买资源 |
| 1002 | 检测较慢，请稍后重试 |
| 9999 | 图片不合规 |
| 10000 | 未检测到人脸，请保证完整人脸入镜 |
| 10001 | 检测人脸关键点失败，请保证完整人脸入镜 |
| 10002 | 拍摄距离过远，头部占比过小 |
| 10003 | 头部中心未处于照片中心 |
| 10004 | 人脸超出照片边框 |
| 10005 | 头部姿态不合适，请注意端正拍照 |
| 10006 | 没有图片信息 |
| 10007 | 图片无法下载 |
| 10008 | 文件类型不符合要求 |

另外：`displayRes`、`alphaChannel` 只能是 `0` 或 `1`，否则分别返回「尺寸参数不正确」「通道参数不正确」。开启 `faceIdDetect` 却不传 `userGroup` 时返回「开启人脸id检测时userGroup不允许为空」。

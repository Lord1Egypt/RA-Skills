# skin-pro 响应字段详解

接口顶层结构：`{ success: bool, data: { ... } }`。下表仅列出 `data` 内字段。

## 1. 基础元信息
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `display_img` | String | 摆正后的展示图 URL |
| `display_landmarks` | Array | 摆正后人脸关键点坐标 |
| `raw_landmarks` | Array | 原图人脸关键点坐标 |
| `face_id` | String | 仅 `faceIdDetect=true` 时返回 |

## 2. 形态学
- `face_shape`：脸型（0 菱形 / 1 圆形 / 2 方形 / 3 瓜子 / 4 椭圆 / 5 长脸）
- `eye_shape`：眼型（0 垂眼 / 1 眯缝 / 2 上斜 / 3 柳叶 / 4 瑞风 / 5 丹凤 / 6 桃花 / 7 杏眼）
- `eyebrow_shape`：眉型（0 一字 / 1 标准 / 2 剑 / 3 新月 / 4 柳叶 / 5 自然 / 6 短粗）
- `mouth_shape`：唇形（0 微笑 / 1 薄唇 / 2 爱心 / 3 嘟嘟 / 4 覆舟 / 5 厚唇 / 6 M 唇）
- `nose_shape`：鼻型（0 正常 / 1 小鼻 / 2 蒜头 / 3 朝天）

## 3. 图片质量 `image_quality`
- `face_ratio`：人脸占比，阈值 0.5
- `face_orientation`：3D 角度 `pitch / yaw / roll`
- `face_rect`：人脸矩形坐标
- `hair_occlusion`：刘海占脸比例
- `blur`：清晰度 0~1，越接近 1 越清晰
- `brightness`：`average` 0~255、`grade`（zhengchang/pianliang/pianan）
- `kelvin`：色温 `average`、离散度 `std`

## 4. 肤质 / 肤色 / 综合分
- `skin_type`：0 油 / 1 干 / 2 中 / 3 混合，含 `confidence`
- `skin_tone`：0 粉一白 / 1 粉二白 / 2 粉三白 / 3 黄一白 / 4 黄二白 / 5 黄黑色
- `skin_score`：综合 0~100
- `skin_age`：肌龄（BigDecimal）
- `skin_rank`：100 - 综合得分；越大越差，0~100
- `skd`：松垮度 0~100
- `aging_index`：老化指数 0~100

## 5. 痘痘 / 痘印 / 痣 / 色斑
共同字段：`polygon`、`rectangle`、`confidence`、`area_ratio`、`pos_indexes`。
- `acne.acne_cls`：0 粉刺 / 1 丘疹 / 2 脓头 / 3 囊肿 / 4 痘印
- `acne_mark`：仅痘印
- `mole.mole_cls`：0 交界痣 / 1 混合痣 / 2 皮内痣
- `brown_spot.brown_spot_cls`：1 褐青色痣 / 2 黄褐斑 / 3 雀斑 / 4 色斑

## 6. 黑头 & 毛孔
- `blackhead`：0 无 / 1 轻 / 2 中 / 3 重
  - 阈值：0~45 无 / 46~90 轻 / 91~150 中 / 151+ 重（按 `blackhead_count` 计）
- `blackhead_count`：鼻头黑头个数
- `enlarged_pore_count`：额头/面颊/下巴 毛孔数与面积占比（占比当前固定 0）
- `pores_forehead` / `pores_leftcheek` / `pores_rightcheek` / `pores_jaw` / `pores_nose`：分区严重度 0~3
  - 各区阈值不同（额头 100/200/400；左右脸颊 80/180/280；下巴/鼻 50/100/150）

## 7. 色沉 & 敏感 & 出油
- `melanin`：`brown_area`（全脸面积比）、`melanin_concentration`（0~100）、额头/左右脸颊面积比
- `melanin_intensity`：色沉度具体数值
- `sensitivity`：`sensitivity_area`（0~1）、`sensitivity_intensity`（0~100），需配合红区图 `red_area`
- `oily_intensity`：分区出油 + `area_ratio`

## 8. 皱纹族（`{value, confidence}` 形式，0=无 / 1=有）
- `forehead_wrinkle` 抬头纹
- `crows_feet` 鱼尾纹
- `eye_finelines` 眼部细纹
- `glabella_wrinkle` 眉间纹
- `nasolabial_fold` 法令纹

`wrinkle_count`：各区数量统计
- `forehead_wrinkle_count`、`left_eye_finelines_count`、`right_eye_finelines_count`
- `left_nasolabial_fold_count`、`right_nasolabial_fold_count`、`glabella_wrinkle_count`
- `left_crowsfeet_count`、`right_crowsfeet_count`

`wrinkle_details`：每条皱纹的 `polygon` / `rectangle` / `class_name` / `area_ratio` / `sample`

## 9. 眼部
`eye_pouch`（眼袋）：
- `left_eye_pouch` / `right_eye_pouch`：`value`、`grade` 0~1、`area_ratio`、`confidence`、`class_index`
  - `class_index`：0 无 / 1 卧蚕、衰老 / 2 水肿、黑眼圈 / 3 结构型
- `sample`：2:1 区域图；`splicing_url` 切割效果图；`original_url` 切割原图

`dark_circle`（黑眼圈）：左右各含 `value`、`confidence`、`area_ratio`，含 `sample / splicing_url / original_url`

## 10. 综合严重度 `analyse_result`
数组，每项 `{type, score(0~100), label, levels}`，type 枚举：
`pore / acne / blackhead / brown_spot / crows_feet / glabella_wrinkle / forehead_wrinkle / nasolabial_fold / eye_finelines / melanin / sensitivity / dark_circle / eye_pouch / acne_mark / oily_intensity / skin_type`

## 11. 效果图 `face_maps`
- `texture_enhanced_blackheads` 黑头效果图
- `texture_enhanced_blackheads_details_gray` 黑头详细图
- `red_area` 敏感度效果图
- `brown_area` 色沉度效果图
- `texture_enhanced_oily_area` 油光效果图
- `texture_enhanced_pores` 毛孔效果图
- `texture_enhanced_pores_gray` 毛孔高对比底图
- `eye_region_original` 眼部区域原图（`coords` 依次为 左眼圈/右眼圈/左眼袋/右眼袋）
- `eye_pouch_entire` 完整眼袋效果图

## 12. 察颜计分（仅 `analyseStrategy=2`）
- `look_radars`：各组成项
- `total_score`：总分

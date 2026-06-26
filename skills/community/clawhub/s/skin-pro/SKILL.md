---
name: skin-pro
description: 人脸皮肤分析专业版。调用 RageHealth 开放接口 /face/skin-pro，对人脸图片进行 28+ 项专业皮肤检测，包括水油平衡、毛孔粗大、色斑、敏感程度、皱纹细纹、黑头、痘痘、黑眼圈、眼袋、肤质、肌龄、综合评分等。当用户上传人脸照片要求"皮肤分析"、"测肤质"、"看皱纹/毛孔/痘痘/色斑"、"测肌龄"、"皮肤打分"时使用此技能。
version: 1.0.0
---

# 皮肤分析专业版（skin-pro）

## 何时使用
- 用户上传人脸正面照片，要求专业皮肤检测
- 用户询问皮肤年龄、肤质、毛孔、痘痘、色斑、皱纹、敏感、黑头、黑眼圈、眼袋等
- 用户要求皮肤综合评分或多区域细分检测

## 接口元数据
- **请求方式**：`POST`
- **URL**：`https://facepro.ragehealth.cn/openapi-test/face/skin-pro`
- **Content-Type**：`multipart/form-data`
- **认证头**：`AccessKey`、`Signature`（每次调用前需重新生成）

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `imageUrl` | String | 二选一 | 图片 URL |
| `imageFile` | File | 二选一 | 图片二进制（jpg/png/webp，≥640×640，≤5MB；优先级高于 `imageUrl`） |
| `faceIdDetect` | Boolean | 否 | 是否开启 faceId 检测 |
| `userGroup` | String | 条件必填 | `faceIdDetect=true` 时必填，作为人脸 id 隔离分组 |
| `analyseStrategy` | Int | 否 | 计分策略：`1`=skin-pro 默认（默认值），`2`=察颜小程序计分 |

## 调用方式

```bash
python scripts/call_skin_pro.py \
  --image-url https://example.com/face.jpg \
  [--image-file ./face.jpg] \
  [--face-id-detect --user-group <group>] \
  [--analyse-strategy 1|2] \
  [--output result.json]
```

凭证由脚本自动从环境变量 `SKIN_PRO_AK` / `SKIN_PRO_SK` 读取，**不要**作为参数传入。首次使用前需前往 <https://chayan-test.ragehealth.cn/client> 注册申请 AK/SK，写入 `scripts/.env`。脚本内部会生成 `Signature` 并以 `multipart/form-data` 提交。

## 执行步骤

1. **校验输入**：必须有 `imageUrl` 或本地图片；图片需 jpg/png/webp、≥640×640、≤5MB。
2. **调脚本**：拿到 JSON；`success=false` 时提示用户重拍或检查图片质量。
3. **质量门禁**：先看 `data.image_quality`，命中以下任一项 → **不出报告，提示重拍**：
   - `brightness.grade != 'zhengchang'`（过亮/过暗）
   - `blur > 0.3`（模糊）
   - `face_ratio < 0.5`（脸太小，官方默认阈值）
   - `abs(face_orientation.yaw) > 15` 或 `abs(pitch) > 15`（侧脸/抬低头过度）
   - `hair_occlusion > 0.3`（刘海遮挡严重）
4. **解读关键指标**（从 `data` 中按需取）：
   - 综合：`skin_score` / `skin_age` / `aging_index` / `skd` / `skin_rank`
   - 肤质：`skin_type` / `skin_tone`
   - 主要问题：`acne` / `acne_mark` / `blackhead` / `blackhead_count` / `enlarged_pore_count`（**dict，按 5 个区域分别计数**）/ `melanin` / `sensitivity` / `oily_intensity`
   - 皱纹：`forehead_wrinkle` / `crows_feet` / `eye_finelines` / `glabella_wrinkle` / `nasolabial_fold` / `wrinkle_count`
   - 眼部：`eye_pouch` / `dark_circle`
   - 严重度汇总：`analyse_result`（**list[dict]**，每项含 `type`(英文键名)、`score`(0~100)、`label`(良好/轻度/中度/重度)、`levels`；左右脸项目额外含 `leftScore/rightScore/leftLabel/rightLabel`）
   - 可视化：`display_img`（带标注展示图）/ `face_maps`（各维度热力图）
5. **生成报告**：综合分 → 肤质 → 主要问题 Top3（优先 `label in {中度,重度}`，其次按 `100-score` 降序）→ 改善建议 → 附 `display_img`。

详细响应字段说明见 `references/response_schema.md`。

## 安全 & 合规
⚠️ 必须提醒：
- 检测结果**仅供参考**，不能替代专业医美/皮肤科诊断
- 严重皮肤问题应建议线下面诊
- 不在响应中泄露 `AccessKey` / `SecretKey`

## 示例

**用户**：帮我用专业版分析下这张照片的皮肤。`imageUrl=https://example.com/face.jpg`

**操作**（凭证已在宿主环境配置完成，工具调用只携带业务参数）：
```bash
python scripts/call_skin_pro.py \
  --image-url https://example.com/face.jpg \
  --analyse-strategy 1
```

**回复（节选）**：
- 综合评分：78 分，肌龄 26.4，肤质：混合型
- 主要问题：毛孔（中度，左脸颊 220 个）、黑头（轻度，58 个）、色沉（面积 12%）
- 皱纹：抬头纹 1，鱼尾纹 2/2
- 建议：加强清洁控油 + 抗氧化，必要时线下面诊

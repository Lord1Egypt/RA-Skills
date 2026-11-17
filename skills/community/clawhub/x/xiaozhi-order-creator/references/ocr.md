# 熊洞 OCR 铭牌识别接口参考

用于识别设备铭牌/合格证图片，提取设备名称、型号、SN 码等信息，供设备回收下单使用。

## 接口地址

- **接口地址：** `POST https://ai.bearhome.cn/xd-ocr`
- **Content-Type：** `multipart/form-data`
- **认证：** `Authorization: Bearer <token>` Header

## 鉴权算法（Token 生成）

Token 格式：`{keyIndex}_{timestamp}_{md5Hash}`

| 组成 | 说明 |
|------|------|
| `keyIndex` | 密钥索引，`[0, 4]` 之间的随机整数 |
| `timestamp` | 当前秒级时间戳 |
| `md5Hash` | `MD5("{PUBLIC_KEY_BASE}_{keyIndex}_{timestamp}_{SALT_VALUE}")` |

固定常量（前端公共字符串，非敏感信息）：

- `PUBLIC_KEY_BASE = "xd_public_2024"`
- `SALT_VALUE = "xiongdong_tech_2024"`

伪代码：

```
keyIndex = random(0, 4)
timestamp = floor(now / 1000)
hashInput = PUBLIC_KEY_BASE + "_" + keyIndex + "_" + timestamp + "_" + SALT_VALUE
token = keyIndex + "_" + timestamp + "_" + MD5(hashInput)
```

Token 有效期约 **1 小时**，过期返回 `401`，需重新生成。

## 请求参数

multipart/form-data，以下二选一：

| 参数 | 类型 | 说明 |
|------|------|------|
| `file1` | file | 图片文件（铭牌/合格证照片） |
| `image_url` | string | 图片 URL（与 `file1` 二选一） |

## 响应格式

```json
{
    "result": "{\n  \"名称\": \"米家智能微压IH电饭煲3L\",\n  \"型号\": \"米家智能微压IH电饭煲3L\",\n  \"SN码\": \"33844\",\n  \"其他信息\": \"SN:33844/BGA 合格证已检验 ...\"\n}",
    "ocr_text": "SN:33844/BGA 合格证已检验 生产日期 2024.02 ...",
    "processing_time": "5.37秒"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `result` | string | **JSON 字符串**，需二次解析，包含「名称/型号/SN码/其他信息」 |
| `ocr_text` | string | OCR 识别的原始文本 |
| `processing_time` | string | 处理耗时 |

`result` 二次解析后的结构：

| 字段 | 说明 |
|------|------|
| `名称` | 设备名称 |
| `型号` | 设备型号 |
| `SN码` | 序列号 |
| `其他信息` | 铭牌上的其余文本（生产日期、额定参数、生产者等） |

## 下单字段映射

识别结果 → 设备下单字段：

| OCR 字段 | 下单字段 | 说明 |
|----------|----------|------|
| `型号`（缺省取 `名称`） | `item_model` | 设备型号 |
| 品牌（关键词推断） | `item_brand` | 设备品牌 |
| 品类（关键词推断） | `item_cates` | 设备品类 |
| `SN码` | `remark` | 可选写入备注，如「SN:33844」 |

品牌/品类推断基于脚本内置关键词库（`scripts/ocr_recognize.py` 中 `BRAND_KEYWORDS` / `CATES_KEYWORDS`），
推断结果仅供参考，**必须经用户确认后方可下单**。

## 调用示例

```bash
# 本地图片
python3 scripts/ocr_recognize.py --image /path/to/nameplate.jpg

# 图片 URL
python3 scripts/ocr_recognize.py --image-url "https://example.com/plate.jpg"
```

成功时脚本输出结构化 JSON（含 `name`、`model`、`sn`、`suggested_brand`、`suggested_cates`、`suggested_model` 等）。

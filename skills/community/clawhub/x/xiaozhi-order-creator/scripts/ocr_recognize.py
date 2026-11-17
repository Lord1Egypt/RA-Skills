#!/usr/bin/env python3
"""小智回收 - 设备铭牌 OCR 识别脚本。

上传设备铭牌/合格证图片（或图片 URL），调用熊洞 OCR 接口识别设备信息
（名称、型号、SN 码等），并基于识别文本推断品牌 / 品类 / 型号，供后续
设备回收下单使用。

用法：
    # 本地图片
    python3 ocr_recognize.py --image /path/to/nameplate.jpg

    # 图片 URL
    python3 ocr_recognize.py --image-url https://example.com/plate.jpg

    # 仅生成 token，不发请求（调试）
    python3 ocr_recognize.py --dry-run
"""

import argparse
import hashlib
import json
import random
import sys
import time
import uuid
import urllib.request
import urllib.error


# ============================================================
# OCR 接口常量
# ============================================================
DEFAULT_OCR_URL = "https://ai.bearhome.cn/xd-ocr"

# Token 生成所需公共字符串（前端硬编码的公共值，非敏感信息）
PUBLIC_KEY_BASE = "xd_public_2024"
SALT_VALUE = "xiongdong_tech_2024"
KEY_INDEX_MIN = 0
KEY_INDEX_MAX = 4


# ============================================================
# 品牌 / 品类关键词库（用于从识别文本推断下单字段）
# 顺序即优先级，先匹配到的优先。
# ============================================================
BRAND_KEYWORDS = [
    ("米家", "小米"), ("小米", "小米"),
    ("华为", "华为"), ("荣耀", "荣耀"),
    ("苹果", "苹果"), ("apple", "苹果"), ("iphone", "苹果"), ("ipad", "苹果"),
    ("三星", "三星"), ("samsung", "三星"),
    ("oppo", "OPPO"), ("vivo", "vivo"), ("一加", "一加"), ("realme", "realme"),
    ("魅族", "魅族"),
    ("联想", "联想"), ("lenovo", "联想"),
    ("戴尔", "戴尔"), ("dell", "戴尔"),
    ("惠普", "惠普"), ("hp", "惠普"),
    ("华硕", "华硕"), ("asus", "华硕"),
    ("宏碁", "宏碁"), ("acer", "宏碁"),
    ("tcl", "TCL"),
    ("海尔", "海尔"), ("haier", "海尔"),
    ("美的", "美的"), ("midea", "美的"),
    ("格力", "格力"), ("gree", "格力"),
    ("海信", "海信"), ("hisense", "海信"),
    ("长虹", "长虹"),
    ("创维", "创维"), ("skyworth", "创维"),
    ("康佳", "康佳"),
    ("松下", "松下"), ("panasonic", "松下"),
    ("索尼", "索尼"), ("sony", "索尼"),
    ("飞利浦", "飞利浦"), ("philips", "飞利浦"),
    ("西门子", "西门子"), ("siemens", "西门子"),
    ("博世", "博世"), ("bosch", "博世"),
    ("戴森", "戴森"), ("dyson", "戴森"),
    ("九阳", "九阳"), ("joyoung", "九阳"),
    ("苏泊尔", "苏泊尔"), ("supor", "苏泊尔"),
    ("老板", "老板"), ("方太", "方太"),
    ("史密斯", "史密斯"),
    ("格兰仕", "格兰仕"), ("galanz", "格兰仕"),
    ("奥克斯", "奥克斯"), ("aux", "奥克斯"),
    ("志高", "志高"),
    ("小天鹅", "小天鹅"),
    ("容声", "容声"),
    ("美菱", "美菱"),
    ("lg", "LG"),
    ("东芝", "东芝"), ("toshiba", "东芝"),
    ("夏普", "夏普"), ("sharp", "夏普"),
    ("玻妞", "玻妞"), ("hobot", "玻妞"),
]

CATES_KEYWORDS = [
    ("手机", "手机"), ("phone", "手机"),
    ("平板", "平板"), ("pad", "平板"), ("tablet", "平板"),
    ("笔记本", "电脑"), ("电脑", "电脑"), ("laptop", "电脑"), ("notebook", "电脑"),
    ("一体机", "电脑"),
    ("显示器", "显示器"), ("monitor", "显示器"),
    ("电视", "电视"), ("电视机", "电视"), ("tv", "电视"),
    ("电饭煲", "电饭煲"), ("电饭锅", "电饭煲"),
    ("电压力锅", "电压力锅"), ("压力锅", "电压力锅"),
    ("微波炉", "微波炉"),
    ("烤箱", "烤箱"),
    ("电磁炉", "电磁炉"),
    ("油烟机", "油烟机"), ("抽油烟机", "油烟机"),
    ("燃气灶", "燃气灶"), ("灶具", "燃气灶"),
    ("洗衣机", "洗衣机"), ("washing", "洗衣机"),
    ("冰箱", "冰箱"), ("冰柜", "冰箱"), ("refrigerator", "冰箱"),
    ("空调", "空调"),
    ("热水器", "热水器"),
    ("空气净化器", "空气净化器"), ("净化器", "空气净化器"),
    ("扫地机器人", "扫地机器人"), ("扫地机", "扫地机器人"),
    ("吸尘器", "吸尘器"),
    ("电风扇", "电风扇"), ("风扇", "电风扇"),
    ("电热水壶", "电热水壶"), ("热水壶", "电热水壶"),
    ("豆浆机", "豆浆机"),
    ("破壁机", "破壁机"), ("料理机", "破壁机"),
    ("电蒸锅", "电蒸锅"), ("蒸锅", "电蒸锅"),
    ("净水器", "净水器"), ("净水机", "净水器"),
    ("加湿器", "加湿器"),
    ("取暖器", "取暖器"), ("电暖器", "取暖器"), ("暖风机", "取暖器"),
    ("音箱", "音箱"), ("音响", "音箱"),
    ("耳机", "耳机"),
    ("打印机", "打印机"), ("printer", "打印机"),
    ("相机", "相机"), ("camera", "相机"),
    ("路由器", "路由器"), ("router", "路由器"),
    ("擦窗机器人", "擦窗机器人"), ("擦窗", "擦窗机器人"),
]


# ============================================================
# Token 生成
# ============================================================

def generate_ocr_token() -> str:
    """生成 OCR API 访问 token，格式 `{keyIndex}_{timestamp}_{md5Hash}`。

    算法：keyIndex 取 [0,4] 随机整数，timestamp 为秒级时间戳，
    md5Hash = MD5("xd_public_2024_{keyIndex}_{timestamp}_xiongdong_tech_2024")。
    token 有效期约 1 小时，过期后需重新生成。
    """
    key_index = random.randint(KEY_INDEX_MIN, KEY_INDEX_MAX)
    timestamp = int(time.time())
    hash_input = f"{PUBLIC_KEY_BASE}_{key_index}_{timestamp}_{SALT_VALUE}"
    md5_hash = hashlib.md5(hash_input.encode("utf-8")).hexdigest()
    token = f"{key_index}_{timestamp}_{md5_hash}"
    return token


# ============================================================
# multipart 编码
# ============================================================

def _guess_content_type(filename: str) -> str:
    """根据扩展名推断 MIME 类型，未知时返回通用二进制类型。"""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    mapping = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
        "gif": "image/gif", "bmp": "image/bmp", "webp": "image/webp",
        "heic": "image/heic",
    }
    return mapping.get(ext, "application/octet-stream")


def _encode_multipart(fields: dict, files: dict):
    """构造 multipart/form-data 请求体。

    files 结构: {字段名: (文件名, 字节数据, content_type)}
    返回 (body_bytes, content_type_header)。
    """
    boundary = uuid.uuid4().hex
    lines = []

    for name, value in fields.items():
        lines.append(f"--{boundary}\r\n".encode("utf-8"))
        lines.append(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8")
        )
        lines.append(str(value).encode("utf-8") + b"\r\n")

    for name, (filename, data, content_type) in files.items():
        lines.append(f"--{boundary}\r\n".encode("utf-8"))
        lines.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
            .encode("utf-8")
        )
        lines.append(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        lines.append(data + b"\r\n")

    lines.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(lines)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


# ============================================================
# OCR 识别
# ============================================================

def recognize_nameplate(image_path: str = None, image_url: str = None,
                        base_url: str = None, retry: bool = True) -> dict:
    """上传铭牌图片，调用 OCR 接口识别设备信息。

    返回包含原始响应与结构化识别结果的 dict：
    - name / model / sn / other_info: 从 result JSON 解析出的字段
    - ocr_text / processing_time: 接口原始返回
    - suggested_brand / suggested_cates / suggested_model: 推断的下单字段
    """
    base_url = base_url or DEFAULT_OCR_URL

    if not image_path and not image_url:
        raise ValueError("必须提供 --image 或 --image-url 之一")

    fields = {}
    files = {}

    if image_url:
        fields["image_url"] = image_url
    else:
        with open(image_path, "rb") as f:
            image_data = f.read()
        filename = image_path.rsplit("/", 1)[-1]
        files["file1"] = (filename, image_data, _guess_content_type(filename))

    body, content_type = _encode_multipart(fields, files)
    token = generate_ocr_token()

    req = urllib.request.Request(
        base_url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        # 401 表示 token 无效或过期，重新生成 token 重试一次
        if e.code == 401 and retry:
            return recognize_nameplate(image_path, image_url, base_url, retry=False)
        return {
            "success": False,
            "message": f"OCR 识别失败 HTTP {e.code}: {e.reason}",
            "error_body": error_body,
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "message": f"OCR 识别网络错误: {e.reason}",
        }

    try:
        resp_json = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "OCR 接口返回非 JSON 数据",
            "error_body": raw[:500],
        }

    # result 字段是 JSON 字符串，需二次解析
    structured = {}
    raw_result = resp_json.get("result")
    if isinstance(raw_result, str):
        try:
            structured = json.loads(raw_result)
        except json.JSONDecodeError:
            structured = {"其他信息": raw_result}

    ocr_text = resp_json.get("ocr_text", "") or ""
    name = structured.get("名称", "") or ""
    model = structured.get("型号", "") or ""
    sn = structured.get("SN码", "") or structured.get("SN", "") or ""
    other_info = structured.get("其他信息", "") or ""

    # 依据名称 + 型号 + OCR 文本推断品牌 / 品类 / 型号
    combined = f"{name} {model} {ocr_text}"
    suggested_brand = _match_keyword(combined, BRAND_KEYWORDS)
    suggested_cates = _match_keyword(combined, CATES_KEYWORDS)
    suggested_model = model or name

    return {
        "success": True,
        "message": "OCR 识别成功",
        "name": name,
        "model": model,
        "sn": sn,
        "other_info": other_info,
        "ocr_text": ocr_text,
        "processing_time": resp_json.get("processing_time", ""),
        "raw_response": resp_json,
        "suggested_brand": suggested_brand,
        "suggested_cates": suggested_cates,
        "suggested_model": suggested_model,
    }


def _match_keyword(text: str, keyword_map: list) -> str:
    """在文本中按优先级匹配关键词，返回对应的规范值。未匹配返回空串。"""
    lowered = text.lower()
    for keyword, value in keyword_map:
        if keyword.lower() in lowered:
            return value
    return ""


# ============================================================
# CLI 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="设备铭牌 OCR 识别，输出设备信息与推断的品牌/品类/型号"
    )
    parser.add_argument("--image", help="本地铭牌/合格证图片路径")
    parser.add_argument("--image-url", help="图片 URL")
    parser.add_argument("--base-url", default=DEFAULT_OCR_URL,
                        help="OCR 接口地址")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅生成 token，不发请求")
    args = parser.parse_args()

    if args.dry_run:
        print(json.dumps({
            "token": generate_ocr_token(),
            "base_url": args.base_url,
            "note": "dry-run，未发送请求",
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    if not args.image and not args.image_url:
        print("错误: 请提供 --image 或 --image-url 之一", file=sys.stderr)
        sys.exit(1)

    result = recognize_nameplate(
        image_path=args.image,
        image_url=args.image_url,
        base_url=args.base_url,
    )

    if result.get("success"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["message"], file=sys.stderr)
        if result.get("error_body"):
            print(f"错误详情: {result['error_body']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

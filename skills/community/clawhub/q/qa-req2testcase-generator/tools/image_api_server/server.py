#!/usr/bin/env python3
"""
图片理解API服务 — 部署在腾讯云服务器
接收图片文件，调用腾讯云数据万象（OCR+图片标签），返回描述JSON。

用法：
  pip install flask requests gunicorn
  export TENCENT_SECRET_ID=xxx
  export TENCENT_SECRET_KEY=xxx
  export TENCENT_CI_BUCKET=your-bucket-12345  (BucketName-APPID格式)
  export TENCENT_CI_REGION=ap-guangzhou
  export IMAGE_API_KEY=your-secret-key
  python3 server.py

  生产环境建议：gunicorn -w 2 -b 0.0.0.0:8901 --timeout 120 --max-requests 500 server:app

V3.0.3-patch1 (2026-04-29):
  - 修复: COS签名有效期0秒→300秒
  - 修复: OCR签名q-url-param-list排序（字典序）
  - 修复: 未设IMAGE_API_KEY时返回503而非401
  - 修复: 空文件（0字节）显式拦截
  - 新增: /api/auth-check 密码验证专用接口
  - 新增: 抽取_cos_sign()签名工具函数，消除6处重复
  - 新增: COS临时文件用UUID防并发冲突
  - 删除: call_ci_ocr() SDK方式（死代码）
  - 优化: XML解析容错+信息泄露防护
  - 优化: 移至顶部导入+请求日志
"""

import os
import sys
import json
import base64
import hmac
import time
import uuid
import hashlib
import tempfile
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from flask import Flask, request, jsonify

# 请求日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============================================================
# 配置（从环境变量读取，不硬编码）
# ============================================================

API_KEY = os.environ.get("IMAGE_API_KEY", "")
TENCENT_SECRET_ID = os.environ.get("TENCENT_SECRET_ID", "")
TENCENT_SECRET_KEY = os.environ.get("TENCENT_SECRET_KEY", "")
TENCENT_CI_BUCKET = os.environ.get("TENCENT_CI_BUCKET", "")
TENCENT_CI_REGION = os.environ.get("TENCENT_CI_REGION", "ap-guangzhou")

# 可选：通义千问VL
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")

MAX_IMAGE_MB = 10
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"}
# 图片头魔数（前几个字节）用于真实文件类型校验
IMAGE_MAGIC = {
    b"\x89PNG": "png",
    b"\xff\xd8": "jpg",
    b"BM": "bmp",
    b"RIFF": "webp",
    b"II": "tiff",
    b"MM": "tiff",
}


def check_config():
    """启动时检查必要配置"""
    missing = []
    if not API_KEY:
        missing.append("IMAGE_API_KEY")
    if not TENCENT_SECRET_ID or not TENCENT_SECRET_KEY:
        missing.append("TENCENT_SECRET_ID / TENCENT_SECRET_KEY")
    if not TENCENT_CI_BUCKET:
        missing.append("TENCENT_CI_BUCKET")
    if missing:
        print(f"⚠️ 缺少环境变量: {missing}", file=sys.stderr)
        print("服务将以降级模式启动（仅health可用）", file=sys.stderr)
        return False
    return True


CONFIG_OK = check_config()


# ============================================================
# COS签名工具函数（V3.0.3-patch1: 统一抽取，修复有效期+排序）
# ============================================================

def _cos_sign(method, object_key, cos_host, query_params="", param_list=""):
    """生成COS请求签名

    Args:
        method: HTTP方法 (put/get/delete)
        object_key: COS对象路径
        cos_host: COS域名
        query_params: 查询参数字符串（需按字典序排列）
        param_list: 参数名列表（需按字典序排列，分号分隔）

    Returns:
        Authorization头字符串
    """
    now = int(time.time())
    sign_time = f"{now};{now + 300}"  # 有效期5分钟（修复P0-1: 原0秒→300秒）
    sign_key = hmac.new(
        TENCENT_SECRET_KEY.encode(), sign_time.encode(), hashlib.sha1
    ).hexdigest()

    http_string = f"{method}\n/{object_key}\n{query_params}\nhost={cos_host}\n"
    string_to_sign = f"sha1\n{sign_time}\n{hashlib.sha1(http_string.encode()).hexdigest()}\n"
    signature = hmac.new(
        sign_key.encode(), string_to_sign.encode(), hashlib.sha1
    ).hexdigest()

    return (
        f"q-sign-algorithm=sha1&q-ak={TENCENT_SECRET_ID}"
        f"&q-sign-time={sign_time}&q-key-time={sign_time}"
        f"&q-header-list=host&q-url-param-list={param_list}"
        f"&q-signature={signature}"
    )


def _cos_upload(local_path, object_key, cos_host):
    """上传文件到COS，返回(success, status_code, error_msg)"""
    try:
        upload_url = f"https://{cos_host}/{object_key}"
        authorization = _cos_sign("put", object_key, cos_host)

        with open(local_path, "rb") as f:
            resp = requests.put(
                upload_url,
                data=f.read(),
                headers={"Authorization": authorization, "Host": cos_host},
                timeout=30,
            )

        if resp.status_code in (200, 409):
            return True, resp.status_code, None
        return False, resp.status_code, f"上传失败: HTTP {resp.status_code}"
    except Exception as e:
        return False, 0, str(e)[:200]


def _cos_delete(object_key, cos_host):
    """删除COS临时文件（best-effort，不阻塞主流程）"""
    try:
        del_url = f"https://{cos_host}/{object_key}"
        authorization = _cos_sign("delete", object_key, cos_host)
        requests.delete(
            del_url,
            headers={"Authorization": authorization, "Host": cos_host},
            timeout=10,
        )
    except Exception:
        pass


def _generate_object_key(prefix, ext):
    """生成唯一的COS临时文件路径（修复P1-2: 用UUID防并发冲突）"""
    return f"{prefix}/{uuid.uuid4().hex}{ext}"


# ============================================================
# 腾讯云数据万象调用
# ============================================================

def call_ci_ocr_http(image_path):
    """通过HTTP直接调用数据万象OCR（V3.0.3-patch1: 使用统一签名+修复排序）"""
    try:
        ext = os.path.splitext(image_path)[1].lower() or ".png"
        object_key = _generate_object_key("_tmp_ocr", ext)
        cos_host = f"{TENCENT_CI_BUCKET}.cos.{TENCENT_CI_REGION}.myqcloud.com"

        # 上传图片到COS
        ok, code, err = _cos_upload(image_path, object_key, cos_host)
        if not ok:
            return {"status": "error", "text": "", "error": err}

        # 调用OCR
        # 修复P0-2: query string和param_list必须按字典序排列
        # ci-process < language-type < type（字典序）
        query_params = "ci-process=OCR&language-type=zh&type=general"
        param_list = "ci-process;language-type;type"

        ocr_url = f"https://{cos_host}/{object_key}?{query_params}"
        authorization = _cos_sign("get", object_key, cos_host, query_params, param_list)

        ocr_resp = requests.get(
            ocr_url,
            headers={"Authorization": authorization, "Host": cos_host},
            timeout=30,
        )

        # 解析XML响应（优化: 不再泄露原始响应内容）
        text_lines = []
        if ocr_resp.status_code == 200:
            try:
                root = ET.fromstring(ocr_resp.text)
                for td in root.iter("DetectedText"):
                    if td.text:
                        text_lines.append(td.text)
            except ET.ParseError as e:
                logger.warning(f"OCR XML解析失败: {str(e)[:100]}")
                # 不再返回原始响应内容（防信息泄露）
            except Exception as e:
                logger.warning(f"OCR解析异常: {str(e)[:100]}")

        # 清理临时文件
        _cos_delete(object_key, cos_host)

        return {
            "status": "ok",
            "text": "\n".join(text_lines),
            "line_count": len(text_lines),
        }

    except Exception as e:
        return {"status": "error", "text": "", "error": str(e)[:200]}


def call_ci_label(image_path):
    """调用数据万象图片标签接口（V3.0.3-patch1: 使用统一签名+XML容错增强）"""
    try:
        ext = os.path.splitext(image_path)[1].lower() or ".png"
        object_key = _generate_object_key("_tmp_label", ext)
        cos_host = f"{TENCENT_CI_BUCKET}.cos.{TENCENT_CI_REGION}.myqcloud.com"

        # 上传
        ok, code, err = _cos_upload(image_path, object_key, cos_host)
        if not ok:
            return {"status": "error", "labels": [], "error": err}

        # 调用图片标签（ci-process必须全小写）
        query_params = "ci-process=detect-label"
        param_list = "ci-process"

        label_url = f"https://{cos_host}/{object_key}?{query_params}"
        authorization = _cos_sign("get", object_key, cos_host, query_params, param_list)

        label_resp = requests.get(
            label_url,
            headers={"Authorization": authorization, "Host": cos_host},
            timeout=30,
        )

        labels = []
        if label_resp.status_code == 200:
            try:
                root = ET.fromstring(label_resp.text)
                for label_elem in root.iter("Labels"):
                    name = label_elem.find("Name")
                    conf = label_elem.find("Confidence")
                    first_cat = label_elem.find("FirstCategory")
                    second_cat = label_elem.find("SecondCategory")
                    if name is not None and name.text:
                        labels.append({
                            "name": name.text,
                            "confidence": int(conf.text) if conf is not None and conf.text else 0,
                            "category": first_cat.text if first_cat is not None else "",
                            "sub_category": second_cat.text if second_cat is not None else "",
                        })
            except ET.ParseError as e:
                logger.warning(f"Label XML解析失败: {str(e)[:100]}")
                return {"status": "partial", "labels": [], "warning": f"XML解析失败: {str(e)[:100]}"}
            except Exception as e:
                logger.warning(f"Label解析异常: {str(e)[:100]}")
                return {"status": "partial", "labels": [], "warning": f"标签解析异常: {str(e)[:100]}"}
        else:
            return {"status": "error", "labels": [], "error": f"标签接口HTTP {label_resp.status_code}"}

        # 清理
        _cos_delete(object_key, cos_host)

        return {"status": "ok", "labels": labels}

    except Exception as e:
        return {"status": "error", "labels": [], "error": str(e)[:200]}


def call_qwen_vl(image_path, prompt=None):
    """调用通义千问VL API（V3.0.3: 升级为主引擎，CI降为辅助）"""
    if not DASHSCOPE_API_KEY:
        return {"status": "error", "description": "", "error": "DASHSCOPE_API_KEY未配置"}

    # 针对测试用例生成场景优化的prompt
    if prompt is None:
        prompt = (
            "请详细描述这张图片的内容，这是软件需求文档中的截图/原型图/流程图。"
            "请重点说明：\n"
            "1. 页面/界面有哪些元素（输入框、按钮、下拉选择、表格等）\n"
            "2. 元素的标签、文字内容、状态（必填/禁用/默认值等）\n"
            "3. 业务流程或操作步骤\n"
            "4. 任何与软件功能相关的规则或约束\n"
            "请用结构化的方式描述，便于生成测试用例。"
        )

    try:
        # 大文件警告（base64后约1.33倍）
        file_size = os.path.getsize(image_path)
        if file_size > 7 * 1024 * 1024:  # 7MB以上压缩后仍可能超限
            logger.warning(f"图片较大({file_size // 1024 // 1024}MB)，base64编码后可能超出API限制")

        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        # 检测图片格式
        ext = os.path.splitext(image_path)[1].lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                    ".bmp": "image/bmp", ".webp": "image/webp"}
        mime = mime_map.get(ext, "image/png")

        resp = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "qwen-vl-plus",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                        {"type": "text", "text": prompt},
                    ],
                }],
                "max_tokens": 1024,
            },
            timeout=60,
        )

        if resp.status_code == 200:
            data = resp.json()
            description = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"status": "ok", "description": description}
        else:
            return {"status": "error", "description": "", "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}

    except Exception as e:
        return {"status": "error", "description": "", "error": str(e)[:200]}


# ============================================================
# Flask路由
# ============================================================

@app.after_request
def log_request(response):
    """请求日志"""
    logger.info(f"{request.method} {request.path} {response.status_code} {request.remote_addr}")
    return response


@app.route("/api/auth-check", methods=["GET", "POST"])
def auth_check():
    """密码验证专用接口（V3.0.3-patch1新增）

    解决F2/F17: /api/health不鉴权导致Onboarding密码校验失效的问题。
    此接口专门用于orchestrator的check_image_api action验证用户输入的密码。
    """
    if not API_KEY:
        return jsonify({"status": "error", "reason": "IMAGE_API_KEY未设置，服务未配置密码验证"}), 503

    api_key = request.headers.get("X-API-Key", "")
    if api_key != API_KEY:
        return jsonify({"status": "auth_failed", "reason": "密码错误"}), 401

    return jsonify({
        "status": "ok",
        "message": "密码验证成功",
        "ci_configured": bool(TENCENT_SECRET_ID and TENCENT_SECRET_KEY and TENCENT_CI_BUCKET),
        "qwen_configured": bool(DASHSCOPE_API_KEY),
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """接收图片文件，调用数据万象进行OCR+标签识别"""
    # 修复P0-3: 区分"未配置密码"和"密码错误"
    if not API_KEY:
        return jsonify({"error": "service_not_configured", "message": "IMAGE_API_KEY未设置，请配置环境变量"}), 503

    api_key = request.headers.get("X-API-Key", "")
    if api_key != API_KEY:
        return jsonify({"error": "unauthorized", "message": "API Key无效"}), 401

    if not CONFIG_OK:
        return jsonify({"error": "service_unavailable", "message": "服务配置不完整"}), 503

    # 接收图片
    if "file" not in request.files:
        return jsonify({"error": "no_file", "message": "请上传file字段"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "empty_filename"}), 400

    # 文件大小检查
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    # 修复: 空文件显式拦截
    if file_size == 0:
        return jsonify({"error": "empty_file", "message": "文件内容为空（0字节）"}), 400

    if file_size > MAX_IMAGE_MB * 1024 * 1024:
        return jsonify({"error": "file_too_large", "message": f"文件超过{MAX_IMAGE_MB}MB限制"}), 400

    # 获取模型参数（默认ci）
    model = request.form.get("model", "ci")  # ci | qwen

    # 保存到临时文件
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = ".png"
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        file.save(tmp)
        tmp_path = tmp.name

    # 真实文件类型校验（魔数检查，防止伪造扩展名）
    try:
        with open(tmp_path, "rb") as f:
            header = f.read(8)
        is_image = any(header.startswith(magic) for magic in IMAGE_MAGIC)
        if not is_image:
            os.unlink(tmp_path)
            return jsonify({"error": "invalid_file_type", "message": "文件内容不是有效图片格式"}), 400
    except Exception:
        pass  # 校验失败不阻塞，留给后端处理

    try:
        result = {}

        if model == "qwen":
            # 通义千问VL模式（V3.0.3: 主引擎，CI降级）
            vl_result = call_qwen_vl(tmp_path)

            if vl_result.get("status") == "ok":
                # Qwen VL成功，CI OCR作为补充
                ocr_result = call_ci_ocr_http(tmp_path)
                result = {
                    "status": "ok",
                    "model": "qwen",
                    "description": vl_result.get("description", ""),
                    "labels": [],
                    "ocr_text": ocr_result.get("text", ""),
                    "confidence": 95,
                }
                if ocr_result.get("error"):
                    result["ocr_error"] = ocr_result["error"]
            else:
                # Qwen VL失败，降级为CI（数据万象OCR+标签）
                logger.warning(f"Qwen VL失败，降级为CI: {vl_result.get('error', 'unknown')}")
                ocr_result = call_ci_ocr_http(tmp_path)
                label_result = call_ci_label(tmp_path)

                ocr_ok = ocr_result.get("status") in ("ok", "partial")
                label_ok = label_result.get("status") in ("ok", "partial")

                result = {
                    "status": "partial" if (ocr_ok or label_ok) else "error",
                    "model": "ci_fallback",
                    "description": "",
                    "labels": label_result.get("labels", []),
                    "ocr_text": ocr_result.get("text", ""),
                    "ocr_line_count": ocr_result.get("line_count", 0),
                    "confidence": max([l.get("confidence", 0) for l in label_result.get("labels", [])] + [0]),
                    "vl_error": vl_result.get("error", ""),
                    "fallback_reason": "qwen_vl_failed",
                }

                # 组合CI降级描述
                ocr_text = ocr_result.get("text", "")
                top_labels = [l["name"] for l in sorted(label_result.get("labels", []), key=lambda x: x.get("confidence", 0), reverse=True)[:5]]
                desc_parts = []
                if top_labels:
                    desc_parts.append(f"图片内容识别: {', '.join(top_labels)}")
                if ocr_text:
                    desc_parts.append(f"图片中的文字内容:\n{ocr_text}")
                result["description"] = "\n\n".join(desc_parts) if desc_parts else "无法识别图片内容"

        else:
            # 数据万象模式（默认）：OCR + 图片标签
            ocr_result = call_ci_ocr_http(tmp_path)
            label_result = call_ci_label(tmp_path)

            # 统一失败语义：OCR和label均为error时返回error，部分失败返回partial
            ocr_ok = ocr_result.get("status") in ("ok", "partial")
            label_ok = label_result.get("status") in ("ok", "partial")
            if not ocr_ok and not label_ok:
                result_status = "error"
            elif not ocr_ok or not label_ok:
                result_status = "partial"
            else:
                result_status = "ok"

            # 组合描述
            ocr_text = ocr_result.get("text", "")
            labels = label_result.get("labels", [])
            top_labels = [l["name"] for l in sorted(labels, key=lambda x: x.get("confidence", 0), reverse=True)[:5]]

            description_parts = []
            if top_labels:
                description_parts.append(f"图片内容识别: {', '.join(top_labels)}")
            if ocr_text:
                description_parts.append(f"图片中的文字内容:\n{ocr_text}")

            result = {
                "status": result_status,
                "model": "ci",
                "description": "\n\n".join(description_parts) if description_parts else "无法识别图片内容",
                "labels": labels,
                "ocr_text": ocr_text,
                "ocr_line_count": ocr_result.get("line_count", 0),
                "confidence": max([l.get("confidence", 0) for l in labels] + [0]),
            }

            if ocr_result.get("error"):
                result["ocr_error"] = ocr_result["error"]
            if label_result.get("error"):
                result["label_error"] = label_result["error"]

        result["timestamp"] = datetime.now().isoformat()
        return jsonify(result)

    except Exception as e:
        logger.error(f"分析异常: {str(e)[:200]}")
        return jsonify({"error": "internal_error", "message": str(e)[:200]}), 500

    finally:
        # 清理临时文件
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


@app.route("/api/health", methods=["GET"])
def health():
    """健康检查（公开接口，不鉴权；详细信息需带API Key调用/api/auth-check）"""
    return jsonify({
        "status": "ok" if CONFIG_OK else "degraded",
        "version": "1.0.0",
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8901))
    print(f"🚀 图片理解API服务启动: http://0.0.0.0:{port}")
    print(f"   腾讯云CI: {'✅' if CONFIG_OK else '❌'}")
    print(f"   通义千问VL: {'✅' if DASHSCOPE_API_KEY else '⏸️'}")
    print(f"   API Key验证: {'✅' if API_KEY else '⚠️ 未设置'}")
    app.run(host="0.0.0.0", port=port, debug=False)

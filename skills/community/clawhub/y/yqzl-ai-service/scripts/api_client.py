#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云启智联AI服务接口调用客户端
支持接口：bank_receipt_parsing, bank_statement_parsing, invoice_parsing, file_parsing, async_result, ping
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("错误：缺少 requests 库。请运行: pip install requests")
    sys.exit(1)

# 添加脚本所在目录到路径，以便导入 config_manager
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import config_manager

# 导入记账凭证生成器（v1.2.0 新增）
try:
    from voucher_generator import (
        VoucherGenerator, VoucherBundle, Voucher,
        generate_voucher_html, _detect_source_type,
    )
    _HAS_VOUCHER = True
except ImportError:
    _HAS_VOUCHER = False

# 导入自动升级模块
try:
    import updater as _updater
except ImportError:
    _updater = None

API_BASE_URL = "http://8.135.62.13:5000/AIService"
GET_API_KEY_URL = "http://8.135.62.13:5000/"

# 体验馆接口地址（游客模式，无需 API Key）
EXPERIENCE_RUN_URL = f"{API_BASE_URL}/experience/run"
EXPERIENCE_RESULT_URL = f"{API_BASE_URL}/experience/result"


def _get_skill_version():
    """读取技能版本号"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    version_file = os.path.join(skill_dir, "version")
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "unknown"


def _get_safe_output_dir():
    """获取可写的 HTML 输出目录，按优先级回退，避免沙箱中生成失败"""
    candidates = []
    try:
        home = os.path.expanduser("~")
        if home and home != "~":
            candidates.append(os.path.join(home, "yqzl-ai-service"))
    except Exception:
        pass
    try:
        cwd = os.getcwd()
        if cwd:
            candidates.append(os.path.join(cwd, "yqzl-ai-service-output"))
    except Exception:
        pass
    try:
        import tempfile
        candidates.append(os.path.join(tempfile.gettempdir(), "yqzl-ai-service"))
    except Exception:
        pass

    for directory in candidates:
        try:
            os.makedirs(directory, exist_ok=True)
            # 测试是否真正可写
            test_file = os.path.join(directory, ".write_test")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test")
            os.remove(test_file)
            return directory
        except Exception:
            continue
    # 最后兜底：脚本所在目录
    return _SCRIPT_DIR


# 接口参数定义（与 yqzlAIService 保持一致）
INTERFACE_DEFS = {
    "bank_receipt_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "银行回单解析（支持每页多张自动裁剪）",
        "supports_experience": True,
    },
    "bank_statement_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "银行对账单解析",
        "supports_experience": True,
    },
    "invoice_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "发票解析",
        "supports_experience": True,
    },
    "file_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "文件解析",
        "supports_experience": True,
    },
    "async_result": {
        "method": "POST",
        "params": ["task_id"],
        "required": ["task_id"],
        "desc": "异步任务结果查询",
        "supports_experience": True,
    },
    "ping": {
        "method": "GET",
        "params": [],
        "desc": "服务连通性测试",
        "supports_experience": False,
    },
    "generate_voucher": {
        "method": "LOCAL",
        "params": ["input_file", "source_type", "business_type"],
        "desc": "从解析结果生成记账凭证（本地处理，不调用远程API）",
        "supports_experience": False,
    },
}


# 字段中文映射（与体验馆保持一致）
FIELD_LABEL_MAP = {
    "bankName": "银行名称",
    "createDate": "交易日期",
    "expendCustomer": "付款人",
    "expendAccount": "付款账号",
    "incomeCustomer": "收款人",
    "incomeAccount": "收款账号",
    "amount": "金额",
    "abstract": "摘要",
    "remark": "备注",
    "transNo": "交易流水号",
    "curName": "币种",
    "image_url": "回单图片",
    "balanceDirection": "借贷方向",
    "valid": "校验结果",
    "companyName": "主体公司",
    "companyAccount": "主体账号",
    # 对账单相关字段
    "accountName": "账户名称",
    "accountNo": "账号",
    "transAccount": "交易账号",
    "bank": "开户行",
    "balance": "余额",
    "transDate": "交易日期",
    "tradeDate": "交易日期",
    "transAmount": "交易金额",
    "debitAmount": "借方金额",
    "amountDebited": "借方金额",
    "creditAmount": "贷方金额",
    "amountCredited": "贷方金额",
    "totalCreditAmount": "贷方总发生额",
    "totalDebitAmount": "借方总发生额",
    "transType": "交易类型",
    "counterparty": "对方户名",
    "counterpartyName": "对方户名",
    "counterpartyAccount": "对方账号",
    "openBank": "开户银行",
    "purpose": "用途",
    "voucherNo": "凭证号",
}


def _fmt_money(n):
    """金额格式化（与体验馆 toLocaleString 一致）"""
    try:
        return "¥ {:,.2f}".format(float(n))
    except (TypeError, ValueError):
        return "¥ 0.00"


def _check_api_key():
    """检查 API KEY 是否已配置"""
    api_key = config_manager.get_api_key()
    if not api_key:
        print("=" * 50)
        print("未配置 API KEY，无法调用接口。")
        print(f"请访问官网获取 API KEY: {GET_API_KEY_URL}")
        print("获取后，运行以下命令配置：")
        print(f"  python {os.path.join(_SCRIPT_DIR, 'config_manager.py')} set \"你的API_KEY\"")
        print("=" * 50)
        sys.exit(1)
    return api_key


def call_api(interface_name, kwargs, experience_mode=False):
    """调用远程接口
    :param experience_mode: 是否使用游客体验模式（无需 API Key，调用体验馆接口）
    """
    definition = INTERFACE_DEFS.get(interface_name)
    if not definition:
        return {"code": 3001, "msg": f"未知接口: {interface_name}"}

    if experience_mode:
        if not definition.get("supports_experience"):
            return {
                "code": 3001,
                "msg": f"接口 {interface_name} 暂不支持游客体验模式，请配置 API Key 后调用"
            }
        return _call_experience_api(interface_name, kwargs)

    api_key = _check_api_key()
    headers = {"Authorization": api_key}
    url = f"{API_BASE_URL}/{interface_name}"
    method = definition["method"]

    # 参数校验
    if "required" in definition:
        for p in definition["required"]:
            if not kwargs.get(p):
                return {"code": 3001, "msg": f"缺少必填参数: {p}"}

    if "required_one_of" in definition:
        found = any(kwargs.get(p) for p in definition["required_one_of"])
        if not found:
            names = ", ".join(definition["required_one_of"])
            return {"code": 3001, "msg": f"参数 {names} 必须提供其中一个"}

    # 构建请求参数和文件
    data = {}
    files = None
    for p in definition["params"]:
        val = kwargs.get(p)
        if val is None:
            continue
        if p == "file":
            if not os.path.isfile(val):
                return {"code": 3001, "msg": f"文件不存在: {val}"}
            files = {"file": open(val, "rb")}
        else:
            data[p] = val

    return _do_request(method, url, headers, data, files)


def _call_experience_api(interface_name, kwargs):
    """调用体验馆接口（游客模式，无需 API Key）"""
    if interface_name == "async_result":
        task_id = kwargs.get("task_id")
        if not task_id:
            return {"code": 3001, "msg": "缺少必填参数: task_id"}
        return _do_request(
            "POST",
            EXPERIENCE_RESULT_URL,
            headers={},
            data={"task_id": task_id},
            files=None,
            send_json=True,
        )

    data = {"interface_name": interface_name}
    files = None

    file_path = kwargs.get("file")
    file_url = kwargs.get("file_url")

    if file_path:
        if not os.path.isfile(file_path):
            return {"code": 3001, "msg": f"文件不存在: {file_path}"}
        files = {"file": open(file_path, "rb")}
    elif file_url:
        data["file_url"] = file_url
    else:
        return {"code": 3001, "msg": "参数 file, file_url 必须提供其中一个"}

    callback_url = kwargs.get("callback_url")
    if callback_url:
        data["callback_url"] = callback_url

    return _do_request("POST", EXPERIENCE_RUN_URL, headers={}, data=data, files=files)


def _do_request(method, url, headers, data, files, send_json=False):
    """执行 HTTP 请求并返回 JSON 结果"""
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=30)
        else:
            if files:
                resp = requests.post(url, data=data, files=files, headers=headers, timeout=120)
            elif send_json:
                resp = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                resp = requests.post(url, data=data, headers=headers, timeout=30)

        if files:
            for f in files.values():
                f.close()

        resp.raise_for_status()
        return resp.json()

    except requests.exceptions.Timeout:
        return {"code": 5001, "msg": "请求超时，请稍后重试"}
    except requests.exceptions.ConnectionError:
        return {"code": 5001, "msg": "无法连接到服务器，请检查网络或服务状态"}
    except requests.exceptions.HTTPError as e:
        return {"code": 5001, "msg": f"服务器返回错误: {e.response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"code": 5001, "msg": f"请求异常: {str(e)}"}
    except Exception as e:
        return {"code": 5001, "msg": f"未知异常: {str(e)}"}


def _extract_receipt_records(data):
    """从回单解析结果中提取单条记录列表，并保留原始 page_index
    同时把 page 级别的 companyName/companyAccount 注入到记录中（若记录自身缺失），
    并保留原始 image_url 供表单视图点击放大使用。
    """
    records = []
    if not isinstance(data, list):
        return records
    for idx, page in enumerate(data):
        if isinstance(page, dict) and isinstance(page.get("page_data"), list):
            page_index = page.get("page_index", idx + 1)
            page_company_name = page.get("companyName")
            page_company_account = page.get("companyAccount")
            for item in page["page_data"]:
                if isinstance(item, dict):
                    record = dict(item)
                    record["_pageIndex"] = page_index
                    if page_company_name and not record.get("companyName"):
                        record["companyName"] = page_company_name
                    if page_company_account and not record.get("companyAccount"):
                        record["companyAccount"] = page_company_account
                    if record.get("image_url"):
                        record["_original_image_url"] = record["image_url"]
                    records.append(record)
    return records


def _extract_statement_records(data):
    """从对账单解析结果中提取明细记录和全局信息"""
    records = []
    global_info = {}
    if not isinstance(data, list):
        return records, global_info
    for idx, page in enumerate(data):
        if not isinstance(page, dict):
            continue
        page_data = page.get("page_data")
        if not isinstance(page_data, dict):
            continue
        if idx == 0 and isinstance(page_data.get("global_fields"), dict):
            global_info = page_data["global_fields"]
        detail_list = page_data.get("detail_fields_list")
        if isinstance(detail_list, list):
            for item in detail_list:
                if isinstance(item, dict):
                    item["_pageIndex"] = page.get("page_index", idx + 1)
                    records.append(item)
    return records, global_info


def _download_image_as_data_uri(url, timeout=15):
    """下载图片并转为 base64 data URI，失败时返回 None"""
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, stream=False)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "image/jpeg")
        if "image" not in content_type:
            content_type = "image/jpeg"
        import base64
        b64 = base64.b64encode(resp.content).decode("ascii")
        return f"data:{content_type};base64,{b64}"
    except Exception:
        return None


def generate_receipt_html(records, raw_data=None, output_path=None):
    """生成体验馆风格的回单 HTML 预览文件（回单视图 + 表单视图 + JSON 视图）"""
    if not records:
        return None

    # 回单图片直接使用原始公网 URL，避免将 base64 数据内嵌到 <script> 中导致
    # 脚本体积过大、浏览器解析失败。_original_image_url 在 _extract_receipt_records
    # 中已保存，如需兜底可直接使用 image_url（此时它仍是原始 URL）。
    for r in records:
        if r.get("image_url") and not r.get("_original_image_url"):
            r["_original_image_url"] = r["image_url"]

    if output_path is None:
        default_dir = _get_safe_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        base_name = f"receipt_viewer_{ts}"
        output_path = os.path.join(default_dir, f"{base_name}.html")
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(default_dir, f"{base_name}_{counter}.html")
            counter += 1

    # 推断主体公司/账号（取所有记录中出现次数最多的值）
    from collections import Counter
    company_names = [r.get("companyName") for r in records if r.get("companyName")]
    company_accounts = [r.get("companyAccount") for r in records if r.get("companyAccount")]
    company_name = Counter(company_names).most_common(1)[0][0] if company_names else ""
    company_account = Counter(company_accounts).most_common(1)[0][0] if company_accounts else ""

    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>银行回单解析结果 - 云启智联AI服务</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f0f2f5; min-height: 100vh; padding: 20px;
}
.header {
    max-width: 1200px; margin: 0 auto 20px;
}
.header h1 { font-size: 20px; color: #333; margin-bottom: 6px; }
.header .subtitle { color: #666; font-size: 13px; }
.container {
    max-width: 1200px; margin: 0 auto;
    background: #fff; border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06); padding: 20px;
}
.view-tabs { display: flex; gap: 0; border-bottom: 1px solid #e8e8e8; margin-bottom: 16px; }
.view-tab { padding: 8px 18px; cursor: pointer; font-size: 13px; color: #888; border-bottom: 2px solid transparent; transition: all 0.2s; }
.view-tab:hover { color: #333; }
.view-tab.active { color: #667eea; border-bottom-color: #667eea; font-weight: 600; }
.view-panel { display: none; }
.view-panel.active { display: block; }
.receipt-nav {
    display: flex; gap: 8px; margin-bottom: 14px;
    flex-wrap: wrap; padding-bottom: 14px;
    border-bottom: 1px solid #f0f0f0;
}
.receipt-nav-btn {
    padding: 5px 14px; background: #f0f0f0;
    border: 1px solid #e0e0e0; border-radius: 6px;
    font-size: 12px; color: #555; cursor: pointer;
    transition: all 0.2s;
}
.receipt-nav-btn:hover { border-color: #667eea; color: #667eea; }
.receipt-nav-btn.active { background: #667eea; color: #fff; border-color: #667eea; }
.receipt-viewer { display: flex; gap: 20px; min-height: 300px; }
.receipt-image-panel {
    flex: 1; min-width: 0; background: #f8f9fa;
    border-radius: 8px; padding: 12px;
    display: flex; flex-direction: column; align-items: center; position: relative;
}
.receipt-image-toolbar {
    display: flex; gap: 6px; margin-bottom: 8px;
    align-items: center; flex-wrap: wrap;
}
.receipt-image-toolbar button {
    padding: 4px 10px; background: #fff;
    border: 1px solid #ddd; border-radius: 4px;
    cursor: pointer; font-size: 14px;
    transition: all 0.2s; line-height: 1;
}
.receipt-image-toolbar button:hover { border-color: #667eea; color: #667eea; }
.receipt-zoom-label { font-size: 12px; color: #666; min-width: 40px; text-align: center; }
.receipt-image-container {
    flex: 1; overflow: auto; display: flex;
    justify-content: center; align-items: flex-start;
    max-height: 520px; width: 100%; border-radius: 4px;
}
.receipt-image-container img {
    max-width: 100%; transition: transform 0.2s ease;
    cursor: zoom-in; transform-origin: top center;
    border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.receipt-data-panel { flex: 1; min-width: 0; overflow-y: auto; max-height: 580px; }
.receipt-card {
    background: #f8f9fa; border-radius: 8px;
    padding: 16px; margin-bottom: 12px;
}
.receipt-card-title {
    font-size: 13px; font-weight: 600; color: #667eea;
    margin-bottom: 10px; padding-bottom: 8px;
    border-bottom: 1px solid #e8e8e8;
    display: flex; align-items: center; gap: 6px;
}
.receipt-data-table {
    width: 100%; border-collapse: collapse; font-size: 13px;
}
.receipt-data-table td {
    padding: 8px 10px; border-bottom: 1px solid #f0f0f0; vertical-align: top;
}
.receipt-data-table tr:last-child td { border-bottom: none; }
.receipt-data-table .field-label {
    color: #888; font-size: 12px; white-space: nowrap; width: 100px;
}
.receipt-data-table .field-value {
    color: #333; font-weight: 500; word-break: break-all;
}
.receipt-data-table .field-value.amount {
    color: #e65100; font-weight: 600; font-size: 14px;
}
.receipt-image-modal {
    display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.85); z-index: 1000;
    justify-content: center; align-items: center; cursor: zoom-out;
}
.receipt-image-modal.active { display: flex; }
.receipt-image-modal img {
    max-width: 92vw; max-height: 92vh; object-fit: contain;
    border-radius: 4px; box-shadow: 0 4px 30px rgba(0,0,0,0.3);
}
.receipt-image-modal-close {
    position: fixed; top: 16px; right: 20px; color: #fff;
    font-size: 28px; cursor: pointer; background: rgba(0,0,0,0.4);
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    border: none; z-index: 1001;
}
.receipt-image-modal-close:hover { background: rgba(255,255,255,0.2); }
.form-view-header { text-align: center; margin-bottom: 8px; }
.form-view-header h2 { font-size: 20px; color: #1a6f3c; margin-bottom: 4px; }
.form-view-header .subtitle { color: #666; font-size: 13px; }
.form-view-stats { display: flex; gap: 16px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
.form-view-stat { background: #1a7f4c; color: #fff; padding: 12px 20px; border-radius: 10px; text-align: center; min-width: 140px; }
.form-view-stat .label { font-size: 12px; opacity: 0.85; margin-bottom: 4px; }
.form-view-stat .value { font-size: 20px; font-weight: bold; }
.form-view-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); font-size: 13px; }
.form-view-table th { background: #1a6f3c; color: #fff; padding: 10px 8px; font-size: 12px; text-align: left; position: sticky; top: 0; }
.form-view-table td { padding: 8px; font-size: 12px; border-bottom: 1px solid #eee; vertical-align: top; }
.form-view-table tr:hover { background: #f8fff8; }
.form-view-table .fv-amount { font-weight: bold; color: #1a6f3c; text-align: right; }
.form-view-table .fv-amount.negative { color: #c0392b; }
.form-view-table .fv-date { white-space: nowrap; color: #555; }
.form-view-table .fv-dir { font-size: 10px; padding: 2px 6px; border-radius: 3px; display: inline-block; margin-top: 2px; }
.form-view-table .fv-dir.in { background: #e8f5e9; color: #1a7f4c; }
.form-view-table .fv-dir.out { background: #ffebee; color: #c0392b; }
.form-view-table .fv-page-sep td { background: #f0f7f2; font-weight: bold; color: #1a6f3c; padding: 6px; font-size: 11px; }
.form-view-table .fv-receipt-img { max-width: 60px; max-height: 60px; border-radius: 4px; cursor: pointer; transition: transform 0.2s; }
.form-view-table .fv-receipt-img:hover { transform: scale(2.5); z-index: 100; position: relative; }
.form-view-footer { text-align: center; font-size: 11px; color: #aaa; margin-top: 16px; }
.json-view { background: #1e1e2e; color: #cdd6f4; border-radius: 8px; padding: 16px; font-family: 'Consolas', 'Monaco', 'Courier New', monospace; font-size: 12px; line-height: 1.6; max-height: 600px; overflow: auto; white-space: pre-wrap; word-break: break-all; position: relative; }
.json-view .copy-btn { position: absolute; top: 8px; right: 8px; padding: 4px 10px; background: rgba(255,255,255,0.1); color: #ccc; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; }
.json-view .copy-btn:hover { background: rgba(255,255,255,0.2); }
.json-view pre { margin: 0; }
.json-key { color: #89b4fa; }
.json-string { color: #a6e3a1; }
.json-number { color: #fab387; }
.json-bool { color: #f38ba8; }
.json-null { color: #6c7086; }
@media (max-width: 1200px) {
    .receipt-viewer { flex-direction: column; }
    .receipt-data-panel { max-height: none; }
    .receipt-image-container { max-height: 360px; }
}
</style>
</head>
<body>
<div class="header">
    <h1>银行回单解析结果</h1>
    <div class="subtitle">{company_info}</div>
</div>
<div class="container">
    <div class="view-tabs">
        <div class="view-tab active" onclick="switchView('receipt')" id="tab-receipt">回单视图</div>
        <div class="view-tab" onclick="switchView('form')" id="tab-form">表单视图</div>
        <div class="view-tab" onclick="switchView('json')" id="tab-json">JSON 视图</div>
    </div>
    <div class="view-panel active" id="panel-receipt">
        <div class="receipt-nav" id="receiptNav"></div>
        <div class="receipt-viewer" id="receiptViewer">
            <div class="receipt-image-panel">
                <div class="receipt-image-toolbar">
                    <button onclick="zoomOut()">-</button>
                    <span class="receipt-zoom-label" id="zoomLabel">100%</span>
                    <button onclick="zoomIn()">+</button>
                    <button onclick="resetZoom()">重置</button>
                    <button onclick="openModal()">全屏</button>
                </div>
                <div class="receipt-image-container">
                    <img id="receiptImage" src="" alt="回单图片" onclick="openModal()">
                </div>
            </div>
            <div class="receipt-data-panel" id="receiptDataPanel"></div>
        </div>
    </div>
    <div class="view-panel" id="panel-form">
        {form_view_html}
    </div>
    <div class="view-panel" id="panel-json">
        <div class="json-view"><button class="copy-btn" onclick="copyJson()">复制</button><pre id="jsonPre"></pre></div>
    </div>
</div>
<div class="receipt-image-modal" id="imageModal" onclick="closeModal()">
    <button class="receipt-image-modal-close" onclick="closeModal()">&times;</button>
    <img id="modalImage" src="" alt="回单大图">
</div>
<script>
const receipts = {json_data_records};
const rawJson = {json_data};
let currentIndex = 0;
let zoomLevel = 1;
function formatAmount(val) {
    return val.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function escapeHtml(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function syntaxHighlight(json) {
    json = escapeHtml(json);
    return json.replace(/("(?:\\.|[^"\\\\])*")(\s*:)?/g, function(m, key, colon) {
        let cls = 'json-string';
        if (colon) { cls = 'json-key'; }
        return '<span class="' + cls + '">' + key + '</span>' + (colon || '');
    }).replace(/\b(true|false)\b/g, '<span class="json-bool">$1</span>')
      .replace(/\b(null)\b/g, '<span class="json-null">$1</span>')
      .replace(/\b(-?\d+(?:\.\d+)?)\b/g, '<span class="json-number">$1</span>');
}
function renderJsonView() {
    const pre = document.getElementById('jsonPre');
    if (pre) pre.innerHTML = syntaxHighlight(JSON.stringify(rawJson, null, 2));
}
function copyJson() {
    navigator.clipboard.writeText(JSON.stringify(rawJson, null, 2)).then(() => {
        const btn = document.querySelector('#panel-json .copy-btn');
        const old = btn.textContent;
        btn.textContent = '已复制';
        setTimeout(() => btn.textContent = old, 1500);
    }).catch(() => {});
}
function switchView(view) {
    document.querySelectorAll('.view-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
    document.getElementById('tab-' + view).classList.add('active');
    document.getElementById('panel-' + view).classList.add('active');
}
function renderNav() {
    const nav = document.getElementById('receiptNav');
    nav.innerHTML = receipts.map((r, i) =>
        `<button class="receipt-nav-btn ${i === currentIndex ? 'active' : ''}" onclick="switchReceipt(${i})">回单 ${i + 1}</button>`
    ).join('');
}
function renderReceipt(index) {
    const r = receipts[index];
    document.getElementById('receiptImage').src = r.image_url || '';
    document.getElementById('modalImage').src = r.image_url || '';
    const fields = [
        { label: '交易日期', key: 'createDate' },
        { label: '摘要', key: 'abstract' },
        { label: '金额', key: 'amount', isAmount: true },
        { label: '借贷方向', key: 'balanceDirection' },
        { label: '币种', key: 'curName' },
        { label: '银行', key: 'bankName' },
        { label: '支出账号', key: 'expendAccount' },
        { label: '支出户名', key: 'expendCustomer' },
        { label: '收入账号', key: 'incomeAccount' },
        { label: '收入户名', key: 'incomeCustomer' },
        { label: '交易流水号', key: 'transNo' },
        { label: '备注', key: 'remark' },
    ];
    const html = `
        <div class="receipt-card">
            <div class="receipt-card-title">回单 ${index + 1} / ${receipts.length}</div>
            <table class="receipt-data-table">
                ${fields.map(f => {
                    let val = r[f.key];
                    if (val === undefined || val === null) val = '';
                    if (f.isAmount) val = formatAmount(val);
                    let valueClass = 'field-value';
                    if (f.isAmount) valueClass += ' amount';
                    return `<tr><td class="field-label">${f.label}</td><td class="${valueClass}">${val}</td></tr>`;
                }).join('')}
            </table>
        </div>
    `;
    document.getElementById('receiptDataPanel').innerHTML = html;
}
function switchReceipt(index) {
    currentIndex = index;
    zoomLevel = 1;
    updateZoom();
    renderNav();
    renderReceipt(index);
}
function updateZoom() {
    document.getElementById('receiptImage').style.transform = `scale(${zoomLevel})`;
    document.getElementById('zoomLabel').textContent = Math.round(zoomLevel * 100) + '%';
}
function zoomIn() { zoomLevel = Math.min(zoomLevel + 0.2, 3); updateZoom(); }
function zoomOut() { zoomLevel = Math.max(zoomLevel - 0.2, 0.4); updateZoom(); }
function resetZoom() { zoomLevel = 1; updateZoom(); }
function openModal() { document.getElementById('imageModal').classList.add('active'); }
function openImageModal(url) {
    if (!url) return;
    zoomLevel = 1;
    updateZoom();
    document.getElementById('receiptImage').src = url;
    document.getElementById('modalImage').src = url;
    document.getElementById('imageModal').classList.add('active');
}
function closeModal() { document.getElementById('imageModal').classList.remove('active'); }
renderNav();
renderReceipt(0);
renderJsonView();
</script>
</body>
</html>"""

    form_view_html = _build_receipt_form_view(records)

    company_info = ""
    if company_name and company_account:
        company_info = f"公司名称：{company_name}　|　账号：{company_account}"
    elif company_name:
        company_info = f"公司名称：{company_name}"
    elif company_account:
        company_info = f"账号：{company_account}"
    # 无法判断主体公司和账号时，不显示这 2 个字段

    json_payload = raw_data if raw_data is not None else records
    json_str = json.dumps(json_payload, ensure_ascii=False, indent=2)
    records_json_str = json.dumps(records, ensure_ascii=False, indent=2)
    html_content = html_template.replace("{count}", str(len(records))) \
        .replace("{company_info}", company_info) \
        .replace("{form_view_html}", form_view_html) \
        .replace("{json_data}", json_str) \
        .replace("{json_data_records}", records_json_str)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


def _build_receipt_form_view(records):
    """构建回单表单视图 HTML 片段"""
    total_in = 0.0
    total_out = 0.0
    for r in records:
        amt = float(r.get("amount") or 0)
        direction = r.get("balanceDirection", "")
        # 银行回单语义：贷方为收入，借方为支出
        if direction == "贷":
            total_in += abs(amt)
        elif direction == "借":
            total_out += abs(amt)
    net_change = total_in - total_out

    fmt = _fmt_money

    html = """
    <div class="form-view-header">
        <h2>银行回单解析结果</h2>
        <div class="subtitle">共 {record_count} 条记录</div>
    </div>
    <div class="form-view-stats">
        <div class="form-view-stat"><div class="label">收入合计</div><div class="value">{total_in}</div></div>
        <div class="form-view-stat"><div class="label">支出合计</div><div class="value">{total_out}</div></div>
        <div class="form-view-stat"><div class="label">净变动</div><div class="value" style="{net_style}">{net_change}</div></div>
    </div>
    <div style="overflow-x:auto;">
    <table class="form-view-table">
    <thead><tr>
        <th>日期</th>
        <th>收款方</th>
        <th>付款方</th>
        <th>金额</th>
        <th>借贷方向</th>
        <th>摘要</th>
        <th>流水号</th>
        <th>回单</th>
    </tr></thead>
    <tbody>""".format(
        record_count=len(records),
        total_in=fmt(total_in),
        total_out=fmt(total_out),
        net_style="color:#ffebee;" if net_change < 0 else "",
        net_change=fmt(net_change),
    )

    current_page = None
    for item in records:
        page_index = item.get("_pageIndex", 1)
        if page_index != current_page:
            current_page = page_index
            html += '<tr class="fv-page-sep"><td colspan="8">第 {} 页</td></tr>'.format(current_page)

        amt = float(item.get("amount") or 0)
        amt_class = "fv-amount negative" if item.get("balanceDirection") == "借" else "fv-amount"
        income_name = item.get("incomeCustomer") or "-"
        income_acc = item.get("incomeAccount") or ""
        expend_name = item.get("expendCustomer") or "-"
        expend_acc = item.get("expendAccount") or ""
        raw_img_url = item.get("_original_image_url") or item.get("image_url") or ""
        display_img_url = item.get("image_url") or item.get("_original_image_url") or ""

        html += """
        <tr>
            <td class="fv-date">{date}</td>
            <td>{income_name}{income_acc_html}</td>
            <td>{expend_name}{expend_acc_html}</td>
            <td class="{amt_class}">{amount}</td>
            <td>{direction}</td>
            <td>{abstract}</td>
            <td>{trans_no}</td>
            <td>{img_html}</td>
        </tr>""".format(
            date=item.get("createDate", ""),
            income_name=income_name,
            income_acc_html='<br><span style="color:#888;font-size:11px">' + income_acc + '</span>' if income_acc else "",
            expend_name=expend_name,
            expend_acc_html='<br><span style="color:#888;font-size:11px">' + expend_acc + '</span>' if expend_acc else "",
            amt_class=amt_class,
            amount=fmt(abs(amt)),
            direction=item.get("balanceDirection", ""),
            abstract=item.get("abstract", ""),
            trans_no=item.get("transNo", ""),
            img_html='<img class="fv-receipt-img" src="{}" onclick="openImageModal(\'{}\')" title="点击放大">'.format(display_img_url, raw_img_url) if display_img_url else "-",
        )

    html += """
    </tbody></table></div>
    <div class="form-view-footer">云启智联 AI 服务 | 银行回单智能解析</div>"""

    return html


def generate_statement_html(data, output_path=None):
    """生成体验馆风格的对账单 HTML 预览文件（表单视图）"""
    records, global_info = _extract_statement_records(data)
    if not records:
        return None

    if output_path is None:
        default_dir = _get_safe_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        base_name = f"statement_viewer_{ts}"
        output_path = os.path.join(default_dir, f"{base_name}.html")
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(default_dir, f"{base_name}_{counter}.html")
            counter += 1

    fmt = _fmt_money

    # 全局字段
    global_items = []
    if global_info.get("accountName"):
        global_items.append(("账户名称", global_info["accountName"]))
    if global_info.get("bankName"):
        global_items.append(("开户行", global_info["bankName"]))
    if global_info.get("transAccount"):
        global_items.append(("账号", global_info["transAccount"]))
    if global_info.get("curName"):
        global_items.append(("币种", global_info["curName"]))

    global_items_html = ""
    if global_items:
        global_items_html = '<div class="st-global">' + "".join(
            '<div class="st-global-item"><div class="gl">{}</div><div class="gv">{}</div></div>'.format(k, v)
            for k, v in global_items
        ) + '</div>'

    # 统计
    total_credit = 0.0
    total_debit = 0.0
    if global_info.get("totalCreditAmount") is not None:
        total_credit = float(global_info["totalCreditAmount"])
    if global_info.get("totalDebitAmount") is not None:
        total_debit = float(global_info["totalDebitAmount"])
    if total_credit == 0 and total_debit == 0:
        for item in records:
            total_credit += float(item.get("amountCredited") or 0)
            total_debit += float(item.get("amountDebited") or 0)
    net_change = total_credit - total_debit

    rows_html = ""
    current_page = None
    for item in records:
        page_index = item.get("_pageIndex", 1)
        if page_index != current_page:
            current_page = page_index
            rows_html += '<tr class="st-page-sep"><td colspan="8">第 {} 页</td></tr>'.format(current_page)

        credit = float(item.get("amountCredited") or 0)
        debit = float(item.get("amountDebited") or 0)
        balance = item.get("balance")
        cp_name = item.get("counterpartyName") or "-"
        cp_acc = item.get("counterpartyAccount") or ""

        rows_html += """
        <tr>
            <td class="st-date">{date}</td>
            <td>{cp_name}{cp_acc_html}</td>
            <td>{cp_acc}</td>
            <td class="st-amt credit">{credit}</td>
            <td class="st-amt debit">{debit}</td>
            <td class="st-balance">{balance}</td>
            <td>{abstract}</td>
            <td>{trans_no}</td>
        </tr>""".format(
            date=item.get("tradeDate", ""),
            cp_name=cp_name,
            cp_acc_html='<br><span style="color:#888;font-size:11px">' + cp_acc + '</span>' if cp_acc else "",
            cp_acc=cp_acc,
            credit=fmt(credit) if credit else "-",
            debit=fmt(debit) if debit else "-",
            balance=fmt(balance) if balance is not None else "-",
            abstract=item.get("abstract", ""),
            trans_no=item.get("transNo", ""),
        )

    net_change_style = "color:#ffcdd2;" if net_change < 0 else ""
    page_count = len(data) if isinstance(data, list) else 1

    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>银行对账单解析结果 - 云启智联AI服务</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f0f2f5; min-height: 100vh; padding: 20px;
}
.header {
    max-width: 1200px; margin: 0 auto 20px;
}
.header h1 { font-size: 20px; color: #333; margin-bottom: 6px; }
.header .subtitle { color: #666; font-size: 13px; }
.container {
    max-width: 1200px; margin: 0 auto;
    background: #fff; border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06); padding: 20px;
}
.st-header { text-align: center; margin-bottom: 8px; }
.st-header h2 { font-size: 20px; color: #1565c0; margin-bottom: 4px; }
.st-header .subtitle { color: #666; font-size: 13px; }
.st-global { background: #f0f7ff; border: 1px solid #bbdefb; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px; display: flex; flex-wrap: wrap; gap: 20px; }
.st-global-item { font-size: 13px; }
.st-global-item .gl { color: #888; font-size: 11px; margin-bottom: 2px; }
.st-global-item .gv { font-weight: 600; color: #333; }
.st-stats { display: flex; gap: 16px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
.st-stat { background: #1565c0; color: #fff; padding: 12px 20px; border-radius: 10px; text-align: center; min-width: 140px; }
.st-stat .label { font-size: 12px; opacity: 0.85; margin-bottom: 4px; }
.st-stat .value { font-size: 20px; font-weight: bold; }
.st-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); font-size: 13px; }
.st-table th { background: #1565c0; color: #fff; padding: 10px 8px; font-size: 12px; text-align: left; position: sticky; top: 0; }
.st-table td { padding: 8px; font-size: 12px; border-bottom: 1px solid #eee; vertical-align: top; }
.st-table tr:hover { background: #f0f7ff; }
.st-table .st-amt { font-weight: bold; text-align: right; white-space: nowrap; }
.st-table .st-amt.credit { color: #1565c0; }
.st-table .st-amt.debit { color: #c0392b; }
.st-table .st-balance { text-align: right; color: #555; white-space: nowrap; }
.st-table .st-date { white-space: nowrap; color: #555; }
.st-table .st-page-sep td { background: #f0f4fa; font-weight: bold; color: #1565c0; padding: 6px; font-size: 11px; }
.st-footer { text-align: center; font-size: 11px; color: #aaa; margin-top: 16px; }
</style>
</head>
<body>
<div class="header">
    <h1>银行对账单解析结果</h1>
    <div class="subtitle">表单视图 | 云启智联 AI 服务</div>
</div>
<div class="container">
    <div class="st-header">
        <h2>银行对账单解析结果</h2>
        <div class="subtitle">共 {page_count} 页 {record_count} 条交易记录</div>
    </div>
    {global_items_html}
    <div class="st-stats">
        <div class="st-stat"><div class="label">贷方合计（转入）</div><div class="value">{total_credit}</div></div>
        <div class="st-stat"><div class="label">借方合计（转出）</div><div class="value">{total_debit}</div></div>
        <div class="st-stat"><div class="label">净变动</div><div class="value" style="{net_change_style}">{net_change}</div></div>
    </div>
    <div style="overflow-x:auto;">
    <table class="st-table">
    <thead><tr>
        <th>交易日期</th>
        <th>对方户名</th>
        <th>对方账号</th>
        <th>贷方金额</th>
        <th>借方金额</th>
        <th>余额</th>
        <th>摘要</th>
        <th>流水号</th>
    </tr></thead>
    <tbody>
        {rows_html}
    </tbody></table></div>
    <div class="st-footer">云启智联 AI 服务 | 银行对账单智能解析</div>
</div>
</body>
</html>"""

    html = html_template.replace("{page_count}", str(page_count)) \
        .replace("{record_count}", str(len(records))) \
        .replace("{global_items_html}", global_items_html) \
        .replace("{total_credit}", fmt(total_credit)) \
        .replace("{total_debit}", fmt(total_debit)) \
        .replace("{net_change_style}", net_change_style) \
        .replace("{net_change}", fmt(net_change)) \
        .replace("{rows_html}", rows_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def format_result(result, interface_name=None, experience_mode=False):
    """格式化输出接口返回结果"""
    if not isinstance(result, dict):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    code = result.get("code")
    msg = result.get("msg", "")
    data = result.get("data")

    if code == 1000:
        print(f"请求成功: {msg}")
    else:
        print(f"请求失败 (code={code}): {msg}")

    if data is not None:
        # 如果是任务提交成功，提取 task_id 提示用户
        task_id = data.get("task_id") if isinstance(data, dict) else None
        if task_id:
            exp_flag = " --experience" if experience_mode else ""
            print(f"任务ID: {task_id}")
            print("可使用以下命令查询结果：")
            print(f'  python {os.path.join(_SCRIPT_DIR, "api_client.py")} async_result --task-id {task_id}{exp_flag}')
        else:
            if interface_name == "bank_receipt_parsing":
                records = _extract_receipt_records(data)
                if records:
                    try:
                        html_path = generate_receipt_html(records, raw_data=data)
                        if html_path:
                            print(f"\n已生成回单预览页面: {html_path}")
                            print("您可以用浏览器打开该文件，在“回单视图”、“表单视图”和“JSON 视图”之间切换查看。\n")
                    except Exception as e:
                        print(f"\n[提示] 回单 HTML 预览文件生成失败（不影响解析结果）: {e}\n")
            elif interface_name == "bank_statement_parsing":
                records, _ = _extract_statement_records(data)
                if records:
                    try:
                        html_path = generate_statement_html(data)
                        if html_path:
                            print(f"\n已生成对账单预览页面: {html_path}")
                            print("您可以用浏览器打开该文件查看表单视图。\n")
                    except Exception as e:
                        print(f"\n[提示] 对账单 HTML 预览文件生成失败（不影响解析结果）: {e}\n")
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        # 直接打印完整结果用于调试
        print(json.dumps(result, ensure_ascii=False, indent=2))


def _generate_voucher_from_result(result, interface_name, business_type="商贸", gen_html=False):
    """v1.2.0：从解析结果自动生成记账凭证并输出"""
    if not isinstance(result, dict) or result.get("code") != 1000:
        return  # 解析未成功，跳过凭证生成

    data = result.get("data")
    if data is None:
        return

    # 映射接口名到凭证来源类型
    type_map = {
        "bank_receipt_parsing": "receipt",
        "bank_statement_parsing": "statement",
        "invoice_parsing": "invoice",
    }
    source_type = type_map.get(interface_name)
    if not source_type:
        print("\n[凭证生成] 当前接口不支持凭证生成，跳过")
        return

    generator = VoucherGenerator(business_type=business_type, vat_rate=0.01)

    try:
        voucher_result = generator.process(data, source_type)
    except Exception as e:
        print(f"\n[凭证生成] 生成失败（不影响解析结果）: {e}")
        return

    if voucher_result is None:
        print("\n[凭证生成] 未生成任何凭证（所有记录金额为0或数据格式不匹配）")
        return

    print("\n" + "=" * 60)
    print("记账凭证（基于 OCR 解析结果自动生成，仅供参考，请人工复核）")
    print("=" * 60)

    if isinstance(voucher_result, VoucherBundle):
        print(f"共生成 {len(voucher_result.vouchers)} 张凭证")
        for i, v in enumerate(voucher_result.vouchers):
            print(f"\n--- 凭证 {i + 1} ---")
            for line in v.to_display_lines():
                print(line)
            if v.review_suggestion:
                s = v.review_suggestion
                print(f"复核级别：{s['level_label']}")
                print(f"复核摘要：{s['summary']}")
                for flag in s.get("flags", []):
                    print(f"  - {flag['suggestion']}")
    elif isinstance(voucher_result, Voucher):
        for line in voucher_result.to_display_lines():
            print(line)
        if voucher_result.review_suggestion:
            s = voucher_result.review_suggestion
            print(f"\n复核级别：{s['level_label']}")
            print(f"复核摘要：{s['summary']}")
            for flag in s.get("flags", []):
                print(f"  - {flag['suggestion']}")

    # 保存凭证 JSON
    try:
        output_dir = _get_safe_output_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        json_path = os.path.join(output_dir, f"voucher_{ts}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(voucher_result.to_json(indent=2))
        print(f"\n凭证 JSON 已保存: {json_path}")
    except Exception as e:
        print(f"\n[凭证生成] JSON 保存失败: {e}")

    # 生成 HTML 预览
    if gen_html:
        try:
            html_path = generate_voucher_html(voucher_result)
            if html_path:
                print(f"凭证预览页面已生成: {html_path}")
        except Exception as e:
            print(f"[凭证生成] HTML 预览生成失败: {e}")

    print("\n" + "=" * 60)
    print("提示：以上凭证为系统自动生成，科目选择和金额需人工复核后方可入账。")
    print("=" * 60)


def main():
    # 启动时检测更新（每24小时最多检测一次，提示用户可手动升级）
    if _updater:
        try:
            _updater.auto_check_and_notify(verbose=True)
        except Exception:
            pass  # 自动检测失败不影响正常使用

    version = _get_skill_version()
    parser = argparse.ArgumentParser(
        description=f"云启智联AI服务接口调用客户端 (版本: {version}) [v1.2.0新增：记账凭证生成]"
    )
    parser.add_argument(
        "interface",
        nargs="?",
        choices=list(INTERFACE_DEFS.keys()),
        help="接口名称"
    )
    parser.add_argument("--file", help="本地文件路径（与 --file-url 二选一）")
    parser.add_argument("--file-url", help="文件URL地址（与 --file 二选一）")
    parser.add_argument("--callback-url", help="任务完成回调地址（可选）")
    parser.add_argument("--task-id", help="任务ID（仅 async_result 接口需要）")
    parser.add_argument("--experience", action="store_true", help="游客体验模式（无需 API Key，每日限20次）")
    parser.add_argument("--wait", type=int, default=None, metavar="SECONDS",
                        help="异步接口自动轮询等待结果（默认120秒，设0禁用）")
    # v1.2.0 新增：记账凭证生成参数
    parser.add_argument("--voucher", action="store_true",
                        help="解析完成后自动生成记账凭证（需 voucher_generator 模块）")
    parser.add_argument("--business-type", default="商贸",
                        choices=["商贸", "服务"],
                        help="企业类型，用于凭证生成（默认：商贸）")
    parser.add_argument("--source-type", default="auto",
                        choices=["auto", "receipt", "statement", "invoice"],
                        help="凭证数据来源类型（默认自动检测，仅 generate_voucher 命令使用）")
    parser.add_argument("--voucher-html", action="store_true",
                        help="同时生成凭证 HTML 预览文件")
    parser.add_argument("--version", action="store_true", help="显示版本号")

    args = parser.parse_args()

    if args.version:
        print(f"yqzl-ai-service 版本: {version}")
        sys.exit(0)

    if not args.interface:
        parser.print_help()
        sys.exit(1)

    # ---- generate_voucher 命令：本地处理，不调用远程 API ----
    if args.interface == "generate_voucher":
        if not _HAS_VOUCHER:
            print("错误：记账凭证生成模块 (voucher_generator) 未安装或导入失败")
            sys.exit(1)
        input_file = args.file
        if not input_file:
            print("错误：generate_voucher 命令需要 --file 参数指定解析结果 JSON 文件")
            sys.exit(1)
        if not os.path.isfile(input_file):
            print(f"错误：文件不存在: {input_file}")
            sys.exit(1)

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"错误：无法加载 JSON 文件: {e}")
            sys.exit(1)

        # 兼容直接传入完整 API 响应（含 code/data/msg）的情况
        if isinstance(data, dict) and isinstance(data.get("data"), (list, dict)):
            data = data["data"]

        source_type = args.source_type
        if source_type == "auto":
            source_type = _detect_source_type(data)
            if not source_type:
                print("错误：无法自动检测数据来源类型，请用 --source-type 指定（receipt/statement/invoice）")
                sys.exit(1)
            print(f"[自动检测] 数据来源类型: {source_type}")

        generator = VoucherGenerator(
            business_type=args.business_type,
            vat_rate=0.01,
        )
        try:
            voucher_result = generator.process(data, source_type)
        except Exception as e:
            print(f"错误：凭证生成失败: {e}")
            sys.exit(1)

        if voucher_result is None:
            print("未生成任何凭证（数据为空或所有记录金额为0）")
            sys.exit(0)

        # 输出摘要
        if isinstance(voucher_result, VoucherBundle):
            print(f"\n共生成 {len(voucher_result.vouchers)} 张凭证")
            for i, v in enumerate(voucher_result.vouchers):
                print(f"\n--- 凭证 {i + 1} ---")
                for line in v.to_display_lines():
                    print(line)
                if v.review_suggestion:
                    s = v.review_suggestion
                    print(f"复核级别：{s['level_label']}")
                    print(f"复核摘要：{s['summary']}")
                    for flag in s.get("flags", []):
                        print(f"  - {flag['suggestion']}")
        elif isinstance(voucher_result, Voucher):
            for line in voucher_result.to_display_lines():
                print(line)
            if voucher_result.review_suggestion:
                s = voucher_result.review_suggestion
                print(f"\n复核级别：{s['level_label']}")
                print(f"复核摘要：{s['summary']}")
                for flag in s.get("flags", []):
                    print(f"  - {flag['suggestion']}")

        # 输出 JSON
        voucher_json = voucher_result.to_json(indent=2)
        print(f"\n--- 凭证 JSON ---\n{voucher_json}")

        # 生成 HTML
        if args.voucher_html:
            try:
                html_path = generate_voucher_html(voucher_result)
                if html_path:
                    print(f"\n已生成凭证预览页面: {html_path}")
            except Exception as e:
                print(f"\n[提示] HTML 预览生成失败: {e}")

        sys.exit(0)

    # ---- 常规接口调用 ----
    kwargs = {
        "file": args.file,
        "file_url": args.file_url,
        "callback_url": args.callback_url,
        "task_id": args.task_id,
    }

    result = call_api(args.interface, kwargs, experience_mode=args.experience)

    # 异步任务自动轮询：文件解析接口返回 task_id 后自动等待结果，避免重复提交
    _POLLING_INTERFACES = {"bank_receipt_parsing", "bank_statement_parsing", "invoice_parsing", "file_parsing"}
    wait_seconds = args.wait if args.wait is not None else 120  # 默认 120 秒
    if args.wait == 0:
        wait_seconds = 0

    if args.interface in _POLLING_INTERFACES and wait_seconds > 0 and isinstance(result, dict):
        # 提取 task_id（兼容多种返回格式）
        task_id = None
        data = result.get("data")
        if isinstance(data, dict):
            task_id = data.get("task_id")
        if not task_id:
            task_id = result.get("task_id")

        if task_id:
            print(f"[异步任务] task_id: {task_id}，自动等待结果（最长 {wait_seconds} 秒）...")
            start_time = time.time()
            poll_interval = 3
            final_result = None

            while time.time() - start_time < wait_seconds:
                time.sleep(poll_interval)
                elapsed = int(time.time() - start_time)

                poll_kwargs = {"task_id": task_id}
                poll_result = call_api("async_result", poll_kwargs, experience_mode=args.experience)

                if isinstance(poll_result, dict):
                    pcode = poll_result.get("code")
                    if pcode == 1000:
                        final_result = poll_result
                        print(f"[异步任务] 解析完成（耗时约 {elapsed} 秒）")
                        break
                    elif pcode in (2001, 3007):
                        # 2001: 处理中；3007: 任务正在执行中，均继续轮询
                        print(f"[异步任务] 处理中...（已等待 {elapsed} 秒）")
                        poll_interval = min(poll_interval + 1, 8)
                    else:
                        final_result = poll_result
                        print(f"[异步任务] 查询异常: {poll_result.get('msg', '未知错误')}")
                        break
                else:
                    print(f"[异步任务] 轮询响应异常，重试中...")

            if final_result:
                result = final_result
            elif not final_result:
                print(f"[异步任务] 超时未完成，task_id: {task_id}")
                print(f"[异步任务] 请稍后手动查询：python scripts/api_client.py async_result --task-id {task_id}"
                      + (" --experience" if args.experience else ""))

    format_result(result, interface_name=args.interface, experience_mode=args.experience)

    # ---- v1.2.0：解析完成后自动生成记账凭证 ----
    if args.voucher and args.interface in _POLLING_INTERFACES:
        if not _HAS_VOUCHER:
            print("\n[凭证生成] 警告：voucher_generator 模块未安装，跳过凭证生成")
        else:
            _generate_voucher_from_result(
                result, args.interface,
                business_type=args.business_type,
                gen_html=args.voucher_html,
            )


if __name__ == "__main__":
    main()

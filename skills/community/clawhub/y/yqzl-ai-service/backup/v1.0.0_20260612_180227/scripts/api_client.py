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

API_BASE_URL = "http://8.135.62.13:5000/AIService"
GET_API_KEY_URL = "http://8.135.62.13:5000/"


def _get_skill_version():
    """读取技能版本号"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    version_file = os.path.join(skill_dir, "version")
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "unknown"


# 接口参数定义（与 yqzlAIService 保持一致）
INTERFACE_DEFS = {
    "bank_receipt_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "银行回单解析"
    },
    "bank_statement_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "银行对账单解析"
    },
    "invoice_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "发票解析"
    },
    "file_parsing": {
        "method": "POST",
        "params": ["file", "file_url", "callback_url"],
        "required_one_of": ["file", "file_url"],
        "desc": "文件解析"
    },
    "async_result": {
        "method": "POST",
        "params": ["task_id"],
        "required": ["task_id"],
        "desc": "异步任务结果查询"
    },
    "ping": {
        "method": "GET",
        "params": [],
        "desc": "服务连通性测试"
    },
}


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


def call_api(interface_name, kwargs):
    """调用远程接口"""
    api_key = _check_api_key()
    headers = {"Authorization": api_key}
    url = f"{API_BASE_URL}/{interface_name}"

    definition = INTERFACE_DEFS.get(interface_name)
    if not definition:
        return {"code": 3001, "msg": f"未知接口: {interface_name}"}

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

    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=30)
        else:
            if files:
                resp = requests.post(url, data=data, files=files, headers=headers, timeout=120)
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


def format_result(result):
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
            print(f"任务ID: {task_id}")
            print("可使用以下命令查询结果：")
            print(f'  python {os.path.join(_SCRIPT_DIR, "api_client.py")} async_result --task-id {task_id}')
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        # 直接打印完整结果用于调试
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    version = _get_skill_version()
    parser = argparse.ArgumentParser(
        description=f"云启智联AI服务接口调用客户端 (版本: {version})"
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
    parser.add_argument("--version", action="store_true", help="显示版本号")

    args = parser.parse_args()

    if args.version:
        print(f"yqzl-ai-service 版本: {version}")
        sys.exit(0)

    if not args.interface:
        parser.print_help()
        sys.exit(1)

    kwargs = {
        "file": args.file,
        "file_url": args.file_url,
        "callback_url": args.callback_url,
        "task_id": args.task_id,
    }

    result = call_api(args.interface, kwargs)
    format_result(result)


if __name__ == "__main__":
    main()

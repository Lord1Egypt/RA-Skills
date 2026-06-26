#!/usr/bin/env python3
"""
腾讯云诊断参数预获取脚本

功能：凭证检查 → 查询实例信息 → 获取可用指标列表。
所有参数（region/namespace/dimension-key）由 AI 从 product profile 查表获得后传入，脚本不做推断。

必填参数:
  --instance-id    实例 ID (如 ins-xxx, cdb-xxx)
  --product        产品类型 (如 cvm, cdb, redis)
  --region         地域编码 (如 ap-shanghai)
  --namespace      监控 namespace (如 QCE/CVM)
  --dimension-key  监控维度 key (如 InstanceId)

可选参数:
  --exec-tat       通过 TAT 远程执行只读 Shell 命令（CVM/Lighthouse 专用）
  --tat-timeout    TAT 命令超时秒数（默认 60）

输出 JSON 格式:
{
  "status": "ok" | "auth_failed" | "not_installed" | "error",
  "region": "ap-shanghai",
  "namespace": "QCE/CVM",
  "dimension_key": "InstanceId",
  "instance_info": { ... },
  "metrics": ["CpuUsage", "MemUsage", ...],
  "message": "..."
}
"""

import argparse
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional


# 产品 → 实例查询 API 的映射（用于查询实例详情）
PRODUCT_INSTANCE_API = {
    "cvm": {"service": "cvm", "action": "DescribeInstances", "id_param": "InstanceIds", "result_key": "InstanceSet", "count_key": "TotalCount"},
    "lighthouse": {"service": "lighthouse", "action": "DescribeInstances", "id_param": "InstanceIds", "result_key": "InstanceSet", "count_key": "TotalCount"},
    "cdb": {"service": "cdb", "action": "DescribeDBInstances", "id_param": "InstanceIds", "result_key": "Items", "count_key": "TotalCount"},
    "cynosdb": {"service": "cynosdb", "action": "DescribeInstances", "id_param": "InstanceIds", "result_key": "InstanceSet", "count_key": "TotalCount"},
    "tdsql-c": {"service": "cynosdb", "action": "DescribeInstances", "id_param": "InstanceIds", "result_key": "InstanceSet", "count_key": "TotalCount"},
    "tdsql": {"service": "cynosdb", "action": "DescribeInstances", "id_param": "InstanceIds", "result_key": "InstanceSet", "count_key": "TotalCount"},
    "postgres": {"service": "postgres", "action": "DescribeDBInstances", "id_param": "DBInstanceIdSet", "result_key": "DBInstanceSet", "count_key": "TotalCount"},
    "sqlserver": {"service": "sqlserver", "action": "DescribeDBInstances", "id_param": "InstanceIdSet", "result_key": "DBInstances", "count_key": "TotalCount"},
    "redis": {"service": "redis", "action": "DescribeInstances", "id_param": "InstanceId", "result_key": "InstanceSet", "count_key": "TotalCount", "id_is_string": True},
    "mongodb": {"service": "mongodb", "action": "DescribeDBInstances", "id_param": "InstanceIds", "result_key": "InstanceDetails", "count_key": "TotalCount"},
    "mariadb": {"service": "mariadb", "action": "DescribeDBInstances", "id_param": "InstanceIds", "result_key": "Instances", "count_key": "TotalCount"},
    "clb": {"service": "clb", "action": "DescribeLoadBalancers", "id_param": "LoadBalancerIds", "result_key": "LoadBalancerSet", "count_key": "TotalCount"},
    "nat": {"service": "vpc", "action": "DescribeNatGateways", "id_param": "NatGatewayIds", "result_key": "NatGatewaySet", "count_key": "TotalCount"},
    "es": {"service": "es", "action": "DescribeInstances", "id_param": "InstanceIds", "result_key": "InstanceList", "count_key": "TotalCount"},
    "ckafka": {"service": "ckafka", "action": "DescribeInstancesDetail", "id_param": "InstanceId", "result_key": "InstanceList", "count_key": "TotalCount", "id_is_string": True},
    "vpn": {"service": "vpc", "action": "DescribeVpnGateways", "id_param": "VpnGatewayIds", "result_key": "VpnGatewaySet", "count_key": "TotalCount"},
}


def run_tccli(args: List[str], timeout: int = 15) -> Optional[Dict[str, Any]]:
    """执行 tccli 命令并返回 JSON 解析结果"""
    cmd = ["tccli"] + args + ["--output", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = (result.stdout + result.stderr).strip()

        auth_keywords = ["AuthFailure", "TokenFailure", "RefreshTokenError", "credential"]
        for kw in auth_keywords:
            if kw.lower() in output.lower():
                return {"_auth_failed": True, "_output": output}

        if result.returncode != 0:
            return {"_error": True, "_output": output}

        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"_error": True, "_output": "命令超时"}
    except json.JSONDecodeError:
        return {"_error": True, "_output": result.stdout[:500] if result else "无输出"}
    except FileNotFoundError:
        return {"_not_installed": True}


def check_tccli() -> Dict[str, Any]:
    """检查 tccli 凭证是否可用"""
    data = run_tccli(["cvm", "DescribeRegions"])
    if data is None:
        return {"status": "not_installed", "message": "tccli 未安装，请执行: pip install tccli"}
    if data.get("_not_installed"):
        return {"status": "not_installed", "message": "tccli 未安装，请执行: pip install tccli"}
    if data.get("_auth_failed"):
        return {"status": "auth_failed", "message": f"tccli 凭证失败: {data.get('_output', '')[:200]}"}
    if data.get("_error"):
        return {"status": "error", "message": f"tccli 异常: {data.get('_output', '')[:200]}"}
    return {"status": "ok"}


def query_instance_info(instance_id: str, product: str, region: str) -> Optional[Dict]:
    """查询指定地域的实例信息"""
    api_config = PRODUCT_INSTANCE_API.get(product)
    if not api_config:
        return None

    service = api_config["service"]
    action = api_config["action"]
    id_param = api_config["id_param"]
    result_key = api_config["result_key"]
    count_key = api_config["count_key"]
    id_is_string = api_config.get("id_is_string", False)

    id_value = instance_id if id_is_string else json.dumps([instance_id])
    cli_args = [service, action, "--region", region, f"--{id_param}", id_value]

    data = run_tccli(cli_args, timeout=10)
    if not data or data.get("_error") or data.get("_auth_failed"):
        return None

    count = data.get(count_key, 0)
    if count and count > 0:
        instances = data.get(result_key, [])
        return instances[0] if instances else None
    return None


def get_metrics_list(region: str, namespace: str) -> Dict:
    """获取指定 namespace 的可用指标列表"""
    data = run_tccli([
        "monitor", "DescribeBaseMetrics",
        "--cli-unfold-argument",
        "--region", region,
        "--Namespace", namespace
    ])

    if not data or data.get("_error"):
        return {"metrics": [], "error": data.get("_output", "获取失败") if data else "获取失败"}

    metric_set = data.get("MetricSet", [])
    metrics = [m.get("MetricName", "") for m in metric_set if m.get("MetricName")]
    return {"metrics": metrics, "total_metrics": len(metrics)}


def exec_tat_command(region: str, instance_id: str, command: str, timeout: int = 60) -> Dict:
    """通过 TAT 远程执行 Shell 命令，自动 base64 编码、执行、等待、解码输出"""
    import base64
    import time

    b64_content = base64.b64encode(command.encode("utf-8")).decode("utf-8")

    data = run_tccli([
        "tat", "RunCommand",
        "--region", region,
        "--InstanceIds", json.dumps([instance_id]),
        "--CommandType", "SHELL",
        "--Content", b64_content,
        "--Timeout", str(timeout),
    ])

    if not data or data.get("_auth_failed") or data.get("_error"):
        msg = data.get("_output", "RunCommand 失败") if data else "RunCommand 失败"
        return {"status": "error", "message": msg[:500], "command": command}

    invocation_id = data.get("InvocationId")
    if not invocation_id:
        return {"status": "error", "message": "RunCommand 未返回 InvocationId", "command": command}

    max_wait = timeout + 15
    waited = 0
    task_id = None
    task_status = None

    while waited < max_wait:
        time.sleep(3)
        waited += 3

        inv_data = run_tccli([
            "tat", "DescribeInvocations",
            "--region", region,
            "--InvocationIds", json.dumps([invocation_id]),
        ])

        if not inv_data or inv_data.get("_error"):
            continue

        inv_set = inv_data.get("InvocationSet", [])
        if not inv_set:
            continue

        inv = inv_set[0]
        inv_status = inv.get("InvocationStatus", "")
        tasks = inv.get("InvocationTaskBasicInfoSet", [])

        if tasks:
            task_id = tasks[0].get("InvocationTaskId")
            task_status = tasks[0].get("TaskStatus")

        if inv_status in ("SUCCESS", "FAILED", "PARTIAL_FAILED", "TIMEOUT"):
            break

    if not task_id:
        return {"status": "error", "message": f"未获取到 TaskId，InvocationStatus={task_status}", "command": command}

    task_data = run_tccli([
        "tat", "DescribeInvocationTasks",
        "--region", region,
        "--InvocationTaskIds", json.dumps([task_id]),
    ])

    if not task_data or task_data.get("_error"):
        return {"status": "error", "message": "获取命令输出失败", "command": command}

    task_set = task_data.get("InvocationTaskSet", [])
    if not task_set:
        return {"status": "error", "message": "InvocationTaskSet 为空", "command": command}

    task = task_set[0]
    task_result = task.get("TaskResult", {})
    exit_code = task_result.get("ExitCode", -1)
    b64_output = task_result.get("Output", "")
    b64_error = task_result.get("Error", "")

    output = ""
    if b64_output:
        try:
            output = base64.b64decode(b64_output).decode("utf-8", errors="replace")
        except Exception:
            output = f"[base64 解码失败: {b64_output[:100]}]"

    error_output = ""
    if b64_error:
        try:
            error_output = base64.b64decode(b64_error).decode("utf-8", errors="replace")
        except Exception:
            error_output = f"[base64 解码失败: {b64_error[:100]}]"

    result = {
        "status": "ok" if task_status == "SUCCESS" and exit_code == 0 else "error",
        "command": command,
        "task_status": task_status,
        "exit_code": exit_code,
        "output": output,
    }
    if error_output:
        result["error_output"] = error_output

    return result


def main():
    parser = argparse.ArgumentParser(description="腾讯云诊断参数预获取")
    parser.add_argument("--instance-id", required=True, help="实例 ID")
    parser.add_argument("--product", required=True, help="产品类型 (如 cvm, cdb, redis)")
    parser.add_argument("--region", required=True, help="地域编码 (如 ap-shanghai)，必须由用户提供或从对话中识别")
    parser.add_argument("--namespace", required=True, help="监控 namespace (如 QCE/CVM)，从 profile 产品参数表获取")
    parser.add_argument("--dimension-key", required=True, help="监控维度 key (如 InstanceId)，从 profile 产品参数表获取")
    parser.add_argument("--exec-tat", default=None,
                        help="通过 TAT 远程执行只读 Shell 命令（CVM/Lighthouse 专用）。"
                             "示例: --exec-tat 'top -bn1 | head -20'")
    parser.add_argument("--tat-timeout", type=int, default=60, help="TAT 命令超时秒数（默认 60）")
    args = parser.parse_args()

    # ── TAT 远程执行模式 ──
    if args.exec_tat:
        tat_result = exec_tat_command(args.region, args.instance_id, args.exec_tat, args.tat_timeout)
        print(json.dumps(tat_result, ensure_ascii=False, indent=2))
        sys.exit(0 if tat_result.get("status") == "ok" else 1)

    # ── 正常预获取模式 ──
    product = args.product.lower()

    # Step 1: 凭证检查
    check = check_tccli()
    if check["status"] != "ok":
        print(json.dumps(check, ensure_ascii=False, indent=2))
        sys.exit(1 if check["status"] == "auth_failed" else 2)

    result = {
        "status": "ok",
        "instance_id": args.instance_id,
        "product": product,
        "region": args.region,
        "namespace": args.namespace,
        "dimension_key": args.dimension_key,
    }

    # Step 2: 查询实例信息（可选，用于获取 OsName、IP 等）
    instance_info = query_instance_info(args.instance_id, product, args.region)
    if instance_info:
        brief = {}
        # CVM/Lighthouse 通用字段
        for key in ["InstanceId", "InstanceName", "InstanceType", "CPU", "Memory",
                     "InstanceState", "PrivateIpAddresses", "PublicIpAddresses",
                     "OsName", "CreatedTime", "ExpiredTime", "Placement"]:
            if key in instance_info:
                brief[key] = instance_info[key]
        # 数据库/缓存类产品的 IP 和端口字段
        for key in ["WanIp", "Vip", "Port", "Vport", "UniqVpcId", "UniqSubnetId",
                     "WanAddress", "VpcId", "SubnetId", "InternalIP"]:
            if key in instance_info and instance_info[key]:
                brief[key] = instance_info[key]
        result["instance_info"] = brief

    # Step 3: 获取可用指标列表
    metrics_info = get_metrics_list(args.region, args.namespace)
    result["metrics"] = metrics_info.get("metrics", [])
    result["total_metrics"] = metrics_info.get("total_metrics", 0)
    if metrics_info.get("error"):
        result["metrics_error"] = metrics_info["error"]

    # 构建 diagnose.py 推荐命令
    result["diagnose_command"] = (
        f"python3 scripts/diagnose.py"
        f" --instance-id {args.instance_id}"
        f" --region {args.region}"
        f" --namespace {args.namespace}"
        f" --dimension-key {args.dimension_key}"
        f" --metrics '<从profile核心指标中选定3~8个>'"
        f" --problem-start '<ISO8601>' --problem-end '<ISO8601>'"
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


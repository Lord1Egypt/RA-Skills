#!/usr/bin/env python3
"""
阿里云 CMS 监控数据采集
支持 ECS / RDS / SLB / EIP
- ECS: acs_ecs_dashboard
- RDS: acs_rds_dashboard
- SLB: acs_slb_dashboard
- EIP: acs_vpc_eip
"""
import json, time, os, sys
import pandas as pd
from aliyunsdkcore.client import AcsClient
from aliyunsdkcms.request.v20190101 import DescribeMetricListRequest

# === 配置 ===
LTAI = os.environ.get("ALIBABA_ACCESS_KEY_ID", "")
SK = os.environ.get("ALIBABA_ACCESS_KEY_SECRET", "")
REGION = os.environ.get("ALIBABA_REGION", "cn-qingdao")

# 指标定义: (namespace, [(metric_name, value_field)])
METRICS = {
    "ECS": ("acs_ecs_dashboard", [
        ("CPUUtilization",      "Average"),
        ("MemoryUsed",          "Average"),
        ("MemoryUtilization",   "Average"),
        ("DiskReadBPS",         "Average"),
        ("DiskWriteBPS",        "Average"),
        ("InternetInRate",      "Average"),
        ("InternetOutRate",     "Average"),
    ]),
    "RDS": ("acs_rds_dashboard", [
        ("CpuUsage",           "Average"),
        ("MemoryUsage",         "Average"),
        ("DiskUsage",          "Average"),
        ("IOPSUsage",          "Average"),
        ("ConnectionUsage",     "Average"),
        ("QPS",                 "Average"),
    ]),
    "SLB": ("acs_slb_dashboard", [
        ("InstanceTrafficRX",  "Average"),
        ("InstanceTrafficTX",   "Average"),
        ("InstanceQps",         "Average"),
        ("InstanceRt",          "Average"),
        ("InstanceMaxConnection", "Average"),
    ]),
    "EIP": ("acs_vpc_eip", [
        ("net_rx.rate",        "Average"),
        ("net_tx.rate",        "Average"),
        ("net_in.rate_percentage", "Average"),
        ("net_out.rate_percentage","Average"),
    ]),
}

now_ms = int(time.time() * 1000)
start_ms = now_ms - 4 * 86400 * 1000

client = AcsClient(LTAI, SK, REGION)


def fetch_metric(namespace, metric, value_field="Average"):
    """拉取单个指标最新数据（全量实例）"""
    all_instances = {}
    next_token = None

    for _ in range(1, 500):
        req = DescribeMetricListRequest.DescribeMetricListRequest()
        req.set_MetricName(metric)
        req.set_Namespace(namespace)
        req.set_Period(60)
        req.set_StartTime(start_ms)
        req.set_EndTime(now_ms)
        req.set_Length(100)
        if next_token:
            req.set_NextToken(next_token)

        try:
            resp = client.do_action_with_exception(req)
            data = json.loads(resp.decode("utf-8"))
        except Exception as e:
            print(f"    [{metric}] 请求异常: {e}", file=sys.stderr)
            break

        if data.get("Code") != "200":
            break

        pts = json.loads(data["Datapoints"])
        for p in pts:
            iid = (p.get("instanceId") or p.get("instanceId") or
                   p.get("instanceId") or p.get("eipId") or
                   p.get("loadBalancerId") or str(p.get("dimensions", {})))
            ts = p.get("timestamp", 0)
            if iid not in all_instances or ts > all_instances[iid].get("timestamp", 0):
                all_instances[iid] = p

        next_token = data.get("NextToken")
        if not next_token:
            break

    return {iid: p.get(value_field, 0) for iid, p in all_instances.items()}


def collect():
    """采集所有服务，构建 DataFrame"""
    rows = []
    for svc, (ns, metrics) in METRICS.items():
        print(f"\n=== {svc} ({ns}) ===")
        svc_rows = {}

        for metric, vf in metrics:
            print(f"  {metric}...", end=" ", flush=True)
            data = fetch_metric(ns, metric, vf)
            print(f"{len(data)} 实例")
            for iid, val in data.items():
                if iid not in svc_rows:
                    svc_rows[iid] = {"instanceId": iid, "service": svc}
                svc_rows[iid][f"{metric}_{vf}"] = round(val, 2)

        rows.extend(svc_rows.values())

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.set_index("instanceId")
    return df


if __name__ == "__main__":
    print(f"阿里云监控采集 | Region: {REGION} | 近4天数据")
    df = collect()
    print(f"\n结果: {len(df)} 条, {len(df.columns)} 列")
    if not df.empty:
        print(df.head(10).to_string())
        out = os.path.join(os.path.expanduser("~/.hermes"), "cron", "output", "aliyun_monitor.xlsx")
        df.reset_index().to_excel(out, index=False)
        print(f"\n已保存: {out}")

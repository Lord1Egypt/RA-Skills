#!/usr/bin/env python3
"""
云服务商监控数据采集 — 统一入口
支持: 阿里云 / 腾讯云 / 华为云

配置方式（环境变量）:
  阿里云: ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET, ALIBABA_REGION
  腾讯云: TENCENT_SECRET_ID, TENCENT_SECRET_KEY, TENCENT_REGION
  华为云: HUAWEI_ACCESS_KEY, HUAWEI_SECRET_KEY, HUAWEI_REGION

输出: ~/.hermes/cron/output/cloud_monitor_{provider}.xlsx
"""
import os, sys, json, time, hashlib, hmac, struct, base64
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()  # 加载 ~/.hermes/.env

# ─── 公共工具 ────────────────────────────────────────────────────────────────

def md5_hex(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def hmac_sha256(key: str, msg: str) -> str:
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# 腾讯云 — TC3-HMAC-SHA256 签名
# ═══════════════════════════════════════════════════════════════════════════════

class TencentCloudSigner:
    """TC3-HMAC-SHA256 签名实现"""
    SERVICE = "cam"
    VERSION = "2020-02-17"           # CAM API 版本（监控用 monitor 版本）

    def __init__(self, secret_id: str, secret_key: str, region: str):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region

    def _sign_tc3(self, key: str, msg: str) -> str:
        """TC3 签名"""
        k = ("TC3" + key).encode()
        return hmac.new(k, msg.encode(), hashlib.sha256).hexdigest()

    def _hmac_sha256_hex(self, key: str, msg: str) -> str:
        return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

    def sign(self, method: str, host: str, uri: str,
             params: dict, payload: str, timestamp: int) -> dict:
        """
        生成签名 v5 标准的 HTTP 头
        返回 {"Authorization": "...", "X-Date": "...", ...}
        """
        # 1. HashedCanonicalRequest
        hashed_payload = sha256_hex(payload)
        timestamp_str = str(timestamp)
        date_str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

        canonical_uri = uri or "/"
        canonical_query = "&".join(f"{k}={params[k]}" for k in sorted(params))

        canonical_request = (
            f"{method}\n"
            f"{canonical_uri}\n"
            f"{canonical_query}\n"
            f"host:{host}\n"
            f"content-type:application/json\n"
            f"host\n"
            f"{hashed_payload}"
        )
        hashed_canonical = sha256_hex(canonical_request)

        # 2. StringToSign
        credential_scope = f"{date_str}/tc3_request"
        string_to_sign = (
            f"TC3-HMAC-SHA256\n"
            f"{timestamp_str}\n"
            f"{credential_scope}\n"
            f"{hashed_canonical}"
        )

        # 3. Signature
        secret_date = self._sign_tc3(self.secret_key, date_str)
        secret_signing = self._sign_tc3(secret_date, "tc3_request")
        signature = self._sign_tc3(secret_signing, string_to_sign)

        # 4. Authorization
        authorization = (
            f"TC3-HMAC-SHA256 "
            f"Credential={self.secret_id}/{credential_scope}, "
            f"SignedHeaders=host;content-type, "
            f"Signature={signature}"
        )

        return {
            "Authorization": authorization,
            "X-Date": timestamp_str,
            "X-Api-Key": self.secret_id,
            "Content-Type": "application/json",
        }


def tencent_api(action: str, payload: dict,
                secret_id: str, secret_key: str,
                region: str, service: str = "monitor",
                version: str = "2018-07-24") -> dict:
    """
    腾讯云 API 调用（Python 实现签名，无 SDK 依赖）
    service: cam / monitor / cvm
    """
    import httpx

    host = f"{service}.tencentcloudapi.com"
    uri = "/"
    timestamp = int(time.time())
    params = {
        "Action": action,
        "Version": version,
        "Region": region,
        "Timestamp": timestamp,
        "Nonce": 1,
    }

    signer = TencentCloudSigner(secret_id, secret_key, region)
    headers = signer.sign("POST", host, uri, params,
                          json.dumps(payload), timestamp)

    url = f"https://{host}/"
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, headers=headers, params=params,
                           content=json.dumps(payload).encode())
    resp.raise_for_status()
    return resp.json()


def collect_tencent_cvm() -> dict:
    """
    采集腾讯云 CVM 实例基础监控
    InstanceId, CPU, Memory, InternetIn, InternetOut
    """
    secret_id = os.environ.get("TENCENT_SECRET_ID")
    secret_key = os.environ.get("TENCENT_SECRET_KEY")
    region = os.environ.get("TENCENT_REGION", "ap-shanghai")

    if not secret_id or not secret_key:
        print("[腾讯云] 未配置 TENCENT_SECRET_ID / TENCENT_SECRET_KEY，跳过")
        return {}

    print(f"\n=== 腾讯云 CVM (region={region}) ===")

    # 1. 拉取实例列表
    try:
        res = tencent_api("DescribeInstances", {},
                          secret_id, secret_key, region, service="cvm",
                          version="2017-03-12")
        instances = res.get("Response", {}).get("InstanceSet", [])
    except Exception as e:
        print(f"  [腾讯云] 拉取实例列表失败: {e}")
        return {}

    if not instances:
        print(f"  [腾讯云] 无 CVM 实例")
        return {}

    print(f"  找到 {len(instances)} 台 CVM")

    rows = {}
    for inst in instances:
        iid = inst.get("InstanceId", "?")
        # 基础信息
        rows[iid] = {
            "instanceId": iid,
            "service": "腾讯云_CVM",
            "InstanceType": inst.get("InstanceType", ""),
            "Status": inst.get("InstanceState", ""),
            "CPU_Average": 0,
            "Memory_Used_G": 0,
            "Memory_Utilization": 0,
            "InternetInRate": 0,
            "InternetOutRate": 0,
        }

    # 2. 拉取监控数据（最新 1 小时）
    end_time = int(time.time())
    start_time = end_time - 3600

    metrics_map = {
        "CPU_Average": ["CPUUtilization"],
        "Memory_Utilization": ["MemUtilization"],
        "InternetInRate": ["InternetIn"],
        "InternetOutRate": ["InternetOut"],
    }

    for iid in rows:
        try:
            m_res = tencent_api("DescribeMonitorData", {
                "Namespace": "QCE/CVM",
                "Instances": [
                    {"Dimensions": {"InstanceId": iid}}
                ],
                "StartTime": start_time,
                "EndTime": end_time,
                "Period": 60,
            }, secret_id, secret_key, region, service="monitor")
            datapoints = m_res.get("Response", {}).get("DataPoints", [])
            for dp in datapoints:
                metric = dp.get("MetricName", "")
                vals = dp.get("Values", [])
                avg = round(sum(vals) / len(vals), 2) if vals else 0
                for k, v in metrics_map.items():
                    if metric in v and k in rows[iid]:
                        rows[iid][k] = avg
        except Exception as e:
            print(f"  [{iid}] 监控数据拉取失败: {e}")

    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# 华为云 — IAM Token + Cloud Eye 监控
# ═══════════════════════════════════════════════════════════════════════════════

def huawei_token(access_key: str, secret_key: str, region: str) -> tuple:
    """获取华为云 IAM Token，返回 (token, endpoint)"""
    import httpx

    # 统一身份认证 endpoint
    iam_endpoints = {
        "cn-east-3": "iam.cn-east-3.myhuaweicloud.com",
        "cn-north-4": "iam.cn-north-4.myhuaweicloud.com",
        "cn-south-1": "iam.cn-south-1.myhuaweicloud.com",
    }
    iam_host = iam_endpoints.get(region, f"iam.{region}.myhuaweicloud.com")

    body = {
        "auth": {
            "identity": {
                "methods": ["hw-access-key"],
                "hw-access-key": {"access_key": access_key}
            },
            "scope": {"project": {"name": region}}
        }
    }

    url = f"https://{iam_host}/v3.0/OS-CREDENTIAL/credentials"
    headers = {"Content-Type": "application/json"}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, headers=headers, json=body)
    resp.raise_for_status()
    data = resp.json()
    token = data["credential"]["token"]
    return token, f"ces.{region}.myhuaweicloud.com"


def collect_huawei_ecs() -> dict:
    """
    采集华为云 ECS 监控数据
    """
    access_key = os.environ.get("HUAWEI_ACCESS_KEY")
    secret_key = os.environ.get("HUAWEI_SECRET_KEY")
    region = os.environ.get("HUAWEI_REGION", "cn-east-3")

    if not access_key or not secret_key:
        print("[华为云] 未配置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY，跳过")
        return {}

    print(f"\n=== 华为云 ECS (region={region}) ===")

    try:
        token, ces_host = huawei_token(access_key, secret_key, region)
    except Exception as e:
        print(f"  [华为云] 获取 Token 失败: {e}")
        return {}

    # 1. 拉取 ECS 实例列表
    import httpx
    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
    list_url = f"https://ecs.{region}.myhuaweicloud.com/v1/{access_key}/cloudservers"
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(list_url, headers=headers,
                              params={"availability_zone": f"{region}-az1"})
        resp.raise_for_status()
        servers = resp.json().get("servers", [])
    except Exception as e:
        print(f"  [华为云] 拉取实例列表失败: {e}")
        return {}

    if not servers:
        print(f"  [华为云] 无 ECS 实例")
        return {}

    print(f"  找到 {len(servers)} 台 ECS")

    # 2. 拉取监控数据
    end_time = int(time.time()) * 1000
    start_time = (int(time.time()) - 3600) * 1000

    rows = {}
    metrics_to_fetch = [
        ("cpu_core", "cpu_core"),
        ("mem_used", "mem_used"),
        ("mem_util", "mem_utilization"),
        ("net_in", "net_in"),
        ("net_out", "net_out"),
    ]

    for srv in servers:
        iid = srv.get("id", "?")
        rows[iid] = {
            "instanceId": iid,
            "service": "华为云_ECS",
            "name": srv.get("name", ""),
            "status": srv.get("status", ""),
            "cpu_core": 0,
            "mem_util": 0,
            "net_in": 0,
            "net_out": 0,
        }

        for metric_key, metric_name in metrics_to_fetch:
            monitor_url = (
                f"https://{ces_host}/V1.0/{access_key}/metric_analytics"
                f"?search_object_id={iid}&namespace=SYS.ECS"
            )
            try:
                with httpx.Client(timeout=30) as client:
                    m_resp = client.get(monitor_url, headers=headers)
                m_resp.raise_for_status()
                m_data = m_resp.json()
                datapoints = m_data.get("datapoints", [])
                if datapoints:
                    vals = [dp.get("average", 0) for dp in datapoints]
                    rows[iid][metric_key] = round(sum(vals) / len(vals), 2)
            except Exception:
                pass

    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# 阿里云 — SDK 采集（参考 aliyun_monitor.py）
# ═══════════════════════════════════════════════════════════════════════════════

def collect_aliyun() -> dict:
    """采集阿里云 ECS 监控"""
    try:
        import json as _json
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcms.request.v20190101 import DescribeMetricListRequest
    except ImportError:
        print("[阿里云] SDK 未安装，跳过 (uv run --with aliyun-python-sdk-core --with aliyun-python-sdk-cms)")
        return {}

    LTAI = os.environ.get("ALIBABA_ACCESS_KEY_ID")
    SK = os.environ.get("ALIBABA_ACCESS_KEY_SECRET")
    REGION = os.environ.get("ALIBABA_REGION", "cn-qingdao")

    if not LTAI or not SK:
        print("[阿里云] 未配置 ALIBABA_ACCESS_KEY_ID / ALIBABA_ACCESS_KEY_SECRET，跳过")
        return {}

    # 指标可配置: ALIBABA_METRICS=CPUUtilization,MemoryUtilization,InternetInRate,...
    # 不配置则使用默认指标
    default_metrics = [
        ("CPUUtilization",   "CPU_Average"),
        ("InternetInRate",  "InternetInRate"),
        ("InternetOutRate", "InternetOutRate"),
        ("DiskReadBPS",     "DiskReadBPS"),
        ("DiskWriteBPS",    "DiskWriteBPS"),
    ]
    metrics_str = os.environ.get("ALIBABA_METRICS", "").strip()
    if metrics_str:
        # 格式: CPUUtilization,InternetInRate,DiskReadBPS
        # 指标名即列名
        METRICS = [(m.strip(), m.strip()) for m in metrics_str.split(",") if m.strip()]
        print(f"[阿里云] 使用自定义指标: {[m[0] for m in METRICS]}")
    else:
        METRICS = default_metrics

    client = AcsClient(LTAI, SK, REGION)
    now_ms = int(time.time() * 1000)
    start_ms = now_ms - 4 * 86400 * 1000

    rows = {}
    for metric, col_name in METRICS:
        next_token = None
        for _ in range(1, 500):
            req = DescribeMetricListRequest.DescribeMetricListRequest()
            req.set_MetricName(metric)
            req.set_Namespace("acs_ecs_dashboard")
            req.set_Period(60)
            req.set_StartTime(start_ms)
            req.set_EndTime(now_ms)
            req.set_Length(100)
            if next_token:
                req.set_NextToken(next_token)

            try:
                resp = client.do_action_with_exception(req)
                data = _json.loads(resp.decode("utf-8"))
            except Exception as e:
                print(f"  [{metric}] 请求异常: {e}")
                break

            if data.get("Code") != "200":
                print(f"  [{metric}] API错误: {data.get('Code')}")
                break

            pts = _json.loads(data["Datapoints"])
            for p in pts:
                iid = p.get("instanceId", "?")
                val = p.get("Average", 0)
                if iid not in rows:
                    rows[iid] = {"instanceId": iid, "service": "阿里云_ECS"}
                rows[iid][col_name] = round(val, 2)

            next_token = data.get("NextToken")
            if not next_token:
                break

    print(f"\n=== 阿里云 ECS (region={REGION}) ===")
    print(f"  共 {len(rows)} 台 ECS 有监控数据")
    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# 统一入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import pandas as pd

    all_rows = {}

    # 阿里云
    aliyun_rows = collect_aliyun()
    all_rows.update(aliyun_rows)

    # 腾讯云
    tencent_rows = collect_tencent_cvm()
    all_rows.update(tencent_rows)

    # 华为云
    huawei_rows = collect_huawei_ecs()
    all_rows.update(huawei_rows)

    if not all_rows:
        print("\n无任何云数据，请检查环境变量配置")
        return

    df = pd.DataFrame(list(all_rows.values()))
    df = df.set_index("instanceId")
    print(f"\n合计 {len(df)} 台实例:")
    print(df.to_string())

    out_dir = os.path.join(os.path.expanduser("~/.hermes"), "cron", "output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "cloud_monitor.xlsx")
    df.reset_index().to_excel(out, index=False)
    print(f"\n已保存: {out}")


if __name__ == "__main__":
    main()

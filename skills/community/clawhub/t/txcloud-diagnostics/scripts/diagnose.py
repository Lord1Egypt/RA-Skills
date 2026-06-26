#!/usr/bin/env python3
"""
腾讯云云产品诊断脚本 — 纯执行器模式

本脚本仅负责：接收精确参数 → 调用 tccli 拉取监控数据 → 分析并输出报告。
所有参数（region、namespace、dimension-key、metrics）均由 AI 模型在调用前
通过 tccli API 动态获取并确定，脚本本身不做任何映射、推断或重试。

必填参数:
  --instance-id    实例 ID (如 ins-arzhtadr)
  --region         精确地域编码 (如 ap-shanghai)，由 AI 通过 DescribeRegions 确定
  --namespace      精确监控命名空间 (如 QCE/CVM)，由 AI 通过 DescribeProductList 确定
  --dimension-key  精确维度键名 (如 InstanceId)，由 AI 通过 DescribeBaseMetrics 确定
  --metrics        AI 选定的监控指标列表，逗号分隔 (如 CpuUsage,MemUsage)
  --problem-start  问题开始时间, ISO 8601 格式
  --problem-end    问题结束时间, ISO 8601 格式

可选参数:
  --pad-before     监控数据往前推的分钟数 (默认 15)
  --pad-after      监控数据往后推的分钟数 (默认 15)
  --extra-dims     额外维度参数，逗号分隔的 Key=Value 对 (多维度产品使用)

用法:
  python3 diagnose.py --instance-id ins-arzhtadr --region ap-shanghai \
    --namespace QCE/CVM --dimension-key InstanceId \
    --metrics CpuUsage,MemUsage,CpuLoadavg,CvmDiskUsage \
    --problem-start '2026-03-22T11:00:00+08:00' --problem-end '2026-03-22T12:00:00+08:00'
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class TencentCloudDiagnostics:
    """腾讯云云产品诊断工具 — 纯执行器，接收精确参数"""

    def __init__(self, instance_id: str, region: str, namespace: str,
                 dimension_key: str, metrics: List[str],
                 problem_start: str, problem_end: str,
                 pad_before_minutes: int = 15, pad_after_minutes: int = 15,
                 extra_dims: Optional[Dict[str, str]] = None):
        """
        初始化诊断工具。所有参数均为精确值，由 AI 模型在调用前确定。

        参数说明:
          instance_id        — 实例 ID (如 ins-arzhtadr)
          region             — 精确地域编码 (如 ap-shanghai)
          namespace          — 精确监控命名空间 (如 QCE/CVM)
          dimension_key      — 精确维度键名 (如 InstanceId)
          metrics            — AI 选定的监控指标列表 (如 [CpuUsage, MemUsage])
          problem_start      — 问题开始时间, ISO 8601 格式
          problem_end        — 问题结束时间, ISO 8601 格式
          pad_before_minutes — 监控数据往前推的分钟数 (10~30, 默认15)
          pad_after_minutes  — 监控数据往后推的分钟数 (10~30, 默认15)
          extra_dims         — 额外维度参数 (可选，如 {"SRegion":"ap-shanghai","DRegion":"ap-guangzhou"})
        """
        self.instance_id = instance_id
        self.region = region
        self.namespace = namespace
        self.dimension_key = dimension_key
        self.metrics = metrics
        self.problem_start = problem_start
        self.problem_end = problem_end
        self.pad_before = max(10, min(30, pad_before_minutes))
        self.pad_after = max(10, min(30, pad_after_minutes))
        self.extra_dims: Dict[str, str] = extra_dims or {}

        # 以下字段由脚本计算
        self.start_time: Optional[str] = None
        self.end_time: Optional[str] = None

    # ─── 工具方法 ────────────────────────────────────────────────────────

    def _run_tccli(self, args: List[str], timeout: int = 30) -> Optional[Dict[str, Any]]:
        """执行 tccli 命令并返回 JSON 解析结果"""
        cmd = ["tccli"] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            combined = (result.stdout + result.stderr).strip()

            # 检查 SDK 异常（tccli 有时 exitcode=0 但 stdout 含错误信息）
            if "TencentCloudSDKException" in combined or "InvalidParameterValue" in combined:
                # 提取有用的错误信息
                for line in combined.split("\n"):
                    if "message:" in line.lower() or "code:" in line.lower():
                        print(f"   ❌ API 错误: {line.strip()[:200]}")
                        return None
                print(f"   ❌ API 错误: {combined[:200]}")
                return None

            if result.returncode != 0:
                print(f"   ⚠️ tccli 命令失败: {' '.join(args[:4])}...")
                if result.stderr:
                    print(f"      stderr: {result.stderr.strip()[:200]}")
                return None
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            print(f"   ❌ tccli 命令超时: {' '.join(args[:4])}...")
            return None
        except json.JSONDecodeError:
            print(f"   ❌ tccli 返回非 JSON 数据: {' '.join(args[:4])}...")
            return None

    def check_tccli(self) -> bool:
        """检查 tccli 是否已安装且凭证有效"""
        # 1. 检查 tccli 是否安装
        try:
            result = subprocess.run(
                ["which", "tccli"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                print("   ❌ tccli 未安装，请先执行: pip install tccli")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("   ❌ tccli 未安装，请先执行: pip install tccli")
            return False

        print("   ✅ tccli 已安装")

        # 2. 检查凭证是否有效
        try:
            result = subprocess.run(
                ["tccli", "cvm", "DescribeRegions", "--output", "json"],
                capture_output=True, text=True, timeout=15
            )
            output = (result.stdout + result.stderr).strip()

            if result.returncode == 0:
                print("   ✅ tccli 凭证有效")
                return True
            else:
                print(f"   ❌ tccli 凭证检查失败: {output}")
                return False

        except subprocess.TimeoutExpired:
            print("   ❌ tccli 凭证验证超时")
            return False
        except Exception as e:
            print(f"   ❌ tccli 凭证验证异常: {e}")
            return False

    # ─── 计算查询时间段 ──────────────────────────────────────────────────

    def resolve_time_range(self) -> bool:
        """根据问题时间段计算实际查询的 starttime / endtime"""
        try:
            start_dt = datetime.fromisoformat(self.problem_start)
            end_dt = datetime.fromisoformat(self.problem_end)

            actual_start = start_dt - timedelta(minutes=self.pad_before)
            actual_end = end_dt + timedelta(minutes=self.pad_after)

            self.start_time = actual_start.isoformat()
            self.end_time = actual_end.isoformat()

            print(f"   ✅ 监控查询时间段:")
            print(f"      用户反馈时段:  {self.problem_start} ~ {self.problem_end}")
            print(f"      实际查询时段:  {self.start_time} ~ {self.end_time}")
            print(f"      (前推 {self.pad_before} 分钟, 后推 {self.pad_after} 分钟)")
            return True
        except (ValueError, TypeError) as e:
            print(f"   ❌ 时间格式解析失败: {e}")
            print(f"      请使用 ISO 8601 格式, 如: 2026-03-20T10:51:23+08:00")
            return False

    # ─── 获取单个监控指标数据 ────────────────────────────────────────────

    def _fetch_metric(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """
        用精确的 namespace + dimension_key 获取单个指标数据。
        如果有 extra_dims，使用多维度查询。
        """
        cmd_args: List[str] = [
            "monitor", "GetMonitorData",
            "--cli-unfold-argument",
            "--region", self.region,
            "--Namespace", self.namespace,
            "--MetricName", metric_name,
        ]

        if self.extra_dims:
            # 多维度查询：实例 ID 维度 + 额外维度
            cmd_args.extend([
                "--Instances.0.Dimensions.0.Name", self.dimension_key,
                "--Instances.0.Dimensions.0.Value", self.instance_id,
            ])
            for idx, (dim_name, dim_value) in enumerate(self.extra_dims.items(), 1):
                cmd_args.extend([
                    f"--Instances.0.Dimensions.{idx}.Name", dim_name,
                    f"--Instances.0.Dimensions.{idx}.Value", dim_value,
                ])
        else:
            # 单维度查询
            cmd_args.extend([
                "--Instances.0.Dimensions.0.Name", self.dimension_key,
                "--Instances.0.Dimensions.0.Value", self.instance_id,
            ])

        cmd_args.extend([
            "--StartTime", self.start_time,
            "--EndTime", self.end_time,
        ])

        data = self._run_tccli(cmd_args)
        if not data:
            return None

        # 检查 API 错误
        if "Error" in data:
            error = data.get("Error", {})
            print(f"      ❌ API 错误: {error.get('Code', '')} - {error.get('Message', '')}")
            return None

        # 检查是否有实际数据点
        datapoints = data.get("DataPoints", [])
        if datapoints and len(datapoints) > 0:
            values = datapoints[0].get("Values", [])
            if values and len(values) > 0:
                return data

        return None  # 空数据

    def analyze_metric(self, metric_name: str, metric_data: Dict[str, Any]) -> Optional[str]:
        """分析单个指标数据，返回分析文本"""
        datapoints = metric_data.get("DataPoints", [])
        if not datapoints or len(datapoints) == 0:
            return "⚠️ 暂无数据（可能未开启或实例未运行）"

        values = datapoints[0].get("Values", [])
        if not values:
            return "⚠️ 无有效数据值"

        min_val = min(values)
        max_val = max(values)
        avg_val = sum(values) / len(values)

        unit = self._guess_unit(metric_name)

        result_text = (f"均值={avg_val:.2f}{unit}  "
                       f"最小={min_val:.2f}{unit}  "
                       f"最大={max_val:.2f}{unit}  "
                       f"(共 {len(values)} 个数据点)")
        return result_text

    @staticmethod
    def _guess_unit(metric_name: str) -> str:
        """根据指标名称猜测单位"""
        name_lower = metric_name.lower()
        if "percent" in name_lower or "usage" in name_lower or "rate" in name_lower or "util" in name_lower:
            return "%"
        if "bandwidth" in name_lower:
            return " Mbps"
        if "flow" in name_lower or "traffic" in name_lower:
            return " MB"
        if "pkg" in name_lower or "pkt" in name_lower:
            return " pps"
        if "count" in name_lower or "connections" in name_lower:
            return ""
        if "latency" in name_lower or "delay" in name_lower:
            return " ms"
        if "iops" in name_lower:
            return " IOPS"
        if "drop" in name_lower:
            return ""
        return ""

    # ─── 主流程: 生成诊断报告 ──────────────────────────────────────────────

    def generate_report(self):
        """生成完整诊断报告"""

        print("\n" + "=" * 70)
        print("🖥️  腾讯云产品实例健康诊断报告")
        print("=" * 70)

        # Step 0: 验证 tccli
        print("\n⚙️  前置检查:")
        if not self.check_tccli():
            return None
        print("   ✅ tccli 已就绪")

        # Step 1: 计算查询时间段
        print(f"\n⏰ 计算监控查询时间段:")
        if not self.resolve_time_range():
            return None

        # 打印参数汇总
        print("\n" + "-" * 70)
        print("📋 诊断参数汇总:")
        print(f"   • 实例 ID:      {self.instance_id}")
        print(f"   • 地域:         {self.region}")
        print(f"   • 命名空间:     {self.namespace}")
        print(f"   • 维度键名:     {self.dimension_key}")
        if self.extra_dims:
            print(f"   • 额外维度:     "
                  f"{', '.join(f'{k}={v}' for k, v in self.extra_dims.items())}")
        print(f"   • 查询开始:     {self.start_time}")
        print(f"   • 查询结束:     {self.end_time}")
        print(f"   • 采集指标:     {', '.join(self.metrics)} ({len(self.metrics)} 个)")
        print("-" * 70)

        # Step 2: 逐个获取并分析监控指标
        print(f"\n📊 开始采集监控数据 (共 {len(self.metrics)} 个指标):")

        results = {}
        issues = []

        for idx, metric_name in enumerate(self.metrics, 1):
            print(f"\n   [{idx}/{len(self.metrics)}] {metric_name}:")

            data = self._fetch_metric(metric_name)
            if not data:
                results[metric_name] = {"status": "error", "text": "获取失败"}
                continue

            analysis = self.analyze_metric(metric_name, data)

            if not analysis:
                results[metric_name] = {"status": "error", "text": "分析失败"}
                continue

            if analysis.startswith("⚠️") or analysis.startswith("❌"):
                print(f"      {analysis}")
                results[metric_name] = {"status": "warning", "text": analysis}
                issues.append(f"{metric_name}: {analysis}")
                continue

            # 对百分比类指标检查阈值
            status_symbol = "✅"
            if "%" in analysis:
                try:
                    avg_str = analysis.split("均值=")[1].split("%")[0]
                    avg_val = float(avg_str)
                    if avg_val >= 95:
                        status_symbol = "🔴"
                        issues.append(f"{metric_name} 严重超限: 均值={avg_val:.1f}%")
                    elif avg_val >= 80:
                        status_symbol = "⚠️"
                        issues.append(f"{metric_name} 偏高: 均值={avg_val:.1f}%")
                except (ValueError, IndexError):
                    pass

            print(f"      {status_symbol} {analysis}")
            results[metric_name] = {"status": "normal", "text": analysis}

        # Step 3: 生成诊断结论
        print("\n" + "=" * 70)
        print("🎯 诊断结论")
        print("=" * 70)

        # 统计成功/失败
        total = len(results)
        failed = sum(1 for r in results.values() if r.get("status") == "error")
        perf_issues = [i for i in issues if "严重超限" in i or "偏高" in i]

        if failed == total and total > 0:
            print(f"\n❌ 所有 {total} 个监控指标均获取失败")
            print("\n   可能原因:")
            print("   • 实例 ID 不正确或实例已销毁")
            print("   • namespace 或 dimension-key 不匹配")
            print("   • tccli 权限不足（当前账号无权访问该实例）")
            print("   • 查询时间段超出监控保留期（15 天）")
        elif perf_issues:
            print("\n❌ 发现性能异常:")
            for issue in perf_issues:
                print(f"   • {issue}")
            print("\n💡 建议排查方向:")
            print("   1. 登录实例查看进程/资源占用情况")
            print("   2. 检查是否有突发流量或异常任务")
            print("   3. 查看对应产品的运维日志")
            print("   4. 考虑升配或优化业务逻辑")
        elif failed > 0:
            print(f"\n⚠️ {failed}/{total} 个监控指标获取失败:")
            failed_metrics = [k for k, v in results.items() if v.get("status") == "error"]
            for m in failed_metrics[:5]:
                print(f"   • {m}")
            print("\n   可能原因:")
            print("   • 实例 ID 或维度键名不正确")
            print("   • namespace 不匹配")
            print("   • tccli 权限不足")
            print("   • 查询时间段超出监控保留期（15 天）")
        else:
            print(f"\n✅ 实例 {self.instance_id} 状态正常")
            print("   核心监控指标均在健康范围内")
            print("\n💡 建议: 定期巡检监控数据，预防突发负载")

        print(f"\n📅 诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # Step 4: CVM 关联 CBS 磁盘 IO 诊断（仅当 namespace 为 QCE/CVM 且 instance_id 为 ins-xxx 时触发）
        cbs_results = self._diagnose_associated_cbs()
        if cbs_results:
            results["_cbs_disk_io"] = cbs_results

        return json.dumps(results, indent=2, ensure_ascii=False)

    # ─── CVM 关联 CBS 磁盘 IO 自动诊断 ────────────────────────────────────

    CBS_IO_METRICS = [
        "DiskReadTraffic", "DiskWriteTraffic",
        "DiskReadIops", "DiskWriteIops",
        "DiskAwait", "DiskUtil", "DiskSvctm",
        "BsDiskUsage",
    ]

    def _diagnose_associated_cbs(self) -> Optional[dict]:
        """
        当 namespace 为 QCE/CVM 且实例 ID 为 ins-xxx 时，
        自动查询关联的 CBS 云硬盘，并采集磁盘 IO 指标。
        """
        if self.namespace.upper() != "QCE/CVM":
            return None
        if not self.instance_id.startswith("ins-"):
            return None

        print(f"\n{'=' * 70}")
        print(f"💿 关联 CBS 磁盘 IO 诊断")
        print(f"{'=' * 70}")

        # 查询挂载的云硬盘
        print(f"\n   ⏳ 正在查询 {self.instance_id} 关联的云硬盘...")
        disks = self._query_associated_disks()
        if not disks:
            print(f"   ⚠️ 未找到关联的云硬盘，跳过磁盘 IO 诊断")
            return None

        print(f"   ✅ 找到 {len(disks)} 块云硬盘:")
        for d in disks:
            print(f"      • {d['DiskId']}  {d['DiskUsage']}  "
                  f"{d['DiskType']}  {d['DiskSize']}GB  {d.get('DiskName', '')}")

        # 获取 CBS namespace 的可用指标
        cbs_metrics = self._get_cbs_available_metrics()
        if not cbs_metrics:
            print(f"   ⚠️ 无法获取 CBS 监控指标列表，跳过")
            return None

        # 筛选出可用的 IO 指标
        cbs_metric_set = set(cbs_metrics)
        metrics_to_fetch = [m for m in self.CBS_IO_METRICS if m in cbs_metric_set]
        if not metrics_to_fetch:
            print(f"   ⚠️ 无可用的 CBS IO 指标，跳过")
            return None

        # 逐盘采集
        all_disk_results = {}
        for disk in disks:
            disk_id = disk["DiskId"]
            disk_label = f"{disk_id} ({disk['DiskUsage']}, {disk['DiskType']} {disk['DiskSize']}GB)"
            print(f"\n   📀 {disk_label}:")

            disk_results = {}
            for metric_name in metrics_to_fetch:
                data = self._fetch_cbs_metric(disk_id, metric_name)
                if not data:
                    continue

                analysis = self._analyze_cbs_metric(metric_name, data)
                if analysis:
                    status = "✅"
                    if "%" in analysis:
                        try:
                            avg_val = float(analysis.split("均值=")[1].split("%")[0])
                            if avg_val >= 95:
                                status = "🔴"
                            elif avg_val >= 80:
                                status = "⚠️"
                        except (ValueError, IndexError):
                            pass
                    print(f"      {status} {metric_name}: {analysis}")
                    disk_results[metric_name] = {"status": "normal", "text": analysis}

            if not disk_results:
                print(f"      ⚠️ 所有指标获取失败")
            all_disk_results[disk_id] = disk_results

        return all_disk_results if all_disk_results else None

    def _query_associated_disks(self) -> List[dict]:
        """通过 tccli cbs DescribeDisks 查询 CVM 实例关联的云硬盘"""
        data = self._run_tccli([
            "cbs", "DescribeDisks",
            "--Filters", json.dumps([{"Name": "instance-id", "Values": [self.instance_id]}]),
            "--region", self.region,
        ])
        if not data:
            return []
        return [
            {
                "DiskId": d["DiskId"],
                "DiskType": d.get("DiskType", "N/A"),
                "DiskSize": d.get("DiskSize", 0),
                "DiskUsage": d.get("DiskUsage", "N/A"),
                "DiskState": d.get("DiskState", "N/A"),
                "DiskName": d.get("DiskName", ""),
            }
            for d in data.get("DiskSet", [])
            if d.get("DiskState") == "ATTACHED"
        ]

    def _get_cbs_available_metrics(self) -> List[str]:
        """获取 QCE/BLOCK_STORAGE namespace 的可用指标列表"""
        data = self._run_tccli([
            "monitor", "DescribeBaseMetrics",
            "--cli-unfold-argument",
            "--Namespace", "QCE/BLOCK_STORAGE",
            "--region", self.region,
        ])
        if not data:
            return []
        return [m["MetricName"] for m in data.get("MetricSet", [])]

    def _fetch_cbs_metric(self, disk_id: str, metric_name: str) -> Optional[Dict]:
        """用 diskId 维度从 QCE/BLOCK_STORAGE 获取单个 CBS 指标"""
        cmd_args = [
            "monitor", "GetMonitorData",
            "--cli-unfold-argument",
            "--region", self.region,
            "--Namespace", "QCE/BLOCK_STORAGE",
            "--MetricName", metric_name,
            "--Instances.0.Dimensions.0.Name", "diskId",
            "--Instances.0.Dimensions.0.Value", disk_id,
            "--StartTime", self.start_time,
            "--EndTime", self.end_time,
        ]
        data = self._run_tccli(cmd_args)
        if not data or "Error" in data:
            return None
        datapoints = data.get("DataPoints", [])
        if datapoints and len(datapoints) > 0:
            dp = datapoints[0]
            values = dp.get("Values", [])
            if values and len(values) > 0:
                return dp
        return None

    def _analyze_cbs_metric(self, metric_name: str, dp: dict) -> Optional[str]:
        """分析 CBS 指标数据点"""
        values = dp.get("Values", [])
        if not values:
            return None
        avg_val = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        m_lower = metric_name.lower()
        if "usage" in m_lower or "util" in m_lower:
            unit = "%"
        elif "iops" in m_lower:
            unit = " IOPS"
        elif "traffic" in m_lower:
            unit = " MB"
        elif "await" in m_lower or "svctm" in m_lower:
            unit = " ms"
        else:
            unit = ""

        return (f"均值={avg_val:.2f}{unit}  最小={min_val:.2f}{unit}  "
                f"最大={max_val:.2f}{unit}  (共 {len(values)} 个数据点)")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="腾讯云云产品诊断工具 — 纯执行器模式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # CVM 实例诊断
  python3 diagnose.py --instance-id ins-arzhtadr --region ap-shanghai \\
    --namespace QCE/CVM --dimension-key InstanceId \\
    --metrics CpuUsage,MemUsage,CpuLoadavg,CvmDiskUsage \\
    --problem-start '2026-03-22T11:00:00+08:00' --problem-end '2026-03-22T12:00:00+08:00'

  # CDB 实例诊断
  python3 diagnose.py --instance-id cdb-k5d6z7p0 --region ap-guangzhou \\
    --namespace QCE/CDB --dimension-key InstanceId \\
    --metrics SlowQueries,QPS,TPS,CPUUseRate,MemoryUseRate,ThreadsConnected \\
    --problem-start '2026-03-22T14:00:00+08:00' --problem-end '2026-03-22T15:30:00+08:00'

  # 云联网 CCN — 单地域指标
  python3 diagnose.py --instance-id ccn-j69yzbyl --region ap-shanghai \\
    --namespace QCE/VBC --dimension-key CcnId \\
    --metrics Ccninflow,Ccnoutflow \\
    --problem-start '2026-03-24T11:45:00+08:00' --problem-end '2026-03-24T12:15:00+08:00' \\
    --extra-dims region=ap-shanghai

  # 云联网 CCN — 地域间指标
  python3 diagnose.py --instance-id ccn-j69yzbyl --region ap-shanghai \\
    --namespace QCE/VBC --dimension-key CcnId \\
    --metrics Outbandwidth,Inbandwidth \\
    --problem-start '2026-03-24T11:45:00+08:00' --problem-end '2026-03-24T12:15:00+08:00' \\
    --extra-dims SRegion=ap-shanghai,DRegion=ap-guangzhou

AI 模型在调用前需通过 tccli 确定以下精确参数:
  region:        tccli cvm DescribeRegions → Region
  namespace:     tccli monitor DescribeProductList → Namespace
  dimension-key: tccli monitor DescribeBaseMetrics → Dimensions
  metrics:       tccli monitor DescribeBaseMetrics → MetricName (AI 从中选定)
"""
    )
    parser.add_argument("--instance-id", type=str, required=True,
                        help="实例 ID (如 ins-arzhtadr, cdb-k5d6z7p0)")
    parser.add_argument("--region", type=str, required=True,
                        help="精确地域编码 (如 ap-shanghai)，由 AI 通过 DescribeRegions 确定")
    parser.add_argument("--namespace", type=str, required=True,
                        help="精确监控命名空间 (如 QCE/CVM)，由 AI 通过 DescribeProductList 确定")
    parser.add_argument("--dimension-key", type=str, required=True,
                        help="精确维度键名 (如 InstanceId)，由 AI 通过 DescribeBaseMetrics 确定")
    parser.add_argument("--metrics", type=str, required=True,
                        help="监控指标列表，逗号分隔 (如 CpuUsage,MemUsage)")
    parser.add_argument("--problem-start", type=str, required=True,
                        help="问题开始时间, ISO 8601 格式 (如 2026-03-22T11:00:00+08:00)")
    parser.add_argument("--problem-end", type=str, required=True,
                        help="问题结束时间, ISO 8601 格式 (如 2026-03-22T12:00:00+08:00)")
    parser.add_argument("--pad-before", type=int, default=15,
                        help="监控数据往前推的分钟数, 范围 10~30 (default: 15)")
    parser.add_argument("--pad-after", type=int, default=15,
                        help="监控数据往后推的分钟数, 范围 10~30 (default: 15)")
    parser.add_argument("--extra-dims", type=str, default=None,
                        help="额外维度参数, 逗号分隔的 Key=Value 对 "
                             "(如 SRegion=ap-shanghai,DRegion=ap-guangzhou)")

    args = parser.parse_args()

    # 解析参数
    metrics_list = [m.strip() for m in args.metrics.split(",") if m.strip()]
    if not metrics_list:
        print("❌ --metrics 参数不能为空")
        sys.exit(1)

    extra_dims = {}
    if args.extra_dims:
        for pair in args.extra_dims.split(","):
            pair = pair.strip()
            if "=" in pair:
                k, v = pair.split("=", 1)
                extra_dims[k.strip()] = v.strip()

    try:
        diagnostics = TencentCloudDiagnostics(
            instance_id=args.instance_id,
            region=args.region,
            namespace=args.namespace,
            dimension_key=args.dimension_key,
            metrics=metrics_list,
            problem_start=args.problem_start,
            problem_end=args.problem_end,
            pad_before_minutes=args.pad_before,
            pad_after_minutes=args.pad_after,
            extra_dims=extra_dims,
        )

        report = diagnostics.generate_report()

        if report:
            save_file = (f"/tmp/txcloud_diagnostics_{args.instance_id}_"
                         f"{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
            with open(save_file, "w") as f:
                f.write(report)
            print(f"\n💾 报告已保存到: {save_file}")

    except Exception as e:
        print(f"❌ 诊断过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

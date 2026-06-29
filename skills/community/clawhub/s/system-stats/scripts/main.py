"""system_stats skill - 读取系统内存、CPU、网络吞吐率等性能指标"""
import sys
import json
import time

# 强制 stdout 使用 UTF-8，避免 Windows 控制台 GBK 编码错误
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import psutil
except ImportError:
    print("错误: 缺少 psutil 模块，请运行: pip install psutil")
    sys.exit(1)


def parse_args(arg):
    arg = arg.strip()
    if not arg:
        return {"interval": 1}
    if arg.startswith("{"):
        try:
            params = json.loads(arg)
            params.setdefault("interval", 1)
            return params
        except json.JSONDecodeError as e:
            return {"error": f"JSON 参数解析失败: {e}"}
    try:
        return {"interval": int(arg)}
    except ValueError:
        return {"interval": 1}


def format_bytes(n):
    """格式化字节数"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def get_stats(interval=1):
    # CPU
    cpu_percent = psutil.cpu_percent(interval=interval)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_count_physical = psutil.cpu_count(logical=False)

    # 内存
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # 网络 - 采样计算吞吐率
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    bytes_sent_per_sec = net2.bytes_sent - net1.bytes_sent
    bytes_recv_per_sec = net2.bytes_recv - net1.bytes_recv

    # 磁盘 I/O
    disk_io = ""
    try:
        d1 = psutil.disk_io_counters()
        time.sleep(1)
        d2 = psutil.disk_io_counters()
        if d1 and d2:
            read_per_sec = d2.read_bytes - d1.read_bytes
            write_per_sec = d2.write_bytes - d1.write_bytes
            disk_io = f"磁盘 I/O: 读 {format_bytes(read_per_sec)}/s, 写 {format_bytes(write_per_sec)}/s"
    except Exception:
        disk_io = "磁盘 I/O: 不支持"

    # 系统负载（仅 Linux/macOS）
    load_avg = ""
    try:
        load1, load5, load15 = psutil.getloadavg()
        load_avg = f"系统负载: {load1:.2f} / {load5:.2f} / {load15:.2f} (1/5/15分钟)"
    except (AttributeError, OSError):
        pass

    # 进程数
    proc_count = len(psutil.pids())

    # 启动时间
    import datetime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    result = []
    result.append("📊 系统性能指标")
    result.append("=" * 50)
    result.append(f"CPU 占用率: {cpu_percent:.1f}% (共 {cpu_count} 核 / 物理 {cpu_count_physical} 核)")
    result.append(f"内存: {format_bytes(mem.used)} / {format_bytes(mem.total)} ({mem.percent}%)")
    result.append(f"可用内存: {format_bytes(mem.available)}")
    result.append(f"交换分区: {format_bytes(swap.used)} / {format_bytes(swap.total)} ({swap.percent}%)")
    result.append(f"网络吞吐: ↑ {format_bytes(bytes_sent_per_sec)}/s, ↓ {format_bytes(bytes_recv_per_sec)}/s")
    if disk_io:
        result.append(disk_io)
    if load_avg:
        result.append(load_avg)
    result.append(f"进程数: {proc_count}")
    result.append(f"系统启动时间: {boot_time}")

    return "\n".join(result)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    params = parse_args(arg)
    if "error" in params:
        print(params["error"])
    else:
        print(get_stats(params.get("interval", 1)))

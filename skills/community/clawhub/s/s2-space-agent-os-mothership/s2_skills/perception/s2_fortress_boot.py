import subprocess
import re
import socket

# 🔌 [极客连接指引 - 系统级指纹]
# 1. 本模块依赖操作系统的底层网络命令 (arp)。
# 2. 在 Linux 下，确保运行该 Python 脚本的用户具有执行 arp 命令的权限。
# 3. 一旦主机被移动到陌生网络 (网关 MAC 发生突变)，将触发 HARD_LOCK 防盗熔断。

class S2RealEnvironmentFingerprint:
    @staticmethod
    def capture_real_fingerprint() -> dict:
        """【真实物理探测】直接击穿到 OS 物理层，抓取真实网络拓扑特征"""
        real_mac = "UNKNOWN_MAC"
        try:
            # 跨平台提取局域网 ARP 缓存表
            arp_result = subprocess.check_output(["arp", "-a"], text=True)
            
            # 使用正则从 arp 表中精准提取网关设备的 MAC 地址
            # 适配格式: xx:xx:xx:xx:xx:xx 或 xx-xx-xx-xx-xx-xx
            mac_match = re.search(r'(([0-9a-fA-F]{1,2}[:-]){5}[0-9a-fA-F]{1,2})', arp_result)
            if mac_match:
                real_mac = mac_match.group(1).upper().replace("-", ":")
        except Exception as e:
            logging.error(f"⚠️ 无法读取底层 ARP 表: {e}")

        return {
            "gateway_mac": real_mac,
            "os_hostname": socket.gethostname()
        }
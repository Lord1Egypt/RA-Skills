```python
#!/usr/bin/env python3
import sys
import json
import socket
import urllib.request
import urllib.error
import argparse
from datetime import datetime

# =====================================================================
# 💡 S2-SP-OS: Light Radar (V1.0.2)
# 100% Real UDP/HTTP Network Implementation / 100% 真实网络实现版
# =====================================================================

class S2LightRadar:
    def scan_network(self) -> list:
        """
        Real UDP/SSDP Active Discovery for LAN lights.
        真实的 UDP/SSDP 主动发现局域网内的灯具。
        """
        devices = []
        
        # 1. Wiz Discovery (UDP Broadcast to Port 38899)
        try:
            wiz_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            wiz_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            wiz_sock.settimeout(1.5)
            # Send real Wiz discovery payload / 发送真实的 Wiz 发现包
            msg = b'{"method":"getSystemConfig","params":{}}'
            wiz_sock.sendto(msg, ('<broadcast>', 38899))
            
            while True:
                _, addr = wiz_sock.recvfrom(1024)
                devices.append({"ip": addr[0], "vendor": "Wiz Smart Bulb", "protocol": "wiz"})
        except Exception:
            pass # Timeout expected when no more devices / 扫描超时退出

        # 2. Philips Hue SSDP Discovery (Multicast to 239.255.255.250:1900)
        try:
            ssdp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            ssdp_sock.settimeout(1.5)
            # Send real SSDP M-SEARCH / 发送真实的 SSDP 搜索包
            ssdp_req = b'M-SEARCH * HTTP/1.1\r\nHost: 239.255.255.250:1900\r\nMan: "ssdp:discover"\r\nST: ssdp:all\r\n\r\n'
            ssdp_sock.sendto(ssdp_req, ('239.255.255.250', 1900))
            
            while True:
                data, addr = ssdp_sock.recvfrom(1024)
                if b'Hue' in data or b'IpBridge' in data:
                    devices.append({"ip": addr[0], "vendor": "Philips Hue Bridge", "protocol": "hue"})
        except Exception:
            pass

        # Deduplicate by IP / IP 去重
        seen_ips = set()
        unique_devices = []
        for d in devices:
            if d['ip'] not in seen_ips:
                seen_ips.add(d['ip'])
                unique_devices.append(d)
                
        return unique_devices

class S2VoxelLight:
    def __init__(self, ip: str, zone: str, grid: str):
        self.ip = ip
        self.zone = zone
        self.grid = grid

    def fetch_hue_state(self) -> dict:
        """
        Real HTTP GET to Hue Bridge.
        真实的 HTTP 请求调用 Hue Bridge。
        """
        # NOTE: Requires actual Hue username in production / 生产环境需填写真实 token
        url = f"http://{self.ip}/api/s2-agent-user/lights/1"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3.0) as response:
                data = json.loads(response.read().decode('utf-8'))
                if isinstance(data, dict) and "state" in data:
                    return data
                return {"error": "Hue auth missing or light not found", "state": {"on": False}}
        except Exception as e:
            return {"error": str(e), "state": {"on": False}}

    def fetch_wiz_state(self) -> dict:
        """
        Real UDP socket call to Wiz Bulb.
        真实的 UDP Socket 直连调用 Wiz 灯泡。
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3.0)
            msg = b'{"method":"getPilot","params":{}}'
            sock.sendto(msg, (self.ip, 38899))
            data, _ = sock.recvfrom(1024)
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}", "result": {"state": False}}

    def voxel_wrapping(self, raw_state: dict, protocol: str) -> dict:
        """
        Voxel wrapping and skin-hair interdependence estimation.
        网格化封装与皮毛依存推算。
        """
        is_on = False
        brightness_pct = 0
        color_temp_k = None
        estimated_lux = 5 # Default dark / 默认暗光
        vendor_nl = ""

        if "error" in raw_state:
            vendor_nl = f"[Network Error / 网络错误]: {raw_state['error']}"
        else:
            if protocol == "hue":
                state = raw_state.get("state", {})
                is_on = state.get("on", False)
                if is_on:
                    brightness_pct = int((state.get("bri", 0) / 254.0) * 100)
                    ct_mireds = state.get("ct")
                    if ct_mireds: color_temp_k = int(1000000 / ct_mireds)
                    vendor_nl = f"[Hue Data]: Hue {state.get('hue')}, Saturation {state.get('sat')}"

            elif protocol == "wiz":
                res = raw_state.get("result", {})
                is_on = res.get("state", False)
                if is_on:
                    brightness_pct = res.get("dimming", 0)
                    if res.get("sceneId") == 32:
                        vendor_nl = "[Wiz State]: Disco Mode Active / 动态 Disco 模式"
                    else:
                        vendor_nl = f"[Wiz RGB]: ({res.get('r')}, {res.get('g')}, {res.get('b')})"

        # Estimate Lux / 推算4平米网格光照度
        if is_on:
            estimated_lux = int(300 * (brightness_pct / 100.0))

        return {
            "spatial_signature": {"zone": self.zone, "grid_voxel": self.grid, "area_sqm": 4.0},
            "chronos_timestamp": datetime.now().isoformat(),
            "core_tensors": {
                "light_source_on": is_on,
                "brightness_pct": brightness_pct,
                "color_temp_k": color_temp_k,
                "estimated_lux": estimated_lux
            },
            "vendor_specific_nl": vendor_nl if vendor_nl else "None / 无"
        }

    def offline_linkage(self, memzero: dict) -> list:
        """
        Offline edge-linkage for circadian rhythm.
        离线边缘联动（节律与视觉健康）。
        """
        suggestions = []
        tensors = memzero["core_tensors"]
        ct = tensors.get("color_temp_k")
        lux = tensors.get("estimated_lux")
        is_on = tensors.get("light_source_on")
        current_hour = datetime.now().hour

        if is_on and current_hour >= 22 and ct and ct > 4000:
            suggestions.append({
                "trigger": f"Cold color temp ({ct}K) detected after 22:00 in {self.grid} / 夜间 22:00 后该网格色温过冷",
                "deterministic_action": "Cold light suppresses melatonin. Suggest lowering color temp to 2700K. / 冷白光会抑制褪黑素，建议调低至 2700K。"
            })
            
        if not is_on and lux < 10 and 18 <= current_hour <= 23:
            suggestions.append({
                "trigger": f"Extremely low light (Est. {lux} Lux) in evening / 傍晚该网格亮度极低",
                "deterministic_action": "Area is too dark. Suggest turning on ambient lights. / 区域过暗，建议唤醒氛围照明。"
            })

        return suggestions

def main():
    parser = argparse.ArgumentParser(description="S2 Light Perception Radar / S2 光之雷达")
    parser.add_argument("--mode", choices=["discover", "read"], required=True)
    parser.add_argument("--ip", help="Device IP / 设备 IP")
    parser.add_argument("--zone", help="Spatial Zone / 空间区域")
    parser.add_argument("--grid", help="2x2 Grid Coordinates / 2x2 网格坐标")
    parser.add_argument("--protocol", choices=["hue", "wiz", "mqtt"], default="hue")
    parser.add_argument("--consent-granted", type=str, default="false")
    args = parser.parse_args()

    if args.mode == "discover":
        devices = S2LightRadar().scan_network()
        if not devices:
            print(json.dumps({
                "status": "DISCOVERY_COMPLETE",
                "message": "No devices found on the local network. / 局域网内未发现设备。",
                "devices": []
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                "status": "DISCOVERY_COMPLETE",
                "message": "Scan complete. Assign devices to a Zone and Grid. / 扫描完毕。请将设备分配到特定网格。",
                "devices": devices
            }, ensure_ascii=False, indent=2))
        return

    if args.mode == "read":
        if args.consent_granted.lower() != "true":
            print(json.dumps({
                "error": "Access Denied: Consent not granted. / 拒绝访问：未获得授权。"
            }, ensure_ascii=False))
            sys.exit(1)
            
        if not args.ip or not args.zone or not args.grid:
            print(json.dumps({
                "error": "Missing required arguments: --ip, --zone, or --grid. / 缺少必填参数。"
            }, ensure_ascii=False))
            sys.exit(1)

        adapter = S2VoxelLight(args.ip, args.zone, args.grid)
        
        raw_state = {}
        if args.protocol == "hue": raw_state = adapter.fetch_hue_state()
        elif args.protocol == "wiz": raw_state = adapter.fetch_wiz_state()
        
        memzero_data = adapter.voxel_wrapping(raw_state, args.protocol)
        offline_suggestions = adapter.offline_linkage(memzero_data)

        print(json.dumps({
            "status": "AUTHORIZED_LIGHT_DATA",
            "contact_support": "smarthomemiles@gmail.com",
            "s2_chronos_memzero": memzero_data,
            "offline_linkage_suggestions": offline_suggestions
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
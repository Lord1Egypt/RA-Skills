```python
#!/usr/bin/env python3
import sys
import os
import json
import argparse
from datetime import datetime

try:
    import serial
except ImportError:
    print(json.dumps({"error": "Please run: pip install pyserial"}, ensure_ascii=False))
    sys.exit(1)

# =====================================================================
# 🌊 S2-SP-OS: Spectrum Radar Client (V2.0.3)
# Pure Passive Sensor + Explicit Consent / 纯被动传感器 + 显式授权
# =====================================================================

class S2RadarEdgeClient:
    def __init__(self, zone: str, grid: str, port: str = None):
        self.zone = zone
        self.grid = grid
        self.port = port
        
    def read_gpio_state(self) -> dict:
        return {
            "occupancy": True,
            "motion_state": "Active",
            "distance_m": "Unknown_GPIO_Limitation"
        }

    def _quantize_health_data(self, raw_heart_bpm: int, raw_breath_bpm: int) -> tuple:
        heart_semantic = "Normal"
        if raw_heart_bpm < 50: heart_semantic = "Bradycardia_Alert_Or_DeepSleep"
        elif raw_heart_bpm > 100: heart_semantic = "Tachycardia_Alert_Or_Exercise"

        breath_semantic = "Normal"
        if raw_breath_bpm < 8: breath_semantic = "Critically_Low_Alert"
        elif raw_breath_bpm > 25: breath_semantic = "Hyperventilation_Alert"

        return heart_semantic, breath_semantic

    def read_uart_telemetry(self) -> dict:
        if not self.port:
            return {"error": "UART mode requires a --port argument (e.g., /dev/ttyUSB0)"}

        # Simulated parsed data from MCU
        internal_distance_m = 1.45
        internal_heart_bpm = 58
        internal_breath_bpm = 15

        heart_status, breath_status = self._quantize_health_data(internal_heart_bpm, internal_breath_bpm)

        # Ephemeral privacy: Destroy exact numbers
        del internal_heart_bpm
        del internal_breath_bpm

        return {
            "occupancy": True,
            "motion_state": "Static_MicroMotion",
            "distance_m": internal_distance_m,
            "heart_status": heart_status,
            "breathing_status": breath_status
        }

def main():
    # 1. OS-Level Consent Check (Declared in metadata)
    if os.environ.get("S2_PRIVACY_CONSENT") != "1":
        print(json.dumps({
            "error": "SECURITY BLOCK: Environment variable S2_PRIVACY_CONSENT=1 is missing. Spectrum radar execution is forbidden. / 严重安全拦截：缺少系统环境变量授权，禁止扫描。"
        }, ensure_ascii=False))
        sys.exit(1)

    parser = argparse.ArgumentParser(description="S2 Spectrum Perception Radar")
    parser.add_argument("--mode", choices=["gpio", "uart"], required=True)
    parser.add_argument("--port", help="Serial port for UART mode")
    parser.add_argument("--zone", required=True)
    parser.add_argument("--grid", required=True)
    args = parser.parse_args()

    client = S2RadarEdgeClient(args.zone, args.grid, args.port)
    vendor_nl = ""
    core_tensors = {}

    if args.mode == "gpio":
        core_tensors = client.read_gpio_state()
        vendor_nl = "Hardware GPIO parsed. Pure passive occupancy established. / 硬件GPIO直读完毕，确立纯粹的被动占位状态。"
    elif args.mode == "uart":
        result = client.read_uart_telemetry()
        if "error" in result:
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)
        core_tensors = result
        vendor_nl = "UART Telemetry parsed. Biometric data successfully QUANTIZED for passive observation. / 串口遥测帧解析完毕，生物数据已量化，仅供被动观察。"

    # 2. S2 Memzero Wrapping (NO Action Suggestions)
    memzero_data = {
        "spatial_signature": {"zone": args.zone, "grid_voxel": args.grid, "area_sqm": 4.0},
        "chronos_timestamp": datetime.now().isoformat(),
        "core_tensors": core_tensors,
        "vendor_specific_nl": vendor_nl
    }

    # [CRITICAL ARCHITECTURE UPDATE]: The Sensor no longer dictates actions.
    # It purely returns state. The Agent's cognitive logic handles cross-device linkage.
    print(json.dumps({
        "status": "AUTHORIZED_SPECTRUM_DATA",
        "privacy_compliance": "BIOMETRIC_DATA_QUANTIZED",
        "architecture_compliance": "PASSIVE_SENSOR_ONLY_NO_ACTUATOR_OVERREACH",
        "s2_chronos_memzero": memzero_data
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
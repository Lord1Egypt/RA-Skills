"""硬件指纹采集（只上报摘要，不上报原始值）。

设计说明：硬件指纹【不承担】身份唯一性判定——身份唯一性由「主体 × 设备密钥」决定。
指纹仅用于两个场景：
  1) 重装补发时判断是否为同一台物理机器；
  2) 风控关联分析。
"""

import hashlib
import platform
import subprocess
import uuid
from typing import Dict


def _run(cmd):
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True, timeout=8)
        return out.stdout.decode(errors="ignore").strip()
    except Exception:
        return ""


def _windows_ids() -> Dict[str, str]:
    machine_guid = _run('reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid')
    bios_serial = _run('wmic bios get serialnumber 2>nul')
    disk_serial = _run('wmic diskdrive get serialnumber 2>nul')
    return {
        "machineGuid": machine_guid.split()[-1] if machine_guid else "",
        "biosSerial": bios_serial.split("\n")[-1].strip() if bios_serial else "",
        "diskSerial": disk_serial.split("\n")[-1].strip() if disk_serial else "",
    }


def _unix_ids() -> Dict[str, str]:
    machine_id = ""
    for p in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                machine_id = f.read().strip()
            break
        except Exception:
            continue
    dmi = _run("cat /sys/class/dmi/id/product_uuid 2>/dev/null")
    return {"machineId": machine_id, "productUuid": dmi}


def collect() -> Dict[str, str]:
    """采集指纹分项（原始值仅在本机内存中用于计算摘要）。"""
    info = {
        "system": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "node": platform.node(),
        "mac": f"{uuid.getnode():012x}",
    }
    if platform.system() == "Windows":
        info.update(_windows_ids())
    else:
        info.update(_unix_ids())
    return info


def _h(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest() if value else ""


def digests() -> Dict[str, object]:
    """返回 {hwFpDigest, hwFpCore, hwFpDetail}，全部为摘要，不含原始值。"""
    info = collect()
    detail = {k: _h(v) for k, v in info.items()}
    # 核心特征：换系统/重装不变的部分
    core_keys = ("machineGuid", "biosSerial", "diskSerial", "machineId", "productUuid", "machine")
    core_raw = "|".join(f"{k}={info.get(k, '')}" for k in core_keys)
    all_raw = "|".join(f"{k}={v}" for k, v in sorted(info.items()))
    return {
        "hwFpDigest": _h(all_raw),
        "hwFpCore": _h(core_raw),
        "hwFpDetail": detail,
    }

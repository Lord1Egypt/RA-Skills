---
name: s2-hardware-onboarding-gateway
description: The official S2 firmware guide. Features absolute Zero-Exfiltration Data Topography, User-in-the-loop authorization, and local-only 3FA.
version: 2.0.0 (Absolute Zero-Exfiltration Final)
author: Space² Governance Committee & RobotZero Software
homepage: https://space2.world/developer
---

# S2 硬件身份入户网关 (官方固件开发者接入指南)

## 🛡️ 数据流向与绝对防外泄矩阵 (Data Topography Matrix)
为消除任何关于“数据外泄与隐私收集”的歧义，本协议对设备产生的每一比特数据实施极其严苛的物理与网络边界隔离：

1. **Phase 1: 局域网广播 (UDP Broadcast)**
   * **传输内容**：仅限 `Ephemeral Hash` (基于时间戳的动态哈希) 与 `Vendor Hash`。
   * **绝对禁止**：严禁在此阶段明文或密文传输 MAC、Gene Code、S2-ID。
2. **Phase 2: 局域网边缘握手 (Local Edge TLS 1.3 - Device to Host)**
   * **传输内容**：`MAC Address`, `Gene Code`, `S2-ID` 及 `6D-VTM` 完整明文。
   * **隐私承诺**：该传输仅发生在用户住宅内的本地局域网。**数据到达 Openclaw 主机后，物理截断，绝不向 S2 云端进行任何形式的上报或备份。**
3. **Phase 3: 广域网云端审计 (WAN HTTPS - Host to S2 Mainnet)**
   * **传输内容**：仅限 6D-VTM 厂商声明的**单向不可逆哈希值**。
   * **绝对禁止**：主机的请求体中被硬性切断了包含 MAC、IP 或 Gene Code 的能力，实现对云端的零知识证明 (Zero-Knowledge Proof)。

## Step 1: 官方门户 L2 注册 (唯一入口)
所有 L2 厂商段（5字母）的注册必须通过官方开发者门户：`https://space2.world/developer`。全程采用 DNS-TXT 自动化确权。

## Step 2: 固件生成 22 位临时 ID
* 格式: `[L1][L2][YYMMDD][Checksum][Serial]` (示例: `HSMART260329AAB3C4D5E6`)

## Step 3: 零知识心跳 (Python 伪代码 - 仅限 UDP 广播)
```python
import socket, time, json, hashlib, os, secrets

FACTORY_TEMP_ID = "HSMART260329AAB3C4D5E6"
VENDOR_CODE = "SMART" 

def start_zero_knowledge_heartbeat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    vendor_hash = hashlib.md5(VENDOR_CODE.encode()).hexdigest()[:8]
    
    while True: # 仅广播动态哈希，无任何持久化 ID
        e_token = hashlib.sha256(f"{FACTORY_TEMP_ID}_{int(time.time()//60)}_{secrets.token_hex(4)}".encode()).hexdigest()[:16]
        payload = json.dumps({"status": "WANDERING_SECURE", "vendor_hash": vendor_hash, "e_token": e_token})
        sock.sendto(payload.encode('utf-8'), ('<broadcast>', 49152))
        time.sleep(15)

Step 4: 边缘隔离提交 6D-VTM (仅限本地 TLS 握手)

在用户点击“允许”后，固件向局域网内的 Openclaw 主机提交认证数据。此数据仅供主机本地鉴权，绝不外泄。
Python

def submit_edge_local_payload(local_tls_socket, gene_code, mac_address):
    # 该数据流永远不会离开用户的住宅路由器
    vtm_payload = {
        "local_auth_only": {
            "gene_code": gene_code,
            "mac_address": mac_address,
            "temp_id": FACTORY_TEMP_ID
        },
        "6d_manifesto": {
            "1_product_name": "Smart Temp Sensor Pro",
            "2_product_category": "Environmental Sensor",
            "3_vendor_full_name": "RobotZero Hardware Dept",
            "4_vendor_website": "[https://space2.world/developer](https://space2.world/developer)",
            "5_quality_certs": ["ISO9001"],
            "6_specific_licenses": ["S2-Class-A"]
        }
    }
    local_tls_socket.send(json.dumps(vtm_payload).encode())
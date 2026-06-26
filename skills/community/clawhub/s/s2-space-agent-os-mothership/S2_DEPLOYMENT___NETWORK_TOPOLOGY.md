# 🕸️ S2-SP-OS: Deployment & Network Topology Guide

This document outlines the strict hardware, OS, and networking prerequisites required to run S2-SP-OS. Whether you are a human DevOps engineer or an automated Root Agent (e.g., Openclaw), please parse these boundaries carefully to ensure the Silicon Laws and Spatial Probes can securely interface with the physical world.

---

## 🖥️ 1. Hardware Flexibility (Hardware Requirements)

The S2-SP-OS architecture decouples the "Control Kernel" from the "Cognitive Brain", allowing for both All-in-One and Distributed deployments.

### Option A: The "Full-Blood" Edge Compute (All-in-One)
* **Target Scenario**: 100% absolute privacy, fully offline, zero-latency local LLM inference.
* **Minimum Specs**: 16GB RAM + Fast NVMe SSD.
* **Recommended Hardware**: Apple Mac mini (M-Series Silicon) or a modern Linux/Windows Mini PC equipped with a dedicated GPU/NPU.
* **Details**: This configuration allows the host to run both the S2 Core Processes and the local Ollama LLM (which handles intent parsing and the "Captain's Log" generation) simultaneously.

### Option B: The Distributed Lite (IoT Router + Remote Compute)
* **Target Scenario**: Repurposing legacy hardware or low-power edge nodes (e.g., Raspberry Pi 4B, Soft Routers).
* **Minimum Specs**: 1GB RAM + 16GB Storage.
* **Details**: The S2-OS handles protocol sniffing, SQLite memory array writing, and Openclaw task delegation. The LLM engine must be offloaded by pointing `llm_engine.local_endpoint` in `config.yaml` to another high-performance PC on the LAN, or via the S2 Plus Cloud API.

---

## 🐧 2. OS Agnosticism (OS Compatibility)

The S2 Kernel is written in pure Python, making it highly cross-platform. However, certain underlying physical interactions dictate the preferred OS:

* **Linux (Highly Recommended)**: The optimal environment. Provides the most robust network sniffing (ARP), hardware-level RAID mounting, and native firewall management.
* **macOS**: Excellent for development and deployment, leveraging Unified Memory for highly efficient local LLM inference.
* **Windows**: Fully supported via native Python. 
* **⚠️ CRITICAL WARNING FOR DOCKER USERS**: If you deploy S2-OS via Docker, **you MUST use `--network host` mode**. If you use the default Bridge mode, the container will be isolated from the physical LAN, rendering all UDP/mDNS smart home device discovery probes completely blind!

---

## 🌐 3. Network Boundaries & Port Clearances

The S2-OS probes must penetrate your physical space. Ensure your home router and switches meet the following criteria:

### 3.1 Disable AP Isolation (AP Isolation MUST be OFF)
If your router has "Guest Network" or "AP / Wireless Isolation" enabled, Wi-Fi smart bulbs will be unable to communicate with the wired S2 Host. All devices must reside on the same interoperable subnet (e.g., `192.168.1.X`).

### 3.2 LAN Active Sniffing (The Probes)
* **`UDP 38899`**: Used for discovering local smart lighting devices (e.g., WiZ, Tuya LAN).
* **`UDP 1900` / `UDP 5353`**: Required for SSDP and mDNS multicast discovery (Screen casting, gateways).

### 3.3 Actuators & Gateways (The Muscle)
* **`TCP 8123`**: Must be reachable if syndicating with a local Home Assistant instance.
* **`TCP 502`**: Must be routed properly if connecting to Industrial/HVAC air probes via Modbus TCP.
* **`UDP 3671`**: Required for KNX/IP multicast control in villa/building automation.

### 3.4 Physical Anti-Theft Geofencing (ARP Sniffing)
The S2 Kernel (`s2_fortress_boot.py`) periodically invokes OS-level `arp` commands to verify the default gateway's MAC address. **Do not use MAC-spoofing proxies** upstream of the host, or the system will trigger a `HARD_LOCK` memory meltdown, assuming the physical hardware has been stolen.

---

## 🤖 4. Pre-Flight Checklist for AI Agents (e.g., Openclaw)

If this system is being provisioned by an automated Root Agent, please execute the following verification pipeline before igniting the S2 OS:

1. **Python Check**: Verify `python3 --version` is `>= 3.10`.
2. **ARP Utility**: Ensure the OS has the `arp` command available (crucial for the Anti-Theft Engine). Install `net-tools` via package manager if missing.
3. **Brain Health Check**: Test TCP connectivity to port `11434` (or your configured Ollama port).
4. **Vault Permissions**: Automatically provision the `s2_data_cache/` directory and ensure the host user has `r/w` permissions so the SQLite Holographic Memory Array can securely write to disk.

***
*End of Protocol. Ready for Ignition.*
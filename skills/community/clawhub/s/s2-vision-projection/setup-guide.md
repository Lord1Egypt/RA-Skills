```markdown
# 👁️ S2 Vision: Edge Hardware Setup Guide

## 1. The Multi-Protocol Sniffer Explained (多协议嗅探器原理)
The S2 `vision_cast.py` includes a lightning-fast port-knocking engine. It does not use heavy libraries like `zeroconf` or `scapy`. Instead, it uses standard TCP socket timeouts (0.1s) to ping known ecosystem ports:
* **TCP 7000**: Exposes Apple AirPlay capabilities.
* **TCP 8009**: Exposes Google Chromecast presence.
* **TCP 49152**: Exposes common UPnP/DLNA XML descriptors.

## 2. Using the Native Protocols (调用原生协议)
If the S2 Agent suggests AirPlay or Chromecast, it relies on your Edge Server having the native bridging tools installed (e.g., `pychromecast` or `pyatv`). The Agent will use these tools outside of this specific SKILL boundary for heavy video streaming.

## 3. The S2 Secure Fallback (S2 安全兜底端)
When the user chooses not to use Apple/Google ecosystems for privacy reasons, S2 utilizes the `S2_Native_Fallback`. You can run a simple OpenCV receiver script on a Raspberry Pi hooked to your monitor (refer to the documentation inside the S2-SP-OS developer portal for the 20-line Flask receiver code).
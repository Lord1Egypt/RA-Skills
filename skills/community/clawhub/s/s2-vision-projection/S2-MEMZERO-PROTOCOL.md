# 👁️ S2 Vision Projection: Memzero Protocol

## 1. The Sniff-First Mandate (嗅探优先法则)
The S2 Agent must NOT forcefully push data using proprietary protocols if a native ecosystem exists. 
Before any projection, the Agent must read the `supported_protocols` array (e.g., `["Apple_AirPlay", "S2_Native_Fallback_Available"]`).

## 2. Protocol Priority Queue (协议优先级队列)
If multiple protocols are discovered on the target display, the Agent should prioritize routing based on user ecosystem:
1. `Apple_AirPlay` / `Google_Chromecast` (Best multimedia performance, zero setup).
2. `UPnP_DLNA` (Universal smart TV support).
3. `S2_Native_Fallback_Available` (The absolute secure fallback for image snapshots).
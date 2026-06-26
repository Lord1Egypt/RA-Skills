#!/usr/bin/env python3
import os
import json
import urllib.request
from datetime import datetime
import logging

# =====================================================================
# ⏱️ S2-Timeline-Orchestrator: The Spatiotemporal Rendering Engine (V2.0)
# 六要素时间线渲染器：空间为画布，时间为画笔，生成 T+Xm 关键帧轨道
# =====================================================================

class S2TimelineOrchestrator:
    def __init__(self, root_dir: str = "."):
        self.logger = logging.getLogger("S2_Orchestrator")
        self.primitive_dir = os.path.join(root_dir, "s2_primitive_data")
        self.mounts_file = os.path.join(self.primitive_dir, "active_hardware_mounts.json")
        self.timeline_dir = os.path.join(root_dir, "s2_timeline_data")
        self.tracks_file = os.path.join(self.timeline_dir, "rendered_tracks.json")
        
        os.makedirs(self.timeline_dir, exist_ok=True)

    def _load_active_mounts(self) -> list:
        if os.path.exists(self.mounts_file):
            with open(self.mounts_file, 'r', encoding='utf-8') as f:
                return json.load(f).get("active_devices", [])
        return []

    def generate_timeline_track(self, intent_nlp: str, llm_endpoint: str = "http://localhost:11434/v1") -> dict:
        """
        核心：通过大语言模型，将人类意图转化为 4D 关键帧时间线
        """
        active_devices = self._load_active_mounts()
        devices_context = json.dumps(active_devices, ensure_ascii=False)
        
        prompt = f"""
        [ROLE] You are the 'S2-Timeline-Orchestrator', a spatiotemporal rendering engine.
        [TASK] Translate the human intent into a JSON "Timeline Track" of keyframes across the 6-Element Matrix.
        You MUST use "T+Xm" (e.g., T+0m, T+15m) as time offsets.
        
        [CONTEXT]
        Intent (意图): {intent_nlp}
        Active Mounts (可用物理设备): {devices_context}
        
        [OUTPUT] Return ONLY a valid JSON:
        {{"track_id": "auto", "scenario": "desc", "keyframes": [ {{"time_offset": "T+0m", "element": "element_1_light", "device_id": "ID", "rendered_state": {{"action": "dim"}}, "reason_nlp": "reason"}} ] }}
        """
        
        data = {
            "model": "local-model", # 适配具体的本地模型名称
            "messages": [
                {"role": "system", "content": "You are a strict JSON Timeline Generator."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        
        try:
            req = urllib.request.Request(f"{llm_endpoint}/chat/completions", data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req, timeout=20)
            content = json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
            
            # 清洗 Markdown 标记
            content = content.replace('```json', '').replace('```', '').strip()
            parsed_data = json.loads(content)
            
            parsed_data["track_id"] = f"TRK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            parsed_data["rendered_at"] = datetime.now().isoformat()
            
            # 存入本地轨道数据库
            self._save_track(parsed_data)
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"时间线渲染失败: {str(e)}")
            return {"error": "LLM Timeline Generation Failed", "details": str(e)}

    def _save_track(self, track_data: dict):
        tracks_db = {"scheduled_tracks": []}
        if os.path.exists(self.tracks_file):
            with open(self.tracks_file, 'r', encoding='utf-8') as f:
                tracks_db = json.load(f)
        
        tracks_db["scheduled_tracks"].append(track_data)
        with open(self.tracks_file, 'w', encoding='utf-8') as f:
            json.dump(tracks_db, f, ensure_ascii=False, indent=2)
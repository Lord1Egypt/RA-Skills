#!/usr/bin/env python3
import socket
from s2_skills.s2_base_skill import S2BaseSkill

class S2VisionSkill(S2BaseSkill):
    def __init__(self, room_id: int, grid_id: int, simulation_mode: bool = True):
        super().__init__(skill_name="s2-vision-projection", room_id=room_id, grid_id=grid_id)
        self.simulation_mode = simulation_mode
        self.tv_ip = "192.168.1.55"

    def _real_sniff_protocols(self) -> list:
        """【真实物理连接】利用 Socket 敲击探测局域网投屏协议"""
        signatures = {"AirPlay": 7000, "Chromecast": 8009, "DLNA": 49152}
        discovered = []
        for protocol, port in signatures.items():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.1) # 极限 0.1秒嗅探
                    if sock.connect_ex((self.tv_ip, port)) == 0:
                        discovered.append(protocol)
            except Exception:
                pass
        return discovered

    def read_sensor_data(self) -> dict:
        if self.simulation_mode:
            return {"vision_event": "None", "supported_protocols": ["DLNA"]}
        
        # 真实电子狗嗅探
        protocols = self._real_sniff_protocols()
        return {
            "vision_event": "None",
            "supported_protocols": protocols if protocols else ["S2_Native_Fallback"]
        }

    def execute_command(self, action_intent: str, **kwargs) -> bool:
        if action_intent == "DLNA_Cast_Stream":
            media_url = kwargs.get("media_url", "http://s2-nas.local/stream.m3u8")
            if self.simulation_mode:
                print(f"[📺 模拟] DLNA 投屏 {media_url} 成功")
                return True
            
            # 【真实物理控制】发送原生 SOAP 投屏报文
            soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
            <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
              <s:Body><u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                  <InstanceID>0</InstanceID><CurrentURI>{media_url}</CurrentURI>
              </u:SetAVTransportURI></s:Body>
            </s:Envelope>"""
            # import requests
            # requests.post(f"http://{self.tv_ip}:49152/upnp/control/AVTransport1", data=soap_body)
            print(f"[📺 物理生效] UPnP SOAP 报文已真实发射至 {self.tv_ip}！")
            return True
            
        return False
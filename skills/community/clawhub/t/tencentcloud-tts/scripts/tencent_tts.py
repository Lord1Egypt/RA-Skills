#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云语音合成(TTS)服务封装
基于腾讯云API签名v3实现，提供文本转语音功能
"""

import os
import hashlib
import hmac
import json
import sys
import time
import base64
from datetime import datetime

if sys.version_info[0] <= 2:
    from httplib import HTTPSConnection
else:
    from http.client import HTTPSConnection


class TextToSpeech:
    """腾讯云语音合成客户端"""
    
    def __init__(self, secret_id=None, secret_key=None):
        """
        初始化TTS客户端
        
        Args:
            secret_id: 腾讯云SecretId，如未提供则从环境变量读取
            secret_key: 腾讯云SecretKey，如未提供则从环境变量读取
        """
        self.secret_id = secret_id or os.getenv("TENCENTCLOUD_SECRET_ID")
        self.secret_key = secret_key or os.getenv("TENCENTCLOUD_SECRET_KEY")
        
        if not self.secret_id or not self.secret_key:
            raise ValueError(
                "腾讯云API密钥未配置。请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY，"
                "或在初始化时直接传入secret_id和secret_key参数。"
            )
        
        # API配置
        self.service = "tts"
        self.host = "tts.tencentcloudapi.com"
        self.version = "2019-08-23"
        self.action = "TextToVoice"
        self.endpoint = "https://tts.tencentcloudapi.com"
        self.algorithm = "TC3-HMAC-SHA256"
    
    def sign(self, key, msg):
        """生成HMAC-SHA256签名"""
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
    
    def generate_signature(self, payload, timestamp):
        """生成腾讯云API签名"""
        date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        
        # 步骤1：拼接规范请求串
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        content_type = "application/json; charset=utf-8"
        canonical_headers = "content-type:{}\nhost:{}\nx-tc-action:{}\n".format(content_type, self.host, self.action.lower())
        signed_headers = "content-type;host;x-tc-action"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        
        canonical_request = ("{}\n"
                           "{}\n"
                           "{}\n"
                           "{}\n"
                           "{}\n"
                           "{}").format(http_request_method, canonical_uri, canonical_querystring, canonical_headers, signed_headers, hashed_request_payload)
        
        # 步骤2：拼接待签名字符串
        credential_scope = "{}/{}/tc3_request".format(date, self.service)
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = ("{}\n"
                         "{}\n"
                         "{}\n"
                         "{}").format(self.algorithm, timestamp, credential_scope, hashed_canonical_request)
        
        # 步骤3：计算签名
        secret_date = self.sign(("TC3" + self.secret_key).encode("utf-8"), date)
        secret_service = self.sign(secret_date, self.service)
        secret_signing = self.sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        
        # 步骤4：拼接Authorization
        authorization = ("{} "
                        "Credential={}/{}, "
                        "SignedHeaders={}, "
                        "Signature={}").format(self.algorithm, self.secret_id, credential_scope, signed_headers, signature)
        
        return {
            "authorization": authorization,
            "timestamp": timestamp,
            "date": date
        }
    
    def synthesize(self, 
                 text,
                 voice_type=101001,
                 codec="mp3",
                 output_file="output.mp3"):
        """
        文本转语音合成
        
        Args:
            text: 要合成的文本内容
            voice_type: 语音类型 (101001-101015)
            codec: 音频编码格式 (mp3/wav)
            output_file: 输出音频文件名
            
        Returns:
            Dict包含合成结果信息
        """
        # 参数验证
        if not text or len(text.strip()) == 0:
            raise ValueError("文本内容不能为空")
        
        if len(text) > 300:
            print("警告：文本长度超过300字符，建议分段处理")
        
        if voice_type < 101001 or voice_type > 101015:
            raise ValueError("语音类型必须在101001-101015范围内")
        
        if codec not in ["mp3", "wav"]:
            raise ValueError("音频编码格式必须是'mp3'或'wav'")
        
        # 构造请求参数
        payload_dict = {
            "Text": text,
            "VoiceType": voice_type,
            "Codec": codec,
            "SessionId": "session_{}".format(int(time.time()))
        }
        
        payload = json.dumps(payload_dict, ensure_ascii=False)
        timestamp = int(time.time())
        
        # 生成签名
        signature_info = self.generate_signature(payload, timestamp)
        
        # 构造请求头
        headers = {
            "Authorization": signature_info["authorization"],
            "Content-Type": "application/json; charset=utf-8",
            "Host": self.host,
            "X-TC-Action": self.action,
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": self.version
        }
        
        try:
            # 发送请求
            conn = HTTPSConnection(self.host)
            conn.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
            response = conn.getresponse()
            
            if response.status == 200:
                response_data = response.read()
                result = json.loads(response_data.decode("utf-8"))
                
                # 检查响应状态
                if result.get("Response", {}).get("Error"):
                    error_info = result["Response"]["Error"]
                    raise Exception("腾讯云API错误: {} - {}".format(error_info.get('Code'), error_info.get('Message')))
                
                # 处理音频数据
                audio_data = result["Response"]["Audio"]
                
                # 解码base64音频数据并保存文件
                audio_bytes = base64.b64decode(audio_data)
                with open(output_file, "wb") as f:
                    f.write(audio_bytes)
                
                return {
                    "success": True,
                    "output_file": output_file,
                    "file_size": len(audio_bytes),
                    "voice_type": voice_type,
                    "codec": codec,
                    "request_id": result["Response"].get("RequestId", "")
                }
            else:
                raise Exception("HTTP请求失败: {} {}".format(response.status, response.reason))
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output_file": None
            }
        finally:
            if 'conn' in locals():
                conn.close()


def main():
    """命令行使用示例"""
    import argparse
    
    parser = argparse.ArgumentParser(description="腾讯云语音合成工具")
    parser.add_argument("text", help="要转换为语音的文本内容")
    parser.add_argument("--voice-type", type=int, default=101001, help="语音类型 (默认: 101001)")
    parser.add_argument("--codec", choices=["mp3", "wav"], default="mp3", help="音频格式 (默认: mp3)")
    parser.add_argument("--output", default="output.mp3", help="输出文件名 (默认: output.mp3)")
    
    args = parser.parse_args()
    
    try:
        tts = TextToSpeech()
        result = tts.synthesize(
            text=args.text,
            voice_type=args.voice_type,
            codec=args.codec,
            output_file=args.output
        )
        
        if result["success"]:
            print("✅ 语音合成成功！")
            print("📁 输出文件: {}".format(result['output_file']))
            print("📊 文件大小: {} 字节".format(result['file_size']))
            print("🎵 语音类型: {}".format(result['voice_type']))
            print("🎵 音频格式: {}".format(result['codec']))
        else:
            print("❌ 语音合成失败: {}".format(result['error']))
            
    except Exception as e:
        print("❌ 发生错误: {}".format(e))


if __name__ == "__main__":
    main()
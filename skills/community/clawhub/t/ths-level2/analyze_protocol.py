"""
同花顺数据协议分析工具

使用方法:
1. 运行同花顺客户端
2. 运行此脚本进行抓包分析
3. 分析结果保存在 ths_protocol_analysis.json
"""

import socket
import threading
import time
import json
import struct
from datetime import datetime
from pathlib import Path
import zlib


class ProtocolAnalyzer:
    """协议分析器"""
    
    def __init__(self, output_file: str = None):
        if output_file is None:
            output_file = Path(__file__).parent / "ths_protocol_analysis.json"
        self.output_file = Path(output_file)
        self.captured_packets = []
        self.running = False
        
    def capture_tcp_stream(self, host: str, port: int, duration: int = 60):
        """捕获TCP数据流
        
        注意: 这需要在同花顺和服务器之间进行中间人代理
        实际使用需要配置SSL证书或使用非加密连接
        """
        print(f"开始捕获 {host}:{port} 的数据...")
        print("提示: 实际抓包建议使用 Wireshark")
        
        # 这里只是示例，实际需要更复杂的设置
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                try:
                    data = sock.recv(4096)
                    if data:
                        packet = {
                            'timestamp': datetime.now().isoformat(),
                            'direction': 'server->client',
                            'data_hex': data.hex(),
                            'data_len': len(data),
                            'preview': self._preview_data(data)
                        }
                        self.captured_packets.append(packet)
                        print(f"[{len(self.captured_packets)}] 收到 {len(data)} 字节")
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"接收错误: {e}")
                    break
                    
        except Exception as e:
            print(f"连接失败: {e}")
        finally:
            sock.close()
    
    def _preview_data(self, data: bytes) -> str:
        """生成数据预览"""
        preview = ""
        
        # 尝试解码为文本
        try:
            text = data.decode('utf-8', errors='ignore')
            if text.isprintable() or '\n' in text or '\r' in text:
                preview = f"文本: {text[:100]}"
        except:
            pass
        
        # 尝试解压
        try:
            decompressed = zlib.decompress(data)
            preview += f"\n解压后: {decompressed[:100]}"
        except:
            pass
        
        return preview
    
    def analyze_data_push_job(self, xml_path: str):
        """分析DataPushJob.xml文件"""
        import xml.etree.ElementTree as ET
        
        print(f"\n分析 {xml_path}...")
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        protocols = []
        
        for item in root.findall('.//item'):
            business = item.find('business')
            operation = item.find('operation')
            message = item.find('message')
            analysis = item.find('analysis')
            
            if message is not None and message.text:
                # 解析消息参数
                params = self._parse_message(message.text)
                
                protocol = {
                    'business': business.text if business is not None else '',
                    'operation': operation.text if operation is not None else '',
                    'message': message.text,
                    'params': params,
                    'analysis': analysis.text if analysis is not None else ''
                }
                protocols.append(protocol)
        
        print(f"找到 {len(protocols)} 个协议定义")
        
        # 按ID分组
        by_id = {}
        for p in protocols:
            msg_id = p['params'].get('id', 'unknown')
            if msg_id not in by_id:
                by_id[msg_id] = []
            by_id[msg_id].append(p)
        
        print("\n按消息ID分组:")
        for msg_id, items in sorted(by_id.items()):
            print(f"  ID={msg_id}: {len(items)} 个请求")
            for item in items[:3]:
                print(f"    - {item['business']}: {item['operation']}")
        
        return protocols
    
    def _parse_message(self, message: str) -> dict:
        """解析消息参数"""
        params = {}
        
        # 格式: id=207&market=USZA&code=300033&date=0&datatype=13,19,10,1
        for part in message.split('&'):
            if '=' in part:
                key, value = part.split('=', 1)
                # 特殊处理URL编码
                if 'base64' in key.lower():
                    try:
                        import base64
                        decoded = base64.b64decode(value)
                        value = decoded.decode('utf-8', errors='ignore')
                    except:
                        pass
                params[key] = value
        
        return params
    
    def save_analysis(self, data: dict):
        """保存分析结果"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n分析结果已保存到 {self.output_file}")
    
    def generate_client_code(self, protocols: list) -> str:
        """根据协议生成客户端代码"""
        code = '''"""
自动生成的同花顺数据请求函数
"""

class THSProtocol:
    """同花顺数据协议"""
    
    @staticmethod
    def build_request(msg_id: int, **kwargs) -> str:
        """构建请求数据包"""
        params = [f"id={msg_id}"]
        for key, value in kwargs.items():
            if isinstance(value, list):
                params.append(f"{key}={','.join(map(str, value))}")
            else:
                params.append(f"{key}={value}")
        return "&".join(params)

'''
        
        # 为每个唯一的ID生成方法
        seen_ids = set()
        for p in protocols:
            msg_id = p['params'].get('id')
            if msg_id and msg_id not in seen_ids:
                seen_ids.add(msg_id)
                business = p['business'].replace('/', '_').replace(' ', '_')
                func_name = f"get_{business.lower()}"
                
                code += f'''
    @staticmethod
    def {func_name}(code: str, **kwargs) -> str:
        """获取{p['business']}
        操作: {p['operation']}
        """
        params = {{'code': code, **kwargs}}
        return THSProtocol.build_request({msg_id}, **params)
'''
        
        return code


def main():
    """主函数"""
    print("=" * 60)
    print("同花顺数据协议分析工具")
    print("=" * 60)
    
    analyzer = ProtocolAnalyzer()
    
    # 分析DataPushJob.xml
    xml_path = r"D:\同花顺远航版\bin\data\public\DataPushJob.xml"
    protocols = analyzer.analyze_data_push_job(xml_path)
    
    # 生成分析报告
    report = {
        'analysis_time': datetime.now().isoformat(),
        'total_protocols': len(protocols),
        'protocols': protocols[:50],  # 只保存前50个作为示例
        'message_ids': list(set(p['params'].get('id') for p in protocols if p['params'].get('id')))
    }
    
    analyzer.save_analysis(report)
    
    # 生成客户端代码
    client_code = analyzer.generate_client_code(protocols)
    code_file = Path(__file__).parent / "ths_protocol_generated.py"
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write(client_code)
    print(f"\n生成的代码已保存到 {code_file}")
    
    print("\n" + "=" * 60)
    print("Level2 数据请求示例:")
    print("=" * 60)
    
    # 打印Level2相关的请求
    level2_keywords = ['成交', '明细', 'Level', '深度', '竞价', 'tick', '明细']
    
    for p in protocols:
        if any(kw in p['business'].lower() or kw in p['operation'].lower() for kw in level2_keywords):
            print(f"\n{p['business']} ({p['operation']})")
            print(f"  消息: {p['message']}")


if __name__ == "__main__":
    main()
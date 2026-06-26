"""101围棋网棋谱下载器"""

import requests
import re
import json
import websocket
import ssl
import time
import threading
from .base import BaseSourceFetcher, FetchResult, register_fetcher

@register_fetcher
class Weiqi101Fetcher(BaseSourceFetcher):
    name = "weiqi101"
    display_name = "101围棋网"
    url_patterns = [
        r'101weiqi\.(com|cn)/play/p/(\d+)',
        r'101weiqi\.(com|cn)/play/(\d+)',
    ]
    url_examples = [
        "https://www.101weiqi.com/play/p/{PLAY_ID}/",
    ]
    
    @classmethod
    def extract_id(cls, url: str) -> str:
        """从URL提取对局ID（覆盖基类以支持多捕获组）"""
        for pattern in cls.url_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(match.lastindex)
        return None
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        import time as time_module
        timing = {}
        
        t0 = time_module.time()
        play_id = self.extract_id(url)
        timing['extract_id'] = time_module.time() - t0
        
        if not play_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取对局ID",
                timing=timing
            )
        
        # 获取页面数据
        t0 = time_module.time()
        page_url = f"https://www.101weiqi.com/play/p/{play_id}/"
        
        try:
            resp = requests.get(page_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K)',
                'Accept': 'text/html,application/xhtml+xml'
            })
            resp.raise_for_status()
            html = resp.text
        except Exception as e:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error=f"页面请求失败: {e}",
                timing=timing
            )
        
        # 提取playInfo
        play_info = self._extract_play_info(html)
        if not play_info:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从页面提取对局数据",
                timing=timing
            )
        timing['extract_data'] = time_module.time() - t0
        
        # 提取元数据
        metadata = self._extract_metadata(play_info)
        
        # 获取棋谱数据
        points = play_info.get('points', [])
        step = play_info.get('step', 0)
        
        # 优先通过WebSocket获取实时数据（页面step可能不准确）
        # WebSocket返回的pos才是准确的棋谱数据
        if True:  # 总是尝试WebSocket，因为页面step可能不是实时的
            t0 = time_module.time()
            ws_result = self._fetch_via_websocket(play_info)
            timing['websocket_fetch'] = time_module.time() - t0
            
            if ws_result and ws_result.get('pos'):
                # 转换坐标格式
                points = self._convert_pos_to_points(ws_result['pos'])
                metadata['moves_count'] = ws_result.get('stepcount', len(points))
                metadata['status'] = '已结束' if ws_result.get('status') == 1 else '进行中'
            else:
                return FetchResult(
                    success=False,
                    source=self.name,
                    url=url,
                    sgf_content=None,
                    output_path=None,
                    error="WebSocket获取棋谱失败",
                    metadata=metadata,
                    timing=timing
                )
        
        # 生成SGF
        t0 = time_module.time()
        sgf = self._generate_sgf(play_info, metadata, points)
        timing['sgf_generation'] = time_module.time() - t0
        
        # 保存文件
        t0 = time_module.time()
        if not output_path:
            output_path = self.get_default_output_path(play_id)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sgf)
        timing['save_file'] = time_module.time() - t0
        
        return FetchResult(
            success=True,
            source=self.name,
            url=url,
            sgf_content=sgf,
            output_path=output_path,
            metadata=metadata,
            timing=timing
        )
    
    def _fetch_via_websocket(self, play_info: dict, timeout: int = 15) -> dict:
        """通过WebSocket获取棋谱数据"""
        ws_url = play_info.get('sockethost') or play_info.get('sockethost2')
        userkey = play_info.get('userkey')
        play_id = play_info.get('id')
        pkey = f"play:{play_id}"
        
        if not ws_url or not userkey:
            return None
        
        result = {"pos": None, "status": None, "stepcount": 0}
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                action = data.get('action')
                
                if action == 'connected':
                    # 发送初始化消息
                    init_msg = {
                        "pkey": pkey,
                        "cmd": "init_user",
                        "userkey": userkey
                    }
                    ws.send(json.dumps(init_msg))
                    
                    # 请求初始数据
                    time.sleep(0.3)
                    get_data_msg = {"cmd": "getinitdata"}
                    ws.send(json.dumps(get_data_msg))
                
                elif action == 'initdata':
                    data_content = json.loads(data.get('data', '{}'))
                    result['pos'] = data_content.get('pos', [])
                    result['status'] = data_content.get('status')
                    result['stepcount'] = data_content.get('stepcount', 0)
                    ws.close()
                    
            except Exception:
                pass
        
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            header={
                "Origin": "https://www.101weiqi.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
            }
        )
        
        # 后台运行
        ws_thread = threading.Thread(
            target=lambda: ws.run_forever()
        )
        ws_thread.daemon = True
        ws_thread.start()
        
        # 等待结果
        start = time.time()
        while time.time() - start < timeout:
            if result['pos'] is not None:
                return result
            time.sleep(0.3)
        
        ws.close()
        return result if result['pos'] is not None else None
    
    def _convert_pos_to_points(self, pos_list: list) -> list:
        """
        将101围棋网坐标转换为SGF格式
        101坐标: 'pc' -> 直接转换为SGF 'pc' (已经是SGF格式)
        注意：101围棋网的坐标系统和SGF一致，不需要y轴翻转
        """
        black_moves = []
        white_moves = []
        
        for i, pos in enumerate(pos_list):
            if pos == 'tt':  # 停一手
                continue
            if len(pos) >= 2:
                # 101围棋网坐标已经是SGF格式，直接使用
                if i % 2 == 0:  # 黑棋先手
                    black_moves.append(pos)
                else:
                    white_moves.append(pos)
        
        return [black_moves, white_moves]
    
    def _extract_play_info(self, html: str) -> dict:
        """从HTML提取playInfo"""
        pattern = r'playInfo:\s*(\{.*?\}),\s*language'
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return None
    
    def _extract_metadata(self, play_info: dict) -> dict:
        """提取元数据"""
        rule_map = {1: 'chinese', 2: 'japanese', 3: 'korean'}
        
        black_rank = play_info.get('blacklevelname', '')
        white_rank = play_info.get('whitelevelname', '')
        
        # 结果处理
        status = play_info.get('status', 0)
        result_str = ""
        if status == 1:
            # 已结束，尝试解析结果
            wintype = play_info.get('wintype', 0)
            winnumber = play_info.get('winnumber', 0)
            if wintype == 1:  # 中盘胜
                result_str = "B+R" if play_info.get('black_first') else "W+R"
            elif wintype == 2 and winnumber > 0:  # 数目胜
                result_str = f"B+{winnumber/100:.1f}"
        
        return {
            'game_id': str(play_info.get('id', '')),
            'black_name': play_info.get('busername', play_info.get('black', 'Black')),
            'white_name': play_info.get('wusername', play_info.get('white', 'White')),
            'black_rank': black_rank,
            'white_rank': white_rank,
            'width': play_info.get('lu', 19),
            'height': play_info.get('lu', 19),
            'komi': play_info.get('daotiemu', 0) or 7.5,
            'handicap': play_info.get('rangzi', 0),
            'rules': rule_map.get(play_info.get('gamerule', 1), 'chinese'),
            'step': play_info.get('step', 0),
            'moves_count': play_info.get('step', 0),
            'status': '进行中' if status == 0 else '已结束',
            'result': result_str,
        }
    
    def _generate_sgf(self, play_info: dict, metadata: dict, points: list) -> str:
        """生成SGF字符串"""
        width = metadata['width']
        height = metadata['height']
        
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append(f"SZ[{width}]")
        parts.append(f"PB[{metadata['black_name']}]")
        parts.append(f"PW[{metadata['white_name']}]")
        
        if metadata['black_rank']:
            parts.append(f"BR[{metadata['black_rank']}]")
        if metadata['white_rank']:
            parts.append(f"WR[{metadata['white_rank']}]")
        
        parts.append(f"KM[{metadata['komi']}]")
        
        if metadata.get('result'):
            parts.append(f"RE[{metadata['result']}]")
        
        rule_code = {'chinese': 'CN', 'japanese': 'JP', 'korean': 'KO'}.get(metadata['rules'], 'CN')
        parts.append(f"RU[{rule_code}]")
        
        if metadata['handicap'] > 0:
            parts.append(f"HA[{metadata['handicap']}]")
            for x, y in self.get_handicap_stones(metadata['handicap'], height):
                coord = self.coord_to_sgf(x, y, height)
                parts.append(f"AB[{coord}]")
        
        # 着法
        # points 现在是SGF字符串坐标列表（如 ['pc', 'dp', ...]）
        if points and len(points) >= 2:
            black_moves = points[0] if len(points) > 0 else []
            white_moves = points[1] if len(points) > 1 else []
            
            max_len = max(len(black_moves), len(white_moves))
            for i in range(max_len):
                if i < len(black_moves):
                    coord = black_moves[i]
                    parts.append(f";B[{coord}]")
                
                if i < len(white_moves):
                    coord = white_moves[i]
                    parts.append(f";W[{coord}]")
        
        parts.append(")")
        return "".join(parts)

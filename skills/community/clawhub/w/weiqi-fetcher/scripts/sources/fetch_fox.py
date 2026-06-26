"""野狐围棋棋谱下载器 - 通过 fox_adapter 调用完整功能"""

import os
import sys
import asyncio

from .base import BaseSourceFetcher, FetchResult, register_fetcher

# 添加 fox_adapter 到路径
_current_dir = os.path.dirname(os.path.abspath(__file__))
_adapter_dir = os.path.join(_current_dir, '..', 'fox_adapter')
if _adapter_dir not in sys.path:
    sys.path.insert(0, _adapter_dir)

from fox_adapter import (
    extract_via_api,
    extract_via_websocket,
    extract_game_info,
    parse_share_url,
    create_sgf,
    parse_sgf_info,
)


@register_fetcher
class FoxwqFetcher(BaseSourceFetcher):
    name = "foxwq"
    display_name = "野狐围棋"
    url_patterns = [
        r'h5\.foxwq\.com/yehunewshare.*chessid=(\d+)',
        r'www\.foxwq\.com/.*chessid=(\d+)',
        r'foxwq\.com.*chessid=(\d+)',
    ]
    url_examples = [
        "https://h5.foxwq.com/yehunewshare/?chessid={CHESS_ID}",
    ]
    
    def __init__(self):
        self._timing = {}
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """
        下载野狐围棋棋谱
        
        实现策略：
        1. 先尝试API模式（历史棋谱，0.1秒）
        2. API失败且模式允许时，尝试WebSocket（进行中对局）
        3. 支持让子棋自动检测
        4. 支持绝艺解说直播棋谱
        """
        import time
        t_start = time.time()
        
        # 解析URL获取chessid
        t0 = time.time()
        params = parse_share_url(url)
        chess_id = params.get('chessid')
        self._timing['parse_url'] = time.time() - t0
        
        if not chess_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取对局ID",
                timing=self._timing
            )
        
        sgf_content = None
        metadata = {}
        error_msg = None
        
        # 步骤1：尝试API模式
        t0 = time.time()
        sgf_content = extract_via_api(chess_id)
        self._timing['api_fetch'] = time.time() - t0
        
        if sgf_content:
            # API成功，获取元数据
            t0 = time.time()
            game_info = extract_game_info(chess_id, params.get('uid'))
            self._timing['fetch_metadata'] = time.time() - t0
            
            if game_info:
                metadata = {
                    'game_id': chess_id,
                    'black_name': game_info.get('black_nick', '黑棋'),
                    'white_name': game_info.get('white_nick', '白棋'),
                    'black_rank': self._format_dan(game_info.get('black_dan')),
                    'white_rank': self._format_dan(game_info.get('white_dan')),
                    'result': game_info.get('result', ''),
                    'date': game_info.get('start_time', ''),
                    'moves_count': game_info.get('movenum', 0),
                    'extract_mode': 'api',
                }
        
        # 步骤2：API失败，尝试WebSocket
        if not sgf_content:
            t0 = time.time()
            try:
                # WebSocket提取返回: (moves, player_names, handicap, is_jueyi)
                ws_result = asyncio.run(extract_via_websocket(url, timeout=15))
                self._timing['websocket_fetch'] = time.time() - t0
                
                if ws_result and ws_result[0]:
                    moves, player_names, handicap, is_jueyi = ws_result
                    
                    pb = player_names[0] if len(player_names) > 0 else "黑棋"
                    pw = player_names[1] if len(player_names) > 1 else "白棋"
                    
                    # 生成SGF
                    sgf_content = create_sgf(moves, pb, pw, handicap)
                    
                    metadata = {
                        'game_id': chess_id,
                        'black_name': pb,
                        'white_name': pw,
                        'moves_count': len(moves),
                        'handicap': handicap,
                        'is_jueyi': is_jueyi,
                        'extract_mode': 'websocket',
                    }
                else:
                    error_msg = "WebSocket获取失败，对局可能已结束或未开始"
            except Exception as e:
                self._timing['websocket_fetch'] = time.time() - t0
                error_msg = f"WebSocket错误: {str(e)}"
        
        # 处理结果
        if not sgf_content:
            self._timing['total'] = time.time() - t_start
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error=error_msg or "无法提取棋谱数据",
                timing=self._timing
            )
        
        # 解析SGF获取更完整的信息
        try:
            sgf_info = parse_sgf_info(sgf_content)
            metadata.update({
                'black_name': sgf_info.get('pb', metadata.get('black_name', '黑棋')),
                'white_name': sgf_info.get('pw', metadata.get('white_name', '白棋')),
                'black_rank': sgf_info.get('br', metadata.get('black_rank', '')),
                'white_rank': sgf_info.get('wr', metadata.get('white_rank', '')),
                'result': sgf_info.get('result', metadata.get('result', '')),
                'date': sgf_info.get('date', metadata.get('date', '')),
                'moves_count': sgf_info.get('movenum', metadata.get('moves_count', 0)),
            })
        except:
            pass
        
        # 确定输出路径
        if not output_path:
            output_path = self.get_default_output_path(chess_id)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存文件
        t0 = time.time()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sgf_content)
        self._timing['save_file'] = time.time() - t0
        self._timing['total'] = time.time() - t_start
        
        return FetchResult(
            success=True,
            source=self.name,
            url=url,
            sgf_content=sgf_content,
            output_path=output_path,
            metadata=metadata,
            timing=self._timing
        )
    
    @staticmethod
    def _format_dan(dan_value):
        """将数值段位转换为显示格式"""
        if not dan_value:
            return ""
        try:
            dan = int(dan_value)
            if dan >= 20:
                return f"P{dan - 19}段"  # 职业段位
            elif dan >= 10:
                return f"{dan - 9}段"     # 业余段位
            else:
                return f"{10 - dan}级"    # 级位
        except:
            return str(dan_value)

"""对弈曲折/手谈赛场棋谱下载器 - REST API版本"""

import re
import os
import time
import requests
from datetime import datetime
from .base import BaseSourceFetcher, FetchResult, register_fetcher

@register_fetcher
class DzqzdFetcher(BaseSourceFetcher):
    name = "dzqzd"
    display_name = "对弈曲折/手谈赛场"
    url_patterns = [
        r'dzqzd\.com.*[?&]kifuId=(\d+)',
        r'v\.dzqzd\.com.*[?&]kifuId=(\d+)',
    ]
    url_examples = [
        "https://v.dzqzd.com/Kifu/chessmanualdetail?kifuId={KIFU_ID}",
    ]
    
    API_URL_TEMPLATE = "https://v.dzqzd.com/Kifu/Details?kifuid={kifu_id}"
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        import time as time_module
        timing = {}
        
        t0 = time_module.time()
        kifu_id = self._extract_kifu_id(url)
        timing['extract_id'] = time_module.time() - t0
        
        if not kifu_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取kifuId",
                timing=timing
            )
        
        # 使用API获取数据
        t0 = time_module.time()
        try:
            result = self._fetch_via_api(kifu_id)
        except Exception as e:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error=f"API错误: {e}",
                timing=timing
            )
        timing['api_fetch'] = time_module.time() - t0
        
        if not result or not result.get('sgf'):
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="未能获取SGF数据",
                metadata=result.get('game_info', {}) if result else {},
                timing=timing
            )
        
        # 保存文件
        t0 = time_module.time()
        if not output_path:
            output_path = self.get_default_output_path(kifu_id)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['sgf'])
        timing['save'] = time_module.time() - t0
        
        return FetchResult(
            success=True,
            source=self.name,
            url=url,
            sgf_content=result['sgf'],
            output_path=output_path,
            metadata=result.get('game_info', {}),
            timing=timing
        )
    
    def _extract_kifu_id(self, url: str) -> str:
        """从URL提取kifuId"""
        match = re.search(r'[?&]kifuId=(\d+)', url)
        if match:
            return match.group(1)
        return None
    
    def _fetch_via_api(self, kifu_id: str) -> dict:
        """通过API直接获取数据"""
        
        url = self.API_URL_TEMPLATE.format(kifu_id=kifu_id)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://v.dzqzd.com/Kifu/chessmanualdetail?kifuId={kifu_id}',
            'Origin': 'https://v.dzqzd.com',
        }
        
        resp = requests.get(url, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        
        result = resp.json()
        if result.get('code') != 1:
            raise Exception(result.get('msg', 'API错误'))
        
        kifu_data = result['data']
        
        # 解析YAML格式的棋谱数据
        yml_content = kifu_data.get('yml', '')
        game_info = self._parse_game_info(kifu_data, yml_content)
        moves = self._parse_moves(yml_content)
        
        sgf = self._generate_sgf(game_info, moves)
        
        return {
            'game_info': game_info,
            'sgf': sgf
        }
    
    def _parse_game_info(self, kifu_data: dict, yml_content: str) -> dict:
        """解析游戏信息"""
        info = {
            'id': kifu_data.get('id'),
            'date': kifu_data.get('date'),
            'event': kifu_data.get('event'),
            'result': kifu_data.get('result'),
            'winner': kifu_data.get('winner'),
        }
        
        # 从YAML头部提取额外信息
        lines = yml_content.strip().split('\n')
        header_keys = ['GM', 'AP', 'SZ', 'PB', 'PW', 'SO', 'EV', 'DT', 'RE']
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('- B:') or line.startswith('- W:'):
                continue
            
            # 匹配头部键值对
            for key in header_keys:
                if line.startswith(f'- {key}:'):
                    value = line.split(':', 1)[1].strip() if ':' in line else ''
                    if key == 'SZ':
                        info['board_size'] = value
                    elif key == 'PB':
                        info['black_name'] = value
                    elif key == 'PW':
                        info['white_name'] = value
                    elif key == 'EV':
                        info['event'] = value
                    elif key == 'DT':
                        info['date'] = value
                    elif key == 'RE':
                        info['result_sgf'] = value
                    break
        
        # 使用API返回的棋手信息作为后备
        black_data = kifu_data.get('black', {})
        white_data = kifu_data.get('white', {})
        if 'black_name' not in info:
            info['black_name'] = black_data.get('name', 'Black')
        if 'white_name' not in info:
            info['white_name'] = white_data.get('name', 'White')
        if 'board_size' not in info:
            info['board_size'] = '19'
        
        return info
    
    def _parse_moves(self, yml_content: str) -> list:
        """解析着法列表"""
        moves = []
        lines = yml_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- B:'):
                coord = line.replace('- B:', '').strip()
                moves.append(('B', coord))
            elif line.startswith('- W:'):
                coord = line.replace('- W:', '').strip()
                moves.append(('W', coord))
        
        return moves
    
    def _generate_sgf(self, info: dict, moves: list) -> str:
        """生成SGF"""
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append(f"SZ[{info.get('board_size', '19')}]")
        parts.append("AP[GoStarV7]")
        parts.append(f"PB[{info.get('black_name', 'Black')}]")
        parts.append(f"PW[{info.get('white_name', 'White')}]")
        
        if info.get('event'):
            parts.append(f"EV[{info['event']}]")
        if info.get('date'):
            parts.append(f"DT[{info['date']}]")
        if info.get('result_sgf'):
            parts.append(f"RE[{info['result_sgf']}]")
        elif info.get('result'):
            # 转换中文结果为SGF格式
            result_map = {
                '黑中盘胜': 'B+R',
                '白中盘胜': 'W+R',
                '黑胜': 'B+',
                '白胜': 'W+',
            }
            re_val = result_map.get(info['result'], info['result'])
            parts.append(f"RE[{re_val}]")
        
        parts.append("SO[丹朱对局集]")
        
        for color, coord in moves:
            parts.append(f";{color}[{coord}]")
        
        parts.append(")")
        return "".join(parts)

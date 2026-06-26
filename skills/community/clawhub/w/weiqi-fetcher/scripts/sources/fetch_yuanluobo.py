"""元萝卜围棋棋谱下载器 - 纯API版本（无需Playwright）"""

import re
import os
import time
import requests
from datetime import datetime
from .base import BaseSourceFetcher, FetchResult, register_fetcher

@register_fetcher
class YuanluoboFetcher(BaseSourceFetcher):
    name = "yuanluobo"
    display_name = "元萝卜围棋"
    url_patterns = [
        r'yuanluobo\.com.*session_id=([A-Za-z0-9]+)',
        r'jupiter\.yuanluobo\.com.*session_id=([A-Za-z0-9]+)',
    ]
    url_examples = [
        "https://jupiter.yuanluobo.com/robot-public/all-in-app/go/review?session_id=...",
    ]
    
    API_URL = "https://jupiter.yuanluobo.com/r2/chess/wq/sdr/v3/record/detail"
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        import time as time_module
        timing = {}
        
        t0 = time_module.time()
        session_id = self._extract_session_id(url)
        timing['extract_id'] = time_module.time() - t0
        
        if not session_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取session_id",
                timing=timing
            )
        
        # 使用API获取数据
        t0 = time_module.time()
        try:
            result = self._fetch_via_api(session_id)
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
            output_path = self.get_default_output_path(session_id)
        
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
    
    def _extract_session_id(self, url: str) -> str:
        """从URL提取session_id"""
        match = re.search(r'session_id=([A-Za-z0-9]+)', url)
        if match:
            return match.group(1)
        return None
    
    def _fetch_via_api(self, session_id: str) -> dict:
        """通过API直接获取数据"""
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Referer': f'https://jupiter.yuanluobo.com/robot-public/all-in-app/go/review?session_id={session_id}',
            'Origin': 'https://jupiter.yuanluobo.com',
        }
        
        data = {'sessionId': session_id}
        
        resp = requests.post(self.API_URL, json=data, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        
        result = resp.json()
        if result.get('code') != 100000:
            raise Exception(result.get('message', 'API错误'))
        
        game_data = result['data']
        game_info = {
            'session_id': game_data.get('session_id'),
            'black_name': game_data.get('black_player_name'),
            'white_name': game_data.get('white_player_name'),
            'handicap': game_data.get('handicap', 0),
            'total_round': game_data.get('total_round', 0),
        }
        
        recording = game_data.get('recording', {})
        moves = recording.get('moves', [])
        
        sgf = self._generate_sgf(game_info, moves)
        
        return {
            'game_info': game_info,
            'sgf': sgf
        }
    
    def _generate_sgf(self, info: dict, moves: list) -> str:
        """生成SGF"""
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append("SZ[19]")
        parts.append(f"PB[{info.get('black_name', 'Black')}]")
        parts.append(f"PW[{info.get('white_name', 'White')}]")
        
        if info.get('handicap', 0) > 0:
            parts.append(f"HA[{info['handicap']}]")
        
        for move in moves:
            coord = move.get('coordinate', '')
            if coord:
                match = re.match(r'([BW])\[([a-z]{2})\]', coord)
                if match:
                    color = match.group(1)
                    pos = match.group(2)
                    parts.append(f";{color}[{pos}]")
        
        parts.append(")")
        return "".join(parts)

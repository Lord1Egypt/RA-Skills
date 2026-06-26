"""OGS (Online-Go.com) 棋谱下载器"""

import requests
from .base import BaseSourceFetcher, FetchResult, register_fetcher

@register_fetcher
class OgsFetcher(BaseSourceFetcher):
    name = "ogs"
    display_name = "OGS (Online-Go)"
    url_patterns = [
        r'online-go\.com/game/(\d+)',
        r'online-go\.com/game/view/(\d+)',
    ]
    url_examples = [
        "https://online-go.com/game/{GAME_ID}",
    ]
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        import time
        timing = {}
        
        t0 = time.time()
        game_id = self.extract_id(url)
        timing['extract_id'] = time.time() - t0
        
        if not game_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                metadata={},
                error="无法从URL提取游戏ID",
                timing=timing
            )
        
        # 获取游戏数据
        t0 = time.time()
        api_url = f"https://online-go.com/api/v1/games/{game_id}"
        try:
            resp = requests.get(api_url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            timing['api_request'] = time.time() - t0
        except Exception as e:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                metadata={},
                error=f"API请求失败: {e}",
                timing=timing
            )
        
        # 提取数据
        t0 = time.time()
        game_data = data.get('gamedata', {})
        players = data.get('players', {})
        
        black = players.get('black', {})
        white = players.get('white', {})
        
        metadata = {
            'game_id': game_id,
            'black_name': black.get('username', 'Black'),
            'white_name': white.get('username', 'White'),
            'black_rank': self.format_ogs_rank(black.get('ranking', 0)),
            'white_rank': self.format_ogs_rank(white.get('ranking', 0)),
            'width': game_data.get('width', 19),
            'height': game_data.get('height', 19),
            'komi': game_data.get('komi', 6.5),
            'handicap': game_data.get('handicap', 0),
            'rules': game_data.get('rules', 'japanese'),
            'date': data.get('started', '')[:10] if data.get('started') else '',
            'moves_count': len(game_data.get('moves', [])),
        }
        
        # 结果
        outcome = data.get('outcome', '')
        if outcome:
            metadata['result'] = outcome
        elif data.get('ended'):
            if data.get('black_lost') and not data.get('white_lost'):
                metadata['result'] = "W+Resign"
            elif data.get('white_lost') and not data.get('black_lost'):
                metadata['result'] = "B+Resign"
            else:
                metadata['result'] = "?"
        else:
            metadata['result'] = "进行中"
        
        # 生成SGF
        sgf = self._generate_sgf(game_data, metadata)
        timing['sgf_generation'] = time.time() - t0
        
        # 保存文件
        t0 = time.time()
        if not output_path:
            output_path = self.get_default_output_path(game_id)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sgf)
        timing['save_file'] = time.time() - t0
        
        return FetchResult(
            success=True,
            source=self.name,
            url=url,
            sgf_content=sgf,
            output_path=output_path,
            metadata=metadata,
            timing=timing
        )
    
    def _generate_sgf(self, game_data: dict, metadata: dict) -> str:
        """生成SGF字符串"""
        moves = game_data.get('moves', [])
        width = metadata['width']
        height = metadata['height']
        
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append(f"SZ[{width}:{height}]")
        parts.append(f"PB[{metadata['black_name']}]")
        parts.append(f"PW[{metadata['white_name']}]")
        
        if metadata['black_rank']:
            parts.append(f"BR[{metadata['black_rank']}]")
        if metadata['white_rank']:
            parts.append(f"WR[{metadata['white_rank']}]")
        
        parts.append(f"KM[{metadata['komi']}]")
        if metadata['date']:
            parts.append(f"DT[{metadata['date']}]")
        
        if metadata['result'] != "进行中":
            parts.append(f"RE[{metadata['result']}]")
        
        if metadata['handicap'] > 0:
            parts.append(f"HA[{metadata['handicap']}]")
            for x, y in self.get_handicap_stones(metadata['handicap'], height):
                coord = self.coord_to_sgf(x, y, height)
                parts.append(f"AB[{coord}]")
        
        # 规则映射
        rules_map = {
            'japanese': 'JP',
            'chinese': 'CN',
            'korean': 'KO',
            'aga': 'AGA',
            'ing': 'ING'
        }
        if metadata['rules'] in rules_map:
            parts.append(f"RU[{rules_map[metadata['rules']]}]")
        
        # 着法
        for i, move in enumerate(moves):
            if len(move) >= 2:
                x, y = move[0], move[1]
                if x == -1 and y == -1:
                    coord = ""  # pass
                else:
                    coord = self.coord_to_sgf(x, y, height)
                
                if i % 2 == 0:
                    parts.append(f";B[{coord}]")
                else:
                    parts.append(f";W[{coord}]")
        
        parts.append(")")
        return "".join(parts)

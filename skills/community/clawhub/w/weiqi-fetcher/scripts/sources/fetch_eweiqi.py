"""弈城围棋 (eweiqi.com) 棋谱下载器"""

import re
import requests
from .base import BaseSourceFetcher, FetchResult, register_fetcher


@register_fetcher
class EweiqiFetcher(BaseSourceFetcher):
    """弈城围棋棋谱下载器"""
    
    name = "eweiqi"
    display_name = "弈城围棋"
    url_patterns = [
        r'eweiqi\.com.*GNO=(\d+)',
        r'eweiqi\.com.*id=(\d+)',
    ]
    url_examples = [
        "http://mobile.eweiqi.com/index_ZHCN.html?LNK=1&GNO={GAME_NO}",
    ]
    
    # API端点
    API_URL = "http://client.eweiqi.com/gibo/gibo_load_data.php"
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """从弈城围棋分享链接提取SGF棋谱"""
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
                error="无法从URL提取游戏ID",
                timing=timing
            )
        
        # 调用API获取数据
        t0 = time.time()
        api_url = f"{self.API_URL}?id={game_id}&mode=my"
        
        try:
            resp = requests.get(
                api_url,
                headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.text
            timing['api_request'] = time.time() - t0
        except Exception as e:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error=f"API请求失败: {e}",
                timing=timing
            )
        
        # 解析数据
        t0 = time.time()
        
        # 解析玩家信息 (使用BID/WID，不是BNICK/WNICK)
        black_match = re.search(r'BID:([^,]+),BLV:([^,]+),BNICK:([^,]+)', data)
        white_match = re.search(r'WID:([^,]+),WLV:([^,]+),WNICK:([^,]+)', data)
        game_match = re.search(r'GDATE:([^,]+)', data)
        
        # 使用BID和WID作为玩家名
        black_name = black_match.group(1) if black_match else '黑棋'
        white_name = white_match.group(1) if white_match else '白棋'
        date = game_match.group(1) if game_match else ''
        
        # 解析段位 (BLV/WLV)
        black_rank = self._parse_level(black_match.group(2)) if black_match else ''
        white_rank = self._parse_level(white_match.group(2)) if white_match else ''
        
        metadata = {
            'game_id': game_id,
            'black_name': black_name,
            'white_name': white_name,
            'black_rank': black_rank,
            'white_rank': white_rank,
            'date': date,
            'moves_count': len(re.findall(r'STO\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+', data)),
        }
        
        # 解析着法并生成SGF
        sgf = self._parse_to_sgf(data, black_name, white_name, date)
        timing['sgf_generation'] = time.time() - t0
        
        # 保存文件
        t0 = time.time()
        if not output_path:
            output_path = self.get_default_output_path(game_id)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sgf)
        timing['save_file'] = time.time() - t0
        
        timing['total'] = sum(timing.values())
        
        return FetchResult(
            success=True,
            source=self.name,
            url=url,
            sgf_content=sgf,
            output_path=output_path,
            metadata=metadata,
            timing=timing
        )
    
    def _parse_level(self, level_str: str) -> str:
        """解析弈城段位
        
        弈城等级系统:
        - 18-26: 职业段位 (1段=18, 9段=26)
        - 0-17: 业余级位 (18级=0, 1级=17)
        """
        try:
            level = int(level_str)
            if level >= 18:
                # 职业段位: 18=1段, 26=9段
                dan = level - 17
                return f"{dan}段"
            else:
                # 业余级位: 0=18级, 17=1级
                kyu = 18 - level
                return f"{kyu}级"
        except:
            return level_str
    
    def _parse_to_sgf(self, data: str, black_name: str, white_name: str, date: str) -> str:
        """将弈城格式转换为SGF"""
        
        # 解析着法
        # 格式: STO 0 N COLOR X Y
        # COLOR: 1=黑, 2=白
        # X,Y: 0-based坐标
        moves = re.findall(r'STO\s+\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', data)
        
        sgf_moves = []
        for move_num, color, x, y in moves:
            # 0-based 转 SGF (a-s)
            sgf_x = chr(ord('a') + int(x))
            sgf_y = chr(ord('a') + int(y))
            sgf_coord = sgf_x + sgf_y
            sgf_color = 'B' if color == '1' else 'W'
            sgf_moves.append(f";{sgf_color}[{sgf_coord}]")
        
        # 构建SGF
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append("AP[弈城围棋]")
        parts.append("SZ[19]")
        parts.append(f"PB[{black_name}]")
        parts.append(f"PW[{white_name}]")
        if date:
            parts.append(f"DT[{date}]")
        parts.append("RU[Chinese]")
        parts.append(''.join(sgf_moves))
        parts.append(")")
        
        return "".join(parts)

"""隐智智能棋盘 (izis.cn) 棋谱下载器"""

import re
import json
import requests
from .base import BaseSourceFetcher, FetchResult, register_fetcher


@register_fetcher
class IzisFetcher(BaseSourceFetcher):
    """隐智智能棋盘棋谱下载器"""
    
    name = "izis"
    display_name = "隐智智能棋盘"
    url_patterns = [
        r'izis\.cn.*gameId=(\d+)',
        r'app\.izis\.cn.*gameId=(\d+)',
    ]
    url_examples = [
        "http://app.izis.cn/web/#/live_detail?gameId={GAME_ID}&type=2",
    ]
    
    # API端点
    API_URL = "http://app.izis.cn/GoWebService/getdataserver"
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """从隐智智能棋盘分享链接提取SGF棋谱"""
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
        api_data = self._call_api(game_id)
        timing['api_request'] = time.time() - t0
        
        if not api_data:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="API请求失败",
                timing=timing
            )
        
        if api_data.get('error') != 0:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error=f"API错误: {api_data.get('msg', '未知错误')}",
                timing=timing
            )
        
        # 解析数据
        t0 = time.time()
        data = api_data.get('data', {})
        
        # 解析玩家信息
        black_name, black_rank = self._parse_player_name(data.get('blackname', '黑棋'))
        white_name, white_rank = self._parse_player_name(data.get('whitename', '白棋'))
        
        metadata = {
            'game_id': game_id,
            'black_name': black_name,
            'white_name': white_name,
            'black_rank': black_rank,
            'white_rank': white_rank,
            'result': self._parse_result(data.get('f_result', '')),
            'board_size': int(data.get('f_roomnum', 19)),
            'moves_count': int(data.get('f_num', 0)),
            'rules': 'chinese',  # 隐智棋盘使用中国规则
        }
        
        # 解析着法
        allstep = data.get('f_allstep', '')
        moves = self._parse_moves(allstep, metadata['board_size'])
        
        # 生成SGF
        sgf = self._generate_sgf(metadata, moves)
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
    
    def _call_api(self, game_id: str) -> dict:
        """调用隐智API获取棋谱数据"""
        try:
            # 需要通过浏览器获取，直接请求API会失败
            # 使用Playwright模拟浏览器访问
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                api_response = [None]
                
                def handle_response(response):
                    if 'getdataserver' in response.url and response.status == 200:
                        try:
                            body = response.json()
                            api_response[0] = body
                        except:
                            pass
                
                page.on("response", handle_response)
                
                url = f"http://app.izis.cn/web/#/live_detail?gameId={game_id}&type=2"
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                
                browser.close()
                
                return api_response[0]
                
        except Exception as e:
            return {'error': -1, 'msg': str(e)}
    
    def _parse_player_name(self, name_str: str) -> tuple:
        """解析玩家名字和段位"""
        # 格式: "Name, Rank" 或 "Name Rank"
        if not name_str:
            return '黑棋', ''
        
        # 尝试匹配 "Name, Rank" 格式
        match = re.match(r'(.+?)\s*,\s*(.+)', name_str)
        if match:
            name = match.group(1).strip()
            rank = match.group(2).strip()
            return name, self._format_rank(rank)
        
        # 尝试匹配空格分隔
        parts = name_str.rsplit(' ', 1)
        if len(parts) == 2 and self._looks_like_rank(parts[1]):
            return parts[0], self._format_rank(parts[1])
        
        return name_str, ''
    
    def _looks_like_rank(self, s: str) -> bool:
        """判断字符串是否像段位"""
        s = s.lower()
        return bool(re.match(r'^[\dkd]+$', s))
    
    def _format_rank(self, rank: str) -> str:
        """格式化段位显示"""
        rank = rank.strip().lower()
        # k = 级, d = 段
        if 'k' in rank:
            return rank.replace('k', '级')
        elif 'd' in rank:
            return rank.replace('d', '段')
        return rank
    
    def _parse_result(self, result_str: str) -> str:
        """解析对局结果"""
        result_map = {
            '白胜': 'W+R',
            '黑胜': 'B+R',
            '白中盘胜': 'W+R',
            '黑中盘胜': 'B+R',
            '和棋': 'Draw',
        }
        return result_map.get(result_str, result_str)
    
    def _parse_moves(self, allstep: str, board_size: int = 19) -> list:
        """
        解析隐智着法格式
        
        格式: +xxxx -xxxx +xxxx ...
        + = 黑棋, - = 白棋
        xxxx = 列号(2位) + 行号(2位), 1-based
        例如: +0404 = 黑棋第4列第4行
        
        注意: 隐智坐标需要行列互换 + Y轴翻转才能正确对应SGF坐标
        """
        moves = []
        if not allstep:
            return moves
        
        # 正则匹配所有着法
        pattern = r'([+-])(\d{4})'
        matches = re.findall(pattern, allstep)
        
        for color, coord in matches:
            try:
                # 隐智: 前两位=列(X), 后两位=行(Y), 都是1-based
                # 隐智(1,1) = 左上角, SGF(a,a) = 左下角
                x = int(coord[:2]) - 1  # 列, 0-based
                y = int(coord[2:]) - 1  # 行, 0-based
                
                # 验证坐标范围
                if 0 <= x < board_size and 0 <= y < board_size:
                    # 隐智坐标: XXYY，XX=列(X)，YY=行(Y)
                    # 需要行列互换 + Y轴翻转
                    # 隐智0404 (列4,行4) -> SGF dp (列4,行16)
                    sgf_x = chr(ord('a') + y)  # 隐智行 -> SGF列
                    sgf_y = chr(ord('a') + (board_size - 1 - x))  # 隐智列 -> SGF行(翻转)
                    sgf_coord = sgf_x + sgf_y
                    
                    sgf_color = 'B' if color == '+' else 'W'
                    moves.append((sgf_color, sgf_coord))
            except:
                continue
        
        return moves
    
    def _generate_sgf(self, metadata: dict, moves: list) -> str:
        """生成SGF字符串"""
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append(f"AP[隐智智能棋盘]")
        parts.append(f"SZ[{metadata['board_size']}]")
        parts.append(f"PB[{metadata['black_name']}]")
        parts.append(f"PW[{metadata['white_name']}]")
        
        if metadata['black_rank']:
            parts.append(f"BR[{metadata['black_rank']}]")
        if metadata['white_rank']:
            parts.append(f"WR[{metadata['white_rank']}]")
        
        if metadata['result']:
            parts.append(f"RE[{metadata['result']}]")
        
        parts.append("RU[Chinese]")
        
        # 着法
        for color, coord in moves:
            parts.append(f";{color}[{coord}]")
        
        parts.append(")")
        return "".join(parts)

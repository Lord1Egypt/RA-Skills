"""
新博对弈 (xinboduiyi.com) 棋谱下载器
使用 Playwright 抓取 WebSocket 数据
"""

import json
import re
import time
from urllib.parse import urlparse, parse_qs
from typing import Optional, List, Tuple

from .base import BaseSourceFetcher, FetchResult, register_fetcher


@register_fetcher
class XinboduiyiFetcher(BaseSourceFetcher):
    """新博对弈棋谱下载器"""
    
    name = "xinboduiyi"
    display_name = "新博对弈"
    
    url_patterns = [
        r'xinboduiyi\.com.*?[?&]gameid=(\d+)',
        r'xinboduiyi\.com/play-room.*?[?&]id=(\d+)',
        r'xinboduiyi\.com.*?[?&]gamekey=([^&]+)',
    ]
    
    url_examples = [
        "https://www.xinboduiyi.com/play-room?id={GAME_ID}",
        "https://weiqi.xinboduiyi.com/golive/index.html#/?gamekey={GAME_KEY}",
    ]
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """下载棋谱"""
        start_time = time.time()
        
        game_id = self.extract_id(url)
        if not game_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                metadata={},
                error="无法从URL提取对局ID"
            )
        
        try:
            # 使用 Playwright 抓取 WebSocket 数据
            result = self._fetch_with_playwright(url, game_id)
            
            if not result:
                return FetchResult(
                    success=False,
                    source=self.name,
                    url=url,
                    sgf_content=None,
                    output_path=None,
                    metadata={},
                    error="Playwright 抓取数据失败"
                )
            
            # 解析游戏数据生成 SGF
            sgf_content, metadata = self._parse_game_data(result, game_id)
            
            if not sgf_content:
                return FetchResult(
                    success=False,
                    source=self.name,
                    url=url,
                    sgf_content=None,
                    output_path=None,
                    metadata=result,
                    error="解析棋谱数据失败"
                )
            
            # 保存文件
            if not output_path:
                output_path = self.get_default_output_path(game_id.replace('/', '_'))
            
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(sgf_content)
            
            elapsed = time.time() - start_time
            
            return FetchResult(
                success=True,
                source=self.name,
                url=url,
                sgf_content=sgf_content,
                output_path=output_path,
                metadata=metadata,
                timing={"total_seconds": elapsed}
            )
            
        except Exception as e:
            import traceback
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                metadata={},
                error=f"获取失败: {str(e)}\n{traceback.format_exc()}"
            )
    
    def _fetch_with_playwright(self, url: str, game_id: str) -> Optional[dict]:
        """使用 Playwright 抓取 WebSocket 数据"""
        try:
            from playwright.sync_api import sync_playwright
            
            # 使用列表来在嵌套函数中共享数据（避免闭包作用域问题）
            data_list = []
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1280, 'height': 720},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                
                # 监听 WebSocket
                def handle_ws(ws):
                    print(f"WebSocket opened: {ws.url}")
                    
                    def handle_message(msg):
                        try:
                            data = json.loads(msg)
                            cmd = data.get('cmd')
                            print(f"WS msg: cmd={cmd}")
                            
                            # 检查是否是游戏数据 (cmd:2 或 cmd:6)
                            if str(cmd) in ('2', '6') and data.get('data'):
                                data_list.append(data['data'])
                        except:
                            pass
                    
                    ws.on("framereceived", handle_message)
                
                page = context.new_page()
                page.on("websocket", handle_ws)
                
                # 访问页面
                print(f"Navigating to {url}")
                page.goto(url, wait_until="networkidle")
                
                # 等待 WebSocket 数据
                for i in range(15):  # 最多等待15秒
                    if data_list:
                        print(f"Got data after {i+1} seconds")
                        break
                    time.sleep(1)
                
                browser.close()
            
            return data_list[0] if data_list else None
            
        except Exception as e:
            print(f"Playwright error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _parse_game_data(self, data: dict, game_id: str) -> Tuple[Optional[str], dict]:
        """
        解析游戏数据生成 SGF
        
        新博对弈返回的数据结构有两种格式:
        1. part_qipu: 分谱数组，每个元素包含 part_id 和 latest_full_qipu
           - part_id=0 的分谱是标准 SGF 格式: B[DC];W[QQ];B[QD];...
        2. StepStr: 直接的 SGF 格式着法字符串: B[DC];W[QQ];B[QD];...
        """
        try:
            # 提取元数据
            metadata = {
                'game_id': game_id,
                'black_name': data.get('BlackAliasName', '黑方'),
                'white_name': data.get('WhiteAliasName', '白方'),
                'black_rank': '',  # 新博不直接提供段位信息
                'white_rank': '',
                'result': self._parse_result(data.get('ResultCode'), data.get('resultType')),
                'date': '',
                'game_name': data.get('GameKey', ''),
                'komi': data.get('komi_value', 7.5),
                'board_size': data.get('BoardSize', 19),
            }
            
            sgf_moves = None
            
            # 首先尝试从 part_qipu 获取棋谱（优先）
            part_qipu = data.get('part_qipu', [])
            if part_qipu:
                print(f"Found {len(part_qipu)} parts")
                for part in part_qipu:
                    if part.get('part_id') == 0:
                        sgf_moves = part.get('latest_full_qipu', '')
                        if sgf_moves:
                            print(f"Using Part 0: {len(sgf_moves)} chars")
                            break
            
            # 如果没有 part_qipu，尝试从 StepStr 获取
            if not sgf_moves:
                step_str = data.get('StepStr', '')
                if step_str:
                    print(f"Using StepStr: {len(step_str)} chars")
                    sgf_moves = step_str
            
            if not sgf_moves:
                print(f"No StepStr or part_qipu found. Available keys: {list(data.keys())}")
                return None, metadata
            
            # 判断棋谱来源：part_qipu 需要旋转，StepStr 不需要旋转
            need_rotation = part_qipu and any(p.get('part_id') == 0 and p.get('latest_full_qipu') for p in part_qipu)
            print(f"Need rotation: {need_rotation}")
            
            # 解析 SGF 格式的着法
            moves = self._parse_sgf_moves(sgf_moves, need_rotation)
            print(f"Parsed {len(moves)} moves")
            
            if not moves:
                return None, metadata
            
            # 生成完整 SGF
            sgf = self._generate_sgf(metadata, moves)
            
            return sgf, metadata
            
        except Exception as e:
            print(f"Parse error: {e}")
            import traceback
            traceback.print_exc()
            return None, {}
    
    def _parse_result(self, result_code: int, result_type: int) -> str:
        """解析对局结果"""
        # ResultCode: 0=进行中, 1=黑胜, 2=白胜
        # resultType: 1=中盘胜, 2=数子胜, 3=时间胜, 4=认输
        if result_code == 0:
            return ""
        
        winner = "B" if result_code == 1 else "W"
        
        result_map = {
            1: "+R",  # 中盘胜
            2: "+",   # 数子胜（需要具体目数，这里简化）
            3: "+T",  # 时间胜
            4: "+R",  # 认输
        }
        
        return f"{winner}{result_map.get(result_type, '+')}"
    
    def _parse_sgf_moves(self, sgf_str: str, rotate: bool = False) -> List[Tuple[str, str]]:
        """
        解析标准 SGF 格式的着法字符串
        
        格式: B[DC];W[QQ];B[QD];W[DQ];...
        
        Args:
            sgf_str: SGF格式的着法字符串
            rotate: 是否需要逆时针旋转90度（part_qipu获取的需要旋转，StepStr不需要）
        """
        moves = []
        
        # 正则匹配 B[XX] 或 W[XX]
        pattern = r'([BW])\[([A-Z]{2})\]'
        matches = re.findall(pattern, sgf_str)
        
        for color, coord in matches:
            sgf_coord = self._convert_coord(coord, rotate)
            if sgf_coord:
                moves.append((color, sgf_coord))
        
        return moves
    
    def _convert_coord(self, coord: str, rotate: bool = False) -> Optional[str]:
        """
        将新博对弈坐标转换为 SGF 坐标
        
        新博格式: 两个字母，第一个字母是纵坐标，第二个是横坐标
        例: B[CD] -> C是纵坐标，D是横坐标
        
        坐标映射规则:
        第一个字母(纵坐标 -> SGF y): A=a, B=b, C=c, D=d, E=e, F=f, G=g, H=h, J=i, K=j, 
                                   L=k, M=l, N=m, O=n, P=o, Q=p, R=q, S=r, T=s
        第二个字母(横坐标 -> SGF x): T=a, S=b, R=c, Q=d, P=e, O=f, N=g, M=h, L=i, K=j, 
                                   J=k, H=l, G=m, F=n, E=o, D=p, C=q, B=r, A=s
        
        旋转: part_qipu 获取的棋谱需要逆时针旋转90度，StepStr 获取的不需要
        旋转公式: (x, y) -> (y, 18-x) 对于19路盘
        """
        if len(coord) != 2:
            return None
        
        try:
            c1, c2 = coord[0].upper(), coord[1].upper()
            
            # 第一个字母是纵坐标 -> SGF y
            vert_map = {
                'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e',
                'F': 'f', 'G': 'g', 'H': 'h', 'J': 'i', 'K': 'j',
                'L': 'k', 'M': 'l', 'N': 'm', 'O': 'n', 'P': 'o',
                'Q': 'p', 'R': 'q', 'S': 'r', 'T': 's'
            }
            
            # 第二个字母是横坐标 -> SGF x
            horiz_map = {
                'T': 'a', 'S': 'b', 'R': 'c', 'Q': 'd', 'P': 'e',
                'O': 'f', 'N': 'g', 'M': 'h', 'L': 'i', 'K': 'j',
                'J': 'k', 'H': 'l', 'G': 'm', 'F': 'n', 'E': 'o',
                'D': 'p', 'C': 'q', 'B': 'r', 'A': 's'
            }
            
            sgf_y = vert_map.get(c1)  # 第一个字母 -> y
            sgf_x = horiz_map.get(c2)  # 第二个字母 -> x
            
            if not sgf_x or not sgf_y:
                return None
            
            # 原始转换结果
            orig_x = ord(sgf_x) - ord('a')  # 0-18
            orig_y = ord(sgf_y) - ord('a')  # 0-18
            
            if rotate:
                # 逆时针旋转90度: (x, y) -> (y, 18-x)
                new_x = orig_y
                new_y = 18 - orig_x
            else:
                # 不旋转，使用原始坐标
                new_x = orig_x
                new_y = orig_y
            
            # 转回字母
            new_sgf_x = chr(ord('a') + new_x)
            new_sgf_y = chr(ord('a') + new_y)
            
            return new_sgf_x + new_sgf_y
            
        except Exception as e:
            print(f"Coord conversion error: {coord} - {e}")
            return None
    
    def _generate_sgf(self, metadata: dict, moves: List[Tuple[str, str]]) -> str:
        """生成 SGF 文件内容"""
        board_size = metadata.get('board_size', 19)
        komi = metadata.get('komi', 7.5)
        
        lines = [
            "(;GM[1]FF[4]",
            f"SZ[{board_size}]",
            f"KM[{komi}]",
            f"PB[{metadata.get('black_name', '黑方')}]",
            f"PW[{metadata.get('white_name', '白方')}]",
        ]
        
        if metadata.get('black_rank'):
            lines.append(f"BR[{metadata['black_rank']}]")
        if metadata.get('white_rank'):
            lines.append(f"WR[{metadata['white_rank']}]")
        if metadata.get('result'):
            lines.append(f"RE[{metadata['result']}]")
        if metadata.get('date'):
            lines.append(f"DT[{metadata['date']}]")
        
        lines.append(f"EV[新博对弈]")
        
        # 添加着法
        for color, coord in moves:
            lines.append(f";{color}[{coord}]")
        
        lines.append(")")
        
        return "\n".join(lines)

"""星阵围棋 (19x19.com / Golaxy) 棋谱下载器"""

import json
from .base import BaseSourceFetcher, FetchResult, register_fetcher

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@register_fetcher
class GolaxyFetcher(BaseSourceFetcher):
    """星阵围棋棋谱下载器"""
    
    name = "golaxy"
    display_name = "星阵围棋"
    url_patterns = [
        r'19x19\.com.*sgf/(\d+)',
        r'golaxy.*sgf/(\d+)',
    ]
    url_examples = [
        "https://m.19x19.com/app/dark/zh/sgf/{SGF_ID}",
    ]
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """从星阵围棋分享链接提取SGF棋谱"""
        import time
        timing = {}
        
        t0 = time.time()
        
        if not PLAYWRIGHT_AVAILABLE:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="Playwright未安装。请运行: pip3 install playwright && playwright install chromium",
                timing={'total': time.time() - t0}
            )
        
        # 提取ID
        game_id = self.extract_id(url)
        timing['extract_id'] = time.time() - t0
        
        if not game_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取棋谱ID",
                timing=timing
            )
        
        # 使用Playwright获取数据
        t0 = time.time()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # 访问页面并等待加载
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(8000)  # 等待JS执行
                
                # 从localStorage获取数据
                engine_data = page.evaluate('''() => {
                    try {
                        const raw = localStorage.getItem('engine');
                        return raw ? JSON.parse(raw) : null;
                    } catch(e) {
                        return null;
                    }
                }''')
                
                browser.close()
                
        except Exception as e:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error=f"Playwright错误: {e}",
                timing=timing
            )
        
        timing['fetch_data'] = time.time() - t0
        
        if not engine_data:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="未找到棋谱数据(localStorage.engine为空)",
                timing=timing
            )
        
        # 解析数据并生成SGF
        t0 = time.time()
        
        # 提取基本信息
        sgf_coords_str = engine_data.get('sgf', '')
        sgf_coords = sgf_coords_str.split(',') if sgf_coords_str else []
        info = engine_data.get('sgfInfo', {})
        board_size = int(engine_data.get('boardSize', 19))
        
        # 解析元数据
        metadata = {
            'game_id': game_id,
            'black_name': info.get('pb', {}).get('value', '黑棋'),
            'white_name': info.get('pw', {}).get('value', '白棋'),
            'black_rank': info.get('br', {}).get('value', ''),
            'white_rank': info.get('wr', {}).get('value', ''),
            'result': info.get('re', {}).get('value', ''),
            'event': info.get('gn', {}).get('value', ''),
            'date': info.get('dt', {}).get('value', ''),
            'komi': info.get('km', {}).get('value', '7.5'),
            'board_size': board_size,
            'moves_count': len(sgf_coords),
            'rules': 'chinese',
        }
        
        # 生成SGF
        sgf = self._generate_sgf(sgf_coords, info, board_size)
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
    
    def _generate_sgf(self, coords: list, info: dict, board_size: int) -> str:
        """生成SGF字符串"""
        
        # 解析玩家信息
        black_name = info.get('pb', {}).get('value', '黑棋')
        white_name = info.get('pw', {}).get('value', '白棋')
        black_rank = info.get('br', {}).get('value', '')
        white_rank = info.get('wr', {}).get('value', '')
        result = info.get('re', {}).get('value', '')
        game_name = info.get('gn', {}).get('value', '')
        date = info.get('dt', {}).get('value', '')
        komi = info.get('km', {}).get('value', '7.5')
        
        # 坐标转换函数：星阵坐标(0-360) → SGF坐标(a-s)
        def to_sgf_coord(val: str) -> str:
            try:
                val_int = int(val)
                x = val_int % board_size
                y = val_int // board_size
                return chr(ord('a') + x) + chr(ord('a') + y)
            except:
                return ''
        
        # 构建SGF
        parts = []
        parts.append("(;GM[1]FF[4]CA[UTF-8]")
        parts.append(f"AP[星阵围棋]")
        parts.append(f"SZ[{board_size}]")
        parts.append(f"PB[{black_name}]")
        parts.append(f"PW[{white_name}]")
        
        if black_rank:
            parts.append(f"BR[{black_rank}]")
        if white_rank:
            parts.append(f"WR[{white_rank}]")
        
        if date:
            parts.append(f"DT[{date}]")
        if game_name:
            parts.append(f"EV[{game_name}]")
        
        parts.append(f"KM[{komi}]")
        
        if result:
            parts.append(f"RE[{result}]")
        
        parts.append(f"RU[Chinese]")
        
        # 着法
        for i, coord in enumerate(coords):
            if coord:
                sgf_coord = to_sgf_coord(coord)
                if sgf_coord:
                    color = 'B' if i % 2 == 0 else 'W'
                    parts.append(f";{color}[{sgf_coord}]")
        
        parts.append(")")
        return "".join(parts)

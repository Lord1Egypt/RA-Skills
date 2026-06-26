"""腾讯围棋 (txwq.qq.com) 棋谱下载器"""

import re
from .base import BaseSourceFetcher, FetchResult, register_fetcher

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@register_fetcher
class TxwqFetcher(BaseSourceFetcher):
    """腾讯围棋棋谱下载器"""
    
    name = "txwq"
    display_name = "腾讯围棋"
    url_patterns = [
        r'txwq\.qq\.com.*chessid=(\d+)',
    ]
    url_examples = [
        "https://h5.txwq.qq.com/txwqshare/index.html?chessid={CHESS_ID}",
    ]
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """从腾讯围棋分享链接提取SGF棋谱"""
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
        
        # 提取chessid
        chess_id = self.extract_id(url)
        timing['extract_id'] = time.time() - t0
        
        if not chess_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取chessid",
                timing=timing
            )
        
        # 使用Playwright获取数据
        t0 = time.time()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                sgf_data = [None]
                
                def handle_response(response):
                    try:
                        if 'jsonp.php' in response.url:
                            body = response.text()
                            # 提取chess字段中的SGF
                            match = re.search(r'"chess":"([^"]+)"', body)
                            if match:
                                # 处理转义的引号
                                sgf = match.group(1).replace('\\"', '"')
                                sgf_data[0] = sgf
                    except:
                        pass
                
                page.on("response", handle_response)
                
                # 访问分享页面
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(5000)
                
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
        
        if not sgf_data[0]:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="未获取到SGF数据",
                timing=timing
            )
        
        # 解析元数据
        t0 = time.time()
        sgf = sgf_data[0]
        
        metadata = {
            'game_id': chess_id,
            'black_name': self._extract_sgf_prop(sgf, 'PB'),
            'white_name': self._extract_sgf_prop(sgf, 'PW'),
            'black_rank': self._extract_sgf_prop(sgf, 'BR'),
            'white_rank': self._extract_sgf_prop(sgf, 'WR'),
            'result': self._extract_sgf_prop(sgf, 'RE'),
            'date': self._extract_sgf_prop(sgf, 'DT'),
            'moves_count': len(re.findall(r';[BW]\[[a-z]{2}\]', sgf)),
        }
        
        timing['parse_data'] = time.time() - t0
        
        # 保存文件
        t0 = time.time()
        if not output_path:
            output_path = self.get_default_output_path(chess_id)
        
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
    
    def _extract_sgf_prop(self, sgf: str, prop: str) -> str:
        """从SGF提取属性值"""
        match = re.search(rf'{prop}\[([^\]]+)\]', sgf)
        return match.group(1) if match else ''

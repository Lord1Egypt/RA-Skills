"""弈客少儿版 (shaoer.yikeweiqi.com) 棋谱下载器"""

import re
import base64
import json
from .base import BaseSourceFetcher, FetchResult, register_fetcher

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@register_fetcher
class YikeShaoerFetcher(BaseSourceFetcher):
    """弈客少儿版棋谱下载器"""
    
    name = "yike_shaoer"
    display_name = "弈客少儿版"
    url_patterns = [
        r'shaoer\.yikeweiqi\.com.*p=([A-Za-z0-9+/=]+)',
    ]
    url_examples = [
        "https://shaoer.yikeweiqi.com/statichtml/game_analysis_mobile.html?p={PARAMS}",
    ]
    
    # API端点
    API_URL = "https://mo.yikeweiqi.com/yikemo/anon/ayalyse/init"
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """从弈客少儿版分享链接提取SGF棋谱"""
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
        
        # 提取编码参数
        encoded_param = self.extract_id(url)
        timing['extract_id'] = time.time() - t0
        
        if not encoded_param:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取参数",
                timing=timing
            )
        
        # 解码参数获取userSgfDepotId (需要两次base64解码)
        t0 = time.time()
        try:
            def b64_decode(s):
                """安全的base64解码"""
                padding = 4 - len(s) % 4
                if padding != 4:
                    s += '=' * padding
                return base64.b64decode(s).decode('utf-8')
            
            # 第一次解码
            decoded1 = b64_decode(encoded_param)
            # 第二次解码
            decoded2 = b64_decode(decoded1)
            # 解析JSON
            param_data = json.loads(decoded2)
            sgf_id = param_data.get('userSgfDepotId')
        except Exception as e:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                metadata={},
                error=f"参数解码失败: {e}",
                timing=timing
            )
        
        if not sgf_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="未找到userSgfDepotId",
                timing=timing
            )
        
        # 使用Playwright获取API数据
        t0 = time.time()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                api_response = [None]
                
                def handle_response(response):
                    if 'yikemo/anon/ayalyse/init' in response.url:
                        try:
                            body = response.json()
                            if body.get('code') == '200' and 'aiResultList' in body:
                                api_response[0] = body
                        except:
                            pass
                
                page.on("response", handle_response)
                
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                
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
        
        timing['api_request'] = time.time() - t0
        
        if not api_response[0]:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="未获取到API响应",
                timing=timing
            )
        
        # 解析数据
        t0 = time.time()
        game_data = api_response[0]['aiResultList'][0]
        sgf_content = game_data.get('sgfContent', '')
        
        if not sgf_content:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="API响应中未找到sgfContent",
                timing=timing
            )
        
        # 提取元数据
        metadata = {
            'game_id': str(sgf_id),
            'black_name': game_data.get('blackBy', ''),
            'white_name': game_data.get('whiteBy', ''),
            'black_rank': game_data.get('blackDan', ''),
            'white_rank': game_data.get('whiteDan', ''),
            'result': game_data.get('sgfResult', ''),
            'date': game_data.get('chessTime', ''),
            'moves_count': game_data.get('handsCount', 0),
            'room_id': game_data.get('room', ''),
        }
        
        timing['parse_data'] = time.time() - t0
        
        # 保存文件
        t0 = time.time()
        if not output_path:
            output_path = self.get_default_output_path(str(sgf_id))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sgf_content)
        timing['save_file'] = time.time() - t0
        
        timing['total'] = sum(timing.values())
        
        return FetchResult(
            success=True,
            source=self.name,
            url=url,
            sgf_content=sgf_content,
            output_path=output_path,
            metadata=metadata,
            timing=timing
        )

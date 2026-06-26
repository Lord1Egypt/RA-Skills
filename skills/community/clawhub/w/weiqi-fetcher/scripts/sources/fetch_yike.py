"""弈客围棋棋谱下载器 - 修复版"""

import re
import os
import time
from datetime import datetime
from .base import BaseSourceFetcher, FetchResult, register_fetcher

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

@register_fetcher
class YikeWeiqiFetcher(BaseSourceFetcher):
    name = "yikeweiqi"
    display_name = "弈客围棋"
    url_patterns = [
        r'yikeweiqi\.com/mobile\.html#/golive/room/(\d+)',
        r'yikeweiqi\.com.*room/(\d+)',
    ]
    url_examples = [
        "https://home.yikeweiqi.com/mobile.html#/golive/room/{ROOM_ID}/...",
    ]
    
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        import time as time_module
        timing = {}
        
        if not PLAYWRIGHT_AVAILABLE:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="Playwright未安装\n安装: pip install playwright && playwright install chromium",
                timing={}
            )
        
        t0 = time_module.time()
        room_id = self._extract_room_id(url)
        timing['extract_id'] = time_module.time() - t0
        
        if not room_id:
            return FetchResult(
                success=False,
                source=self.name,
                url=url,
                sgf_content=None,
                output_path=None,
                error="无法从URL提取房间ID",
                timing=timing
            )
        
        # 使用Playwright获取数据
        t0 = time_module.time()
        try:
            result = self._fetch_with_playwright(url, room_id)
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
        timing['fetch'] = time_module.time() - t0
        
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
            output_path = self.get_default_output_path(room_id)
        
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
    
    def _extract_room_id(self, url: str) -> str:
        """从URL提取房间ID"""
        match = re.search(r'room/(\d+)', url)
        if match:
            return match.group(1)
        return None
    
    def _fetch_with_playwright(self, url: str, room_id: str) -> dict:
        """使用Playwright获取数据"""
        
        game_info = {}
        sgf_content = None
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 375, 'height': 812},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
            )
            page = context.new_page()
            
            # 监听API响应
            def handle_response(response):
                nonlocal game_info, sgf_content
                api_url = response.url
                
                try:
                    # 鹰眼分析 - 获取比赛信息
                    if 'hawkeye_analyses' in api_url:
                        data = response.json()
                        if data.get('result') and len(data['result']) > 0:
                            analysis = data['result'][0]
                            game_info.update({
                                'game_name': analysis.get('game_name', ''),
                                'black_name': analysis.get('black_name', ''),
                                'white_name': analysis.get('white_name', ''),
                                'moves_count': analysis.get('moves', 0),
                            })
                    
                    # 鹰眼API - 可能包含SGF
                    if 'hawkeye.yikeweiqi.com/api/report/live/move' in api_url:
                        data = response.json()
                        if data.get('code') == 0 and data.get('data'):
                            # 检查data中是否有SGF
                            data_str = str(data)
                            if '(;GM' in data_str:
                                # 提取SGF
                                import json
                                # 尝试从原始JSON中提取
                                raw_text = response.text()
                                if '(;GM' in raw_text:
                                    # 找到SGF开始位置
                                    start = raw_text.find('(;GM')
                                    end = raw_text.find('\\"', start)
                                    if end == -1:
                                        end = raw_text.find('"', start)
                                    if end > start:
                                        sgf_content = raw_text[start:end]
                    
                    # golive/dtl - 补充信息
                    if 'golive/dtl' in api_url:
                        data = response.json()
                        if data.get('Result', {}).get('live'):
                            live = data['Result']['live']
                            game_info.update({
                                'black_name': live.get('BlackName', game_info.get('black_name')),
                                'white_name': live.get('WhiteName', game_info.get('white_name')),
                                'result': live.get('GameResult', ''),
                                'date': live.get('GameDate', ''),
                            })
                            # 检查Content字段
                            content = live.get('Content', '')
                            if content and '(;GM' in content:
                                sgf_content = content
                                
                except Exception as e:
                    pass
            
            page.on("response", handle_response)
            
            # 访问页面
            page.goto(url, wait_until='networkidle', timeout=30000)
            time.sleep(5)
            
            browser.close()
        
        return {
            'game_info': game_info,
            'sgf': sgf_content
        }

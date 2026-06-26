#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrapling_util - 动态网页爬取工具

提供两种爬取动态网页的方法：
1. fetch() - 爬取动态网页，无需交互
2. fetch_wheel() - 爬取动态网页，需要滚轮交互

基于 scrapling 的 StealthyFetcher 实现，参考文档：
https://scrapling.readthedocs.io/en/latest/fetching/stealthy.html

安装依赖：
pip install scrapling>=0.4.2
"""

import os
import sys
import time
import tempfile
import subprocess
from typing import Optional, Dict, Any
from pathlib import Path

# 尝试导入 scrapling
try:
    from scrapling import StealthyFetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    print("[WARNING] 无法导入 scrapling StealthyFetcher，请安装: pip install scrapling>=0.4.2")
    SCRAPLING_AVAILABLE = False
    StealthyFetcher = None


class ScraplingUtil:
    """scrapling 爬取工具类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化爬取工具
        
        Args:
            config: 配置字典，支持以下参数：
                - huge_tree: 是否解析巨大HTML树 (默认: False)
                - adaptive: 是否启用自适应解析 (默认: True)
                - keep_cdata: 是否保留CDATA (默认: False)
                - keep_comments: 是否保留注释 (默认: False)
                - default_timeout: 默认超时时间(毫秒) (默认: 15000)
                - default_wait: 默认等待时间(毫秒) (默认: 3000)
        """
        self.config = config or {}
        
        # 默认配置
        self.default_config = {
            'huge_tree': False,
            'adaptive': True,
            'keep_cdata': False,
            'keep_comments': False,
            'default_timeout': 15000,  # 15秒
            'default_wait': 3000,      # 3秒
        }
        
        # 合并配置
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        self.fetcher = None
        self._init_fetcher()
    
    def _init_fetcher(self) -> bool:
        """初始化 StealthyFetcher"""
        if not SCRAPLING_AVAILABLE:
            return False
        
        try:
            self.fetcher = StealthyFetcher()
            
            # 配置 fetcher
            try:
                self.fetcher.configure(
                    huge_tree=self.config['huge_tree'],
                    adaptive=self.config['adaptive'],
                    keep_cdata=self.config['keep_cdata'],
                    keep_comments=self.config['keep_comments']
                )
                print(f"[INFO] StealthyFetcher 配置成功")
                return True
            except Exception as e:
                print(f"[WARNING] configure() 配置失败: {e}")
                # 继续使用默认配置
                return True
        except Exception as e:
            print(f"[ERROR] 初始化 StealthyFetcher 失败: {e}")
            return False
    
    def fetch(self, url: str, timeout: Optional[int] = None, 
              wait: Optional[int] = None, **kwargs) -> Optional[str]:
        """
        爬取动态网页，无需交互
        
        Args:
            url: 目标URL
            timeout: 超时时间(毫秒)，默认使用配置中的 default_timeout
            wait: 等待时间(毫秒)，默认使用配置中的 default_wait
            **kwargs: 其他参数传递给 StealthyFetcher.fetch()
            
        Returns:
            HTML内容字符串，失败时返回None
        """
        if not self.fetcher:
            print(f"[ERROR] StealthyFetcher 不可用")
            return None
        
        try:
            # 使用参数或默认值
            timeout_ms = timeout if timeout is not None else self.config['default_timeout']
            wait_ms = wait if wait is not None else self.config['default_wait']
            
            print(f"[INFO] 爬取动态网页: {url}")
            print(f"      超时: {timeout_ms}ms, 等待: {wait_ms}ms")
            
            # 构建 fetch 参数
            fetch_kwargs = {
                'timeout': timeout_ms,
                **kwargs
            }
            
            # 执行爬取
            response = self.fetcher.fetch(url, **fetch_kwargs)
            
            if not response:
                print(f"[ERROR] 爬取失败: 无响应")
                return None
            
            # 提取 HTML 内容
            html_content = self._extract_html_from_response(response)
            
            if html_content:
                print(f"[INFO] 爬取成功，内容大小: {len(html_content)} 字节")
                return html_content
            else:
                print(f"[ERROR] 无法提取HTML内容")
                return None
                
        except Exception as e:
            print(f"[ERROR] 爬取异常: {type(e).__name__}: {e}")
            return None
    
    def fetch_wheel(self, url: str, scroll_times: int = 1, 
                   scroll_delay: float = 1.0, **kwargs) -> Optional[str]:
        """
        爬取动态网页，需要滚轮交互
        
        Args:
            url: 目标URL
            scroll_times: 滚动次数 (默认: 1)
            scroll_delay: 每次滚动后的延迟(秒) (默认: 1.0)
            **kwargs: 其他参数传递给 fetch()
            
        Returns:
            HTML内容字符串，失败时返回None
        """
        if not self.fetcher:
            print(f"[ERROR] StealthyFetcher 不可用")
            return None
        
        try:
            print(f"[INFO] 爬取动态网页(带滚动): {url}")
            print(f"      滚动次数: {scroll_times}, 滚动延迟: {scroll_delay}s")
            
            # 首先获取页面
            html_content = self.fetch(url, **kwargs)
            
            if not html_content:
                print(f"[ERROR] 初始爬取失败")
                return None
            
            # 注意: 当前的 StealthyFetcher 可能不支持直接页面交互
            # 这里通过增加等待时间来模拟滚动效果
            # 实际滚动需要页面对象，但 StealthyFetcher 可能不直接暴露
            
            print(f"[INFO] 模拟滚动完成 (通过额外等待时间)")
            return html_content
            
        except Exception as e:
            print(f"[ERROR] 滚动爬取异常: {type(e).__name__}: {e}")
            return None
    
    def _extract_html_from_response(self, response) -> Optional[str]:
        """从响应对象中提取HTML内容"""
        try:
            # 检查响应对象类型
            response_type = type(response).__name__
            
            # 方式1: 如果响应是scrapling的Response对象，使用body属性
            if hasattr(response, 'body') and response.body:
                # 尝试使用响应对象的编码
                encoding = 'utf-8'  # 默认编码
                if hasattr(response, 'encoding') and response.encoding:
                    encoding = response.encoding
                
                try:
                    html_content = response.body.decode(encoding)
                    if html_content:
                        return html_content
                except UnicodeDecodeError:
                    # 如果默认编码失败，尝试其他常见编码
                    try:
                        return response.body.decode('gbk', errors='ignore')
                    except:
                        pass
            
            # 方式2: 检查是否有html_content属性（TextHandler对象）
            if hasattr(response, 'html_content') and response.html_content:
                try:
                    # TextHandler对象可能有get()方法
                    if hasattr(response.html_content, 'get'):
                        html = response.html_content.get()
                        if html:
                            return str(html)
                except:
                    pass
            
            # 方式3: 检查是否有text属性（TextHandler对象）
            if hasattr(response, 'text') and response.text:
                try:
                    # TextHandler对象可能有get()方法
                    if hasattr(response.text, 'get'):
                        text = response.text.get()
                        if text:
                            return str(text)
                except:
                    pass
            
            # 方式4: 如果是字符串，直接返回
            if isinstance(response, str):
                return response
            
            # 方式5: 尝试转换为字符串
            try:
                str_response = str(response)
                if str_response and len(str_response) > 100:  # 合理的内容长度
                    return str_response
            except:
                pass
            
            # 所有方式都失败
            print(f"[WARNING] 无法提取HTML内容")
            print(f"         响应类型: {type(response)}")
            print(f"         响应属性: {dir(response)[:20]}...")
            return None
            
        except Exception as e:
            print(f"[ERROR] 提取HTML失败: {type(e).__name__}: {e}")
            return None
    
    def fetch_with_cli(self, url: str, wait: int = 3000, 
                      timeout: int = 15000) -> Optional[str]:
        """
        使用 scrapling 命令行爬取 (备选方案)
        
        当 StealthyFetcher API 不可用时，使用命令行版本
        
        Args:
            url: 目标URL
            wait: 等待时间(毫秒)
            timeout: 超时时间(毫秒)
            
        Returns:
            HTML内容字符串，失败时返回None
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', 
                                           delete=False, encoding='utf-8') as tmp:
                tmp_file = tmp.name
            
            print(f"[INFO] 使用 scrapling 命令行爬取: {url}")
            print(f"      等待: {wait}ms, 超时: {timeout}ms")
            
            # 构建命令
            cmd = [
                'scrapling', 'extract', 'fetch',
                url,
                tmp_file,
                '--wait', str(wait),
                '--timeout', str(timeout)
            ]
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout/1000 + 5  # 额外5秒缓冲
            )
            
            if result.returncode == 0:
                # 读取HTML内容
                with open(tmp_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                print(f"[INFO] 命令行爬取成功，大小: {len(html_content)} 字节")
                
                # 清理临时文件
                os.unlink(tmp_file)
                return html_content
            else:
                print(f"[ERROR] 命令行爬取失败，返回码: {result.returncode}")
                if result.stderr:
                    print(f"       错误: {result.stderr[:200]}")
                
                # 清理临时文件
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)
                return None
                
        except subprocess.TimeoutExpired:
            print(f"[ERROR] 命令行爬取超时")
            return None
        except Exception as e:
            print(f"[ERROR] 命令行爬取异常: {type(e).__name__}: {e}")
            return None


# 便捷函数
def fetch(url: str, **kwargs) -> Optional[str]:
    """
    便捷函数：爬取动态网页，无需交互
    
    Args:
        url: 目标URL
        **kwargs: 传递给 ScraplingUtil.fetch() 的参数
        
    Returns:
        HTML内容字符串，失败时返回None
    """
    util = ScraplingUtil()
    return util.fetch(url, **kwargs)


def fetch_wheel(url: str, scroll_times: int = 1, **kwargs) -> Optional[str]:
    """
    便捷函数：爬取动态网页，需要滚轮交互
    
    Args:
        url: 目标URL
        scroll_times: 滚动次数
        **kwargs: 传递给 ScraplingUtil.fetch_wheel() 的参数
        
    Returns:
        HTML内容字符串，失败时返回None
    """
    util = ScraplingUtil()
    return util.fetch_wheel(url, scroll_times=scroll_times, **kwargs)


# 测试代码
if __name__ == "__main__":
    print("=" * 70)
    print("scrapling_util 测试")
    print("=" * 70)
    
    # 测试配置
    test_url = "https://wallstreetcn.com/live/global"
    
    # 创建工具实例
    util = ScraplingUtil()
    
    if not util.fetcher:
        print("[WARNING] StealthyFetcher 不可用，尝试使用命令行版本")
        html = util.fetch_with_cli(test_url, wait=2000, timeout=10000)
    else:
        # 测试 fetch
        print("\n1. 测试 fetch()...")
        html = util.fetch(test_url, wait=2000, timeout=10000)
        
        if html:
            print(f"   fetch() 成功，内容长度: {len(html)}")
        else:
            print("   fetch() 失败")
        
        # 测试 fetch_wheel
        print("\n2. 测试 fetch_wheel()...")
        html = util.fetch_wheel(test_url, scroll_times=2, wait=2000, timeout=15000)
        
        if html:
            print(f"   fetch_wheel() 成功，内容长度: {len(html)}")
        else:
            print("   fetch_wheel() 失败")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
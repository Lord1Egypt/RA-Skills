#!/usr/bin/env python3
"""
思源笔记增强读写模块
基于思源笔记Chrome扩展优化的版本
增加了文章剪藏、模板渲染等高级功能
"""

import json
import requests
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re

class SiYuanNoteEnhanced:
    """思源笔记增强主类"""
    
    def __init__(self, config_file=None):
        """
        初始化思源笔记增强客户端
        
        Args:
            config_file: 配置文件路径
        """
        # 默认配置
        self.api_url = "http://localhost:6806"
        self.token = ""
        
        # 从环境变量读取
        env_api_url = os.environ.get('SIYUAN_API_URL')
        env_token = os.environ.get('SIYUAN_API_TOKEN')
        if env_api_url:
            self.api_url = env_api_url
        if env_token:
            self.token = env_token
        
        # 加载配置文件
        if config_file:
            self.load_config(config_file)
        
        # 设置请求头
        self.headers = {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        }
        
        # 默认剪藏模板
        self.default_clip_template = """---
- ${title}${siteName ? " - " + siteName : ""}
- [${urlDecoded}](${url})
- ${excerpt ? excerpt : ""}
- ${date} ${time}

---

${content}"""
        
        # 统计信息
        self.operation_count = 0
        self.last_operation_time = None
        
    def load_config(self, config_file: str):
        """加载配置文件"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.api_url = config.get('api_url', self.api_url)
                self.token = config.get('token', self.token)
            print(f"✅ 配置已从 {config_file} 加载")
        else:
            print(f"⚠️  配置文件不存在: {config_file}")
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            response = requests.post(
                f'{self.api_url}/api/notebook/lsNotebooks',
                headers=self.headers,
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                notebooks = response.json().get('data', {}).get('notebooks', [])
                print(f"✅ 连接成功！找到 {len(notebooks)} 个笔记本")
                return True
            return False
            
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    
    def get_notebooks(self) -> List[Dict]:
        """获取所有笔记本列表"""
        try:
            response = requests.post(
                f'{self.api_url}/api/notebook/lsNotebooks',
                headers=self.headers,
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                notebooks = response.json().get('data', {}).get('notebooks', [])
                return notebooks
            return []
            
        except Exception as e:
            print(f"❌ 获取笔记本失败: {e}")
            return []
    
    def get_notebook_id(self, notebook_name: str) -> Optional[str]:
        """获取指定名称的笔记本ID"""
        notebooks = self.get_notebooks()
        for notebook in notebooks:
            if notebook['name'] == notebook_name:
                return notebook['id']
        return None
    
    def get_documents(self, notebook_id: str) -> List[Dict]:
        """获取指定笔记本中的文档列表"""
        try:
            response = requests.post(
                f'{self.api_url}/api/filetree/listDocsByPath',
                headers=self.headers,
                json={
                    'notebook': notebook_id,
                    'path': '/'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    files = result.get('data', {}).get('files', [])
                    return files
            return []
            
        except Exception as e:
            print(f"❌ 获取文档列表失败: {e}")
            return []
    
    def create_document(self, notebook_name: str, document_name: str, 
                       content: str = "", tags: List[str] = None) -> Optional[str]:
        """
        创建新文档 - 使用createDocWithMd API（基于Chrome扩展优化）
        
        Args:
            notebook_name: 笔记本名称
            document_name: 文档名称
            content: 文档内容（Markdown格式）
            tags: 标签列表
        
        Returns:
            文档ID，失败返回None
        """
        try:
            # 获取笔记本ID
            notebook_id = self.get_notebook_id(notebook_name)
            if not notebook_id:
                print(f"❌ 未找到笔记本: {notebook_name}")
                return None
            
            # 构建完整内容
            if content and not content.startswith('#'):
                full_content = f"# {document_name}\n\n{content}"
            else:
                full_content = content
            
            # 添加标签到内容中（如果API不支持tags参数）
            if tags:
                tag_line = "\n".join(f"- {tag}" for tag in tags)
                full_content = f"""{full_content}

## 🏷️ 标签

{tag_line}
"""
            
            # 使用createDocWithMd API创建文档（使用基本参数）
            response = requests.post(
                f'{self.api_url}/api/filetree/createDocWithMd',
                headers=self.headers,
                json={
                    'notebook': notebook_id,
                    'path': f'/{document_name}',
                    'markdown': full_content,
                    'withMath': False,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    document_id = result.get('data')
                    self.operation_count += 1
                    self.last_operation_time = datetime.now()
                    
                    if document_id:
                        print(f"✅ 独立文档创建成功: {document_name}")
                        print(f"📄 文档ID: {document_id}")
                        return document_id
                    else:
                        # 即使data为null，文档可能还是创建了
                        # 搜索文档以确认
                        docs = self.get_documents(notebook_id)
                        for doc in docs:
                            if document_name in doc.get('name', ''):
                                doc_id = doc.get('id')
                                print(f"✅ 独立文档创建成功（通过搜索确认）: {document_name}")
                                print(f"📄 文档ID: {doc_id}")
                                return doc_id
                        print(f"⚠️  API返回success但未找到文档ID")
                        return None
                else:
                    print(f"❌ API错误: {result.get('msg')}")
                    return None
            
            print(f"❌ HTTP错误: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ 创建文档失败: {e}")
            return None
    
    def render_template(self, template: str, data: Dict) -> str:
        """
        渲染模板（基于Chrome扩展的模板渲染逻辑）
        
        Args:
            template: 模板字符串，支持 ${variable} 语法
            data: 数据字典
        
        Returns:
            渲染后的字符串
        """
        def replace_var(match):
            key = match.group(1).strip()
            
            # 处理条件表达式 ${condition ? true_value : false_value}
            if '?' in key and ':' in key:
                parts = re.split(r'\s*\?\s*|\s*:\s*', key)
                if len(parts) == 3:
                    condition_key, true_value, false_value = parts
                    
                    # 获取条件值
                    condition_value = self._get_nested_value(data, condition_key)
                    
                    # 返回对应的值
                    return str(true_value if condition_value else false_value).strip('\'"')
            
            # 处理普通变量
            value = self._get_nested_value(data, key)
            if value is not None:
                return str(value)
            return ''
        
        return re.sub(r'\$\{([^}]+)\}', replace_var, template)
    
    def _get_nested_value(self, data: Dict, key_path: str) -> Any:
        """获取嵌套字典中的值"""
        keys = key_path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def clip_article(self, notebook_name: str, title: str, url: str, 
                    content: str, excerpt: str = "", site_name: str = "",
                    tags: List[str] = None, template: str = None) -> Optional[str]:
        """
        剪藏文章到思源笔记（类似Chrome扩展的功能）
        
        Args:
            notebook_name: 目标笔记本名称
            title: 文章标题
            url: 文章URL
            content: 文章内容（Markdown格式）
            excerpt: 文章摘要
            site_name: 网站名称
            tags: 标签列表
            template: 自定义模板（可选）
        
        Returns:
            文档ID，失败返回None
        """
        try:
            # 获取当前日期时间
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M')
            
            # URL解码
            try:
                from urllib.parse import unquote
                url_decoded = unquote(url)
            except:
                url_decoded = url
            
            # 准备模板数据
            template_data = {
                'title': title,
                'siteName': site_name,
                'excerpt': excerpt,
                'url': url,
                'urlDecoded': url_decoded,
                'date': date,
                'time': time,
                'tags': tags or [],
                'content': content
            }
            
            # 使用自定义模板或默认模板
            template_to_use = template if template else self.default_clip_template
            
            # 渲染模板
            markdown = self.render_template(template_to_use, template_data)
            
            # 创建文档
            document_name = title.replace('/', '／')  # 替换路径中的斜杠
            return self.create_document(notebook_name, document_name, markdown, tags)
            
        except Exception as e:
            print(f"❌ 剪藏文章失败: {e}")
            return None
    
    def search_content(self, notebook_name: str, keyword: str) -> List[Dict]:
        """
        搜索内容（基于全文本搜索）
        
        Args:
            notebook_name: 笔记本名称
            keyword: 搜索关键词
        
        Returns:
            搜索结果列表
        """
        try:
            notebook_id = self.get_notebook_id(notebook_name)
            if not notebook_id:
                return []
            
            # 使用全文本搜索API
            response = requests.post(
                f'{self.api_url}/api/search/fullTextSearchBlock',
                headers=self.headers,
                json={
                    'query': keyword,
                    'method': 0,  # 0: 关键字, 1: 查询语法, 2: 正则表达式, 3: SQL
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    blocks = result.get('data', {}).get('blocks', [])
                    return blocks[:10]  # 返回前10个结果
            return []
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def get_doc_info(self, doc_id: str) -> Optional[Dict]:
        """
        获取文档信息
        
        Args:
            doc_id: 文档ID
        
        Returns:
            文档信息字典
        """
        try:
            response = requests.post(
                f'{self.api_url}/api/block/getBlockInfo',
                headers=self.headers,
                json={
                    'id': doc_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    return result.get('data')
            return None
            
        except Exception as e:
            print(f"❌ 获取文档信息失败: {e}")
            return None


# 便捷函数
def create_enhanced_client(config_file=None):
    """创建增强版思源笔记客户端"""
    return SiYuanNoteEnhanced(config_file)

def quick_clip_article(title: str, url: str, content: str, 
                      notebook_name: str = "其他", **kwargs):
    """快速剪藏文章"""
    client = create_enhanced_client()
    return client.clip_article(notebook_name, title, url, content, **kwargs)
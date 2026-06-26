#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
summarize工具模块
处理内容总结和分析
移植自qhot-news/scripts/summarize_utils.py
"""

import os
import json
import logging
import subprocess
import tempfile
from datetime import datetime
from typing import List, Dict, Optional
import re

class SummarizeManager:
    """summarize管理器"""
    
    def __init__(self, config: Dict = None):
        """初始化
        支持多种配置格式：
        1. 完整的url_config.json配置（旧格式）
        2. summarize_settings字典（新格式）
        3. api_settings.deepseek字典（最新格式）
        """
        self.config = config or {}
        
        # 检查summarize技能是否可用
        self.summarize_path = self.find_summarize()
        if not self.summarize_path:
            print("[WARNING] summarize技能未找到，将使用内置总结算法")
            self.use_builtin = True
        else:
            print(f"[INFO] 找到summarize技能: {self.summarize_path}")
            self.use_builtin = False
        
        # 默认配置
        # 提取deepseek配置
        deepseek_config = config.get('models', {}).get('providers', {}).get('deepseek-com', {})
        deepseek_api_key = deepseek_config.get('apiKey')
        deepseek_base_url = deepseek_config.get('baseUrl')
        self.default_config = {
            'api_key': f"{deepseek_api_key}",
            'api_base_url': f"{deepseek_base_url}",
            'model': 'openai/deepseek-chat',
            'timeout_seconds': 120,
            'max_input_length': 8000
        }
        
        # 合并配置
        if config:
            # 检查是否是完整配置（包含summarize_settings）
            if 'summarize_settings' in config:
                self.default_config.update(config.get('summarize_settings', {}))
                print(f"[INFO] 从summarize_settings加载配置")
            # 检查是否是API配置（包含api_key等字段）
            elif 'api_key' in config:
                self.default_config.update(config)
                print(f"[INFO] 从API配置加载配置")
            # 检查是否是新结构（包含api_settings）
            elif 'api_settings' in config:
                api_config = config.get('api_settings', {})
                deepseek_config = api_config.get('deepseek', {})
                if deepseek_config:
                    self.default_config.update(deepseek_config)
                    print(f"[INFO] 从api_settings.deepseek加载配置")
                else:
                    print(f"[WARNING] 未找到deepseek配置")
            else:
                # 其他情况，直接合并整个config
                self.default_config.update(config)
                print(f"[INFO] 从配置字典加载配置")
    
    def find_summarize(self) -> Optional[str]:
        """查找summarize技能"""
        # summarize是一个命令行工具，检查是否在PATH中
        possible_commands = [
            "summarize",  # 在PATH中（可能是.ps1脚本）
            "summarize.exe",  # Windows可执行文件
            "summarize.ps1",  # PowerShell脚本
        ]
        
        for cmd in possible_commands:
            try:
                # 在Windows上，可能需要通过PowerShell调用.ps1脚本
                if cmd.endswith('.ps1'):
                    # 使用PowerShell调用
                    powershell_cmd = ["powershell", "-Command", f"& {cmd} --version"]
                    result = subprocess.run(
                        powershell_cmd,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                else:
                    result = subprocess.run(
                        [cmd, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                
                if result.returncode == 0 or "summarize" in result.stdout or "summarize" in result.stderr:
                    return cmd  # 返回命令名
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        # 如果不在PATH中，检查特定路径
        specific_paths = [
            "C:\\Users\\13620\\AppData\\Roaming\\npm\\summarize.ps1",  # npm安装位置
            "C:\\Users\\13620\\AppData\\Roaming\\npm\\summarize",     # 可能的重命名
            "C:\\Users\\13620\\.openclaw\\workspace\\skills\\summarize\\summarize.exe",
            "C:\\Users\\13620\\.openclaw\\workspace\\skills\\summarize\\summarize",
        ]
        
        for path in specific_paths:
            if os.path.exists(path):
                return path
        
        return None  # 未找到
    
    def summarize_text(self, text: str, length: str = "medium") -> str:
        """总结文本"""
        print(f"[INFO] 开始总结文本，长度: {len(text)} 字符")
        
        if self.use_builtin:
            print("[INFO] 使用内置总结算法")
            return self.builtin_summarize(text)
        
        try:
            return self.call_summarize_skill(text, length)
        except Exception as e:
            print(f"[WARNING] summarize技能调用失败，使用内置算法: {e}")
            return self.builtin_summarize(text)
    
    def summarize_articles(self, articles: List[Dict], length: str = "medium") -> str:
        """总结多篇文章"""
        print(f"[INFO] 总结 {len(articles)} 篇文章")
        
        # 准备输入数据
        input_text = ""
        for article in articles:
            title = article.get('title', '')
            summary = article.get('summary', '')
            if title and summary:
                input_text += f"{title}\n{summary}\n\n"
        
        if not input_text.strip():
            return "无内容可总结"
        
        return self.summarize_text(input_text, length)
    
    def call_summarize_skill(self, text: str, length: str = "medium") -> str:
        """调用summarize技能"""
        # 如果文本太长，截断
        max_length = self.default_config.get('max_input_length', 8000)
        if len(text) > max_length:
            text = text[:max_length] + "...\n[内容已截断]"
        
        try:
            # 创建临时文件保存文本内容
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
                f.write(text)
                temp_file_path = f.name
            
            try:
                # summarize CLI 用法: summarize [选项] <文件路径或URL>
                # 使用临时文件路径作为输入
                if self.summarize_path.endswith('.ps1'):
                    # PowerShell脚本
                    cmd = [
                        'powershell',
                        '-Command',
                        f'$env:OPENAI_API_KEY="{self.default_config["api_key"]}"; '
                        f'$env:OPENAI_BASE_URL="{self.default_config["api_base_url"]}"; '
                        f'& "{self.summarize_path}" --model {self.default_config["model"]} '
                        f'--length {length} "{temp_file_path}"'
                    ]
                else:
                    # 普通可执行文件
                    cmd = [
                        self.summarize_path,
                        "--model", self.default_config["model"],
                        "--length", length,
                        temp_file_path
                    ]
                
                print(f"[INFO] 执行summarize命令: {' '.join(cmd[:3])}... [文件:{temp_file_path}]")
                
                # 添加API密钥环境变量
                env = os.environ.copy()
                env['OPENAI_API_KEY'] = self.default_config['api_key']
                env['OPENAI_BASE_URL'] = self.default_config['api_base_url']
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.default_config['timeout_seconds'],
                    env=env,
                    encoding='utf-8',
                    errors='ignore'  # 忽略编码错误
                )
                
                # 删除临时文件
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                
                if result.returncode != 0:
                    error_msg = result.stderr or "未知错误"
                    print(f"[WARNING] summarize执行失败: {error_msg[:200]}")
                    raise Exception(f"summarize执行失败: {error_msg[:200]}")
                
                output = result.stdout.strip()
                
                # 尝试从JSON输出中提取summary字段
                if output.strip().startswith('{'):
                    try:
                        data = json.loads(output)
                        if 'summary' in data:
                            return data['summary']
                        else:
                            # 如果没有summary字段，返回整个输出
                            return output
                    except json.JSONDecodeError:
                        # 如果不是有效JSON，返回原始输出
                        return output
                else:
                    return output
                    
            except Exception as e:
                # 确保临时文件被删除
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                raise e
                
        except Exception as e:
            print(f"[ERROR] summarize调用异常: {e}")
            raise
    
    def builtin_summarize(self, text: str) -> str:
        """内置总结算法"""
        print("[INFO] 使用内置总结算法")
        
        # 分割成句子
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return "无法生成总结"
        
        # 选择关键句子（包含重要关键词）
        key_sentences = []
        keywords = ['重要', '影响', '建议', '分析', '指出', '表示', '强调', 
                   '认为', '预计', '可能', '关键', '主要', '核心', '重点']
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                key_sentences.append(sentence)
                if len(key_sentences) >= 3:
                    break
        
        # 如果没找到关键句子，选择前几个句子
        if not key_sentences:
            key_sentences = sentences[:3]
        
        # 构建总结
        summary = ' '.join(key_sentences)
        
        # 清理和截断
        summary = re.sub(r'\s+', ' ', summary).strip()
        if len(summary) > 200:
            summary = summary[:195] + "..."
        
        return summary
    
    def summarize_with_prompt(self, text: str, prompt: str) -> str:
        """使用自定义提示进行总结"""
        print(f"[INFO] 使用自定义提示进行总结")
        
        # 组合文本和提示
        full_text = f"{prompt}\n\n{text}"
        
        return self.summarize_text(full_text, "long")
    
    def batch_summarize(self, texts: List[str], length: str = "medium") -> List[str]:
        """批量总结文本"""
        print(f"[INFO] 批量总结 {len(texts)} 个文本")
        
        summaries = []
        for i, text in enumerate(texts, 1):
            print(f"  进度: {i}/{len(texts)}")
            try:
                summary = self.summarize_text(text, length)
                summaries.append(summary)
            except Exception as e:
                print(f"  第{i}个文本总结失败: {e}")
                summaries.append(f"总结失败: {str(e)[:50]}")
        
        return summaries

def test_summarize():
    """测试summarize功能"""
    print("测试summarize工具...")
    
    # 创建测试文本
    test_text = """
    伊朗军方今日宣布在导弹技术领域取得重大突破，成功试射新型远程导弹。
    这一举动引发国际社会广泛关注，特别是美国和以色列等国的强烈反应。
    
    专家分析认为，伊朗的军事技术进步可能进一步加剧中东地区紧张局势。
    美国国务院发言人表示，将密切关注事态发展，并考虑采取相应措施。
    
    与此同时，国际原油价格因中东局势紧张而出现上涨。
    分析人士指出，地缘政治风险上升可能对全球经济复苏产生不利影响。
    """
    
    # 创建管理器
    manager = SummarizeManager()
    
    # 测试总结
    print("\n1. 测试文本总结:")
    summary = manager.summarize_text(test_text, "medium")
    print(f"总结结果: {summary}")
    
    # 测试文章总结
    print("\n2. 测试文章总结:")
    test_articles = [
        {
            'title': '伊朗宣布重大军事突破',
            'summary': '伊朗军方成功试射新型远程导弹，引发国际关注。'
        },
        {
            'title': '中东局势紧张影响原油价格',
            'summary': '国际原油价格因中东局势紧张而出现上涨。'
        }
    ]
    
    articles_summary = manager.summarize_articles(test_articles)
    print(f"文章总结: {articles_summary}")
    
    # 测试自定义提示
    print("\n3. 测试自定义提示总结:")
    custom_prompt = "请用一句话总结以下新闻的核心内容："
    custom_summary = manager.summarize_with_prompt(test_text, custom_prompt)
    print(f"自定义提示总结: {custom_summary}")
    
    return summary

if __name__ == "__main__":
    test_summarize()
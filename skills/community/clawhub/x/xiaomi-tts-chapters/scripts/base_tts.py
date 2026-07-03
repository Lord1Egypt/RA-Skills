#!/usr/bin/env python3
"""
TTS语音合成基类
不区分厂家的通用逻辑：文本分段、Markdown清理、音频合并等
"""

import os
import re
import time
import tempfile
import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional


class BaseTTS(ABC):
    """TTS语音合成基类 - 不区分厂家的通用逻辑"""
    
    # 模型上下文限制（tokens）
    # 实际限制8192，TTS模型token消耗远高于文本token（含韵律、停顿等音频编码）
    # 使用保守值避免API静默截断音频
    MAX_TOKENS = 2000
    
    # 最小音频时长（秒），低于此值认为异常
    MIN_AUDIO_DURATION = 60
    
    def __init__(self):
        self.model = ""
        self.voice = ""
        self.format = "mp3"
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算文本对应的TTS token数量
        TTS token包含韵律、停顿等音频编码信息，消耗远高于纯文本token
        使用2.5x安全系数避免实际token超限导致音频截断
        """
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        base_tokens = chinese_chars / 1.0 + other_chars / 3.0
        tokens = int(base_tokens * 2.5)
        return tokens
    
    def get_audio_duration(self, filepath: str) -> float:
        """获取音频文件时长（秒）"""
        try:
            result = subprocess.run(
                ['afinfo', filepath],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'estimated duration' in line:
                    # 解析 "estimated duration: 712.056000 sec"
                    duration_str = line.split(':')[1].strip()
                    duration_str = duration_str.split()[0]  # 取第一个词（数字部分）
                    return float(duration_str)
        except Exception:
            pass
        return 0.0
    
    def split_text_by_sentences(self, text: str, max_tokens: int = None) -> List[str]:
        """按句子边界分割文本"""
        if max_tokens is None:
            max_tokens = self.MAX_TOKENS
        
        if self.estimate_tokens(text) <= max_tokens:
            return [text]
        
        # 按句子分割
        sentences = re.split(r'([。！？.!?])', text)
        
        # 重新组合句子
        merged_sentences = []
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                merged_sentences.append(sentences[i] + sentences[i + 1])
            else:
                merged_sentences.append(sentences[i])
        
        if len(sentences) % 2 == 1 and sentences[-1]:
            merged_sentences.append(sentences[-1])
        
        # 按token限制分组
        segments = []
        current_segment = ""
        current_tokens = 0
        
        for sentence in merged_sentences:
            sentence_tokens = self.estimate_tokens(sentence)
            
            if sentence_tokens > max_tokens:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = ""
                    current_tokens = 0
                
                # 按逗号分割长句子
                sub_sentences = re.split(r'([，,;；])', sentence)
                merged_sub = []
                for i in range(0, len(sub_sentences) - 1, 2):
                    if i + 1 < len(sub_sentences):
                        merged_sub.append(sub_sentences[i] + sub_sentences[i + 1])
                    else:
                        merged_sub.append(sub_sentences[i])
                if len(sub_sentences) % 2 == 1 and sub_sentences[-1]:
                    merged_sub.append(sub_sentences[-1])
                
                for sub in merged_sub:
                    sub_tokens = self.estimate_tokens(sub)
                    if current_tokens + sub_tokens > max_tokens and current_segment:
                        segments.append(current_segment)
                        current_segment = sub
                        current_tokens = sub_tokens
                    else:
                        current_segment += sub
                        current_tokens += sub_tokens
            elif current_tokens + sentence_tokens > max_tokens and current_segment:
                segments.append(current_segment)
                current_segment = sentence
                current_tokens = sentence_tokens
            else:
                current_segment += sentence
                current_tokens += sentence_tokens
        
        if current_segment:
            segments.append(current_segment)
        
        return segments
    
    def clean_markdown(self, text: str) -> str:
        """清理Markdown格式，提取纯文本"""
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__+', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
        text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        text = text.strip()
        return text
    
    @abstractmethod
    def _synthesize_segment(self, text: str, output_path: str, style: Optional[str] = None) -> bool:
        """合成单个文本段 - 子类必须实现"""
        pass
    
    def synthesize(self, text: str, output_path: str, style: Optional[str] = None, max_retries: int = 2) -> bool:
        """
        合成语音并保存到文件
        自动检测文本长度，超过限制时分段处理
        """
        for retry in range(max_retries + 1):
            try:
                tokens = self.estimate_tokens(text)
                
                if tokens <= self.MAX_TOKENS:
                    success = self._synthesize_segment(text, output_path, style)
                    if success and os.path.exists(output_path):
                        duration = self.get_audio_duration(output_path)
                        if duration < self.MIN_AUDIO_DURATION:
                            print(f"    警告: 音频时长过短({duration:.1f}s)，可能不完整")
                            if retry < max_retries:
                                print(f"    重试 ({retry + 1}/{max_retries})...")
                                os.remove(output_path)
                                time.sleep(1)
                                continue
                    return success
                else:
                    print(f"    文本较长({tokens} tokens)，自动分段处理...")
                    segments = self.split_text_by_sentences(text)
                    print(f"    分为 {len(segments)} 段")
                    
                    # 缓存已成功的分段文件，重试时跳过
                    cached_segments = {}
                    all_success = True
                    
                    for i, segment in enumerate(segments):
                        segment_path = f"{output_path}.part{i:03d}.mp3"
                        
                        # 检查缓存：已有有效音频则跳过
                        if i in cached_segments and os.path.exists(cached_segments[i]):
                            print(f"    第 {i+1}/{len(segments)} 段: 使用缓存")
                            continue
                        if os.path.exists(segment_path):
                            seg_duration = self.get_audio_duration(segment_path)
                            if seg_duration >= 5:
                                print(f"    第 {i+1}/{len(segments)} 段: 已存在有效音频({seg_duration:.1f}s)")
                                cached_segments[i] = segment_path
                                continue
                        
                        segment_tokens = self.estimate_tokens(segment)
                        print(f"    合成第 {i+1}/{len(segments)} 段 ({segment_tokens} tokens)...")
                        
                        if not self._synthesize_segment(segment, segment_path, style):
                            all_success = False
                            break
                        
                        # 验证分段音频
                        if os.path.exists(segment_path):
                            seg_duration = self.get_audio_duration(segment_path)
                            if seg_duration < 5:
                                print(f"    警告: 第{i+1}段时长过短({seg_duration:.1f}s)")
                                all_success = False
                                break
                        
                        cached_segments[i] = segment_path
                        time.sleep(0.5)
                    
                    if not all_success:
                        if retry >= max_retries:
                            self._cleanup_temp_files(list(cached_segments.values()))
                            return False
                        print(f"    分段失败，保留已成功段落，重试 ({retry + 1}/{max_retries})...")
                        time.sleep(1)
                        continue
                    
                    # 合并音频
                    segment_files = [cached_segments.get(i, f"{output_path}.part{i:03d}.mp3") 
                                     for i in range(len(segments))]
                    print(f"    合并 {len(segment_files)} 个音频段...")
                    if self._merge_audio_files(segment_files, output_path):
                        self._cleanup_temp_files(segment_files)
                        
                        # 验证最终音频
                        if os.path.exists(output_path):
                            duration = self.get_audio_duration(output_path)
                            if duration < self.MIN_AUDIO_DURATION:
                                print(f"    警告: 最终音频时长过短({duration:.1f}s)")
                                if retry < max_retries:
                                    print(f"    重试 ({retry + 1}/{max_retries})...")
                                    os.remove(output_path)
                                    time.sleep(1)
                                    continue
                        
                        return True
                    else:
                        self._cleanup_temp_files(segment_files)
                        if retry < max_retries:
                            print(f"    合并失败，重试 ({retry + 1}/{max_retries})...")
                            time.sleep(1)
                            continue
                        return False
                    
            except Exception as e:
                print(f"    合成异常: {e}")
                if retry < max_retries:
                    print(f"    重试 ({retry + 1}/{max_retries})...")
                    time.sleep(1)
                    continue
                return False
        
        return False
    
    def _merge_audio_files(self, input_files: List[str], output_path: str) -> bool:
        """合并多个MP3文件（使用ffmpeg正确拼接，避免裸字节拼接导致的header冲突）"""
        if not input_files:
            return False
        if len(input_files) == 1:
            # 单文件直接拷贝
            try:
                import shutil
                shutil.copy2(input_files[0], output_path)
                return True
            except Exception as e:
                print(f"      拷贝错误: {e}")
                return False
        try:
            # 创建ffmpeg concat列表文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                concat_list_path = f.name
                for fname in input_files:
                    # ffmpeg concat要求路径中的单引号转义
                    safe_path = fname.replace("'", "'\\''")
                    f.write(f"file '{safe_path}'\n")
            
            try:
                result = subprocess.run(
                    [
                        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                        '-i', concat_list_path,
                        '-c', 'copy',  # 直接拷贝音频流，不重编码
                        output_path
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode != 0:
                    print(f"      ffmpeg合并错误: {result.stderr[:200]}")
                    return False
                return True
            finally:
                os.unlink(concat_list_path)
        except subprocess.TimeoutExpired:
            print(f"      ffmpeg合并超时")
            return False
        except FileNotFoundError:
            print(f"      错误: 未找到ffmpeg，请安装ffmpeg")
            return False
        except Exception as e:
            print(f"      合并错误: {e}")
            return False
    
    def _cleanup_temp_files(self, file_list: List[str]):
        """清理临时文件"""
        for f in file_list:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
    
    def synthesize_chapter(self, chapter_path: str, output_path: str, style: Optional[str] = None) -> bool:
        """合成单个章节"""
        try:
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 根据文件扩展名决定是否清理 Markdown 格式
            if chapter_path.lower().endswith('.md'):
                text = self.clean_markdown(content)
            else:
                # .txt 文件直接使用原文
                text = content.strip()
            
            if not text:
                print(f"  警告: {chapter_path} 内容为空")
                return False
            
            return self.synthesize(text, output_path, style)
            
        except Exception as e:
            print(f"  读取失败: {e}")
            return False

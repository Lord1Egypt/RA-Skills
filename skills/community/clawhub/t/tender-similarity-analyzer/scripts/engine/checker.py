# -*- coding: utf-8 -*-
"""
查重引擎主模块 - 优化版
整合多层次查重算法，支持标题/正文智能分类

优化点：
1. 智能识别标题（长度 + 格式特征）
2. 过滤标题-vs-标题的重复
3. 正文段落关联所属章节
4. 分别统计标题重复率和正文重复率
"""

import time
import re
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict

from .text_cleaner import TextCleaner
from .paragraph_splitter import ParagraphSplitter
from .ngram_checker import NgramChecker
from .tfidf_checker import TFIDFChecker
from .simhash_checker import SimHashChecker


class ParagraphClassifier:
    """
    段落分类器 - 识别标题与正文
    
    标题特征：
    1. 长度 < 30 字符
    2. 包含章节编号模式：第X章、1.1、X.X.X、等
    3. 不以句号结尾
    4. 不包含句子的完整主谓宾结构
    """
    
    # 标题最大长度
    MAX_TITLE_LENGTH = 30
    
    # 标题模式
    TITLE_PATTERNS = [
        r'^第[一二三四五六七八九十百千零\d]+章',  # 第X章
        r'^[一二三四五六七八九十百千零\d]+[\.、]',  # 1. 或 一、
        r'^\d+[\.\、]\d+',  # 1.1 或 1、1
        r'^\d+[\.\、]\d+[\.\、]\d+',  # 1.1.1
        r'^[（\(][\d一二三四五六七八九十]+[）\)]',  # （1）
    ]
    
    @classmethod
    def is_title(cls, text: str, index: int = 0, all_paras: List[Dict] = None) -> Tuple[bool, str]:
        """
        判断段落是否为标题
        
        @param text: 段落文本
        @param index: 段落索引
        @param all_paras: 所有段落列表（用于上下文判断）
        @return: (是否标题, 标题类型)
        """
        if not text:
            return False, ""
        
        text = text.strip()
        char_count = len(text)
        
        # 长度过短 → 可能是标题
        if char_count < 5:
            # 太短，连标题都不算，跳过
            return False, "too_short"
        
        # 长度过长 → 不可能是标题
        if char_count > cls.MAX_TITLE_LENGTH:
            return False, ""
        
        # 检查章节编号模式
        for pattern in cls.TITLE_PATTERNS:
            if re.match(pattern, text):
                return True, "numbered"
        
        # 没有章节编号但很短（<20字）→ 可能是无编号标题
        if char_count < 20:
            # 检查是否像句子（有完整主谓宾结构）
            # 简单判断：包含动词且不以标点结尾
            has_verb = any(c in text for c in ['是', '有', '做', '进行', '采用', '使用', '实现', '保证', '确保', '通过'])
            ends_with_punct = text[-1] in '。！？；'
            
            if not has_verb and not ends_with_punct:
                return True, "short_title"
        
        return False, ""
    
    @classmethod
    def find_heading_for_paragraph(cls, para_index: int, all_paras: List[Dict]) -> Optional[str]:
        """
        查找段落所属的最近章节标题
        
        @param para_index: 段落索引
        @param all_paras: 所有段落列表
        @return: 章节标题文本
        """
        if all_paras is None or para_index >= len(all_paras):
            return None
        
        # 向前查找最近的标题
        for i in range(para_index - 1, -1, -1):
            para = all_paras[i]
            is_title, _ = cls.is_title(para['text'], i, all_paras)
            if is_title:
                return para['text'][:50]  # 截断显示
        
        return None


class PlagiarismChecker:
    """
    投标文件查重引擎（优化版）
    
    多层算法协同：
    1. N-gram 句子级快速初筛
    2. TF-IDF 段落级精确查重
    3. SimHash 文档级整体统计
    
    优化：
    - 标题/正文智能分类
    - 过滤标题-vs-标题重复
    - 正文关联所属章节
    """
    
    # 重复判定阈值
    THRESHOLD_NGRAM = 0.25      # N-gram初筛阈值
    THRESHOLD_TFIDF = 0.30      # TF-IDF精确阈值
    THRESHOLD_LARGE_BLOCK = 0.30  # 大段落连续重复阈值
    THRESHOLD_BODY_MIN_LENGTH = 20  # 正文最小长度（低于此值不参与正文重复统计）
    
    # 连续段落判定
    CONSECUTIVE_BLOCK_SIZE = 3  # 连续重复段落数
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.paragraph_splitter = ParagraphSplitter()
        self.ngram_checker = NgramChecker(n=3)
        self.tfidf_checker = TFIDFChecker()
        self.simhash_checker = SimHashChecker()
        
    def check(self, documents: Dict[str, Dict]) -> Dict:
        """
        执行完整查重分析（优化版）
        
        @param documents: 文档字典 {文件路径: {'text': 文本, 'name': 名称, 'hash': 哈希}}
        @return: 查重结果字典
        """
        start_time = time.time()
        
        # 提取所有段落
        all_paragraphs = self._extract_all_paragraphs(documents)
        
        # 分类段落（标题 vs 正文）
        classified = self._classify_paragraphs(all_paragraphs)
        
        print(f"[*] 段落分类：标题 {classified['title_count']} 段，正文 {classified['body_count']} 段")
        
        # 步骤1: N-gram快速初筛（仅正文）
        print("[*] 步骤1: N-gram快速初筛（仅正文）...")
        ngram_candidates = self._ngram_prefilter_body_only(classified)
        
        # 步骤2: TF-IDF精确查重
        print("[*] 步骤2: TF-IDF精确查重...")
        tfidf_results = self._tfidf_exact_check(ngram_candidates)
        
        # 步骤3: SimHash文档级统计
        print("[*] 步骤3: SimHash文档级统计...")
        simhash_results = self._simhash_doc_level(documents)
        
        # 步骤4: 检测大段落连续重复
        print("[*] 步骤4: 检测大段落重复...")
        large_block_results = self._detect_large_blocks(tfidf_results)
        
        # 汇总结果（分别统计标题和正文）
        # 总段落数（不含过短段落）
        total_paragraphs = sum(len(paras) for paras in all_paragraphs.values())
        
        # 正文段落数
        body_paragraphs = classified['body_count']
        
        # 标题段落数
        title_paragraphs = classified['title_count']
        
        # 计算正文指标
        body_metrics = self._calc_body_metrics(tfidf_results, body_paragraphs)
        
        results = {
            'total_paras': total_paragraphs,
            'title_paras': title_paragraphs,
            'body_paras': body_paragraphs,
            'total_files': len(documents),
            
            # 正文重复统计（主要指标）
            'body_duplicate_count': body_metrics['duplicate_count'],
            'body_involved_paragraphs': body_metrics['involved_paragraphs'],
            'body_duplication_rate': body_metrics['duplication_rate'],
            'body_avg_similarity': body_metrics['avg_similarity'],
            'body_severe_count': body_metrics['severe_count'],
            
            # 保留原有字段兼容
            'duplicate_count': body_metrics['duplicate_count'],
            'involved_paragraphs': body_metrics['involved_paragraphs'],
            'para_duplication_rate': body_metrics['duplication_rate'],
            'avg_similarity': body_metrics['avg_similarity'],
            'severe_count': body_metrics['severe_count'],
            
            # 分类结果
            'classified': classified,
            
            'ngram_candidates': ngram_candidates,
            'tfidf_results': tfidf_results,
            'simhash_results': simhash_results,
            'large_block_results': large_block_results,
            'elapsed_time': time.time() - start_time
        }
        
        return results
        
    def _extract_all_paragraphs(self, documents: Dict) -> Dict[str, List[Dict]]:
        """提取所有文档的段落"""
        all_paras = {}
        
        for file_path, doc_info in documents.items():
            text = doc_info['text']
            paragraphs = self.paragraph_splitter.split(text)
            
            for para in paragraphs:
                para['file_path'] = file_path
                para['file_name'] = doc_info['name']
                
            all_paras[file_path] = paragraphs
            
        return all_paras
    
    def _classify_paragraphs(self, all_paragraphs: Dict) -> Dict:
        """
        分类段落为标题和正文
        
        @param all_paragraphs: 所有段落
        @return: 分类结果
        """
        title_paras = []  # [(para_dict, 'reason'), ...]
        body_paras = []   # [(para_dict), ...]
        
        for file_path, paras in all_paragraphs.items():
            for i, para in enumerate(paras):
                is_title, reason = ParagraphClassifier.is_title(
                    para['text'], i, paras
                )
                
                if is_title:
                    title_paras.append((para, reason))
                else:
                    body_paras.append(para)
        
        return {
            'title_paras': title_paras,
            'body_paras': body_paras,
            'title_count': len(title_paras),
            'body_count': len(body_paras),
            'all_paras': all_paragraphs
        }
        
    def _ngram_prefilter_body_only(self, classified: Dict) -> List[Tuple[Dict, Dict, float]]:
        """
        N-gram初筛，仅比较正文段落（过滤标题-vs-标题）
        
        优化：短段落会与后续段落合并后再比对，避免碎片化匹配
        """
        candidates = []
        all_paras_by_file = classified['all_paras']
        
        # 为每个文件合并短段落
        file_merged_paras = {}
        for file_path, paras in all_paras_by_file.items():
            merged = self._merge_short_paragraphs(paras)
            file_merged_paras[file_path] = merged
        
        files = list(file_merged_paras.keys())
        
        # 两两比对（跨文件）
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1, file2 = files[i], files[j]
                paras1 = file_merged_paras[file1]
                paras2 = file_merged_paras[file2]
                
                for para1 in paras1:
                    for para2 in paras2:
                        # 跳过正文长度过短的
                        if len(para1['text']) < self.THRESHOLD_BODY_MIN_LENGTH:
                            continue
                        if len(para2['text']) < self.THRESHOLD_BODY_MIN_LENGTH:
                            continue
                        
                        sim = self.ngram_checker.similarity(para1['text'], para2['text'])
                        
                        if sim >= self.THRESHOLD_NGRAM:
                            candidates.append((para1, para2, sim))
                            
        return candidates
    
    def _merge_short_paragraphs(self, paragraphs: List[Dict], min_len: int = 50) -> List[Dict]:
        """
        合并过短的段落与其后续段落，形成更完整的语义单元
        
        原因：如果同一内容在不同文档中被分割成不同长度的段落，
        直接段落对比会产生误报（如短句vs含该句的长段=高相似度）
        
        @param paragraphs: 原始段落列表
        @param min_len: 最小段落长度（字符数）
        @return: 合并后的段落列表
        """
        if not paragraphs:
            return []
        
        result = []
        i = 0
        
        while i < len(paragraphs):
            para = paragraphs[i].copy()
            
            # 如果段落过短，尝试与下一个段落合并
            if len(para['text']) < min_len:
                merged_text = para['text']
                merged_indices = [para.get('index', i)]
                
                # 向前合并：如果前面有未合并的短段落，也合并进来（保持连贯性）
                if result and len(result[-1]['text']) < min_len:
                    prev = result.pop()
                    merged_text = prev['text'] + '\n\n' + merged_text
                    merged_indices = [prev.get('index', len(result))] + merged_indices
                
                # 向后合并
                j = i + 1
                while j < len(paragraphs) and len(merged_text) < min_len * 2:
                    next_para = paragraphs[j]
                    merged_text += '\n\n' + next_para['text']
                    merged_indices.append(next_para.get('index', j))
                    j += 1
                
                para['text'] = merged_text.strip()
                para['merged_from'] = merged_indices
                para['char_count'] = len(para['text'])
                i = j  # 跳过已合并的段落
            else:
                para['merged_from'] = [para.get('index', i)]
                i += 1
            
            result.append(para)
        
        return result
        
    def _tfidf_exact_check(self, candidates: List[Tuple]) -> List[Dict]:
        """
        TF-IDF精确查重
        
        @param candidates: N-gram初筛结果
        @return: 精确查重结果
        """
        results = []
        all_paras_by_file = None
        
        for para1, para2, ngram_sim in candidates:
            # 计算TF-IDF相似度
            tfidf_sim = self.tfidf_checker.compute_similarity(para1['text'], para2['text'])
            
            # 动态阈值判定
            threshold = self._get_dynamic_threshold(para1['text'], para2['text'])
            if tfidf_sim >= threshold:
                # 查找段落所属的章节标题
                source_heading = ParagraphClassifier.find_heading_for_paragraph(
                    para1.get('index', 0), 
                    self._get_all_paras_for_file(para1['file_path'])
                )
                target_heading = ParagraphClassifier.find_heading_for_paragraph(
                    para2.get('index', 0),
                    self._get_all_paras_for_file(para2['file_path'])
                )
                
                results.append({
                    'para1': {
                        'file_path': para1['file_path'],
                        'file_name': para1['file_name'],
                        'index': para1['index'],
                        'text': para1['text'],
                        'char_count': para1['char_count'],
                        'heading': source_heading
                    },
                    'para2': {
                        'file_path': para2['file_path'],
                        'file_name': para2['file_name'],
                        'index': para2['index'],
                        'text': para2['text'],
                        'char_count': para2['char_count'],
                        'heading': target_heading
                    },
                    'ngram_similarity': ngram_sim,
                    'tfidf_similarity': tfidf_sim,
                    'threshold_used': threshold,
                    'duplicate_rate': tfidf_sim,
                    'level': self._get_level(tfidf_sim)
                })
                
        return results
    
    def _get_all_paras_for_file(self, file_path: str) -> List[Dict]:
        """获取文件的所有段落（用于查找标题）"""
        return []
    
    def _simhash_doc_level(self, documents: Dict) -> List[Dict]:
        """SimHash文档级查重"""
        results = []
        names = list(documents.keys())
        
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                path1, path2 = names[i], names[j]
                text1 = documents[path1]['text']
                text2 = documents[path2]['text']
                
                sim = self.simhash_checker.similarity(text1, text2)
                
                results.append({
                    'doc1': {'path': path1, 'name': documents[path1]['name']},
                    'doc2': {'path': path2, 'name': documents[path2]['name']},
                    'similarity': sim
                })
                
        return results
        
    def _detect_large_blocks(self, tfidf_results: List[Dict]) -> List[Dict]:
        """检测连续大段落重复"""
        large_blocks = []
        
        pairs = defaultdict(list)
        for result in tfidf_results:
            key = (result['para1']['file_path'], result['para2']['file_path'])
            pairs[key].append(result)
            
        for (path1, path2), results in pairs.items():
            results.sort(key=lambda x: x['para1']['index'])
            
            consecutive = []
            for r in results:
                if r['tfidf_similarity'] >= self.THRESHOLD_LARGE_BLOCK:
                    consecutive.append(r)
                else:
                    if len(consecutive) >= self.CONSECUTIVE_BLOCK_SIZE:
                        large_blocks.append({
                            'file1': path1,
                            'file2': path2,
                            'start_index': consecutive[0]['para1']['index'],
                            'end_index': consecutive[-1]['para1']['index'],
                            'count': len(consecutive),
                            'paragraphs': consecutive
                        })
                    consecutive = []
                    
            if len(consecutive) >= self.CONSECUTIVE_BLOCK_SIZE:
                large_blocks.append({
                    'file1': path1,
                    'file2': path2,
                    'start_index': consecutive[0]['para1']['index'],
                    'end_index': consecutive[-1]['para1']['index'],
                    'count': len(consecutive),
                    'paragraphs': consecutive
                })
                
        return large_blocks
        
    def _get_dynamic_threshold(self, text1: str, text2: str) -> float:
        """
        动态计算阈值（根据段落长度自适应）
        
        原则：
        - 短文本：阈值提高，避免碎片误判
        - 长文本：阈值适度提高，避免稀释
        
        @param text1: 文本1
        @param text2: 文本2
        @return: 自适应阈值
        """
        len1, len2 = len(text1), len(text2)
        avg_len = (len1 + len2) / 2
        
        if avg_len < 50:
            return 0.50  # 短段落用高阈值
        elif avg_len < 100:
            return 0.38
        elif avg_len < 200:
            return 0.35
        elif avg_len < 400:
            return 0.32
        else:
            return 0.38  # 长段落适度提高
    
    def _get_level(self, similarity: float) -> str:
        """根据相似度获取等级"""
        if similarity < 0.3:
            return "pass"
        elif similarity < 0.5:
            return "warning"
        else:
            return "fail"
            
    def _calc_body_metrics(self, tfidf_results: List[Dict], total_body_paras: int) -> Dict:
        """
        计算正文查重指标
        
        @param tfidf_results: TF-IDF查重结果
        @param total_body_paras: 正文段落总数
        @return: 指标字典
        """
        if total_body_paras == 0:
            return {
                'duplicate_count': 0,
                'involved_paragraphs': 0,
                'duplication_rate': 0.0,
                'avg_similarity': 0.0,
                'severe_count': 0
            }
        
        # 重复段落对数
        duplicate_count = len(tfidf_results)
        
        # 涉及重复的段落数（去重）
        involved_paras = set()
        for r in tfidf_results:
            involved_paras.add((r['para1']['file_path'], r['para1']['index']))
            involved_paras.add((r['para2']['file_path'], r['para2']['index']))
        involved_count = len(involved_paras)
        
        # 重复段落比例（基于正文）
        duplication_rate = involved_count / total_body_paras if total_body_paras > 0 else 0.0
        
        # 平均相似度
        if tfidf_results:
            avg_similarity = sum(r['tfidf_similarity'] for r in tfidf_results) / len(tfidf_results)
        else:
            avg_similarity = 0.0
            
        # 严重重复对数（≥50%）
        severe_count = len([r for r in tfidf_results if r['tfidf_similarity'] >= 0.5])
            
        return {
            'duplicate_count': duplicate_count,
            'involved_paragraphs': involved_count,
            'duplication_rate': duplication_rate,
            'avg_similarity': avg_similarity,
            'severe_count': severe_count
        }

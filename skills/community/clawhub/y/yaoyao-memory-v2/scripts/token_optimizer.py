#!/usr/bin/env python3
"""Token 优化器 - 减少 Token 消耗
功能：
1. 上下文压缩 - 移除冗余信息
2. 批量处理 - 合并多次操作
3. 智能摘要 - 提取关键信息
"""
import re
from typing import List, Dict, Optional

class TokenOptimizer:
    """Token 优化器"""
    
    # 停用词
    STOP_WORDS = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
        '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
        '你', '会', '着', '没有', '哦', '啊', '呢', '吧', '嗯',
        '当然', '其实', '可能', '应该', '可以', '这个', '那个'
    }
    
    # 冗余模式
    REDUNDANT_PATTERNS = [
        r'重复以上内容',
        r'如上所述',
        r'综上所述',
        r'简单来说',
        r'总的来说',
    ]
    
    @classmethod
    def compress(cls, text: str, max_length: int = 500) -> str:
        """压缩文本，移除冗余"""
        if not text:
            return ''
        
        # 去除冗余模式
        for pattern in cls.REDUNDANT_PATTERNS:
            text = re.sub(pattern, '', text)
        
        # 分词
        words = text.split()
        
        # 去除停用词
        meaningful = [w for w in words if w not in cls.STOP_WORDS]
        
        # 重新组合
        compressed = ' '.join(meaningful)
        
        # 截断
        if len(compressed) > max_length:
            compressed = compressed[:max_length] + '...'
        
        return compressed
    
    @classmethod
    def extract_key_info(cls, text: str) -> str:
        """提取关键信息"""
        key_indicators = [
            '决定', '采用', '配置', '偏好', '错误', '修复',
            'token', 'Token', '消耗', '性能', '优化',
            '用户', '系统', '记忆', '搜索'
        ]
        
        for indicator in key_indicators:
            if indicator in text:
                # 提取包含关键词的句子
                sentences = re.split(r'[。!?]', text)
                for sentence in sentences:
                    if indicator in sentence:
                        return sentence.strip()
        
        # 没有关键信息则压缩
        return cls.compress(text, 200)
    
    @classmethod
    def batch_summarize(cls, items: List[str], max_items: int = 5) -> List[str]:
        """批量摘要 - 保留最重要的 N 条"""
        if len(items) <= max_items:
            return items
        
        # 简单的优先级排序
        priority_keywords = ['错误', 'bug', '修复', '决策', '配置', 'token', '优化']
        
        scored = []
        for item in items:
            score = sum(1 for kw in priority_keywords if kw in item.lower())
            scored.append((score, item))
        
        # 按优先级排序，保留 top N
        scored.sort(key=lambda x: -x[0])
        return [item for _, item in scored[:max_items]]
    
    @classmethod
    @classmethod
    def format_compact_report(cls, data: Dict) -> str:
        """紧凑格式报告"""
        lines = []
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f'{key}: {len(value)} items')
            elif isinstance(value, dict):
                lines.append(f'{key}: {len(value)} fields')
            else:
                lines.append(f'{key}: {value}')
        return ' | '.join(lines)


# 批量操作优化器
class BatchOptimizer:
    """批量操作优化器"""
    
    def __init__(self):
        self.queue = []
        self.max_batch_size = 10
        self.max_wait_ms = 100
    
    def add(self, operation: str, *args, **kwargs):
        """添加操作到队列"""
        self.queue.append({
            'op': operation,
            'args': args,
            'kwargs': kwargs
        })
    
    def should_execute(self) -> bool:
        """判断是否应该执行"""
        return len(self.queue) >= self.max_batch_size
    
    def execute_all(self, executor) -> List:
        """执行所有队列中的操作"""
        results = []
        for item in self.queue:
            op = item['op']
            if hasattr(executor, op):
                result = getattr(executor, op)(*item['args'], **item['kwargs'])
                results.append(result)
        self.queue.clear()
        return results


if __name__ == '__main__':
    # 测试
    print('=== Token 优化器测试 ===\n')
    
    text = '这是一个很长的文本需要被压缩因为里面有很多的停用词比如说 的 和 了 还有 在 等等'
    print(f'原文本: {text}')
    print(f'压缩后: {TokenOptimizer.compress(text, 30)}')
    
    print('\n--- 批量摘要 ---')
    items = ['错误日志', '系统配置', '常规日志', '用户偏好', '临时数据', '决策记录', '缓存清理']
    print(f'原始: {items}')
    print(f'摘要: {TokenOptimizer.batch_summarize(items, 3)}')

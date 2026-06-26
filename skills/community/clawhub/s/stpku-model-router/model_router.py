#!/usr/bin/env python3
"""
智能模型路由器
根据任务类型自动选择最佳模型
"""

import json
from pathlib import Path

class ModelRouter:
    """智能模型路由器"""
    
    # 模型能力画像
    MODEL_PROFILES = {
        'qwen3.5-plus': {
            'name': '通义千问 3.5 Plus',
            'strengths': ['general', 'multimodal', 'long-context'],
            'context': 1000000,
            'max_output': 65536,
            'cost_level': 2,
            'speed': 'fast'
        },
        'qwen3-max-2026-01-23': {
            'name': '通义千问 3 Max',
            'strengths': ['reasoning', 'complex-tasks', 'high-quality'],
            'context': 262144,
            'max_output': 65536,
            'cost_level': 4,
            'speed': 'medium'
        },
        'qwen3-coder-next': {
            'name': '通义千问 Coder Next',
            'strengths': ['coding', 'quick-response'],
            'context': 262144,
            'max_output': 65536,
            'cost_level': 1,
            'speed': 'fastest'
        },
        'qwen3-coder-plus': {
            'name': '通义千问 Coder Plus',
            'strengths': ['coding', 'large-project', 'code-review'],
            'context': 1000000,
            'max_output': 65536,
            'cost_level': 2,
            'speed': 'fast'
        },
        'MiniMax-M2.5': {
            'name': 'MiniMax M2.5',
            'strengths': ['long-form-writing', 'creative', 'storytelling'],
            'context': 204800,
            'max_output': 131072,
            'cost_level': 1,
            'speed': 'fast'
        },
        'glm-5': {
            'name': '智谱 GLM-5',
            'strengths': ['chinese', 'knowledge', 'research'],
            'context': 202752,
            'max_output': 16384,
            'cost_level': 2,
            'speed': 'fast'
        },
        'glm-4.7': {
            'name': '智谱 GLM-4.7',
            'strengths': ['quick-qa', 'simple-tasks'],
            'context': 202752,
            'max_output': 16384,
            'cost_level': 1,
            'speed': 'fastest'
        },
        'kimi-k2.5': {
            'name': 'Kimi K2.5',
            'strengths': ['long-document', 'multimodal', 'summarization'],
            'context': 262144,
            'max_output': 32768,
            'cost_level': 2,
            'speed': 'fast'
        }
    }
    
    # 任务类型到模型的映射
    TASK_MODEL_MAP = {
        # 编程任务
        'coding': {
            'quick-fix': 'qwen3-coder-next',
            'new-feature': 'qwen3-coder-plus',
            'code-review': 'qwen3-coder-plus',
            'refactoring': 'qwen3-coder-plus',
            'debug': 'qwen3.5-plus',
            'documentation': 'qwen3-coder-next',
            'test': 'qwen3-coder-next'
        },
        # 写作任务
        'writing': {
            'short-content': 'glm-4.7',
            'long-article': 'MiniMax-M2.5',
            'technical-doc': 'qwen3.5-plus',
            'creative-writing': 'MiniMax-M2.5',
            'email': 'glm-4.7',
            'report': 'qwen3.5-plus',
            'script': 'kimi-k2.5'
        },
        # 分析任务
        'analysis': {
            'simple-qa': 'glm-4.7',
            'complex-reasoning': 'qwen3-max-2026-01-23',
            'data-analysis': 'qwen3.5-plus',
            'research': 'glm-5',
            'comparison': 'glm-5'
        },
        # 多模态任务
        'multimodal': {
            'image-understanding': 'qwen3.5-plus',
            'document-ocr': 'kimi-k2.5',
            'chart-analysis': 'qwen3.5-plus',
            'diagram': 'qwen3.5-plus'
        },
        # 长上下文任务
        'long-context': {
            'book-summary': 'qwen3-coder-plus',
            'legal-doc': 'qwen3.5-plus',
            'meeting-notes': 'MiniMax-M2.5',
            'transcript': 'kimi-k2.5'
        }
    }
    
    def __init__(self, config_path='/home/skyswind/.openclaw/openclaw.json'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def select(self, task_type, task_subtype=None, content_length=0, quality='balanced'):
        """
        智能选择模型
        
        Args:
            task_type: 任务类型 (coding/writing/analysis/multimodal/long-context)
            task_subtype: 任务子类型 (如 quick-fix/new-feature 等)
            content_length: 输入内容长度（字符数）
            quality: 质量要求 (economy/balanced/premium)
        
        Returns:
            str: 推荐的模型 ID
        """
        # 1. 根据任务类型选择
        if task_type in self.TASK_MODEL_MAP:
            if task_subtype and task_subtype in self.TASK_MODEL_MAP[task_type]:
                model = self.TASK_MODEL_MAP[task_type][task_subtype]
                return f'bailian/{model}'
        
        # 2. 根据内容长度选择
        if content_length > 500000:  # 超长文本
            return 'bailian/qwen3.5-plus'
        elif content_length > 100000:  # 长文本
            return 'bailian/kimi-k2.5'
        
        # 3. 根据质量要求选择
        if quality == 'economy':
            return 'bailian/glm-4.7'
        elif quality == 'premium':
            return 'bailian/qwen3-max-2026-01-23'
        
        # 4. 默认选择
        return 'bailian/qwen3.5-plus'
    
    def get_model_info(self, model_id):
        """获取模型详细信息"""
        # 移除 provider 前缀
        model_name = model_id.replace('bailian/', '')
        return self.MODEL_PROFILES.get(model_name, {})
    
    def list_available_models(self):
        """列出所有可用模型"""
        return list(self.MODEL_PROFILES.keys())
    
    def get_agent_model(self, agent_id):
        """获取指定 Agent 的默认模型"""
        agents = self.config.get('agents', {}).get('list', [])
        for agent in agents:
            if agent.get('id') == agent_id:
                if 'model' in agent:
                    return agent['model'].get('primary', 'bailian/qwen3.5-plus')
        return 'bailian/qwen3.5-plus'
    
    def explain_choice(self, model_id, task_type, task_subtype):
        """解释为什么选择这个模型"""
        model_info = self.get_model_info(model_id)
        if not model_info:
            return "未知模型"
        
        explanation = []
        explanation.append(f"🎯 选择 {model_info['name']}")
        explanation.append(f"\n**优势领域**: {', '.join(model_info['strengths'])}")
        explanation.append(f"**上下文窗口**: {model_info['context']:,} tokens")
        explanation.append(f"**最大输出**: {model_info['max_output']:,} tokens")
        explanation.append(f"**速度**: {model_info['speed']}")
        explanation.append(f"**成本等级**: {'💰' * model_info['cost_level']}")
        
        if task_type and task_subtype:
            explanation.append(f"\n**适合任务**: {task_type} → {task_subtype}")
        
        return '\n'.join(explanation)

# 命令行工具
if __name__ == '__main__':
    import sys
    
    router = ModelRouter()
    
    if len(sys.argv) < 2:
        print("用法：python model_router.py <task_type> [task_subtype] [content_length] [quality]")
        print("\n示例:")
        print("  python model_router.py coding quick-fix")
        print("  python model_router.py writing long-article 50000")
        print("  python model_router.py analysis complex-reasoning 0 premium")
        sys.exit(1)
    
    task_type = sys.argv[1]
    task_subtype = sys.argv[2] if len(sys.argv) > 2 else None
    content_length = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 0
    quality = sys.argv[4] if len(sys.argv) > 4 else 'balanced'
    
    model = router.select(task_type, task_subtype, content_length, quality)
    print(f"推荐模型：{model}")
    print()
    print(router.explain_choice(model, task_type, task_subtype))

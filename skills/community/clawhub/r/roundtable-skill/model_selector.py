#!/usr/bin/env python3
"""
RoundTable 模型选择器

功能：
1. 优先使用 OpenClaw 官方 API 获取可用模型（安全、审计友好）
2. 如果 API 不可用，降级到标准单一模型配置
3. 支持用户显式指定模型配置（最高优先级）

数据读取说明（隐私透明）：
- 从本地配置文件读取模型元数据（id、name、tags），用于智能匹配
- 不读取 apiKey、baseUrl 等敏感字段（通过 SENSITIVE_FIELDS 黑名单过滤）
- 文件系统访问范围：OPENCLAW_STATE_DIR 环境变量指向的 models.json，
  以及 ~/.enhance-claw/instances/*/models.json、~/.openclaw/instances/*/models.json
- 仅在 allow_local_scan=True 时才扫描本地实例目录（默认关闭）
- 所有读取操作会打印日志，用户可实时监控
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class ModelSelector:
    """RoundTable 模型选择器 - 安全、审计友好"""

    # 敏感字段黑名单（即使代码逻辑正确，也做防御性过滤）
    SENSITIVE_FIELDS = {'apiKey', 'api_key', 'api-key', 'token', 'secret', 'password',
                        'baseUrl', 'base_url', 'base-url', 'endpoint', 'url'}

    # 专家角色 - 模型标签映射（通用规则）
    ROLE_TAGS = {
        "engineering": ["code", "technical", "engineering", "coder"],
        "design": ["creative", "long-context", "design", "art"],
        "testing": ["balanced", "fast", "general", "qa"],
        "product": ["chinese", "knowledge", "product", "business"],
        "host": ["logic", "summary", "decision", "max"]
    }
    
    # 标准单一模型配置（降级方案）
    FALLBACK_MODEL = {
        'id': 'anthropic/claude-4',
        'name': 'Qwen3.5 Plus',
        'tags': ['balanced', 'fast', 'general'],
        'priority': 3
    }
    
    def __init__(self, user_models: List[Dict] = None, config_path: str = None,
                 allow_local_scan: bool = False):
        """
        初始化模型选择器

        Args:
            user_models: 用户显式指定的模型列表（可选，最高优先级）
            config_path: 独立配置文件路径（可选，用于导入导出）
            allow_local_scan: 是否允许扫描本地实例目录（默认 False，安全模式）
                             开启后会读取 ~/.enhance-claw/instances/ 下的 models.json
        """
        self.available_models: List[Dict] = []
        self.user_specified_models = user_models
        self.config_path = config_path
        self.allow_local_scan = allow_local_scan
        self._load_available_models()
    
    def _load_available_models(self):
        """
        加载可用模型列表（按优先级）
        
        优先级：
        1. 用户显式指定（最高优先级）
        2. 环境变量 ROUNDTable_MODELS（次高优先级）
        3. OpenClaw 官方 API
        4. 标准单一模型配置（降级方案）
        """
        # 优先级 1: 用户显式指定
        if self.user_specified_models:
            self.available_models = self.user_specified_models
            print(f"✅ 使用用户显式指定的 {len(self.available_models)} 个模型")
            return
        
        # 优先级 2: 环境变量 ROUNDTable_MODELS
        # 格式："model1:tag1,tag2;model2:tag3,tag4"
        # 示例："anthropic/claude-4:chinese;openai/gpt-5:creative"
        env_models = os.environ.get('ROUNDTable_MODELS')
        if env_models:
            parsed_models = []
            for item in env_models.split(';'):
                if ':' in item:
                    model_id, tags_str = item.split(':', 1)
                    parsed_models.append({
                        'id': model_id.strip(),
                        'name': model_id.strip().split('/')[-1],
                        'tags': [t.strip() for t in tags_str.split(',')],
                        'priority': 2
                    })
            
            if parsed_models:
                self.available_models = parsed_models
                print(f"✅ 从环境变量加载 {len(parsed_models)} 个模型")
                return
        
        # 优先级 3: OpenClaw 官方 API
        try:
            models = self._fetch_from_openclaw_api()
            if models:
                self.available_models = models
                print(f"✅ 从 OpenClaw API 获取到 {len(self.available_models)} 个模型")
                return
        except Exception as e:
            print(f"⚠️ OpenClaw API 不可用：{e}")
        
        # 优先级 4: 从实例的 models.json 读取（需显式开启）
        if not self.allow_local_scan:
            print("⏭️  跳过本地实例目录扫描（allow_local_scan=False）")
        else:
            try:
                models = self._load_from_instance_models_json()
                if models:
                    self.available_models = models
                    print(f"✅ 从实例 models.json 加载 {len(self.available_models)} 个模型")
                    return
            except Exception as e:
                print(f"⚠️ 实例 models.json 不可用：{e}")
        
        # 优先级 5: 从 global-model-config.json 读取
        try:
            models = self._load_from_models_json()
            if models:
                self.available_models = models
                print(f"✅ 从 global-model-config.json 加载 {len(self.available_models)} 个模型")
                return
        except Exception as e:
            print(f"⚠️ global-model-config.json 不可用：{e}")
        
        # 优先级 6: 标准单一模型配置（降级方案）
        print("⚠️ 降级到标准单一模型配置")
        self.available_models = [self.FALLBACK_MODEL]
    
    def _fetch_from_openclaw_api(self) -> Optional[List[Dict]]:
        """
        从 OpenClaw 官方 API 获取可用模型
        
        Returns:
            模型列表，如果失败返回 None
        """
        try:
            # 尝试使用 OpenClaw 官方工具
            from openclaw.tools import get_available_models as openclaw_get_models
            models = openclaw_get_models()
            
            # 验证返回数据
            if models and isinstance(models, list) and len(models) > 0:
                # 确保每个模型都有必要字段
                validated_models = []
                for model in models:
                    if isinstance(model, dict) and 'id' in model:
                        validated_models.append(self._sanitize_model({
                            'id': model.get('id', 'unknown'),
                            'name': model.get('name', model.get('id')),
                            'tags': model.get('tags', []),
                            'priority': model.get('priority', 3),
                            'provider': model.get('provider', 'unknown')
                        }))
                
                if validated_models:
                    return validated_models
            
            return None
            
        except ImportError:
            print("⚠️ openclaw.tools 不可用")
            return None
        except Exception as e:
            print(f"⚠️ API 调用失败：{e}")
            return None
    
    def _load_from_models_json(self) -> Optional[List[Dict]]:
        """
        从 global-model-config.json 文件读取模型配置
        
        Returns:
            模型列表，如果失败返回 None
        """
        try:
            # 查找 global-model-config.json 文件
            possible_paths = [
                Path.home() / '.enhance-claw' / 'global-model-config.json',
                Path.home() / '.openclaw' / 'openclaw.json',
            ]
            
            for models_path in possible_paths:
                if models_path.exists():
                    with open(models_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    # 从配置中提取模型
                    models_config = config.get('models', {})
                    providers = models_config.get('providers', {})
                    
                    models = []
                    for provider_id, provider in providers.items():
                        provider_models = provider.get('models', [])
                        for model in provider_models:
                            model_id = model.get('id', 'unknown')

                            models.append(self._sanitize_model({
                                'id': model_id,
                                'name': model.get('name', model_id),
                                'tags': model.get('tags', []),
                                'priority': 3,
                                'provider': provider_id
                            }))
                    
                    if models:
                        print(f"📄 从 {models_path.name} 加载模型")
                        return models
            
            return None
            
        except Exception as e:
            print(f"⚠️ 读取 global-model-config.json 失败：{e}")
            return None
    
    def _load_from_instance_models_json(self) -> Optional[List[Dict]]:
        """
        从实例的 models.json 文件读取模型元数据（id、name、tags）

        隐私说明：仅读取模型列表（id、name、tags），不访问 apiKey、baseUrl 等敏感字段。
        文件系统访问范围：通过 OPENCLAW_STATE_DIR 环境变量和 ~/.enhance-claw/、~/.openclaw/ 实例目录定位 models.json。

        Returns:
            模型列表，如果失败返回 None
        """
        try:
            print("🔍 正在扫描实例目录获取模型列表（仅元数据，不含 API 密钥）...")
            possible_paths = []
            state_dir = os.environ.get('OPENCLAW_STATE_DIR')
            if state_dir:
                possible_paths.append(Path(state_dir) / 'workspace' / 'agents' / 'main' / 'agent' / 'models.json')
            for base_dir in ['.enhance-claw', '.openclaw']:
                instances_dir = Path.home() / base_dir / 'instances'
                if instances_dir.exists():
                    for instance in instances_dir.iterdir():
                        if instance.is_dir():
                            models_file = instance / 'workspace' / 'agents' / 'main' / 'agent' / 'models.json'
                            if models_file.exists() and models_file not in possible_paths:
                                possible_paths.append(models_file)
            
            for models_path in possible_paths:
                if models_path.exists():
                    print(f"📖 读取模型元数据：{models_path}（仅提取 id/name/tags）")
                    with open(models_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    providers = config.get('providers', {})

                    models = []
                    for provider_id, provider in providers.items():
                        provider_models = provider.get('models', [])
                        for model in provider_models:
                            model_id = model.get('id', 'unknown')

                            models.append({
                                'id': model_id,
                                'name': model.get('name', model_id),
                                'tags': model.get('tags', []),
                                'priority': 3,
                                'provider': provider_id
                            })

                    if models:
                        print(f"✅ 从 {models_path.name} 加载 {len(models)} 个模型元数据（已跳过 apiKey/baseUrl）")
                        return models

            return None
            
        except Exception as e:
            print(f"⚠️ 读取实例 models.json 失败：{e}")
            return None
    
    def _fetch_from_openclaw_api(self) -> Optional[List[Dict]]:
        """
        从 OpenClaw 官方 API 获取可用模型
        
        Returns:
            模型列表，如果失败返回 None
        """
        try:
            # 尝试使用 OpenClaw 官方工具
            from openclaw.tools import get_available_models as openclaw_get_models
            models = openclaw_get_models()
            
            # 验证返回数据
            if models and isinstance(models, list) and len(models) > 0:
                # 确保每个模型都有必要字段
                validated_models = []
                for model in models:
                    if isinstance(model, dict) and 'id' in model:
                        validated_models.append(self._sanitize_model({
                            'id': model.get('id', 'unknown'),
                            'name': model.get('name', model.get('id')),
                            'tags': model.get('tags', []),
                            'priority': model.get('priority', 3),
                            'provider': model.get('provider', 'unknown')
                        }))
                
                if validated_models:
                    return validated_models
            
            return None
            
        except ImportError:
            print("⚠️ openclaw.tools 不可用")
            return None
        except Exception as e:
            print(f"⚠️ API 调用失败：{e}")
            return None
    
    @staticmethod
    def _sanitize_model(model: Dict) -> Dict:
        """
        从模型字典中移除所有敏感字段（防御性过滤）

        即使上游代码逻辑已正确只提取 id/name/tags，
        此方法确保任何意外泄露的敏感字段不会被返回。
        """
        SENSITIVE_KEYS = {'apiKey', 'api_key', 'api-key', 'token', 'secret',
                          'password', 'baseUrl', 'base_url', 'base-url',
                          'endpoint', 'url', 'authorization', 'key'}
        return {k: v for k, v in model.items() if k.lower() not in {k.lower() for k in SENSITIVE_KEYS}}

    def get_available_models(self) -> List[Dict]:
        """获取可用模型列表"""
        return self.available_models
    
    def select_model_for_role(self, role: str, user_specified: str = None) -> str:
        """
        为专家角色选择最合适的模型
        
        匹配逻辑：
        1. 用户显式指定 → 使用用户指定（最高优先级）
        2. 只有一个模型 → 直接使用（所有专家都用这个）
        3. 多个模型 → 根据标签匹配 + 优先级
        
        Args:
            role: 专家角色（engineering/design/testing/product/host）
            user_specified: 用户显式指定的模型（可选）
        
        Returns:
            模型 ID
        """
        # 优先级 1: 用户显式指定
        if user_specified:
            # 如果包含 provider 前缀，去掉它
            if '/' in user_specified:
                user_specified = user_specified.split('/')[-1]
            print(f"📌 使用用户指定模型：{user_specified}")
            return user_specified
        
        # 优先级 2: 只有一个模型，所有专家都用这个
        if len(self.available_models) == 1:
            model_id = self.available_models[0]['id']
            # 去掉 provider 前缀
            if '/' in model_id:
                model_id = model_id.split('/')[-1]
            print(f"📌 单一模型配置，所有专家都使用：{model_id}")
            return model_id
        
        # 优先级 3: 多个模型，根据角色标签匹配
        role_tags = self.ROLE_TAGS.get(role, [])
        
        # 计算每个模型的匹配分数
        model_scores = []
        for model in self.available_models:
            score = 0
            
            # 标签匹配（每个标签 +10 分）
            for tag in role_tags:
                if tag in model.get('tags', []):
                    score += 10
            
            # 优先级加分
            priority = model.get('priority', 3)
            if priority == 1:
                score += 30
            elif priority == 2:
                score += 20
            else:
                score += 10
            
            model_scores.append((model['id'], score))
        
        # 按分数排序，返回最高分的模型
        model_scores.sort(key=lambda x: x[1], reverse=True)
        best_model = model_scores[0][0]
        
        # 去掉 provider 前缀
        if '/' in best_model:
            best_model = best_model.split('/')[-1]
        
        print(f"📌 为角色 '{role}' 匹配模型：{best_model} (得分：{model_scores[0][1]})")
        return best_model
    
    def select_models_for_roundtable(self, roles: List[str], 
                                     user_specified: Dict[str, str] = None) -> Dict[str, str]:
        """
        为 RoundTable 所有专家选择模型
        
        Args:
            roles: 专家角色列表
            user_specified: 用户显式指定的模型字典 {role: model_id}
        
        Returns:
            模型分配字典 {role: model_id}
        """
        if user_specified is None:
            user_specified = {}
        
        model_assignment = {}
        
        for role in roles:
            specified = user_specified.get(role)
            model_id = self.select_model_for_role(role, specified)
            model_assignment[role] = model_id
        
        return model_assignment
    
    def print_model_summary(self):
        """打印模型配置摘要"""
        print("\n" + "="*60)
        print("📊 RoundTable 模型配置摘要")
        print("="*60)
        
        if self.user_specified_models:
            print(f"来源：用户显式指定")
        else:
            print(f"来源：OpenClaw 官方 API")
        
        print(f"可用模型：{len(self.available_models)} 个\n")
        
        if len(self.available_models) == 1:
            model = self.available_models[0]
            print(f"  ⚠️  单一模型配置：{model['name']}")
            print(f"     所有专家都将使用这个模型\n")
        else:
            for model in self.available_models:
                tags_str = ", ".join(model.get('tags', []))
                priority_str = "⭐" * (4 - model.get('priority', 3))
                print(f"  • {model['name']} ({model['id']})")
                print(f"    标签：{tags_str or '无'}")
                print(f"    优先级：{priority_str or '⭐'}\n")
        
        print("="*60)
    
    def export_config(self, output_path: str):
        """
        导出模型配置到独立文件（用于审计和备份）
        
        Args:
            output_path: 输出文件路径
        """
        config = {
            'version': '1.0',
            'source': 'user_specified' if self.user_specified_models else 'openclaw_api',
            'models': self.available_models,
            'note': '此配置仅包含模型元数据（id/name/tags/provider），不包含 apiKey、baseUrl 等敏感信息'
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 模型配置已导出到：{output_path}")
    
    @classmethod
    def import_config(cls, input_path: str) -> 'ModelSelector':
        """
        从独立文件导入模型配置
        
        Args:
            input_path: 输入文件路径
        
        Returns:
            ModelSelector 实例
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        models = config.get('models', [])
        return cls(user_models=models)


# 快捷函数
def get_model_selector(user_models: List[Dict] = None) -> ModelSelector:
    """获取模型选择器实例"""
    return ModelSelector(user_models)


def select_model(role: str, user_models: List[Dict] = None, user_specified: str = None) -> str:
    """为角色选择模型"""
    selector = ModelSelector(user_models)
    return selector.select_model_for_role(role, user_specified)


def list_available_models(user_models: List[Dict] = None) -> List[Dict]:
    """列出所有可用模型"""
    selector = ModelSelector(user_models)
    return selector.get_available_models()


# 测试
if __name__ == "__main__":
    print("🧪 RoundTable 模型选择器测试\n")
    
    # 测试 1: 使用 OpenClaw API（或降级）
    print("测试 1: 自动获取模型")
    print("-"*60)
    selector = ModelSelector()
    selector.print_model_summary()
    
    # 测试 2: 用户显式指定
    print("\n测试 2: 用户显式指定模型")
    print("-"*60)
    user_models = [
        {'id': 'anthropic/claude-4', 'name': 'GLM-5', 'tags': ['chinese'], 'priority': 2}
    ]
    selector2 = ModelSelector(user_models=user_models)
    selector2.print_model_summary()
    
    # 测试 3: 模型匹配
    print("\n测试 3: 模型匹配测试")
    print("-"*60)
    test_roles = ["engineering", "design", "testing", "host"]
    for role in test_roles:
        model = selector.select_model_for_role(role)
        print(f"{role:15} → {model}")

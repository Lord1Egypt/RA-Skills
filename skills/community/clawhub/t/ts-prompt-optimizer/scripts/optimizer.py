#!/usr/bin/env python3
"""
TS-Prompt-Optimizer [EMOJI:6838][EMOJI:5FC3][EMOJI:4F18][EMOJI:5316][EMOJI:5F15][EMOJI:64CE]
[EMOJI:51AC][EMOJI:51AC][EMOJI:4E3B][EMOJI:4EBA][EMOJI:5B9A][EMOJI:5236][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD][EMOJI:4F18][EMOJI:5316][EMOJI:5668]
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class TSPromptOptimizer:
    """[EMOJI:51AC][EMOJI:51AC][EMOJI:4E3B][EMOJI:4EBA][EMOJI:5B9A][EMOJI:5236][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD][EMOJI:4F18][EMOJI:5316][EMOJI:5668]"""
    
    def __init__(self, config_dir: str = None):
        # [EMOJI:8BBE][EMOJI:7F6E][EMOJI:8DEF][EMOJI:5F84]
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = Path(config_dir) if config_dir else self.base_dir / "config"
        self.memory_dir = self.base_dir / "memory"
        
        # [EMOJI:786E][EMOJI:4FDD][EMOJI:76EE][EMOJI:5F55][EMOJI:5B58][EMOJI:5728]
        self.memory_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        
        # [EMOJI:52A0][EMOJI:8F7D][EMOJI:914D][EMOJI:7F6E] - [EMOJI:4F7F][EMOJI:7528][EMOJI:65B0][EMOJI:7684][EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF]
        self.dongdong_rules = self._load_config("dongdong_rules.json")
        
        # [EMOJI:521D][EMOJI:59CB][EMOJI:5316][EMOJI:914D][EMOJI:7F6E][EMOJI:7BA1][EMOJI:7406][EMOJI:5668]
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            from config_manager import TSConfigManager
            self.config_manager = TSConfigManager()
            self.model_config = self.config_manager.load_config()
        except ImportError as e:
            print(f"[EMOJI:8B66][EMOJI:544A][EMOJI:FF1A][EMOJI:65E0][EMOJI:6CD5][EMOJI:5BFC][EMOJI:5165][EMOJI:914D][EMOJI:7F6E][EMOJI:7BA1][EMOJI:7406][EMOJI:5668][EMOJI:FF0C][EMOJI:4F7F][EMOJI:7528][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E]: {e}")
            self.model_config = self._load_config("model_config.json")
            self.config_manager = None
        
        # [EMOJI:521D][EMOJI:59CB][EMOJI:5316][EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55]
        self.history_file = self.memory_dir / "optimization_history.md"
        self.preferences_file = self.memory_dir / "preferences.md"
        
        # [EMOJI:4F18][EMOJI:5316][EMOJI:89C4][EMOJI:5219]
        self.optimization_rules = self._init_optimization_rules()
        
    def _load_config(self, filename: str) -> Dict:
        """[EMOJI:52A0][EMOJI:8F7D][EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6]"""
        config_file = self.config_dir / filename
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[EMOJI:8B66][EMOJI:544A][EMOJI:FF1A][EMOJI:52A0][EMOJI:8F7D][EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6] {filename} [EMOJI:5931][EMOJI:8D25]: {e}")
        
        # [EMOJI:8FD4][EMOJI:56DE][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E]
        return self._get_default_config(filename)
    
    def _get_default_config(self, filename: str) -> Dict:
        """[EMOJI:83B7][EMOJI:53D6][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E]"""
        if filename == "dongdong_rules.json":
            return {
                "preferred_roles": {
                    "technical": "[EMOJI:8D44][EMOJI:6DF1][EMOJI:5168][EMOJI:6808][EMOJI:5DE5][EMOJI:7A0B][EMOJI:5E08]",
                    "writing": "[EMOJI:4E13][EMOJI:4E1A][EMOJI:6587][EMOJI:6848][EMOJI:7B56][EMOJI:5212][EMOJI:5E08]", 
                    "analysis": "[EMOJI:6570][EMOJI:636E][EMOJI:5206][EMOJI:6790][EMOJI:4E13][EMOJI:5BB6]",
                    "creative": "[EMOJI:521B][EMOJI:610F][EMOJI:7B56][EMOJI:5212][EMOJI:4E13][EMOJI:5BB6]",
                    "general": "[EMOJI:8D44][EMOJI:6DF1]AI[EMOJI:52A9][EMOJI:624B][EMOJI:4E13][EMOJI:5BB6]"
                },
                "output_formats": {
                    "code": "[EMOJI:5B8C][EMOJI:6574][EMOJI:53EF][EMOJI:8FD0][EMOJI:884C][EMOJI:4EE3][EMOJI:7801] + [EMOJI:8BE6][EMOJI:7EC6][EMOJI:6CE8][EMOJI:91CA] + [EMOJI:4F7F][EMOJI:7528][EMOJI:8BF4][EMOJI:660E]",
                    "report": "Markdown[EMOJI:683C][EMOJI:5F0F] + [EMOJI:6E05][EMOJI:6670][EMOJI:7ED3][EMOJI:6784] + [EMOJI:6570][EMOJI:636E][EMOJI:53EF][EMOJI:89C6][EMOJI:5316]",
                    "email": "[EMOJI:6B63][EMOJI:5F0F][EMOJI:5546][EMOJI:52A1][EMOJI:90AE][EMOJI:4EF6][EMOJI:683C][EMOJI:5F0F]",
                    "document": "[EMOJI:7ED3][EMOJI:6784][EMOJI:5316][EMOJI:6587][EMOJI:6863] + [EMOJI:7AE0][EMOJI:8282][EMOJI:5212][EMOJI:5206]",
                    "analysis": "[EMOJI:6570][EMOJI:636E][EMOJI:8868][EMOJI:683C] + [EMOJI:7ED3][EMOJI:8BBA][EMOJI:603B][EMOJI:7ED3] + [EMOJI:5EFA][EMOJI:8BAE]"
                },
                "quality_constraints": {
                    "default_word_count": 500,
                    "preferred_tech_stack": ["Python", "JavaScript", "React", "Node.js"],
                    "writing_style": "[EMOJI:4E13][EMOJI:4E1A][EMOJI:3001][EMOJI:7B80][EMOJI:6D01][EMOJI:3001][EMOJI:5B9E][EMOJI:7528][EMOJI:3001][EMOJI:51C6][EMOJI:786E]",
                    "code_style": "[EMOJI:7B26][EMOJI:5408]PEP 8[EMOJI:89C4][EMOJI:8303][EMOJI:FF0C][EMOJI:6709][EMOJI:5B8C][EMOJI:6574][EMOJI:6CE8][EMOJI:91CA]"
                },
                "optimization_levels": {
                    "minimal": ["[EMOJI:89D2][EMOJI:8272][EMOJI:5B9A][EMOJI:4E49]", "[EMOJI:4EFB][EMOJI:52A1][EMOJI:6F84][EMOJI:6E05]"],
                    "standard": ["[EMOJI:89D2][EMOJI:8272][EMOJI:5B9A][EMOJI:4E49]", "[EMOJI:4EFB][EMOJI:52A1][EMOJI:6F84][EMOJI:6E05]", "[EMOJI:8F93][EMOJI:51FA][EMOJI:683C][EMOJI:5F0F]", "[EMOJI:8D28][EMOJI:91CF][EMOJI:7EA6][EMOJI:675F]"],
                    "full": ["[EMOJI:89D2][EMOJI:8272][EMOJI:5B9A][EMOJI:4E49]", "[EMOJI:4EFB][EMOJI:52A1][EMOJI:6F84][EMOJI:6E05]", "[EMOJI:4E0A][EMOJI:4E0B][EMOJI:6587][EMOJI:8865][EMOJI:5145]", "[EMOJI:8F93][EMOJI:51FA][EMOJI:683C][EMOJI:5F0F]", "[EMOJI:8D28][EMOJI:91CF][EMOJI:7EA6][EMOJI:675F]", "[EMOJI:793A][EMOJI:4F8B][EMOJI:53C2][EMOJI:8003]"]
                }
            }
        elif filename == "model_config.json":
            return {
                "optimization_models": {
                    "simple": "deepseek/deepseek-chat",
                    "complex": "bailian/qwen3.5-plus", 
                    "technical": "bailian/qwen3-coder-next",
                    "creative": "bailian/qwen3.5-plus",
                    "analysis": "bailian/qwen3.5-plus"
                },
                "routing_strategy": "cost_effective",
                "fallback_model": "deepseek/deepseek-chat",
                "cost_priority": True
            }
        return {}
    
    def _init_optimization_rules(self) -> Dict:
        """[EMOJI:521D][EMOJI:59CB][EMOJI:5316][EMOJI:4F18][EMOJI:5316][EMOJI:89C4][EMOJI:5219]"""
        return {
            "technical": {
                "role": self.dongdong_rules.get("preferred_roles", {}).get("technical", "[EMOJI:8D44][EMOJI:6DF1][EMOJI:5168][EMOJI:6808][EMOJI:5DE5][EMOJI:7A0B][EMOJI:5E08]"),
                "format": self.dongdong_rules.get("output_formats", {}).get("code", "[EMOJI:5B8C][EMOJI:6574][EMOJI:4EE3][EMOJI:7801]"),
                "constraints": ["[EMOJI:4EE3][EMOJI:7801][EMOJI:8D28][EMOJI:91CF]", "[EMOJI:6027][EMOJI:80FD][EMOJI:4F18][EMOJI:5316]", "[EMOJI:53EF][EMOJI:7EF4][EMOJI:62A4][EMOJI:6027]"]
            },
            "writing": {
                "role": self.dongdong_rules.get("preferred_roles", {}).get("writing", "[EMOJI:4E13][EMOJI:4E1A][EMOJI:6587][EMOJI:6848][EMOJI:7B56][EMOJI:5212][EMOJI:5E08]"),
                "format": self.dongdong_rules.get("output_formats", {}).get("document", "[EMOJI:7ED3][EMOJI:6784][EMOJI:5316][EMOJI:6587][EMOJI:6863]"),
                "constraints": ["[EMOJI:6587][EMOJI:98CE][EMOJI:4E00][EMOJI:81F4]", "[EMOJI:903B][EMOJI:8F91][EMOJI:6E05][EMOJI:6670]", "[EMOJI:76EE][EMOJI:6807][EMOJI:660E][EMOJI:786E]"]
            },
            "analysis": {
                "role": self.dongdong_rules.get("preferred_roles", {}).get("analysis", "[EMOJI:6570][EMOJI:636E][EMOJI:5206][EMOJI:6790][EMOJI:4E13][EMOJI:5BB6]"),
                "format": self.dongdong_rules.get("output_formats", {}).get("analysis", "[EMOJI:6570][EMOJI:636E][EMOJI:5206][EMOJI:6790][EMOJI:62A5][EMOJI:544A]"),
                "constraints": ["[EMOJI:6570][EMOJI:636E][EMOJI:51C6][EMOJI:786E]", "[EMOJI:7ED3][EMOJI:8BBA][EMOJI:53EF][EMOJI:9760]", "[EMOJI:5EFA][EMOJI:8BAE][EMOJI:53EF][EMOJI:884C]"]
            },
            "creative": {
                "role": self.dongdong_rules.get("preferred_roles", {}).get("creative", "[EMOJI:521B][EMOJI:610F][EMOJI:7B56][EMOJI:5212][EMOJI:4E13][EMOJI:5BB6]"),
                "format": self.dongdong_rules.get("output_formats", {}).get("document", "[EMOJI:521B][EMOJI:610F][EMOJI:5185][EMOJI:5BB9]"),
                "constraints": ["[EMOJI:521B][EMOJI:610F][EMOJI:65B0][EMOJI:9896]", "[EMOJI:8868][EMOJI:8FBE][EMOJI:751F][EMOJI:52A8]", "[EMOJI:60C5][EMOJI:611F][EMOJI:5171][EMOJI:9E23]"]
            },
            "general": {
                "role": self.dongdong_rules.get("preferred_roles", {}).get("general", "[EMOJI:8D44][EMOJI:6DF1]AI[EMOJI:52A9][EMOJI:624B][EMOJI:4E13][EMOJI:5BB6]"),
                "format": "[EMOJI:6E05][EMOJI:6670][EMOJI:660E][EMOJI:786E][EMOJI:7684][EMOJI:56DE][EMOJI:7B54]",
                "constraints": ["[EMOJI:51C6][EMOJI:786E]", "[EMOJI:6709][EMOJI:7528]", "[EMOJI:7B80][EMOJI:6D01]"]
            }
        }
    
    def detect_task_type(self, user_input: str) -> str:
        """[EMOJI:68C0][EMOJI:6D4B][EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]"""
        input_lower = user_input.lower()
        
        # [EMOJI:6280][EMOJI:672F][EMOJI:4EFB][EMOJI:52A1][EMOJI:5173][EMOJI:952E][EMOJI:8BCD]
        technical_keywords = ["[EMOJI:4EE3][EMOJI:7801]", "[EMOJI:7F16][EMOJI:7A0B]", "[EMOJI:811A][EMOJI:672C]", "[EMOJI:51FD][EMOJI:6570]", "[EMOJI:7B97][EMOJI:6CD5]", "[EMOJI:5F00][EMOJI:53D1]", "[EMOJI:6280][EMOJI:672F]", "python", "java", "javascript", "html", "css", "[EMOJI:6570][EMOJI:636E][EMOJI:5E93]", "api"]
        writing_keywords = ["[EMOJI:5199]", "[EMOJI:6587][EMOJI:7AE0]", "[EMOJI:62A5][EMOJI:544A]", "[EMOJI:90AE][EMOJI:4EF6]", "[EMOJI:6587][EMOJI:6863]", "[EMOJI:6587][EMOJI:6848]", "[EMOJI:5185][EMOJI:5BB9]", "[EMOJI:5199][EMOJI:4F5C]", "[EMOJI:7F16][EMOJI:8F91]"]
        analysis_keywords = ["[EMOJI:5206][EMOJI:6790]", "[EMOJI:7EDF][EMOJI:8BA1]", "[EMOJI:6570][EMOJI:636E]", "[EMOJI:56FE][EMOJI:8868]", "[EMOJI:62A5][EMOJI:544A]", "[EMOJI:7814][EMOJI:7A76]", "[EMOJI:8BC4][EMOJI:4F30]", "[EMOJI:603B][EMOJI:7ED3]"]
        creative_keywords = ["[EMOJI:521B][EMOJI:610F]", "[EMOJI:6545][EMOJI:4E8B]", "[EMOJI:8BBE][EMOJI:8BA1]", "[EMOJI:7B56][EMOJI:5212]", "[EMOJI:65B9][EMOJI:6848]", "[EMOJI:60F3][EMOJI:6CD5]", "[EMOJI:7075][EMOJI:611F]", "[EMOJI:8111][EMOJI:6D1E]"]
        
        # [EMOJI:68C0][EMOJI:6D4B][EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]
        for kw in technical_keywords:
            if kw in input_lower:
                return "technical"
        
        for kw in writing_keywords:
            if kw in input_lower:
                return "writing"
        
        for kw in analysis_keywords:
            if kw in input_lower:
                return "analysis"
        
        for kw in creative_keywords:
            if kw in input_lower:
                return "creative"
        
        return "general"
    
    def select_optimization_model(self, task_type: str, complexity: str = "medium") -> str:
        """[EMOJI:9009][EMOJI:62E9][EMOJI:4F18][EMOJI:5316][EMOJI:6A21][EMOJI:578B]"""
        # [EMOJI:4F7F][EMOJI:7528][EMOJI:65B0][EMOJI:7684][EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF]
        if self.config_manager:
            # [EMOJI:4ECE][EMOJI:914D][EMOJI:7F6E][EMOJI:4E2D][EMOJI:83B7][EMOJI:53D6][EMOJI:6A21][EMOJI:578B][EMOJI:6620][EMOJI:5C04]
            models_config = self.model_config.get("models", {})
            
            # [EMOJI:6839][EMOJI:636E][EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B][EMOJI:548C][EMOJI:590D][EMOJI:6742][EMOJI:5EA6][EMOJI:9009][EMOJI:62E9][EMOJI:6A21][EMOJI:578B]
            if complexity in ["low", "simple"]:
                # [EMOJI:7B80][EMOJI:5355][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F18][EMOJI:5148][EMOJI:4F7F][EMOJI:7528]DeepSeek
                for model_id, config in models_config.items():
                    if config.get("enabled", False) and config.get("provider") == "deepseek":
                        if self.config_manager.is_model_available(model_id):
                            return f"deepseek/{config.get('model', 'deepseek-chat')}"
            
            # [EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1][EMOJI:6839][EMOJI:636E][EMOJI:7C7B][EMOJI:578B][EMOJI:9009][EMOJI:62E9]
            if task_type in ["technical", "creative", "analysis", "writing"]:
                # [EMOJI:4F18][EMOJI:5148][EMOJI:4F7F][EMOJI:7528][EMOJI:5343][EMOJI:95EE][EMOJI:FF08][EMOJI:514D][EMOJI:8D39][EMOJI:FF09]
                for model_id, config in models_config.items():
                    if config.get("enabled", False) and config.get("provider") == "bailian":
                        if task_type == "technical" and "coder" in model_id.lower():
                            if self.config_manager.is_model_available(model_id):
                                return f"bailian/{config.get('model', 'qwen3-coder-next')}"
                        elif task_type in ["creative", "analysis", "writing"]:
                            if self.config_manager.is_model_available(model_id):
                                return f"bailian/{config.get('model', 'qwen3.5-plus')}"
            
            # [EMOJI:56DE][EMOJI:9000][EMOJI:5230][EMOJI:7B2C][EMOJI:4E00][EMOJI:4E2A][EMOJI:53EF][EMOJI:7528][EMOJI:7684][EMOJI:6A21][EMOJI:578B]
            for model_id, config in models_config.items():
                if config.get("enabled", False) and self.config_manager.is_model_available(model_id):
                    return f"{config.get('provider', 'deepseek')}/{config.get('model', 'deepseek-chat')}"
        
        # [EMOJI:5982][EMOJI:679C][EMOJI:914D][EMOJI:7F6E][EMOJI:7BA1][EMOJI:7406][EMOJI:5668][EMOJI:4E0D][EMOJI:53EF][EMOJI:7528][EMOJI:FF0C][EMOJI:4F7F][EMOJI:7528][EMOJI:65E7][EMOJI:903B][EMOJI:8F91]
        model_map = self.model_config.get("optimization_models", {})
        routing_strategy = self.model_config.get("routing_strategy", "cost_effective")
        
        if routing_strategy == "cost_effective":
            # [EMOJI:6210][EMOJI:672C][EMOJI:4F18][EMOJI:5148][EMOJI:7B56][EMOJI:7565]
            if complexity in ["low", "simple"]:
                return model_map.get("simple", "deepseek/deepseek-chat")
            elif task_type in ["technical", "creative", "analysis"]:
                return model_map.get(task_type, model_map.get("complex", "bailian/qwen3.5-plus"))
            else:
                return model_map.get("simple", "deepseek/deepseek-chat")
        else:
            # [EMOJI:8D28][EMOJI:91CF][EMOJI:4F18][EMOJI:5148][EMOJI:7B56][EMOJI:7565]
            return model_map.get(task_type, model_map.get("complex", "bailian/qwen3.5-plus"))
    
    def estimate_complexity(self, user_input: str) -> str:
        """[EMOJI:4F30][EMOJI:8BA1][EMOJI:4EFB][EMOJI:52A1][EMOJI:590D][EMOJI:6742][EMOJI:5EA6]"""
        length = len(user_input)
        word_count = len(user_input.split())
        
        # [EMOJI:7B80][EMOJI:5355][EMOJI:89C4][EMOJI:5219][EMOJI:FF1A][EMOJI:6839][EMOJI:636E][EMOJI:957F][EMOJI:5EA6][EMOJI:548C][EMOJI:5173][EMOJI:952E][EMOJI:8BCD][EMOJI:5224][EMOJI:65AD][EMOJI:590D][EMOJI:6742][EMOJI:5EA6]
        if word_count < 10:
            return "low"
        elif word_count < 30:
            return "medium"
        else:
            return "high"
    
    def optimize_prompt(self, user_input: str, task_type: str = None, 
                       optimization_level: str = "standard") -> Dict:
        """[EMOJI:4F18][EMOJI:5316][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]"""
        
        # [EMOJI:68C0][EMOJI:6D4B][EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]
        if not task_type:
            task_type = self.detect_task_type(user_input)
        
        # [EMOJI:4F30][EMOJI:8BA1][EMOJI:590D][EMOJI:6742][EMOJI:5EA6]
        complexity = self.estimate_complexity(user_input)
        
        # [EMOJI:9009][EMOJI:62E9][EMOJI:6A21][EMOJI:578B]
        model = self.select_optimization_model(task_type, complexity)
        
        # [EMOJI:83B7][EMOJI:53D6][EMOJI:4F18][EMOJI:5316][EMOJI:89C4][EMOJI:5219]
        rules = self.optimization_rules.get(task_type, self.optimization_rules["general"])
        
        # [EMOJI:6784][EMOJI:5EFA][EMOJI:4F18][EMOJI:5316][EMOJI:540E][EMOJI:7684][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]
        optimized_prompt = self._build_optimized_prompt(
            user_input, task_type, rules, optimization_level
        )
        
        # [EMOJI:8BB0][EMOJI:5F55][EMOJI:4F18][EMOJI:5316][EMOJI:5386][EMOJI:53F2]
        self._record_optimization_history(user_input, optimized_prompt, task_type, model)
        
        return {
            "original_input": user_input,
            "optimized_prompt": optimized_prompt,
            "task_type": task_type,
            "complexity": complexity,
            "recommended_model": model,
            "optimization_level": optimization_level,
            "rules_applied": list(rules.keys()) if isinstance(rules, dict) else rules,
            "timestamp": datetime.now().isoformat()
        }
    
    def _build_optimized_prompt(self, user_input: str, task_type: str, 
                               rules: Dict, level: str) -> str:
        """[EMOJI:6784][EMOJI:5EFA][EMOJI:4F18][EMOJI:5316][EMOJI:540E][EMOJI:7684][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]"""
        
        # [EMOJI:83B7][EMOJI:53D6][EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B][EMOJI:914D][EMOJI:7F6E]
        levels = self.dongdong_rules.get("optimization_levels", {})
        components = levels.get(level, levels.get("standard", []))
        
        prompt_parts = []
        
        # 1. [EMOJI:89D2][EMOJI:8272][EMOJI:5B9A][EMOJI:4E49]
        if "[EMOJI:89D2][EMOJI:8272][EMOJI:5B9A][EMOJI:4E49]" in components:
            role = rules.get("role", "[EMOJI:8D44][EMOJI:6DF1]AI[EMOJI:52A9][EMOJI:624B][EMOJI:4E13][EMOJI:5BB6]")
            prompt_parts.append(f"[EMOJI:4F5C][EMOJI:4E3A]{role}[EMOJI:FF0C]")
        
        # 2. [EMOJI:4EFB][EMOJI:52A1][EMOJI:6F84][EMOJI:6E05]
        if "[EMOJI:4EFB][EMOJI:52A1][EMOJI:6F84][EMOJI:6E05]" in components:
            # [EMOJI:5C06][EMOJI:6A21][EMOJI:7CCA][EMOJI:6307][EMOJI:4EE4][EMOJI:8F6C][EMOJI:5316][EMOJI:4E3A][EMOJI:5177][EMOJI:4F53][EMOJI:4EFB][EMOJI:52A1]
            clarified_task = self._clarify_task(user_input, task_type)
            prompt_parts.append(f"[EMOJI:8BF7]{clarified_task}")
        
        # 3. [EMOJI:4E0A][EMOJI:4E0B][EMOJI:6587][EMOJI:8865][EMOJI:5145]
        if "[EMOJI:4E0A][EMOJI:4E0B][EMOJI:6587][EMOJI:8865][EMOJI:5145]" in components:
            context = self._add_context(user_input, task_type)
            if context:
                prompt_parts.append(context)
        
        # 4. [EMOJI:8F93][EMOJI:51FA][EMOJI:683C][EMOJI:5F0F]
        if "[EMOJI:8F93][EMOJI:51FA][EMOJI:683C][EMOJI:5F0F]" in components:
            format_spec = rules.get("format", "[EMOJI:6E05][EMOJI:6670][EMOJI:660E][EMOJI:786E][EMOJI:7684][EMOJI:56DE][EMOJI:7B54]")
            prompt_parts.append(f"[EMOJI:8F93][EMOJI:51FA][EMOJI:683C][EMOJI:5F0F][EMOJI:8981][EMOJI:6C42][EMOJI:FF1A]{format_spec}")
        
        # 5. [EMOJI:8D28][EMOJI:91CF][EMOJI:7EA6][EMOJI:675F]
        if "[EMOJI:8D28][EMOJI:91CF][EMOJI:7EA6][EMOJI:675F]" in components:
            constraints = rules.get("constraints", [])
            if constraints:
                constraints_str = "[EMOJI:3001]".join(constraints)
                prompt_parts.append(f"[EMOJI:8D28][EMOJI:91CF][EMOJI:8981][EMOJI:6C42][EMOJI:FF1A]{constraints_str}")
            
            # [EMOJI:6DFB][EMOJI:52A0][EMOJI:4E3B][EMOJI:4EBA][EMOJI:504F][EMOJI:597D][EMOJI:7EA6][EMOJI:675F]
            quality_config = self.dongdong_rules.get("quality_constraints", {})
            if task_type == "technical" and "preferred_tech_stack" in quality_config:
                tech_stack = "[EMOJI:3001]".join(quality_config["preferred_tech_stack"])
                prompt_parts.append(f"[EMOJI:6280][EMOJI:672F][EMOJI:6808][EMOJI:504F][EMOJI:597D][EMOJI:FF1A]{tech_stack}")
        
        # 6. [EMOJI:793A][EMOJI:4F8B][EMOJI:53C2][EMOJI:8003][EMOJI:FF08][EMOJI:4EC5][EMOJI:9650][EMOJI:5B8C][EMOJI:6574][EMOJI:4F18][EMOJI:5316][EMOJI:FF09]
        if "[EMOJI:793A][EMOJI:4F8B][EMOJI:53C2][EMOJI:8003]" in components and level == "full":
            example = self._get_example_reference(task_type)
            if example:
                prompt_parts.append(f"[EMOJI:53C2][EMOJI:8003][EMOJI:793A][EMOJI:4F8B][EMOJI:FF1A]{example}")
        
        # [EMOJI:7EC4][EMOJI:5408][EMOJI:6240][EMOJI:6709][EMOJI:90E8][EMOJI:5206]
        optimized_prompt = " ".join(prompt_parts)
        
        # [EMOJI:786E][EMOJI:4FDD][EMOJI:4EE5][EMOJI:53E5][EMOJI:53F7][EMOJI:7ED3][EMOJI:675F]
        if not optimized_prompt.endswith(('.', '[EMOJI:3002]', '!', '[EMOJI:FF01]', '?', '[EMOJI:FF1F]')):
            optimized_prompt += "[EMOJI:3002]"
        
        return optimized_prompt
    
    def _clarify_task(self, user_input: str, task_type: str) -> str:
        """[EMOJI:6F84][EMOJI:6E05][EMOJI:4EFB][EMOJI:52A1]"""
        # [EMOJI:7B80][EMOJI:5355][EMOJI:7684][EMOJI:4EFB][EMOJI:52A1][EMOJI:6F84][EMOJI:6E05][EMOJI:89C4][EMOJI:5219]
        clarifications = {
            "technical": {
                "[EMOJI:5199][EMOJI:4E2A]": "[EMOJI:7F16][EMOJI:5199][EMOJI:4E00][EMOJI:4E2A][EMOJI:5B8C][EMOJI:6574][EMOJI:7684]",
                "[EMOJI:505A][EMOJI:4E2A]": "[EMOJI:5F00][EMOJI:53D1][EMOJI:4E00][EMOJI:4E2A][EMOJI:529F][EMOJI:80FD][EMOJI:5B8C][EMOJI:6574][EMOJI:7684]",
                "[EMOJI:5B9E][EMOJI:73B0]": "[EMOJI:5B9E][EMOJI:73B0][EMOJI:4E00][EMOJI:4E2A][EMOJI:9AD8][EMOJI:6548][EMOJI:7684]",
                "[EMOJI:4EE3][EMOJI:7801]": "[EMOJI:53EF][EMOJI:8FD0][EMOJI:884C][EMOJI:7684][EMOJI:4EE3][EMOJI:7801][EMOJI:FF0C][EMOJI:8981][EMOJI:6C42]"
            },
            "writing": {
                "[EMOJI:5199]": "[EMOJI:64B0][EMOJI:5199][EMOJI:4E00][EMOJI:7BC7][EMOJI:4E13][EMOJI:4E1A][EMOJI:7684]",
                "[EMOJI:6587][EMOJI:7AE0]": "[EMOJI:7ED3][EMOJI:6784][EMOJI:5B8C][EMOJI:6574][EMOJI:7684][EMOJI:6587][EMOJI:7AE0][EMOJI:FF0C][EMOJI:8981][EMOJI:6C42]",
                "[EMOJI:90AE][EMOJI:4EF6]": "[EMOJI:6B63][EMOJI:5F0F][EMOJI:7684][EMOJI:5546][EMOJI:52A1][EMOJI:90AE][EMOJI:4EF6][EMOJI:FF0C][EMOJI:8981][EMOJI:6C42]",
                "[EMOJI:62A5][EMOJI:544A]": "[EMOJI:8BE6][EMOJI:7EC6][EMOJI:7684][EMOJI:62A5][EMOJI:544A][EMOJI:FF0C][EMOJI:5305][EMOJI:542B]"
            },
            "analysis": {
                "[EMOJI:5206][EMOJI:6790]": "[EMOJI:8FDB][EMOJI:884C][EMOJI:6DF1][EMOJI:5165][EMOJI:5206][EMOJI:6790][EMOJI:FF0C][EMOJI:5305][EMOJI:62EC]",
                "[EMOJI:7EDF][EMOJI:8BA1]": "[EMOJI:8BE6][EMOJI:7EC6][EMOJI:7EDF][EMOJI:8BA1][EMOJI:FF0C][EMOJI:63D0][EMOJI:4F9B]",
                "[EMOJI:6570][EMOJI:636E]": "[EMOJI:6570][EMOJI:636E][EMOJI:5904][EMOJI:7406][EMOJI:548C][EMOJI:5206][EMOJI:6790][EMOJI:FF0C][EMOJI:5C55][EMOJI:793A]",
                "[EMOJI:603B][EMOJI:7ED3]": "[EMOJI:5168][EMOJI:9762][EMOJI:603B][EMOJI:7ED3][EMOJI:FF0C][EMOJI:6DB5][EMOJI:76D6]"
            }
        }
        
        task_clarifications = clarifications.get(task_type, {})
        clarified = user_input
        
        for pattern, replacement in task_clarifications.items():
            if pattern in clarified:
                clarified = clarified.replace(pattern, replacement)
                break
        
        return clarified
    
    def _add_context(self, user_input: str, task_type: str) -> str:
        """[EMOJI:6DFB][EMOJI:52A0][EMOJI:4E0A][EMOJI:4E0B][EMOJI:6587]"""
        context_rules = {
            "technical": "[EMOJI:5047][EMOJI:8BBE][EMOJI:8FD9][EMOJI:662F][EMOJI:751F][EMOJI:4EA7][EMOJI:73AF][EMOJI:5883][EMOJI:4EE3][EMOJI:7801][EMOJI:FF0C][EMOJI:9700][EMOJI:8981][EMOJI:826F][EMOJI:597D][EMOJI:7684][EMOJI:9519][EMOJI:8BEF][EMOJI:5904][EMOJI:7406][EMOJI:548C][EMOJI:6027][EMOJI:80FD][EMOJI:4F18][EMOJI:5316][EMOJI:3002]",
            "writing": "[EMOJI:5047][EMOJI:8BBE][EMOJI:8BFB][EMOJI:8005][EMOJI:662F][EMOJI:4E13][EMOJI:4E1A][EMOJI:4EBA][EMOJI:58EB][EMOJI:FF0C][EMOJI:9700][EMOJI:8981][EMOJI:51C6][EMOJI:786E][EMOJI:3001][EMOJI:6E05][EMOJI:6670][EMOJI:3001][EMOJI:6709][EMOJI:8BF4][EMOJI:670D][EMOJI:529B][EMOJI:7684][EMOJI:5185][EMOJI:5BB9][EMOJI:3002]",
            "analysis": "[EMOJI:5047][EMOJI:8BBE][EMOJI:6570][EMOJI:636E][EMOJI:6765][EMOJI:6E90][EMOJI:53EF][EMOJI:9760][EMOJI:FF0C][EMOJI:9700][EMOJI:8981][EMOJI:5BA2][EMOJI:89C2][EMOJI:3001][EMOJI:51C6][EMOJI:786E][EMOJI:3001][EMOJI:6709][EMOJI:6D1E][EMOJI:5BDF][EMOJI:529B][EMOJI:7684][EMOJI:5206][EMOJI:6790][EMOJI:3002]",
            "creative": "[EMOJI:5047][EMOJI:8BBE][EMOJI:9700][EMOJI:8981][EMOJI:65B0][EMOJI:9896][EMOJI:3001][EMOJI:6709][EMOJI:8DA3][EMOJI:3001][EMOJI:6709][EMOJI:611F][EMOJI:67D3][EMOJI:529B][EMOJI:7684][EMOJI:521B][EMOJI:610F][EMOJI:5185][EMOJI:5BB9][EMOJI:3002]"
        }
        
        return context_rules.get(task_type, "")
    
    def _get_example_reference(self, task_type: str) -> str:
        """[EMOJI:83B7][EMOJI:53D6][EMOJI:793A][EMOJI:4F8B][EMOJI:53C2][EMOJI:8003]"""
        examples = {
            "technical": "[EMOJI:53C2][EMOJI:8003]Python[EMOJI:5B98][EMOJI:65B9][EMOJI:6587][EMOJI:6863][EMOJI:548C][EMOJI:6700][EMOJI:4F73][EMOJI:5B9E][EMOJI:8DF5]",
            "writing": "[EMOJI:53C2][EMOJI:8003][EMOJI:4E13][EMOJI:4E1A][EMOJI:5546][EMOJI:52A1][EMOJI:5199][EMOJI:4F5C][EMOJI:89C4][EMOJI:8303]",
            "analysis": "[EMOJI:53C2][EMOJI:8003][EMOJI:6570][EMOJI:636E][EMOJI:5206][EMOJI:6790][EMOJI:62A5][EMOJI:544A][EMOJI:6807][EMOJI:51C6][EMOJI:683C][EMOJI:5F0F]",
            "creative": "[EMOJI:53C2][EMOJI:8003][EMOJI:4F18][EMOJI:79C0][EMOJI:521B][EMOJI:610F][EMOJI:4F5C][EMOJI:54C1][EMOJI:7684][EMOJI:7ED3][EMOJI:6784][EMOJI:548C][EMOJI:8868][EMOJI:8FBE]"
        }
        
        return examples.get(task_type, "")
    
    def _record_optimization_history(self, original: str, optimized: str, 
                                   task_type: str, model: str):
        """[EMOJI:8BB0][EMOJI:5F55][EMOJI:4F18][EMOJI:5316][EMOJI:5386][EMOJI:53F2]"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            history_entry = f"""
## {timestamp}

**[EMOJI:539F][EMOJI:59CB][EMOJI:8F93][EMOJI:5165]**: {original}

**[EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]**: {task_type}

**[EMOJI:4F18][EMOJI:5316][EMOJI:6A21][EMOJI:578B]**: {model}

**[EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]**:
```
{optimized}
```

---
"""
            
            # [EMOJI:8FFD][EMOJI:52A0][EMOJI:5230][EMOJI:5386][EMOJI:53F2][EMOJI:6587][EMOJI:4EF6]
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(history_entry)
                
        except Exception as e:
            print(f"[EMOJI:8BB0][EMOJI:5F55][EMOJI:4F18][EMOJI:5316][EMOJI:5386][EMOJI:53F2][EMOJI:5931][EMOJI:8D25]: {e}")
    
    def learn_from_feedback(self, original: str, optimized: str, 
                          feedback: str, notes: str = ""):
        """[EMOJI:4ECE][EMOJI:53CD][EMOJI:9988][EMOJI:4E2D][EMOJI:5B66][EMOJI:4E60]"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            feedback_entry = f"""
## [EMOJI:53CD][EMOJI:9988][EMOJI:8BB0][EMOJI:5F55] - {timestamp}

**[EMOJI:539F][EMOJI:59CB][EMOJI:8F93][EMOJI:5165]**: {original}

**[EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]**: {optimized}

**[EMOJI:53CD][EMOJI:9988]**: {feedback}

**[EMOJI:5907][EMOJI:6CE8]**: {notes}

**[EMOJI:5B66][EMOJI:4E60][EMOJI:8981][EMOJI:70B9]**:
1. [EMOJI:5206][EMOJI:6790][EMOJI:53CD][EMOJI:9988][EMOJI:539F][EMOJI:56E0]
2. [EMOJI:8C03][EMOJI:6574][EMOJI:4F18][EMOJI:5316][EMOJI:7B56][EMOJI:7565]
3. [EMOJI:66F4][EMOJI:65B0][EMOJI:4E2A][EMOJI:6027][EMOJI:5316][EMOJI:89C4][EMOJI:5219]

---
"""
            
            # [EMOJI:521B][EMOJI:5EFA][EMOJI:53CD][EMOJI:9988][EMOJI:6587][EMOJI:4EF6]
            feedback_file = self.memory_dir / "feedback_history.md"
            with open(feedback_file, 'a', encoding='utf-8') as f:
                f.write(feedback_entry)
                
            print("[EMOJI:53CD][EMOJI:9988][EMOJI:5DF2][EMOJI:8BB0][EMOJI:5F55][EMOJI:FF0C][EMOJI:5C06][EMOJI:7528][EMOJI:4E8E][EMOJI:6539][EMOJI:8FDB][EMOJI:4F18][EMOJI:5316][EMOJI:7B56][EMOJI:7565][EMOJI:3002]")
            
        except Exception as e:
            print(f"[EMOJI:8BB0][EMOJI:5F55][EMOJI:53CD][EMOJI:9988][EMOJI:5931][EMOJI:8D25]: {e}")

def main():
    """[EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5165][EMOJI:53E3]"""
    if len(sys.argv) < 2:
        print("[EMOJI:7528][EMOJI:6CD5]: python optimizer.py \"[EMOJI:7528][EMOJI:6237][EMOJI:8F93][EMOJI:5165]\" [[EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]] [[EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B]]")
        print("[EMOJI:793A][EMOJI:4F8B]: python optimizer.py \"[EMOJI:5199][EMOJI:4E2A][EMOJI:6392][EMOJI:5E8F][EMOJI:51FD][EMOJI:6570]\" technical standard")
        sys.exit(1)
    
    user_input = sys.argv[1]
    task_type = sys.argv[2] if len(sys.argv) > 2 else None
    optimization_level = sys.argv[3] if len(sys.argv) > 3 else "standard"
    
    optimizer = TSPromptOptimizer()
    result = optimizer.optimize_prompt(user_input, task_type, optimization_level)
    
    # [EMOJI:8F93][EMOJI:51FA][EMOJI:7ED3][EMOJI:679C]
    print("=" * 80)
    print("[DART] TS-Prompt-Optimizer [EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]")
    print("=" * 80)
    print(f"\n[NOTE] [EMOJI:539F][EMOJI:59CB][EMOJI:8F93][EMOJI:5165]: {result['original_input']}")
    print(f"[WRENCH] [EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]: {result['task_type']}")
    print(f"[FAST] [EMOJI:590D][EMOJI:6742][EMOJI:5EA6]: {result['complexity']}")
    print(f"[BOT] [EMOJI:63A8][EMOJI:8350][EMOJI:6A21][EMOJI:578B]: {result['recommended_model']}")
    print(f"[STATS] [EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B]: {result['optimization_level']}")
    print("\n" + "=" * 80)
    print("[ROCKET] [EMOJI:4F18][EMOJI:5316][EMOJI:540E][EMOJI:7684][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]:")
    print("=" * 80)
    print(f"\n{result['optimized_prompt']}\n")
    print("=" * 80)
    
    # [EMOJI:4FDD][EMOJI:5B58][EMOJI:8BE6][EMOJI:7EC6][EMOJI:7ED3][EMOJI:679C][EMOJI:5230][EMOJI:6587][EMOJI:4EF6]
    output_file = Path("optimization_result.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n[FILE] [EMOJI:8BE6][EMOJI:7EC6][EMOJI:7ED3][EMOJI:679C][EMOJI:5DF2][EMOJI:4FDD][EMOJI:5B58][EMOJI:5230]: {output_file}")

if __name__ == "__main__":
    main()
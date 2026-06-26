#!/usr/bin/env python3
"""
TS-Prompt-Optimizer [EMOJI:914D][EMOJI:7F6E][EMOJI:7BA1][EMOJI:7406][EMOJI:7CFB][EMOJI:7EDF]
[EMOJI:6838][EMOJI:5FC3][EMOJI:914D][EMOJI:7F6E][EMOJI:7BA1][EMOJI:7406][EMOJI:7C7B]
"""

import os
import json
import yaml
import getpass
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

class TSConfigManager:
    """TS-Prompt-Optimizer [EMOJI:914D][EMOJI:7F6E][EMOJI:7BA1][EMOJI:7406][EMOJI:5668]"""
    
    def __init__(self, config_dir: str = None):
        # [EMOJI:8BBE][EMOJI:7F6E][EMOJI:914D][EMOJI:7F6E][EMOJI:8DEF][EMOJI:5F84]
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = Path(config_dir) if config_dir else self.base_dir / "config"
        self.user_config_dir = Path.home() / ".openclaw"
        
        # [EMOJI:786E][EMOJI:4FDD][EMOJI:76EE][EMOJI:5F55][EMOJI:5B58][EMOJI:5728]
        self.config_dir.mkdir(exist_ok=True)
        self.user_config_dir.mkdir(exist_ok=True)
        
        # [EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6][EMOJI:8DEF][EMOJI:5F84]
        self.default_config = self.config_dir / "model_config.json"
        self.user_config = self.user_config_dir / "ts-optimizer-config.yaml"
        self.env_config = self.user_config_dir / "ts-env-config.json"
        
        # [EMOJI:914D][EMOJI:7F6E][EMOJI:7F13][EMOJI:5B58]
        self._config_cache = None
        self._config_loaded = False
        
    def _load_default_config(self) -> Dict:
        """[EMOJI:52A0][EMOJI:8F7D][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E]"""
        if self.default_config.exists():
            try:
                with open(self.default_config, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[EMOJI:8B66][EMOJI:544A][EMOJI:FF1A][EMOJI:52A0][EMOJI:8F7D][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E][EMOJI:5931][EMOJI:8D25]: {e}")
        
        # [EMOJI:8FD4][EMOJI:56DE][EMOJI:57FA][EMOJI:7840][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E]
        return {
            "models": {
                "deepseek": {
                    "provider": "deepseek",
                    "model": "deepseek-chat",
                    "api_key_source": "env",
                    "api_key_env": "DEEPSEEK_API_KEY",
                    "enabled": True,
                    "priority": 1,
                    "cost_per_1k_tokens": 0.42,
                    "capabilities": ["[EMOJI:65E5][EMOJI:5E38][EMOJI:5BF9][EMOJI:8BDD]", "[EMOJI:7B80][EMOJI:5355][EMOJI:4F18][EMOJI:5316]", "[EMOJI:4EE3][EMOJI:7801][EMOJI:5BA1][EMOJI:67E5]"]
                },
                "qwen35": {
                    "provider": "bailian",
                    "model": "qwen3.5-plus",
                    "api_key_source": "env",
                    "api_key_env": "BAILIAN_API_KEY",
                    "enabled": True,
                    "priority": 2,
                    "cost_per_1k_tokens": 0.00,
                    "capabilities": ["[EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1]", "[EMOJI:56FE][EMOJI:50CF][EMOJI:8BC6][EMOJI:522B]", "[EMOJI:4E2D][EMOJI:6587][EMOJI:5199][EMOJI:4F5C]"]
                },
                "qwen_coder": {
                    "provider": "bailian",
                    "model": "qwen3-coder-next",
                    "api_key_source": "env",
                    "api_key_env": "BAILIAN_API_KEY",
                    "enabled": True,
                    "priority": 3,
                    "cost_per_1k_tokens": 0.00,
                    "capabilities": ["[EMOJI:6280][EMOJI:672F][EMOJI:5F00][EMOJI:53D1]", "[EMOJI:4EE3][EMOJI:7801][EMOJI:751F][EMOJI:6210]", "[EMOJI:7CFB][EMOJI:7EDF][EMOJI:8BBE][EMOJI:8BA1]"]
                }
            },
            "routing": {
                "strategy": "cost_effective",
                "fallback_model": "deepseek",
                "cost_threshold": 1.00
            },
            "user_preferences": {
                "default_optimization_level": "standard",
                "show_config_summary": True,
                "auto_test_connections": True
            }
        }
    
    def _load_user_config(self) -> Dict:
        """[EMOJI:52A0][EMOJI:8F7D][EMOJI:7528][EMOJI:6237][EMOJI:914D][EMOJI:7F6E]"""
        user_configs = []
        
        # 1. [EMOJI:68C0][EMOJI:67E5]YAML[EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6]
        if self.user_config.exists():
            try:
                with open(self.user_config, 'r', encoding='utf-8') as f:
                    yaml_config = yaml.safe_load(f)
                    if yaml_config:
                        user_configs.append(yaml_config)
            except Exception as e:
                print(f"[EMOJI:8B66][EMOJI:544A][EMOJI:FF1A][EMOJI:52A0][EMOJI:8F7D]YAML[EMOJI:914D][EMOJI:7F6E][EMOJI:5931][EMOJI:8D25]: {e}")
        
        # 2. [EMOJI:68C0][EMOJI:67E5]JSON[EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6]
        if self.env_config.exists():
            try:
                with open(self.env_config, 'r', encoding='utf-8') as f:
                    json_config = json.load(f)
                    if json_config:
                        user_configs.append(json_config)
            except Exception as e:
                print(f"[EMOJI:8B66][EMOJI:544A][EMOJI:FF1A][EMOJI:52A0][EMOJI:8F7D]JSON[EMOJI:914D][EMOJI:7F6E][EMOJI:5931][EMOJI:8D25]: {e}")
        
        # [EMOJI:5408][EMOJI:5E76][EMOJI:6240][EMOJI:6709][EMOJI:7528][EMOJI:6237][EMOJI:914D][EMOJI:7F6E]
        merged_config = {}
        for config in user_configs:
            merged_config = self._merge_configs(merged_config, config)
        
        return merged_config
    
    def _merge_configs(self, base: Dict, override: Dict) -> Dict:
        """[EMOJI:6DF1][EMOJI:5EA6][EMOJI:5408][EMOJI:5E76][EMOJI:914D][EMOJI:7F6E]"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _resolve_env_vars(self, config: Dict) -> Dict:
        """[EMOJI:89E3][EMOJI:6790][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]"""
        resolved = config.copy()
        
        # [EMOJI:68C0][EMOJI:67E5]models[EMOJI:914D][EMOJI:7F6E][EMOJI:4E2D][EMOJI:7684][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]
        if "models" in resolved:
            for model_name, model_config in resolved["models"].items():
                if "api_key_env" in model_config:
                    env_var = model_config["api_key_env"]
                    api_key = os.getenv(env_var)
                    
                    if api_key:
                        # [EMOJI:5C06][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:503C][EMOJI:5B58][EMOJI:50A8][EMOJI:5230][EMOJI:914D][EMOJI:7F6E][EMOJI:4E2D][EMOJI:FF08][EMOJI:4EC5][EMOJI:5185][EMOJI:5B58][EMOJI:FF0C][EMOJI:4E0D][EMOJI:5199][EMOJI:6587][EMOJI:4EF6][EMOJI:FF09]
                        model_config["api_key"] = api_key
                        model_config["api_key_source"] = "env"
                    elif "api_key" not in model_config:
                        # [EMOJI:6CA1][EMOJI:6709][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:4E5F][EMOJI:6CA1][EMOJI:6709][EMOJI:914D][EMOJI:7F6E][EMOJI:7684]API[EMOJI:5BC6][EMOJI:94A5]
                        model_config["api_key"] = None
                        model_config["api_key_source"] = "missing"
        
        return resolved
    
    def load_config(self) -> Dict:
        """[EMOJI:52A0][EMOJI:8F7D][EMOJI:5B8C][EMOJI:6574][EMOJI:914D][EMOJI:7F6E]"""
        if self._config_loaded and self._config_cache:
            return self._config_cache
        
        # [EMOJI:52A0][EMOJI:8F7D][EMOJI:9ED8][EMOJI:8BA4][EMOJI:914D][EMOJI:7F6E]
        config = self._load_default_config()
        
        # [EMOJI:52A0][EMOJI:8F7D][EMOJI:7528][EMOJI:6237][EMOJI:914D][EMOJI:7F6E]
        user_config = self._load_user_config()
        config = self._merge_configs(config, user_config)
        
        # [EMOJI:89E3][EMOJI:6790][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]
        config = self._resolve_env_vars(config)
        
        # [EMOJI:7F13][EMOJI:5B58][EMOJI:914D][EMOJI:7F6E]
        self._config_cache = config
        self._config_loaded = True
        
        return config
    
    def check_config_status(self) -> Dict:
        """[EMOJI:68C0][EMOJI:67E5][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]"""
        config = self.load_config()
        
        status = {
            "total_models": 0,
            "configured_models": 0,
            "enabled_models": 0,
            "models": {},
            "issues": []
        }
        
        if "models" in config:
            for model_name, model_config in config["models"].items():
                status["total_models"] += 1
                
                model_status = {
                    "name": model_name,
                    "enabled": model_config.get("enabled", False),
                    "api_key_configured": "api_key" in model_config and model_config["api_key"] is not None,
                    "api_key_source": model_config.get("api_key_source", "unknown"),
                    "provider": model_config.get("provider", "unknown"),
                    "model": model_config.get("model", "unknown")
                }
                
                if model_status["enabled"]:
                    status["enabled_models"] += 1
                
                if model_status["api_key_configured"]:
                    status["configured_models"] += 1
                elif model_status["enabled"]:
                    # [EMOJI:542F][EMOJI:7528][EMOJI:4E86][EMOJI:4F46][EMOJI:6CA1][EMOJI:6709][EMOJI:914D][EMOJI:7F6E]API[EMOJI:5BC6][EMOJI:94A5]
                    status["issues"].append(f"[EMOJI:6A21][EMOJI:578B] {model_name} [EMOJI:5DF2][EMOJI:542F][EMOJI:7528][EMOJI:4F46][EMOJI:672A][EMOJI:914D][EMOJI:7F6E]API[EMOJI:5BC6][EMOJI:94A5]")
                
                status["models"][model_name] = model_status
        
        return status
    
    def get_model_config(self, model_name: str) -> Optional[Dict]:
        """[EMOJI:83B7][EMOJI:53D6][EMOJI:7279][EMOJI:5B9A][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]"""
        config = self.load_config()
        return config.get("models", {}).get(model_name)
    
    def get_api_key(self, model_name: str) -> Optional[str]:
        """[EMOJI:83B7][EMOJI:53D6][EMOJI:6A21][EMOJI:578B]API[EMOJI:5BC6][EMOJI:94A5]"""
        model_config = self.get_model_config(model_name)
        if model_config:
            return model_config.get("api_key")
        return None
    
    def is_model_available(self, model_name: str) -> bool:
        """[EMOJI:68C0][EMOJI:67E5][EMOJI:6A21][EMOJI:578B][EMOJI:662F][EMOJI:5426][EMOJI:53EF][EMOJI:7528]"""
        model_config = self.get_model_config(model_name)
        if not model_config:
            return False
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:662F][EMOJI:5426][EMOJI:542F][EMOJI:7528]
        if not model_config.get("enabled", False):
            return False
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:662F][EMOJI:5426][EMOJI:6709]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF08][EMOJI:514D][EMOJI:8D39][EMOJI:6A21][EMOJI:578B][EMOJI:53EF][EMOJI:80FD][EMOJI:4E0D][EMOJI:9700][EMOJI:8981][EMOJI:FF09]
        api_key = model_config.get("api_key")
        cost = model_config.get("cost_per_1k_tokens", 999)
        
        # [EMOJI:514D][EMOJI:8D39][EMOJI:6A21][EMOJI:578B][EMOJI:53EF][EMOJI:4EE5][EMOJI:6CA1][EMOJI:6709]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF08][EMOJI:4F7F][EMOJI:7528][EMOJI:7CFB][EMOJI:7EDF][EMOJI:9ED8][EMOJI:8BA4][EMOJI:FF09]
        if cost == 0.00 and api_key is None:
            return True
        
        # [EMOJI:4ED8][EMOJI:8D39][EMOJI:6A21][EMOJI:578B][EMOJI:5FC5][EMOJI:987B][EMOJI:6709]API[EMOJI:5BC6][EMOJI:94A5]
        return api_key is not None
    
    def save_user_config(self, config: Dict, format: str = "yaml") -> bool:
        """[EMOJI:4FDD][EMOJI:5B58][EMOJI:7528][EMOJI:6237][EMOJI:914D][EMOJI:7F6E]"""
        try:
            if format == "yaml":
                with open(self.user_config, 'w', encoding='utf-8') as f:
                    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            else:  # json
                with open(self.env_config, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
            
            # [EMOJI:6E05][EMOJI:9664][EMOJI:7F13][EMOJI:5B58]
            self._config_cache = None
            self._config_loaded = False
            
            return True
        except Exception as e:
            print(f"[EMOJI:4FDD][EMOJI:5B58][EMOJI:914D][EMOJI:7F6E][EMOJI:5931][EMOJI:8D25]: {e}")
            return False
    
    def update_model_config(self, model_name: str, updates: Dict) -> bool:
        """[EMOJI:66F4][EMOJI:65B0][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]"""
        try:
            # [EMOJI:52A0][EMOJI:8F7D][EMOJI:5F53][EMOJI:524D][EMOJI:914D][EMOJI:7F6E]
            config = self.load_config()
            
            # [EMOJI:786E][EMOJI:4FDD]models[EMOJI:7ED3][EMOJI:6784][EMOJI:5B58][EMOJI:5728]
            if "models" not in config:
                config["models"] = {}
            
            # [EMOJI:66F4][EMOJI:65B0][EMOJI:6216][EMOJI:6DFB][EMOJI:52A0][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]
            if model_name in config["models"]:
                config["models"][model_name].update(updates)
            else:
                config["models"][model_name] = updates
            
            # [EMOJI:4FDD][EMOJI:5B58][EMOJI:7528][EMOJI:6237][EMOJI:914D][EMOJI:7F6E][EMOJI:90E8][EMOJI:5206]
            user_config = {
                "models": {
                    model_name: config["models"][model_name]
                }
            }
            
            return self.save_user_config(user_config)
        except Exception as e:
            print(f"[EMOJI:66F4][EMOJI:65B0][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E][EMOJI:5931][EMOJI:8D25]: {e}")
            return False

def main():
    """[EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5165][EMOJI:53E3]"""
    if len(sys.argv) < 2:
        print("[EMOJI:7528][EMOJI:6CD5]: python config_manager.py [[EMOJI:547D][EMOJI:4EE4]]")
        print("[EMOJI:547D][EMOJI:4EE4]:")
        print("  status    - [EMOJI:663E][EMOJI:793A][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]")
        print("  show      - [EMOJI:663E][EMOJI:793A][EMOJI:5B8C][EMOJI:6574][EMOJI:914D][EMOJI:7F6E]")
        print("  check     - [EMOJI:68C0][EMOJI:67E5][EMOJI:914D][EMOJI:7F6E][EMOJI:95EE][EMOJI:9898]")
        print("  get <[EMOJI:6A21][EMOJI:578B]> - [EMOJI:83B7][EMOJI:53D6][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]")
        print("  test      - [EMOJI:6D4B][EMOJI:8BD5][EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF]")
        sys.exit(1)
    
    command = sys.argv[1]
    config_manager = TSConfigManager()
    
    if command == "status":
        status = config_manager.check_config_status()
        print("TS-Prompt-Optimizer [EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]")
        print("=" * 60)
        print(f"[EMOJI:603B][EMOJI:6A21][EMOJI:578B][EMOJI:6570]: {status['total_models']}")
        print(f"[EMOJI:5DF2][EMOJI:914D][EMOJI:7F6E][EMOJI:6A21][EMOJI:578B]: {status['configured_models']}")
        print(f"[EMOJI:542F][EMOJI:7528][EMOJI:6A21][EMOJI:578B]: {status['enabled_models']}")
        
        if status['issues']:
            print("\n[EMOJI:914D][EMOJI:7F6E][EMOJI:95EE][EMOJI:9898]:")
            for issue in status['issues']:
                print(f"  - {issue}")
        else:
            print("\n[EMOJI:914D][EMOJI:7F6E][EMOJI:6B63][EMOJI:5E38]")
        
        print("\n[EMOJI:6A21][EMOJI:578B][EMOJI:8BE6][EMOJI:60C5]:")
        for model_name, model_status in status['models'].items():
            status_icon = "" if model_status['api_key_configured'] else ""
            enabled_icon = "" if model_status['enabled'] else ""
            print(f"  {enabled_icon} {status_icon} {model_name}: {model_status['provider']}/{model_status['model']}")
    
    elif command == "show":
        config = config_manager.load_config()
        print("[FILE] [EMOJI:5B8C][EMOJI:6574][EMOJI:914D][EMOJI:7F6E]:")
        print(json.dumps(config, ensure_ascii=False, indent=2))
    
    elif command == "check":
        status = config_manager.check_config_status()
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:5173][EMOJI:952E][EMOJI:6A21][EMOJI:578B]
        critical_models = ["deepseek", "qwen35"]
        all_ok = True
        
        for model in critical_models:
            if model in status['models']:
                model_status = status['models'][model]
                if model_status['api_key_configured']:
                    print(f"[OK] {model}: [EMOJI:914D][EMOJI:7F6E][EMOJI:6B63][EMOJI:5E38]")
                else:
                    print(f"[FAIL] {model}: [EMOJI:672A][EMOJI:914D][EMOJI:7F6E]API[EMOJI:5BC6][EMOJI:94A5]")
                    all_ok = False
            else:
                print(f"[WARN] {model}: [EMOJI:672A][EMOJI:5728][EMOJI:914D][EMOJI:7F6E][EMOJI:4E2D][EMOJI:627E][EMOJI:5230]")
                all_ok = False
        
        if all_ok:
            print("\n[CELE] [EMOJI:6240][EMOJI:6709][EMOJI:5173][EMOJI:952E][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E][EMOJI:6B63][EMOJI:5E38][EMOJI:FF01]")
        else:
            print("\n[WRENCH] [EMOJI:8BF7][EMOJI:8FD0][EMOJI:884C][EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC][EMOJI:8BBE][EMOJI:7F6E][EMOJI:7F3A][EMOJI:5931][EMOJI:7684]API[EMOJI:5BC6][EMOJI:94A5]")
    
    elif command == "get" and len(sys.argv) > 2:
        model_name = sys.argv[2]
        config = config_manager.get_model_config(model_name)
        if config:
            print(f"[LIST] {model_name} [EMOJI:914D][EMOJI:7F6E]:")
            print(json.dumps(config, ensure_ascii=False, indent=2))
        else:
            print(f"[FAIL] [EMOJI:672A][EMOJI:627E][EMOJI:5230][EMOJI:6A21][EMOJI:578B] {model_name} [EMOJI:7684][EMOJI:914D][EMOJI:7F6E]")
    
    elif command == "test":
        print("[TEST] [EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5]")
        print("=" * 60)
        
        # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:914D][EMOJI:7F6E][EMOJI:52A0][EMOJI:8F7D]
        config_manager = TSConfigManager()
        config = config_manager.load_config()
        print(f"[OK] [EMOJI:914D][EMOJI:7F6E][EMOJI:52A0][EMOJI:8F7D][EMOJI:6210][EMOJI:529F][EMOJI:FF0C][EMOJI:5305][EMOJI:542B] {len(config.get('models', {}))} [EMOJI:4E2A][EMOJI:6A21][EMOJI:578B]")
        
        # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:72B6][EMOJI:6001][EMOJI:68C0][EMOJI:67E5]
        status = config_manager.check_config_status()
        print(f"[OK] [EMOJI:72B6][EMOJI:6001][EMOJI:68C0][EMOJI:67E5][EMOJI:6210][EMOJI:529F][EMOJI:FF0C][EMOJI:53D1][EMOJI:73B0] {len(status['issues'])} [EMOJI:4E2A][EMOJI:95EE][EMOJI:9898]")
        
        # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:6A21][EMOJI:578B][EMOJI:53EF][EMOJI:7528][EMOJI:6027][EMOJI:68C0][EMOJI:67E5]
        test_models = ["deepseek", "qwen35", "qwen_coder"]
        for model in test_models:
            available = config_manager.is_model_available(model)
            status = "[EMOJI:53EF][EMOJI:7528]" if available else "[EMOJI:4E0D][EMOJI:53EF][EMOJI:7528]"
            print(f"  {model}: {status}")
        
        print("\n[CELE] [EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5][EMOJI:901A][EMOJI:8FC7][EMOJI:FF01]")
    
    else:
        print(f"[EMOJI:672A][EMOJI:77E5][EMOJI:547D][EMOJI:4EE4]: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
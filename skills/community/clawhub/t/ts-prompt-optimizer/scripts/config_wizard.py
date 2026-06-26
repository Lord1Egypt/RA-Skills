#!/usr/bin/env python3
"""
TS-Prompt-Optimizer [EMOJI:4EA4][EMOJI:4E92][EMOJI:5F0F][EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC]
[EMOJI:7528][EMOJI:6237][EMOJI:53CB][EMOJI:597D][EMOJI:7684][EMOJI:914D][EMOJI:7F6E][EMOJI:8BBE][EMOJI:7F6E][EMOJI:5DE5][EMOJI:5177]
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional

# [EMOJI:6DFB][EMOJI:52A0][EMOJI:7236][EMOJI:76EE][EMOJI:5F55][EMOJI:5230][EMOJI:8DEF][EMOJI:5F84]
sys.path.insert(0, str(Path(__file__).parent))
from config_manager import TSConfigManager

class TSConfigWizard:
    """[EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC]"""
    
    def __init__(self):
        self.config_manager = TSConfigManager()
        self.current_config = self.config_manager.load_config()
        
    def clear_screen(self):
        """[EMOJI:6E05][EMOJI:5C4F][EMOJI:FF08][EMOJI:8DE8][EMOJI:5E73][EMOJI:53F0][EMOJI:FF09]"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """[EMOJI:6253][EMOJI:5370][EMOJI:6807][EMOJI:9898]"""
        print("\n" + "=" * 60)
        print(f"TS-Prompt-Optimizer [EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC] - {title}")
        print("=" * 60)
    
    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """[EMOJI:8BE2][EMOJI:95EE][EMOJI:662F]/[EMOJI:5426][EMOJI:95EE][EMOJI:9898]"""
        choices = "Y/n" if default else "y/N"
        while True:
            response = input(f"{question} [{choices}]: ").strip().lower()
            if response == "":
                return default
            if response in ["y", "yes", "[EMOJI:662F]", "[EMOJI:5BF9][EMOJI:7684]"]:
                return True
            if response in ["n", "no", "[EMOJI:5426]", "[EMOJI:4E0D][EMOJI:5BF9]"]:
                return False
            print("[EMOJI:8BF7][EMOJI:8F93][EMOJI:5165] y/n [EMOJI:6216] [EMOJI:662F]/[EMOJI:5426]")
    
    def ask_input(self, question: str, default: str = "", password: bool = False) -> str:
        """[EMOJI:8BE2][EMOJI:95EE][EMOJI:8F93][EMOJI:5165]"""
        if default:
            prompt = f"{question} [{default}]: "
        else:
            prompt = f"{question}: "
        
        if password:
            import getpass
            response = getpass.getpass(prompt)
        else:
            response = input(prompt)
        
        return response.strip() if response.strip() else default
    
    def setup_deepseek(self) -> Optional[Dict]:
        """[EMOJI:914D][EMOJI:7F6E]DeepSeek"""
        self.print_header("[EMOJI:914D][EMOJI:7F6E] DeepSeek")
        
        print("DeepSeek [EMOJI:7528][EMOJI:4E8E][EMOJI:65E5][EMOJI:5E38][EMOJI:5BF9][EMOJI:8BDD][EMOJI:548C][EMOJI:7B80][EMOJI:5355][EMOJI:4EFB][EMOJI:52A1][EMOJI:FF0C][EMOJI:6210][EMOJI:672C][EMOJI:8F83][EMOJI:4F4E][EMOJI:3002]")
        print("[EMOJI:60A8][EMOJI:9700][EMOJI:8981]DeepSeek API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF0C][EMOJI:53EF][EMOJI:4EE5][EMOJI:4ECE] https://platform.deepseek.com/ [EMOJI:83B7][EMOJI:53D6]")
        
        if not self.ask_yes_no("[EMOJI:662F][EMOJI:5426][EMOJI:914D][EMOJI:7F6E]DeepSeek[EMOJI:FF1F]", default=True):
            return None
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:73B0][EMOJI:6709][EMOJI:914D][EMOJI:7F6E]
        current_config = self.config_manager.get_model_config("deepseek")
        current_key = current_config.get("api_key") if current_config else None
        
        if current_key and current_key != "None":
            print("[EMOJI:68C0][EMOJI:6D4B][EMOJI:5230][EMOJI:73B0][EMOJI:6709]DeepSeek[EMOJI:914D][EMOJI:7F6E]")
            if not self.ask_yes_no("[EMOJI:662F][EMOJI:5426][EMOJI:91CD][EMOJI:65B0][EMOJI:914D][EMOJI:7F6E][EMOJI:FF1F]", default=False):
                return None
        
        # [EMOJI:83B7][EMOJI:53D6]API[EMOJI:5BC6][EMOJI:94A5]
        print("\nDeepSeek API[EMOJI:5BC6][EMOJI:94A5][EMOJI:914D][EMOJI:7F6E]")
        print("1. [EMOJI:76F4][EMOJI:63A5][EMOJI:8F93][EMOJI:5165]API[EMOJI:5BC6][EMOJI:94A5]")
        print("2. [EMOJI:8BBE][EMOJI:7F6E][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]")
        print("3. [EMOJI:4F7F][EMOJI:7528][EMOJI:73B0][EMOJI:6709][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]")
        
        choice = self.ask_input("[EMOJI:9009][EMOJI:62E9][EMOJI:914D][EMOJI:7F6E][EMOJI:65B9][EMOJI:5F0F] [1/2/3]", "1")
        
        api_key = None
        api_key_source = "inline"
        
        if choice == "1":
            # [EMOJI:76F4][EMOJI:63A5][EMOJI:8F93][EMOJI:5165]
            api_key = self.ask_input("[EMOJI:8BF7][EMOJI:8F93][EMOJI:5165]DeepSeek API[EMOJI:5BC6][EMOJI:94A5]", password=True)
            if not api_key:
                print("[EMOJI:672A][EMOJI:8F93][EMOJI:5165]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF0C][EMOJI:8DF3][EMOJI:8FC7]DeepSeek[EMOJI:914D][EMOJI:7F6E]")
                return None
            api_key_source = "inline"
            
        elif choice == "2":
            # [EMOJI:8BBE][EMOJI:7F6E][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]
            env_var = "DEEPSEEK_API_KEY"
            api_key = self.ask_input(f"[EMOJI:8BF7][EMOJI:8F93][EMOJI:5165]DeepSeek API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF08][EMOJI:5C06][EMOJI:4FDD][EMOJI:5B58][EMOJI:5230]{env_var}[EMOJI:FF09]", password=True)
            if api_key:
                # [EMOJI:5C1D][EMOJI:8BD5][EMOJI:8BBE][EMOJI:7F6E][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]
                self._set_environment_variable(env_var, api_key)
                api_key_source = "env"
            else:
                print("[EMOJI:672A][EMOJI:8F93][EMOJI:5165]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF0C][EMOJI:8DF3][EMOJI:8FC7]DeepSeek[EMOJI:914D][EMOJI:7F6E]")
                return None
                
        elif choice == "3":
            # [EMOJI:4F7F][EMOJI:7528][EMOJI:73B0][EMOJI:6709][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]
            env_var = self.ask_input("[EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:540D]", "DEEPSEEK_API_KEY")
            api_key = os.getenv(env_var)
            if api_key:
                print(f"[EMOJI:4ECE][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF] {env_var} [EMOJI:83B7][EMOJI:53D6][EMOJI:5230]API[EMOJI:5BC6][EMOJI:94A5]")
                api_key_source = "env"
            else:
                print(f"[EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF] {env_var} [EMOJI:672A][EMOJI:8BBE][EMOJI:7F6E]")
                return None
        
        # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:8FDE][EMOJI:63A5][EMOJI:FF08][EMOJI:53EF][EMOJI:9009][EMOJI:FF09]
        if api_key and self.ask_yes_no("[EMOJI:662F][EMOJI:5426][EMOJI:6D4B][EMOJI:8BD5]API[EMOJI:8FDE][EMOJI:63A5][EMOJI:FF1F]", default=True):
            if self._test_deepseek_connection(api_key):
                print("DeepSeek API[EMOJI:8FDE][EMOJI:63A5][EMOJI:6D4B][EMOJI:8BD5][EMOJI:6210][EMOJI:529F]")
            else:
                print("DeepSeek API[EMOJI:8FDE][EMOJI:63A5][EMOJI:6D4B][EMOJI:8BD5][EMOJI:5931][EMOJI:8D25][EMOJI:FF0C][EMOJI:4F46][EMOJI:4ECD][EMOJI:4FDD][EMOJI:5B58][EMOJI:914D][EMOJI:7F6E]")
        
        # [EMOJI:6784][EMOJI:5EFA][EMOJI:914D][EMOJI:7F6E]
        config = {
            "provider": "deepseek",
            "model": "deepseek-chat",
            "api_key": api_key,
            "api_key_source": api_key_source,
            "enabled": True,
            "priority": 1,
            "cost_per_1k_tokens": 0.42,
            "capabilities": ["[EMOJI:65E5][EMOJI:5E38][EMOJI:5BF9][EMOJI:8BDD]", "[EMOJI:7B80][EMOJI:5355][EMOJI:4F18][EMOJI:5316]", "[EMOJI:4EE3][EMOJI:7801][EMOJI:5BA1][EMOJI:67E5]", "[EMOJI:7FFB][EMOJI:8BD1][EMOJI:6458][EMOJI:8981]"]
        }
        
        return config
    
    def setup_qwen(self) -> Optional[Dict]:
        """[EMOJI:914D][EMOJI:7F6E][EMOJI:5343][EMOJI:95EE][EMOJI:6A21][EMOJI:578B]"""
        self.print_header("[EMOJI:914D][EMOJI:7F6E] [EMOJI:5343][EMOJI:95EE][EMOJI:6A21][EMOJI:578B]")
        
        print("[EMOJI:5343][EMOJI:95EE][EMOJI:6A21][EMOJI:578B][EMOJI:FF08][EMOJI:963F][EMOJI:91CC][EMOJI:4E91][EMOJI:767E][EMOJI:70BC][EMOJI:FF09][EMOJI:63D0][EMOJI:4F9B][EMOJI:514D][EMOJI:8D39][EMOJI:989D][EMOJI:5EA6][EMOJI:FF0C][EMOJI:9002][EMOJI:5408][EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1][EMOJI:3002]")
        print("[EMOJI:5305][EMOJI:62EC][EMOJI:FF1A][EMOJI:5343][EMOJI:95EE] 3.5 Plus[EMOJI:FF08][EMOJI:901A][EMOJI:7528][EMOJI:FF09][EMOJI:548C][EMOJI:5343][EMOJI:95EE] Coder Next[EMOJI:FF08][EMOJI:6280][EMOJI:672F][EMOJI:FF09]")
        
        if not self.ask_yes_no("[EMOJI:662F][EMOJI:5426][EMOJI:914D][EMOJI:7F6E][EMOJI:5343][EMOJI:95EE][EMOJI:6A21][EMOJI:578B][EMOJI:FF1F]", default=True):
            return None
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:73B0][EMOJI:6709][EMOJI:914D][EMOJI:7F6E]
        current_config = self.config_manager.get_model_config("qwen35")
        current_key = current_config.get("api_key") if current_config else None
        
        if current_key and current_key != "None":
            print("[EMOJI:68C0][EMOJI:6D4B][EMOJI:5230][EMOJI:73B0][EMOJI:6709][EMOJI:5343][EMOJI:95EE][EMOJI:914D][EMOJI:7F6E]")
            if not self.ask_yes_no("[EMOJI:662F][EMOJI:5426][EMOJI:91CD][EMOJI:65B0][EMOJI:914D][EMOJI:7F6E][EMOJI:FF1F]", default=False):
                return None
        
        # [EMOJI:83B7][EMOJI:53D6]API[EMOJI:5BC6][EMOJI:94A5]
        print("\n[EMOJI:5343][EMOJI:95EE]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:914D][EMOJI:7F6E]")
        print("[EMOJI:5343][EMOJI:95EE][EMOJI:4F7F][EMOJI:7528][EMOJI:963F][EMOJI:91CC][EMOJI:4E91][EMOJI:767E][EMOJI:70BC][EMOJI:5E73][EMOJI:53F0][EMOJI:FF0C][EMOJI:9700][EMOJI:8981][EMOJI:914D][EMOJI:7F6E]BAILIAN_API_KEY")
        print("[EMOJI:53EF][EMOJI:4EE5][EMOJI:4ECE] https://bailian.console.aliyun.com/ [EMOJI:83B7][EMOJI:53D6]")
        
        env_var = "BAILIAN_API_KEY"
        current_env = os.getenv(env_var)
        
        if current_env:
            print(f"[EMOJI:68C0][EMOJI:6D4B][EMOJI:5230][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF] {env_var}")
            if self.ask_yes_no(f"[EMOJI:4F7F][EMOJI:7528][EMOJI:73B0][EMOJI:6709][EMOJI:7684] {env_var} [EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:FF1F]", default=True):
                api_key = current_env
                api_key_source = "env"
            else:
                api_key = self.ask_input(f"[EMOJI:8BF7][EMOJI:8F93][EMOJI:5165][EMOJI:65B0][EMOJI:7684]{env_var}[EMOJI:503C]", password=True)
                if api_key:
                    self._set_environment_variable(env_var, api_key)
                    api_key_source = "env"
                else:
                    print("[EMOJI:672A][EMOJI:8F93][EMOJI:5165]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF0C][EMOJI:4F7F][EMOJI:7528][EMOJI:73B0][EMOJI:6709][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]")
                    api_key = current_env
                    api_key_source = "env"
        else:
            api_key = self.ask_input(f"[EMOJI:8BF7][EMOJI:8F93][EMOJI:5165]{env_var}[EMOJI:FF08][EMOJI:5C06][EMOJI:4FDD][EMOJI:5B58][EMOJI:4E3A][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:FF09]", password=True)
            if api_key:
                self._set_environment_variable(env_var, api_key)
                api_key_source = "env"
            else:
                print("[EMOJI:672A][EMOJI:8F93][EMOJI:5165]API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF0C][EMOJI:8DF3][EMOJI:8FC7][EMOJI:5343][EMOJI:95EE][EMOJI:914D][EMOJI:7F6E]")
                return None
        
        # [EMOJI:914D][EMOJI:7F6E][EMOJI:4E24][EMOJI:4E2A][EMOJI:5343][EMOJI:95EE][EMOJI:6A21][EMOJI:578B]
        models_to_setup = []
        
        if self.ask_yes_no("[EMOJI:914D][EMOJI:7F6E][EMOJI:5343][EMOJI:95EE] 3.5 Plus[EMOJI:FF08][EMOJI:901A][EMOJI:7528][EMOJI:6A21][EMOJI:578B][EMOJI:FF09][EMOJI:FF1F]", default=True):
            models_to_setup.append(("qwen35", "qwen3.5-plus", "[EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1]", 2))
        
        if self.ask_yes_no("[EMOJI:914D][EMOJI:7F6E][EMOJI:5343][EMOJI:95EE] Coder Next[EMOJI:FF08][EMOJI:6280][EMOJI:672F][EMOJI:6A21][EMOJI:578B][EMOJI:FF09][EMOJI:FF1F]", default=True):
            models_to_setup.append(("qwen_coder", "qwen3-coder-next", "[EMOJI:6280][EMOJI:672F][EMOJI:4EFB][EMOJI:52A1]", 3))
        
        configs = {}
        for model_id, model_name, description, priority in models_to_setup:
            configs[model_id] = {
                "provider": "bailian",
                "model": model_name,
                "api_key": api_key,
                "api_key_source": api_key_source,
                "enabled": True,
                "priority": priority,
                "cost_per_1k_tokens": 0.00,  # [EMOJI:514D][EMOJI:8D39]
                "capabilities": [description, "[EMOJI:56FE][EMOJI:50CF][EMOJI:8BC6][EMOJI:522B]", "[EMOJI:4E2D][EMOJI:6587][EMOJI:4F18][EMOJI:5316]"]
            }
        
        return configs if configs else None
    
    def setup_custom_model(self) -> Optional[Dict]:
        """[EMOJI:914D][EMOJI:7F6E][EMOJI:81EA][EMOJI:5B9A][EMOJI:4E49][EMOJI:6A21][EMOJI:578B]"""
        self.print_header("[EMOJI:914D][EMOJI:7F6E][EMOJI:81EA][EMOJI:5B9A][EMOJI:4E49][EMOJI:6A21][EMOJI:578B]")
        
        if not self.ask_yes_no("[EMOJI:662F][EMOJI:5426][EMOJI:914D][EMOJI:7F6E][EMOJI:81EA][EMOJI:5B9A][EMOJI:4E49][EMOJI:6A21][EMOJI:578B][EMOJI:FF1F]", default=False):
            return None
        
        model_name = self.ask_input("[EMOJI:6A21][EMOJI:578B][EMOJI:540D][EMOJI:79F0][EMOJI:FF08][EMOJI:82F1][EMOJI:6587][EMOJI:6807][EMOJI:8BC6][EMOJI:FF09]", "custom_model")
        display_name = self.ask_input("[EMOJI:663E][EMOJI:793A][EMOJI:540D][EMOJI:79F0]", model_name)
        provider = self.ask_input("[EMOJI:63D0][EMOJI:4F9B][EMOJI:5546]", "openai")
        model_id = self.ask_input("[EMOJI:6A21][EMOJI:578B]ID", "gpt-4")
        
        # API[EMOJI:914D][EMOJI:7F6E]
        print("\nAPI[EMOJI:914D][EMOJI:7F6E]")
        print("1. [EMOJI:76F4][EMOJI:63A5][EMOJI:8F93][EMOJI:5165]API[EMOJI:5BC6][EMOJI:94A5]")
        print("2. [EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]")
        print("3. [EMOJI:81EA][EMOJI:5B9A][EMOJI:4E49][EMOJI:7AEF][EMOJI:70B9]")
        
        choice = self.ask_input("[EMOJI:9009][EMOJI:62E9][EMOJI:914D][EMOJI:7F6E][EMOJI:65B9][EMOJI:5F0F] [1/2/3]", "1")
        
        api_key = None
        endpoint = None
        api_key_source = "inline"
        
        if choice == "1":
            api_key = self.ask_input("API[EMOJI:5BC6][EMOJI:94A5]", password=True)
        elif choice == "2":
            env_var = self.ask_input("[EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:540D]", f"{model_name.upper()}_API_KEY")
            api_key = os.getenv(env_var)
            if not api_key:
                api_key = self.ask_input(f"[EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF] {env_var} [EMOJI:672A][EMOJI:8BBE][EMOJI:7F6E][EMOJI:FF0C][EMOJI:8BF7][EMOJI:8F93][EMOJI:5165][EMOJI:503C]", password=True)
                if api_key:
                    self._set_environment_variable(env_var, api_key)
            api_key_source = "env"
        elif choice == "3":
            endpoint = self.ask_input("API[EMOJI:7AEF][EMOJI:70B9]URL", "https://api.example.com/v1")
            api_key = self.ask_input("API[EMOJI:5BC6][EMOJI:94A5][EMOJI:FF08][EMOJI:5982][EMOJI:679C][EMOJI:9700][EMOJI:8981][EMOJI:FF09]", password=True)
        
        # [EMOJI:6210][EMOJI:672C][EMOJI:914D][EMOJI:7F6E]
        cost = self.ask_input("[EMOJI:6BCF]1K tokens[EMOJI:6210][EMOJI:672C][EMOJI:FF08][EMOJI:7F8E][EMOJI:5143][EMOJI:FF09]", "1.50")
        try:
            cost_per_1k = float(cost)
        except:
            cost_per_1k = 1.50
            print(f"[EMOJI:65E0][EMOJI:6548][EMOJI:7684][EMOJI:6210][EMOJI:672C][EMOJI:8F93][EMOJI:5165][EMOJI:FF0C][EMOJI:4F7F][EMOJI:7528][EMOJI:9ED8][EMOJI:8BA4][EMOJI:503C] {cost_per_1k}")
        
        # [EMOJI:80FD][EMOJI:529B][EMOJI:63CF][EMOJI:8FF0]
        capabilities_input = self.ask_input("[EMOJI:80FD][EMOJI:529B][EMOJI:63CF][EMOJI:8FF0][EMOJI:FF08][EMOJI:9017][EMOJI:53F7][EMOJI:5206][EMOJI:9694][EMOJI:FF09]", "[EMOJI:901A][EMOJI:7528][EMOJI:4EFB][EMOJI:52A1]")
        capabilities = [c.strip() for c in capabilities_input.split(",")]
        
        # [EMOJI:6784][EMOJI:5EFA][EMOJI:914D][EMOJI:7F6E]
        config = {
            model_name: {
                "provider": provider,
                "model": model_id,
                "api_key": api_key,
                "api_key_source": api_key_source,
                "endpoint": endpoint,
                "enabled": True,
                "priority": 10,  # [EMOJI:81EA][EMOJI:5B9A][EMOJI:4E49][EMOJI:6A21][EMOJI:578B][EMOJI:4F18][EMOJI:5148][EMOJI:7EA7][EMOJI:8F83][EMOJI:4F4E]
                "cost_per_1k_tokens": cost_per_1k,
                "capabilities": capabilities,
                "display_name": display_name
            }
        }
        
        return config
    
    def _set_environment_variable(self, var_name: str, value: str):
        """[EMOJI:8BBE][EMOJI:7F6E][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:FF08][EMOJI:5C1D][EMOJI:8BD5][EMOJI:5199][EMOJI:5165]shell[EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6][EMOJI:FF09]"""
        print(f"[EMOJI:8BBE][EMOJI:7F6E][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF] {var_name}")
        
        # [EMOJI:8BBE][EMOJI:7F6E][EMOJI:5F53][EMOJI:524D][EMOJI:8FDB][EMOJI:7A0B][EMOJI:7684][EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF]
        os.environ[var_name] = value
        
        # [EMOJI:5C1D][EMOJI:8BD5][EMOJI:5199][EMOJI:5165]shell[EMOJI:914D][EMOJI:7F6E][EMOJI:6587][EMOJI:4EF6]
        home = Path.home()
        shell_files = [
            home / ".bashrc",
            home / ".bash_profile",
            home / ".zshrc",
            home / ".profile"
        ]
        
        for shell_file in shell_files:
            if shell_file.exists():
                try:
                    with open(shell_file, 'a') as f:
                        f.write(f'\n# TS-Prompt-Optimizer API Key\n')
                        f.write(f'export {var_name}="{value}"\n')
                    print(f"[EMOJI:5DF2][EMOJI:6DFB][EMOJI:52A0][EMOJI:5230] {shell_file}")
                    print(f"[EMOJI:8BF7][EMOJI:8FD0][EMOJI:884C] 'source {shell_file}' [EMOJI:6216][EMOJI:91CD][EMOJI:65B0][EMOJI:6253][EMOJI:5F00][EMOJI:7EC8][EMOJI:7AEF]")
                    break
                except Exception as e:
                    print(f"[EMOJI:65E0][EMOJI:6CD5][EMOJI:5199][EMOJI:5165] {shell_file}: {e}")
        
        print(f"[EMOJI:73AF][EMOJI:5883][EMOJI:53D8][EMOJI:91CF][EMOJI:5DF2][EMOJI:8BBE][EMOJI:7F6E][EMOJI:FF0C][EMOJI:5F53][EMOJI:524D][EMOJI:4F1A][EMOJI:8BDD][EMOJI:6709][EMOJI:6548]")
    
    def _test_deepseek_connection(self, api_key: str) -> bool:
        """[EMOJI:6D4B][EMOJI:8BD5]DeepSeek[EMOJI:8FDE][EMOJI:63A5]"""
        print("[EMOJI:6D4B][EMOJI:8BD5]DeepSeek API[EMOJI:8FDE][EMOJI:63A5]...")
        try:
            # [EMOJI:7B80][EMOJI:5355][EMOJI:6D4B][EMOJI:8BD5][EMOJI:FF1A][EMOJI:5C1D][EMOJI:8BD5][EMOJI:5BFC][EMOJI:5165][EMOJI:548C][EMOJI:6D4B][EMOJI:8BD5]
            # [EMOJI:8FD9][EMOJI:91CC][EMOJI:53EF][EMOJI:4EE5][EMOJI:6DFB][EMOJI:52A0][EMOJI:5B9E][EMOJI:9645][EMOJI:7684]API[EMOJI:6D4B][EMOJI:8BD5][EMOJI:4EE3][EMOJI:7801]
            # [EMOJI:6682][EMOJI:65F6][EMOJI:6A21][EMOJI:62DF][EMOJI:6210][EMOJI:529F]
            import time
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[EMOJI:8FDE][EMOJI:63A5][EMOJI:6D4B][EMOJI:8BD5][EMOJI:5931][EMOJI:8D25]: {e}")
            return False
    
    def run_wizard(self):
        """[EMOJI:8FD0][EMOJI:884C][EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC]"""
        self.clear_screen()
        self.print_header("[EMOJI:6B22][EMOJI:8FCE][EMOJI:4F7F][EMOJI:7528]")
        
        print("[EMOJI:6B22][EMOJI:8FCE][EMOJI:4F7F][EMOJI:7528]TS-Prompt-Optimizer[EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC][EMOJI:FF01]")
        print("[EMOJI:6211][EMOJI:5C06][EMOJI:5F15][EMOJI:5BFC][EMOJI:60A8][EMOJI:5B8C][EMOJI:6210][EMOJI:591A][EMOJI:6A21][EMOJI:578B]API[EMOJI:7684][EMOJI:914D][EMOJI:7F6E][EMOJI:3002]")
        print("\n[EMOJI:914D][EMOJI:7F6E][EMOJI:5B8C][EMOJI:6210][EMOJI:540E][EMOJI:FF0C][EMOJI:60A8][EMOJI:5C06][EMOJI:53EF][EMOJI:4EE5][EMOJI:FF1A]")
        print("[EMOJI:4F7F][EMOJI:7528]DeepSeek[EMOJI:5904][EMOJI:7406][EMOJI:65E5][EMOJI:5E38][EMOJI:4EFB][EMOJI:52A1][EMOJI:FF08][EMOJI:6210][EMOJI:672C][EMOJI:4F4E][EMOJI:FF09]")
        print("[EMOJI:4F7F][EMOJI:7528][EMOJI:5343][EMOJI:95EE][EMOJI:5904][EMOJI:7406][EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1][EMOJI:FF08][EMOJI:514D][EMOJI:8D39][EMOJI:989D][EMOJI:5EA6][EMOJI:FF09]")
        print("[EMOJI:667A][EMOJI:80FD][EMOJI:8DEF][EMOJI:7531][EMOJI:9009][EMOJI:62E9][EMOJI:6700][EMOJI:4F18][EMOJI:6A21][EMOJI:578B]")
        print("[EMOJI:4EAB][EMOJI:53D7][EMOJI:5B8C][EMOJI:5168][EMOJI:81EA][EMOJI:52A8][EMOJI:5316][EMOJI:7684][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD][EMOJI:4F18][EMOJI:5316]")
        
        input("\n[EMOJI:6309]Enter[EMOJI:952E][EMOJI:7EE7][EMOJI:7EED]...")
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:5F53][EMOJI:524D][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]
        self.clear_screen()
        self.print_header("[EMOJI:5F53][EMOJI:524D][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]")
        
        status = self.config_manager.check_config_status()
        print(f"[EMOJI:53D1][EMOJI:73B0] {status['total_models']} [EMOJI:4E2A][EMOJI:6A21][EMOJI:578B][EMOJI:FF0C]{status['configured_models']} [EMOJI:4E2A][EMOJI:5DF2][EMOJI:914D][EMOJI:7F6E]")
        
        if status['issues']:
            print("\n[EMOJI:53D1][EMOJI:73B0][EMOJI:914D][EMOJI:7F6E][EMOJI:95EE][EMOJI:9898]:")
            for issue in status['issues']:
                print(f"  {issue}")
        
        input("\n[EMOJI:6309]Enter[EMOJI:952E][EMOJI:5F00][EMOJI:59CB][EMOJI:914D][EMOJI:7F6E]...")
        
        # [EMOJI:5F00][EMOJI:59CB][EMOJI:914D][EMOJI:7F6E]
        config_updates = {}
        
        # [EMOJI:914D][EMOJI:7F6E]DeepSeek
        self.clear_screen()
        deepseek_config = self.setup_deepseek()
        if deepseek_config:
            config_updates["deepseek"] = deepseek_config
        
        # [EMOJI:914D][EMOJI:7F6E][EMOJI:5343][EMOJI:95EE]
        self.clear_screen()
        qwen_config = self.setup_qwen()
        if qwen_config:
            if isinstance(qwen_config, dict):
                # [EMOJI:591A][EMOJI:4E2A][EMOJI:5343][EMOJI:95EE][EMOJI:6A21][EMOJI:578B]
                for model_id, config in qwen_config.items():
                    config_updates[model_id] = config
            else:
                config_updates["qwen35"] = qwen_config
        
        # [EMOJI:914D][EMOJI:7F6E][EMOJI:81EA][EMOJI:5B9A][EMOJI:4E49][EMOJI:6A21][EMOJI:578B]
        self.clear_screen()
        custom_config = self.setup_custom_model()
        if custom_config:
            config_updates.update(custom_config)
        
        # [EMOJI:4FDD][EMOJI:5B58][EMOJI:914D][EMOJI:7F6E]
        if config_updates:
            self.clear_screen()
            self.print_header("[EMOJI:4FDD][EMOJI:5B58][EMOJI:914D][EMOJI:7F6E]")
            
            print("[EMOJI:5C06][EMOJI:4FDD][EMOJI:5B58][EMOJI:4EE5][EMOJI:4E0B][EMOJI:914D][EMOJI:7F6E]:")
            for model_id, config in config_updates.items():
                provider = config.get("provider", "unknown")
                model = config.get("model", "unknown")
                enabled = "[EMOJI:5DF2][EMOJI:542F][EMOJI:7528]" if config.get("enabled", False) else "[EMOJI:672A][EMOJI:542F][EMOJI:7528]"
                print(f"  {model_id}: {provider}/{model} ({enabled})")
            
            if self.ask_yes_no("\n[EMOJI:662F][EMOJI:5426][EMOJI:4FDD][EMOJI:5B58][EMOJI:914D][EMOJI:7F6E][EMOJI:FF1F]", default=True):
                # [EMOJI:4FDD][EMOJI:5B58][EMOJI:6BCF][EMOJI:4E2A][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]
                for model_id, config in config_updates.items():
                    success = self.config_manager.update_model_config(model_id, config)
                    if success:
                        print(f"{model_id} [EMOJI:914D][EMOJI:7F6E][EMOJI:5DF2][EMOJI:4FDD][EMOJI:5B58]")
                    else:
                        print(f"{model_id} [EMOJI:914D][EMOJI:7F6E][EMOJI:4FDD][EMOJI:5B58][EMOJI:5931][EMOJI:8D25]")
                
                print("\n[EMOJI:914D][EMOJI:7F6E][EMOJI:5B8C][EMOJI:6210][EMOJI:FF01]")
            else:
                print("\n[EMOJI:914D][EMOJI:7F6E][EMOJI:5DF2][EMOJI:53D6][EMOJI:6D88]")
        else:
            print("\n[EMOJI:672A][EMOJI:8FDB][EMOJI:884C][EMOJI:4EFB][EMOJI:4F55][EMOJI:914D][EMOJI:7F6E][EMOJI:66F4][EMOJI:6539]")
        
        # [EMOJI:663E][EMOJI:793A][EMOJI:6700][EMOJI:7EC8][EMOJI:72B6][EMOJI:6001]
        self.clear_screen()
        self.print_header("[EMOJI:914D][EMOJI:7F6E][EMOJI:5B8C][EMOJI:6210]")
        
        final_status = self.config_manager.check_config_status()
        print("[EMOJI:6700][EMOJI:7EC8][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]:")
        print(f"  [EMOJI:603B][EMOJI:6A21][EMOJI:578B][EMOJI:6570]: {final_status['total_models']}")
        print(f"  [EMOJI:5DF2][EMOJI:914D][EMOJI:7F6E][EMOJI:6A21][EMOJI:578B]: {final_status['configured_models']}")
        print(f"  [EMOJI:542F][EMOJI:7528][EMOJI:6A21][EMOJI:578B]: {final_status['enabled_models']}")
        
        print("\n[EMOJI:53EF][EMOJI:7528][EMOJI:6A21][EMOJI:578B]:")
        for model_name, model_status in final_status['models'].items():
            if model_status['enabled'] and model_status['api_key_configured']:
                status_text = "[[EMOJI:53EF][EMOJI:7528]]"
            elif model_status['enabled']:
                status_text = "[[EMOJI:542F][EMOJI:7528][EMOJI:4F46][EMOJI:672A][EMOJI:914D][EMOJI:7F6E]]"
            else:
                status_text = "[[EMOJI:7981][EMOJI:7528]]"
            
            print(f"  {model_name}: {model_status['provider']}/{model_status['model']} {status_text}")
        
        print("\n[EMOJI:4F7F][EMOJI:7528][EMOJI:8BF4][EMOJI:660E]:")
        print("  1. [EMOJI:5728][EMOJI:6D88][EMOJI:606F][EMOJI:524D][EMOJI:6DFB][EMOJI:52A0] 'ts:' [EMOJI:4F7F][EMOJI:7528][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD][EMOJI:4F18][EMOJI:5316]")
        print("  2. [EMOJI:7CFB][EMOJI:7EDF][EMOJI:4F1A][EMOJI:81EA][EMOJI:52A8][EMOJI:9009][EMOJI:62E9][EMOJI:6700][EMOJI:4F18][EMOJI:6A21][EMOJI:578B]")
        print("  3. [EMOJI:8FD0][EMOJI:884C] 'python config_manager.py status' [EMOJI:67E5][EMOJI:770B][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]")
        print("  4. [EMOJI:8FD0][EMOJI:884C] 'python config_manager.py test' [EMOJI:6D4B][EMOJI:8BD5][EMOJI:6240][EMOJI:6709][EMOJI:6A21][EMOJI:578B]")
        
        print("\n[EMOJI:63D0][EMOJI:793A]:")
        print("  [EMOJI:65E5][EMOJI:5E38][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F1A][EMOJI:81EA][EMOJI:52A8][EMOJI:4F7F][EMOJI:7528]DeepSeek[EMOJI:FF08][EMOJI:6210][EMOJI:672C][EMOJI:4F4E][EMOJI:FF09]")
        print("  [EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F1A][EMOJI:81EA][EMOJI:52A8][EMOJI:4F7F][EMOJI:7528][EMOJI:5343][EMOJI:95EE][EMOJI:FF08][EMOJI:514D][EMOJI:8D39][EMOJI:FF09]")
        print("  [EMOJI:6240][EMOJI:6709][EMOJI:64CD][EMOJI:4F5C][EMOJI:5B8C][EMOJI:5168][EMOJI:81EA][EMOJI:52A8][EMOJI:5316][EMOJI:FF0C][EMOJI:65E0][EMOJI:9700][EMOJI:624B][EMOJI:52A8][EMOJI:5207][EMOJI:6362]")
        
        print("\n" + "=" * 60)
        print("TS-Prompt-Optimizer [EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC][EMOJI:5B8C][EMOJI:6210][EMOJI:FF01]")
        print("=" * 60)

def main():
    """[EMOJI:4E3B][EMOJI:51FD][EMOJI:6570]"""
    try:
        wizard = TSConfigWizard()
        wizard.run_wizard()
    except KeyboardInterrupt:
        print("\n[EMOJI:914D][EMOJI:7F6E][EMOJI:5DF2][EMOJI:53D6][EMOJI:6D88]")
        sys.exit(1)
    except Exception as e:
        print(f"\n[EMOJI:914D][EMOJI:7F6E][EMOJI:8FC7][EMOJI:7A0B][EMOJI:4E2D][EMOJI:53D1][EMOJI:751F][EMOJI:9519][EMOJI:8BEF]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
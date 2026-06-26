#!/usr/bin/env python3
"""
TS-Prompt-Optimizer [EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5DE5][EMOJI:5177]
[EMOJI:63D0][EMOJI:4F9B][EMOJI:4FBF][EMOJI:6377][EMOJI:7684][EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:63A5][EMOJI:53E3]
"""

import os
import sys
import argparse
from pathlib import Path

# [EMOJI:6DFB][EMOJI:52A0][EMOJI:811A][EMOJI:672C][EMOJI:8DEF][EMOJI:5F84]
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """[EMOJI:4E3B][EMOJI:51FD][EMOJI:6570]"""
    parser = argparse.ArgumentParser(
        description="TS-Prompt-Optimizer [EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5DE5][EMOJI:5177]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
[EMOJI:4F7F][EMOJI:7528][EMOJI:793A][EMOJI:4F8B]:
  ts-config status          # [EMOJI:67E5][EMOJI:770B][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]
  ts-config setup           # [EMOJI:8FD0][EMOJI:884C][EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC]
  ts-config test            # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:6240][EMOJI:6709][EMOJI:6A21][EMOJI:578B]
  ts-config optimize "[EMOJI:4EFB][EMOJI:52A1]" # [EMOJI:4F18][EMOJI:5316][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]
  ts-config check           # [EMOJI:68C0][EMOJI:67E5][EMOJI:914D][EMOJI:7F6E][EMOJI:95EE][EMOJI:9898]
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="[EMOJI:547D][EMOJI:4EE4]")
    
    # status [EMOJI:547D][EMOJI:4EE4]
    status_parser = subparsers.add_parser("status", help="[EMOJI:67E5][EMOJI:770B][EMOJI:914D][EMOJI:7F6E][EMOJI:72B6][EMOJI:6001]")
    
    # setup [EMOJI:547D][EMOJI:4EE4]
    setup_parser = subparsers.add_parser("setup", help="[EMOJI:8FD0][EMOJI:884C][EMOJI:914D][EMOJI:7F6E][EMOJI:5411][EMOJI:5BFC]")
    
    # test [EMOJI:547D][EMOJI:4EE4]
    test_parser = subparsers.add_parser("test", help="[EMOJI:6D4B][EMOJI:8BD5][EMOJI:6240][EMOJI:6709][EMOJI:6A21][EMOJI:578B][EMOJI:8FDE][EMOJI:63A5]")
    
    # optimize [EMOJI:547D][EMOJI:4EE4]
    optimize_parser = subparsers.add_parser("optimize", help="[EMOJI:4F18][EMOJI:5316][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]")
    optimize_parser.add_argument("input", help="[EMOJI:8981][EMOJI:4F18][EMOJI:5316][EMOJI:7684][EMOJI:8F93][EMOJI:5165][EMOJI:6587][EMOJI:672C]")
    optimize_parser.add_argument("--type", help="[EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B] (technical/writing/analysis/creative/general)")
    optimize_parser.add_argument("--level", default="standard", help="[EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B] (minimal/standard/full)")
    
    # check [EMOJI:547D][EMOJI:4EE4]
    check_parser = subparsers.add_parser("check", help="[EMOJI:68C0][EMOJI:67E5][EMOJI:914D][EMOJI:7F6E][EMOJI:95EE][EMOJI:9898]")
    
    # show [EMOJI:547D][EMOJI:4EE4]
    show_parser = subparsers.add_parser("show", help="[EMOJI:663E][EMOJI:793A][EMOJI:5B8C][EMOJI:6574][EMOJI:914D][EMOJI:7F6E]")
    
    # get [EMOJI:547D][EMOJI:4EE4]
    get_parser = subparsers.add_parser("get", help="[EMOJI:83B7][EMOJI:53D6][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]")
    get_parser.add_argument("model", help="[EMOJI:6A21][EMOJI:578B][EMOJI:540D][EMOJI:79F0]")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "status":
            from config_manager import TSConfigManager
            config_manager = TSConfigManager()
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
                if model_status['enabled'] and model_status['api_key_configured']:
                    status_text = "[[EMOJI:53EF][EMOJI:7528]]"
                elif model_status['enabled']:
                    status_text = "[[EMOJI:542F][EMOJI:7528][EMOJI:4F46][EMOJI:672A][EMOJI:914D][EMOJI:7F6E]]"
                else:
                    status_text = "[[EMOJI:7981][EMOJI:7528]]"
                
                print(f"  {model_name}: {model_status['provider']}/{model_status['model']} {status_text}")
        
        elif args.command == "setup":
            from config_wizard import TSConfigWizard
            wizard = TSConfigWizard()
            wizard.run_wizard()
        
        elif args.command == "test":
            from config_manager import TSConfigManager
            config_manager = TSConfigManager()
            
            print("[EMOJI:6D4B][EMOJI:8BD5][EMOJI:6A21][EMOJI:578B][EMOJI:8FDE][EMOJI:63A5]...")
            print("=" * 60)
            
            config = config_manager.load_config()
            models = config.get("models", {})
            
            for model_id, model_config in models.items():
                if model_config.get("enabled", False):
                    available = config_manager.is_model_available(model_id)
                    status = "[EMOJI:53EF][EMOJI:7528]" if available else "[EMOJI:4E0D][EMOJI:53EF][EMOJI:7528]"
                    provider = model_config.get("provider", "unknown")
                    model_name = model_config.get("model", "unknown")
                    
                    print(f"{model_id}: {provider}/{model_name} - {status}")
            
            print("\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:5B8C][EMOJI:6210]")
        
        elif args.command == "optimize":
            from optimizer import TSPromptOptimizer
            optimizer = TSPromptOptimizer()
            
            result = optimizer.optimize_prompt(
                args.input, 
                args.type, 
                args.level
            )
            
            print("[EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]")
            print("=" * 60)
            print(f"[EMOJI:539F][EMOJI:59CB][EMOJI:8F93][EMOJI:5165]: {result['original_input']}")
            print(f"[EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]: {result['task_type']}")
            print(f"[EMOJI:590D][EMOJI:6742][EMOJI:5EA6]: {result['complexity']}")
            print(f"[EMOJI:63A8][EMOJI:8350][EMOJI:6A21][EMOJI:578B]: {result['recommended_model']}")
            print(f"[EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B]: {result['optimization_level']}")
            print("\n[EMOJI:4F18][EMOJI:5316][EMOJI:540E][EMOJI:7684][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]:")
            print("=" * 60)
            print(result['optimized_prompt'])
            print("=" * 60)
        
        elif args.command == "check":
            from config_manager import TSConfigManager
            config_manager = TSConfigManager()
            status = config_manager.check_config_status()
            
            # [EMOJI:68C0][EMOJI:67E5][EMOJI:5173][EMOJI:952E][EMOJI:6A21][EMOJI:578B]
            critical_models = ["deepseek", "qwen35"]
            all_ok = True
            
            for model in critical_models:
                if model in status['models']:
                    model_status = status['models'][model]
                    if model_status['api_key_configured']:
                        print(f"{model}: [EMOJI:914D][EMOJI:7F6E][EMOJI:6B63][EMOJI:5E38]")
                    else:
                        print(f"{model}: [EMOJI:672A][EMOJI:914D][EMOJI:7F6E]API[EMOJI:5BC6][EMOJI:94A5]")
                        all_ok = False
                else:
                    print(f"{model}: [EMOJI:672A][EMOJI:5728][EMOJI:914D][EMOJI:7F6E][EMOJI:4E2D][EMOJI:627E][EMOJI:5230]")
                    all_ok = False
            
            if all_ok:
                print("\n[EMOJI:6240][EMOJI:6709][EMOJI:5173][EMOJI:952E][EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E][EMOJI:6B63][EMOJI:5E38][EMOJI:FF01]")
            else:
                print("\n[EMOJI:8BF7][EMOJI:8FD0][EMOJI:884C] 'ts-config setup' [EMOJI:8BBE][EMOJI:7F6E][EMOJI:7F3A][EMOJI:5931][EMOJI:7684]API[EMOJI:5BC6][EMOJI:94A5]")
        
        elif args.command == "show":
            from config_manager import TSConfigManager
            import json
            config_manager = TSConfigManager()
            config = config_manager.load_config()
            print(json.dumps(config, ensure_ascii=False, indent=2))
        
        elif args.command == "get":
            from config_manager import TSConfigManager
            import json
            config_manager = TSConfigManager()
            config = config_manager.get_model_config(args.model)
            if config:
                print(json.dumps(config, ensure_ascii=False, indent=2))
            else:
                print(f"[EMOJI:672A][EMOJI:627E][EMOJI:5230][EMOJI:6A21][EMOJI:578B] {args.model} [EMOJI:7684][EMOJI:914D][EMOJI:7F6E]")
        
    except ImportError as e:
        print(f"[EMOJI:9519][EMOJI:8BEF][EMOJI:FF1A][EMOJI:65E0][EMOJI:6CD5][EMOJI:5BFC][EMOJI:5165][EMOJI:6A21][EMOJI:5757]: {e}")
        print("[EMOJI:8BF7][EMOJI:786E][EMOJI:4FDD][EMOJI:5728][EMOJI:6B63][EMOJI:786E][EMOJI:7684][EMOJI:76EE][EMOJI:5F55][EMOJI:4E2D][EMOJI:8FD0][EMOJI:884C]")
        sys.exit(1)
    except Exception as e:
        print(f"[EMOJI:9519][EMOJI:8BEF][EMOJI:FF1A]{e}")
        sys.exit(1)

if __name__ == "__main__":
    # [EMOJI:521B][EMOJI:5EFA][EMOJI:7B26][EMOJI:53F7][EMOJI:94FE][EMOJI:63A5][EMOJI:6216][EMOJI:6279][EMOJI:5904][EMOJI:7406][EMOJI:6587][EMOJI:4EF6][EMOJI:7684][EMOJI:66FF][EMOJI:4EE3][EMOJI:65B9][EMOJI:6848]
    # [EMOJI:5728]Windows[EMOJI:4E0A][EMOJI:FF0C][EMOJI:6211][EMOJI:4EEC][EMOJI:53EF][EMOJI:4EE5][EMOJI:521B][EMOJI:5EFA][EMOJI:6279][EMOJI:5904][EMOJI:7406][EMOJI:6587][EMOJI:4EF6]
    main()
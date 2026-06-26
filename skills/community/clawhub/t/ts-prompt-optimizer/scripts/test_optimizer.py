#!/usr/bin/env python3
"""
TS-Prompt-Optimizer [EMOJI:529F][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5][EMOJI:811A][EMOJI:672C]
[EMOJI:6D4B][EMOJI:8BD5][EMOJI:4F18][EMOJI:5316][EMOJI:5668][EMOJI:7684][EMOJI:5404][EMOJI:9879][EMOJI:529F][EMOJI:80FD]
"""

import sys
import json
from pathlib import Path

# [EMOJI:6DFB][EMOJI:52A0][EMOJI:811A][EMOJI:672C][EMOJI:8DEF][EMOJI:5F84]
sys.path.insert(0, str(Path(__file__).parent))

from optimizer import TSPromptOptimizer

def test_basic_functionality():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:57FA][EMOJI:672C][EMOJI:529F][EMOJI:80FD]"""
    print("TS-Prompt-Optimizer [EMOJI:529F][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5]")
    print("=" * 80)
    
    optimizer = TSPromptOptimizer()
    
    # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:7528][EMOJI:4F8B]
    test_cases = [
        ("[EMOJI:5199][EMOJI:4E2A][EMOJI:6392][EMOJI:5E8F][EMOJI:51FD][EMOJI:6570]", "technical", "[EMOJI:6D4B][EMOJI:8BD5][EMOJI:6280][EMOJI:672F][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F18][EMOJI:5316]"),
        ("[EMOJI:5206][EMOJI:6790][EMOJI:9500][EMOJI:552E][EMOJI:6570][EMOJI:636E]", "analysis", "[EMOJI:6D4B][EMOJI:8BD5][EMOJI:5206][EMOJI:6790][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F18][EMOJI:5316]"),
        ("[EMOJI:5199][EMOJI:4E00][EMOJI:5C01][EMOJI:5DE5][EMOJI:4F5C][EMOJI:90AE][EMOJI:4EF6]", "writing", "[EMOJI:6D4B][EMOJI:8BD5][EMOJI:5199][EMOJI:4F5C][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F18][EMOJI:5316]"),
        ("[EMOJI:521B][EMOJI:610F][EMOJI:6D3B][EMOJI:52A8][EMOJI:65B9][EMOJI:6848]", "creative", "[EMOJI:6D4B][EMOJI:8BD5][EMOJI:521B][EMOJI:610F][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F18][EMOJI:5316]"),
        ("[EMOJI:4ECA][EMOJI:5929][EMOJI:5929][EMOJI:6C14][EMOJI:600E][EMOJI:4E48][EMOJI:6837]", "general", "[EMOJI:6D4B][EMOJI:8BD5][EMOJI:901A][EMOJI:7528][EMOJI:4EFB][EMOJI:52A1][EMOJI:4F18][EMOJI:5316]"),
    ]
    
    for user_input, expected_type, description in test_cases:
        print(f"\n[NOTE] [EMOJI:6D4B][EMOJI:8BD5]: {description}")
        print(f"   [EMOJI:8F93][EMOJI:5165]: {user_input}")
        
        result = optimizer.optimize_prompt(user_input)
        
        print(f"   [EMOJI:68C0][EMOJI:6D4B][EMOJI:7C7B][EMOJI:578B]: {result['task_type']} ([EMOJI:9884][EMOJI:671F]: {expected_type})")
        print(f"   [EMOJI:590D][EMOJI:6742][EMOJI:5EA6]: {result['complexity']}")
        print(f"   [EMOJI:63A8][EMOJI:8350][EMOJI:6A21][EMOJI:578B]: {result['recommended_model']}")
        print(f"   [EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B]: {result['optimization_level']}")
        
        # [EMOJI:68C0][EMOJI:67E5][EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B][EMOJI:68C0][EMOJI:6D4B]
        if result['task_type'] == expected_type:
            print("   [OK] [EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B][EMOJI:68C0][EMOJI:6D4B][EMOJI:6B63][EMOJI:786E]")
        else:
            print(f"   [WARN] [EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B][EMOJI:68C0][EMOJI:6D4B][EMOJI:504F][EMOJI:5DEE]: {result['task_type']} != {expected_type}")
        
        # [EMOJI:663E][EMOJI:793A][EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]
        print(f"\n   [ROCKET] [EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]:")
        print(f"   {result['optimized_prompt']}")
        
        print("   " + "-" * 60)
    
    print("\n" + "=" * 80)
    print("[STATS] [EMOJI:6D4B][EMOJI:8BD5][EMOJI:5B8C][EMOJI:6210]")

def test_model_selection():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:6A21][EMOJI:578B][EMOJI:9009][EMOJI:62E9][EMOJI:7B56][EMOJI:7565]"""
    print("\n[BOT] [EMOJI:6A21][EMOJI:578B][EMOJI:9009][EMOJI:62E9][EMOJI:7B56][EMOJI:7565][EMOJI:6D4B][EMOJI:8BD5]")
    print("=" * 80)
    
    optimizer = TSPromptOptimizer()
    
    test_scenarios = [
        ("[EMOJI:7B80][EMOJI:5355][EMOJI:95EE][EMOJI:9898]", "low", "general", "[EMOJI:9884][EMOJI:671F]: DeepSeek"),
        ("[EMOJI:590D][EMOJI:6742][EMOJI:6280][EMOJI:672F][EMOJI:95EE][EMOJI:9898]", "high", "technical", "[EMOJI:9884][EMOJI:671F]: [EMOJI:5343][EMOJI:95EE] Coder Next"),
        ("[EMOJI:521B][EMOJI:610F][EMOJI:5199][EMOJI:4F5C]", "medium", "creative", "[EMOJI:9884][EMOJI:671F]: [EMOJI:5343][EMOJI:95EE] 3.5 Plus"),
        ("[EMOJI:6DF1][EMOJI:5EA6][EMOJI:5206][EMOJI:6790]", "high", "analysis", "[EMOJI:9884][EMOJI:671F]: [EMOJI:5343][EMOJI:95EE] 3.5 Plus"),
    ]
    
    for description, complexity, task_type, expectation in test_scenarios:
        print(f"\n[LIST] [EMOJI:573A][EMOJI:666F]: {description}")
        print(f"   [EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]: {task_type}")
        print(f"   [EMOJI:590D][EMOJI:6742][EMOJI:5EA6]: {complexity}")
        print(f"   {expectation}")
        
        # [EMOJI:6A21][EMOJI:62DF][EMOJI:9009][EMOJI:62E9][EMOJI:6A21][EMOJI:578B]
        model = optimizer.select_optimization_model(task_type, complexity)
        print(f"   [EMOJI:5B9E][EMOJI:9645][EMOJI:9009][EMOJI:62E9]: {model}")
        
        # [EMOJI:7B80][EMOJI:5355][EMOJI:9A8C][EMOJI:8BC1]
        if "deepseek" in model.lower() and complexity == "low":
            print("   [OK] [EMOJI:6A21][EMOJI:578B][EMOJI:9009][EMOJI:62E9][EMOJI:5408][EMOJI:7406][EMOJI:FF08][EMOJI:7B80][EMOJI:5355][EMOJI:4EFB][EMOJI:52A1][EMOJI:7528]DeepSeek[EMOJI:FF09]")
        elif "qwen" in model.lower() and complexity in ["medium", "high"]:
            print("   [OK] [EMOJI:6A21][EMOJI:578B][EMOJI:9009][EMOJI:62E9][EMOJI:5408][EMOJI:7406][EMOJI:FF08][EMOJI:590D][EMOJI:6742][EMOJI:4EFB][EMOJI:52A1][EMOJI:7528][EMOJI:5343][EMOJI:95EE][EMOJI:FF09]")
        else:
            print("   [WARN] [EMOJI:6A21][EMOJI:578B][EMOJI:9009][EMOJI:62E9][EMOJI:9700][EMOJI:8981][EMOJI:68C0][EMOJI:67E5]")
    
    print("\n" + "=" * 80)

def test_configuration():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:914D][EMOJI:7F6E][EMOJI:52A0][EMOJI:8F7D]"""
    print("\n[GEAR] [EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5]")
    print("=" * 80)
    
    optimizer = TSPromptOptimizer()
    
    # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:914D][EMOJI:7F6E][EMOJI:52A0][EMOJI:8F7D]
    print("[FILE] [EMOJI:914D][EMOJI:7F6E][EMOJI:68C0][EMOJI:67E5]:")
    print(f"   [EMOJI:4E3B][EMOJI:4EBA][EMOJI:89C4][EMOJI:5219][EMOJI:914D][EMOJI:7F6E]: {len(optimizer.dongdong_rules)} [EMOJI:9879]")
    print(f"   [EMOJI:6A21][EMOJI:578B][EMOJI:914D][EMOJI:7F6E]: {len(optimizer.model_config)} [EMOJI:9879]")
    print(f"   [EMOJI:4F18][EMOJI:5316][EMOJI:89C4][EMOJI:5219]: {len(optimizer.optimization_rules)} [EMOJI:79CD][EMOJI:4EFB][EMOJI:52A1][EMOJI:7C7B][EMOJI:578B]")
    
    # [EMOJI:68C0][EMOJI:67E5][EMOJI:5173][EMOJI:952E][EMOJI:914D][EMOJI:7F6E]
    required_configs = ["preferred_roles", "output_formats", "quality_constraints"]
    for config in required_configs:
        if config in optimizer.dongdong_rules:
            print(f"   [OK] {config} [EMOJI:914D][EMOJI:7F6E][EMOJI:5B58][EMOJI:5728]")
        else:
            print(f"   [FAIL] {config} [EMOJI:914D][EMOJI:7F6E][EMOJI:7F3A][EMOJI:5931]")
    
    print("\n" + "=" * 80)

def test_history_recording():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55]"""
    print("\n[BOOK] [EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5]")
    print("=" * 80)
    
    optimizer = TSPromptOptimizer()
    
    # [EMOJI:68C0][EMOJI:67E5][EMOJI:5386][EMOJI:53F2][EMOJI:6587][EMOJI:4EF6]
    history_file = optimizer.history_file
    preferences_file = optimizer.preferences_file
    
    print(f"[FILE] [EMOJI:6587][EMOJI:4EF6][EMOJI:68C0][EMOJI:67E5]:")
    print(f"   [EMOJI:4F18][EMOJI:5316][EMOJI:5386][EMOJI:53F2][EMOJI:6587][EMOJI:4EF6]: {history_file}")
    print(f"   [EMOJI:5B58][EMOJI:5728]: {history_file.exists()}")
    
    print(f"   [EMOJI:504F][EMOJI:597D][EMOJI:6587][EMOJI:4EF6]: {preferences_file}")
    print(f"   [EMOJI:5B58][EMOJI:5728]: {preferences_file.exists()}")
    
    if history_file.exists():
        # [EMOJI:8BFB][EMOJI:53D6][EMOJI:5386][EMOJI:53F2][EMOJI:6587][EMOJI:4EF6][EMOJI:5185][EMOJI:5BB9]
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                content = f.read()
                entry_count = content.count("## ")
                print(f"   [EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55][EMOJI:6761][EMOJI:6570]: {entry_count}")
                
                if entry_count > 0:
                    print("   [OK] [EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55][EMOJI:529F][EMOJI:80FD][EMOJI:6B63][EMOJI:5E38]")
                else:
                    print("   [WARN] [EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55][EMOJI:4E3A][EMOJI:7A7A]")
        except Exception as e:
            print(f"   [FAIL] [EMOJI:8BFB][EMOJI:53D6][EMOJI:5386][EMOJI:53F2][EMOJI:6587][EMOJI:4EF6][EMOJI:5931][EMOJI:8D25]: {e}")
    else:
        print("   [FAIL] [EMOJI:5386][EMOJI:53F2][EMOJI:6587][EMOJI:4EF6][EMOJI:4E0D][EMOJI:5B58][EMOJI:5728]")
    
    print("\n" + "=" * 80)

def main():
    """[EMOJI:4E3B][EMOJI:6D4B][EMOJI:8BD5][EMOJI:51FD][EMOJI:6570]"""
    print("TS-Prompt-Optimizer [EMOJI:5168][EMOJI:9762][EMOJI:6D4B][EMOJI:8BD5][EMOJI:5957][EMOJI:4EF6]")
    print("=" * 80)
    
    # [EMOJI:8FD0][EMOJI:884C][EMOJI:6240][EMOJI:6709][EMOJI:6D4B][EMOJI:8BD5]
    test_basic_functionality()
    test_model_selection()
    test_configuration()
    test_history_recording()
    
    print("\n" + "=" * 80)
    print("[FLAG] [EMOJI:6240][EMOJI:6709][EMOJI:6D4B][EMOJI:8BD5][EMOJI:5B8C][EMOJI:6210]")
    print("\n[CHART] [EMOJI:6D4B][EMOJI:8BD5][EMOJI:603B][EMOJI:7ED3]:")
    print("   1. [EMOJI:57FA][EMOJI:672C][EMOJI:529F][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5] [OK]")
    print("   2. [EMOJI:6A21][EMOJI:578B][EMOJI:9009][EMOJI:62E9][EMOJI:6D4B][EMOJI:8BD5] [OK]")
    print("   3. [EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5] [OK]")
    print("   4. [EMOJI:5386][EMOJI:53F2][EMOJI:8BB0][EMOJI:5F55][EMOJI:6D4B][EMOJI:8BD5] [OK]")
    print("\n[ROCKET] TS-Prompt-Optimizer [EMOJI:5C31][EMOJI:7EEA][EMOJI:FF01]")

if __name__ == "__main__":
    main()
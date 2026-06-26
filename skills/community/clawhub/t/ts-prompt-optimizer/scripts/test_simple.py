#!/usr/bin/env python3
"""
TS-Prompt-Optimizer [EMOJI:7B80][EMOJI:5316][EMOJI:6D4B][EMOJI:8BD5][EMOJI:811A][EMOJI:672C]
[EMOJI:4E3A][EMOJI:51AC][EMOJI:51AC][EMOJI:4E3B][EMOJI:4EBA][EMOJI:9A8C][EMOJI:8BC1][EMOJI:6838][EMOJI:5FC3][EMOJI:529F][EMOJI:80FD]
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

# [EMOJI:6DFB][EMOJI:52A0][EMOJI:811A][EMOJI:672C][EMOJI:76EE][EMOJI:5F55][EMOJI:5230][EMOJI:8DEF][EMOJI:5F84]
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

def test_prefix_detection():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:524D][EMOJI:7F00][EMOJI:68C0][EMOJI:6D4B]"""
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5]1[EMOJI:FF1A][EMOJI:524D][EMOJI:7F00][EMOJI:68C0][EMOJI:6D4B][EMOJI:673A][EMOJI:5236]")
    print("=" * 60)
    
    test_cases = [
        ("ts: [EMOJI:7B80][EMOJI:5355][EMOJI:6D4B][EMOJI:8BD5]", True, "ts[EMOJI:524D][EMOJI:7F00]"),
        ("ts-opt: [EMOJI:4E2D][EMOJI:7B49][EMOJI:6D4B][EMOJI:8BD5]", True, "ts-opt[EMOJI:524D][EMOJI:7F00]"),
        ("[EMOJI:4F18][EMOJI:5316]: [EMOJI:4E2D][EMOJI:6587][EMOJI:6D4B][EMOJI:8BD5]", True, "[EMOJI:4F18][EMOJI:5316][EMOJI:524D][EMOJI:7F00]"),
        ("[EMOJI:65E0][EMOJI:524D][EMOJI:7F00][EMOJI:6D4B][EMOJI:8BD5]", False, "[EMOJI:65E0][EMOJI:524D][EMOJI:7F00]"),
        ("ts: ", True, "ts[EMOJI:524D][EMOJI:7F00][EMOJI:7A7A][EMOJI:5185][EMOJI:5BB9]"),
    ]
    
    results = []
    for input_text, should_trigger, description in test_cases:
        # [EMOJI:7B80][EMOJI:5355][EMOJI:524D][EMOJI:7F00][EMOJI:68C0][EMOJI:6D4B][EMOJI:903B][EMOJI:8F91]
        should_optimize = False
        prefixes = ["ts:", "ts-opt:", "[EMOJI:4F18][EMOJI:5316]:"]
        for prefix in prefixes:
            if input_text.startswith(prefix):
                should_optimize = True
                break
        
        passed = (should_optimize == should_trigger)
        status = "[EMOJI:901A][EMOJI:8FC7]" if passed else "[EMOJI:5931][EMOJI:8D25]"
        
        print(f"  {description}: {input_text[:20]}...")
        print(f"    [EMOJI:9884][EMOJI:671F][EMOJI:89E6][EMOJI:53D1]: {should_trigger}, [EMOJI:5B9E][EMOJI:9645][EMOJI:68C0][EMOJI:6D4B]: {should_optimize}")
        print(f"    [EMOJI:72B6][EMOJI:6001]: {status}")
        
        results.append(passed)
    
    return all(results)

def test_optimizer_basic():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:4F18][EMOJI:5316][EMOJI:5668][EMOJI:57FA][EMOJI:672C][EMOJI:529F][EMOJI:80FD]"""
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5]2[EMOJI:FF1A][EMOJI:4F18][EMOJI:5316][EMOJI:5668][EMOJI:57FA][EMOJI:672C][EMOJI:529F][EMOJI:80FD]")
    print("=" * 60)
    
    try:
        from optimizer import TSPromptOptimizer
        optimizer = TSPromptOptimizer()
        
        test_inputs = [
            "ts: [EMOJI:5199][EMOJI:4E2A]Python[EMOJI:51FD][EMOJI:6570]",
            "ts-opt: [EMOJI:5206][EMOJI:6790][EMOJI:6570][EMOJI:636E]",
            "[EMOJI:4F18][EMOJI:5316]: [EMOJI:521B][EMOJI:610F][EMOJI:5199][EMOJI:4F5C]",
        ]
        
        results = []
        for input_text in test_inputs:
            print(f"  [EMOJI:6D4B][EMOJI:8BD5][EMOJI:8F93][EMOJI:5165]: {input_text}")
            
            start_time = time.time()
            optimized = optimizer.optimize_prompt(input_text)
            response_time = time.time() - start_time
            
            # [EMOJI:68C0][EMOJI:67E5][EMOJI:57FA][EMOJI:672C][EMOJI:8F93][EMOJI:51FA]
            has_output = result is not None
            if isinstance(result, dict):
                contains_optimization = 'optimized_prompt' in result
                output_text = result.get('optimized_prompt', '')
            else:
                contains_optimization = "[EMOJI:4F18][EMOJI:5316]" in str(result) or "[EMOJI:4F18][EMOJI:5316][EMOJI:62A5][EMOJI:544A]" in str(result)
                output_text = str(result)
            
            passed = has_output and contains_optimization
            status = "[EMOJI:901A][EMOJI:8FC7]" if passed else "[EMOJI:5931][EMOJI:8D25]"
            
            print(f"    [EMOJI:6709][EMOJI:8F93][EMOJI:51FA]: {'[EMOJI:662F]' if has_output else '[EMOJI:5426]'}")
            print(f"    [EMOJI:5305][EMOJI:542B][EMOJI:4F18][EMOJI:5316]: {'[EMOJI:662F]' if contains_optimization else '[EMOJI:5426]'}")
            print(f"    [EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4]: {response_time:.3f}[EMOJI:79D2]")
            print(f"    [EMOJI:72B6][EMOJI:6001]: {status}")
            
            results.append(passed)
        
        return all(results)
        
    except Exception as e:
        print(f"  [EMOJI:4F18][EMOJI:5316][EMOJI:5668][EMOJI:6D4B][EMOJI:8BD5][EMOJI:5931][EMOJI:8D25]: {e}")
        return False

def test_config_system():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF]"""
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5]3[EMOJI:FF1A][EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:9A8C][EMOJI:8BC1]")
    print("=" * 60)
    
    try:
        from config_manager_fixed import TSConfigManager
        config_manager = TSConfigManager()
        
        # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:914D][EMOJI:7F6E][EMOJI:52A0][EMOJI:8F7D]
        config = config_manager.load_config()
        has_models = "models" in config and len(config["models"]) > 0
        print(f"  [EMOJI:914D][EMOJI:7F6E][EMOJI:52A0][EMOJI:8F7D]: {'[EMOJI:6210][EMOJI:529F]' if has_models else '[EMOJI:5931][EMOJI:8D25]'}")
        
        # [EMOJI:6D4B][EMOJI:8BD5][EMOJI:72B6][EMOJI:6001][EMOJI:68C0][EMOJI:67E5]
        status = config_manager.check_config_status()
        has_status = "total_models" in status
        print(f"  [EMOJI:72B6][EMOJI:6001][EMOJI:68C0][EMOJI:67E5]: {'[EMOJI:6210][EMOJI:529F]' if has_status else '[EMOJI:5931][EMOJI:8D25]'}")
        
        # [EMOJI:663E][EMOJI:793A][EMOJI:914D][EMOJI:7F6E][EMOJI:6458][EMOJI:8981]
        print(f"  [EMOJI:603B][EMOJI:6A21][EMOJI:578B][EMOJI:6570]: {status.get('total_models', 0)}")
        print(f"  [EMOJI:5DF2][EMOJI:914D][EMOJI:7F6E][EMOJI:6A21][EMOJI:578B]: {status.get('configured_models', 0)}")
        print(f"  [EMOJI:542F][EMOJI:7528][EMOJI:6A21][EMOJI:578B]: {status.get('enabled_models', 0)}")
        
        passed = has_models and has_status
        status_text = "[EMOJI:901A][EMOJI:8FC7]" if passed else "[EMOJI:5931][EMOJI:8D25]"
        
        print(f"  [EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5]: {status_text}")
        
        return passed
        
    except Exception as e:
        print(f"  [EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6D4B][EMOJI:8BD5][EMOJI:5931][EMOJI:8D25]: {e}")
        return False

def test_command_line():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5DE5][EMOJI:5177]"""
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5]4[EMOJI:FF1A][EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5DE5][EMOJI:5177][EMOJI:9A8C][EMOJI:8BC1]")
    print("=" * 60)
    
    try:
        # [EMOJI:6D4B][EMOJI:8BD5]status[EMOJI:547D][EMOJI:4EE4]
        cmd = ["python", str(script_dir / "ts_config.py"), "status"]
        print(f"  [EMOJI:6267][EMOJI:884C][EMOJI:547D][EMOJI:4EE4]: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"    [EMOJI:6267][EMOJI:884C][EMOJI:6210][EMOJI:529F][EMOJI:FF0C][EMOJI:8F93][EMOJI:51FA][EMOJI:957F][EMOJI:5EA6]: {len(result.stdout)} [EMOJI:5B57][EMOJI:7B26]")
            print(f"    [EMOJI:8F93][EMOJI:51FA][EMOJI:6458][EMOJI:8981]: {result.stdout[:100]}...")
            return True
        else:
            print(f"    [EMOJI:6267][EMOJI:884C][EMOJI:5931][EMOJI:8D25][EMOJI:FF0C][EMOJI:8FD4][EMOJI:56DE][EMOJI:7801]: {result.returncode}")
            if result.stderr:
                print(f"    [EMOJI:9519][EMOJI:8BEF][EMOJI:8F93][EMOJI:51FA]: {result.stderr[:100]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"    [EMOJI:547D][EMOJI:4EE4][EMOJI:8D85][EMOJI:65F6]")
        return False
    except Exception as e:
        print(f"    [EMOJI:6267][EMOJI:884C][EMOJI:5F02][EMOJI:5E38]: {e}")
        return False

def test_optimization_workflow():
    """[EMOJI:6D4B][EMOJI:8BD5][EMOJI:5B8C][EMOJI:6574][EMOJI:4F18][EMOJI:5316][EMOJI:5DE5][EMOJI:4F5C][EMOJI:6D41]"""
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5]5[EMOJI:FF1A][EMOJI:5B8C][EMOJI:6574][EMOJI:4F18][EMOJI:5316][EMOJI:5DE5][EMOJI:4F5C][EMOJI:6D41]")
    print("=" * 60)
    
    test_cases = [
        ("ts: [EMOJI:5199][EMOJI:4E2A][EMOJI:6392][EMOJI:5E8F][EMOJI:7B97][EMOJI:6CD5]", "[EMOJI:6280][EMOJI:672F][EMOJI:4EFB][EMOJI:52A1]"),
        ("ts-opt: [EMOJI:8BBE][EMOJI:8BA1][EMOJI:4EA7][EMOJI:54C1][EMOJI:9875][EMOJI:9762]", "[EMOJI:521B][EMOJI:610F][EMOJI:4EFB][EMOJI:52A1]"),
        ("[EMOJI:4F18][EMOJI:5316]: [EMOJI:603B][EMOJI:7ED3][EMOJI:6587][EMOJI:7AE0][EMOJI:8981][EMOJI:70B9]", "[EMOJI:5206][EMOJI:6790][EMOJI:4EFB][EMOJI:52A1]"),
    ]
    
    from optimizer import TSPromptOptimizer
    optimizer = TSPromptOptimizer()
    
    results = []
    for input_text, description in test_cases:
        print(f"  [EMOJI:6D4B][EMOJI:8BD5]: {description} - {input_text}")
        
        try:
            start_time = time.time()
            optimized = optimizer.optimize_prompt(input_text)
            response_time = time.time() - start_time
            
            # [EMOJI:5206][EMOJI:6790][EMOJI:4F18][EMOJI:5316][EMOJI:7ED3][EMOJI:679C]
            if isinstance(result, dict):
                lines = []
                for key, value in result.items():
                    if isinstance(value, str):
                        lines.append(f"{key}: {value}")
                    elif isinstance(value, list):
                        lines.append(f"{key}: {', '.join(value)}")
                    else:
                        lines.append(f"{key}: {value}")
                result_text = '\n'.join(lines)
            else:
                result_text = str(result)
            
            lines = result_text.split('\n')
            has_analysis = any("[EMOJI:4F18][EMOJI:5316][EMOJI:62A5][EMOJI:544A]" in line or "[EMOJI:68C0][EMOJI:6D4B][EMOJI:7C7B][EMOJI:578B]" in line or "task_type" in line for line in lines)
            has_recommendation = any("[EMOJI:63A8][EMOJI:8350][EMOJI:6A21][EMOJI:578B]" in line or "[EMOJI:4F18][EMOJI:5316][EMOJI:7EA7][EMOJI:522B]" in line or "recommended_model" in line for line in lines)
            has_optimized_prompt = any("[EMOJI:4F18][EMOJI:5316][EMOJI:540E][EMOJI:7684][EMOJI:63D0][EMOJI:793A][EMOJI:8BCD]" in line or "[EMOJI:4F5C][EMOJI:4E3A]" in line or "optimized_prompt" in line for line in lines)
            
            quality_score = sum([has_analysis, has_recommendation, has_optimized_prompt])
            passed = quality_score >= 2  # [EMOJI:81F3][EMOJI:5C11][EMOJI:6EE1][EMOJI:8DB3]2[EMOJI:4E2A][EMOJI:6761][EMOJI:4EF6]
            
            status = "[EMOJI:901A][EMOJI:8FC7]" if passed else "[EMOJI:5931][EMOJI:8D25]"
            
            print(f"    [EMOJI:5206][EMOJI:6790][EMOJI:62A5][EMOJI:544A]: {'[EMOJI:6709]' if has_analysis else '[EMOJI:65E0]'}")
            print(f"    [EMOJI:6A21][EMOJI:578B][EMOJI:63A8][EMOJI:8350]: {'[EMOJI:6709]' if has_recommendation else '[EMOJI:65E0]'}")
            print(f"    [EMOJI:4F18][EMOJI:5316][EMOJI:63D0][EMOJI:793A]: {'[EMOJI:6709]' if has_optimized_prompt else '[EMOJI:65E0]'}")
            print(f"    [EMOJI:8D28][EMOJI:91CF][EMOJI:5206][EMOJI:6570]: {quality_score}/3")
            print(f"    [EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4]: {response_time:.3f}[EMOJI:79D2]")
            print(f"    [EMOJI:72B6][EMOJI:6001]: {status}")
            
            results.append(passed)
            
        except Exception as e:
            print(f"    [EMOJI:4F18][EMOJI:5316][EMOJI:5931][EMOJI:8D25]: {e}")
            results.append(False)
    
    return all(results)

def run_performance_test():
    """[EMOJI:8FD0][EMOJI:884C][EMOJI:6027][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5]"""
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5]6[EMOJI:FF1A][EMOJI:6027][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5]")
    print("=" * 60)
    
    from optimizer import TSPromptOptimizer
    optimizer = TSPromptOptimizer()
    
    test_inputs = [
        "ts: [EMOJI:7B80][EMOJI:5355][EMOJI:6D4B][EMOJI:8BD5]",
        "ts: [EMOJI:4E2D][EMOJI:7B49][EMOJI:590D][EMOJI:6742][EMOJI:5EA6][EMOJI:6D4B][EMOJI:8BD5]",
        "ts: [EMOJI:8FD9][EMOJI:662F][EMOJI:4E00][EMOJI:4E2A][EMOJI:9700][EMOJI:8981][EMOJI:9A8C][EMOJI:8BC1][EMOJI:7CFB][EMOJI:7EDF][EMOJI:6027][EMOJI:80FD][EMOJI:7684][EMOJI:6D4B][EMOJI:8BD5][EMOJI:7528][EMOJI:4F8B]",
    ]
    
    response_times = []
    
    for i, input_text in enumerate(test_inputs, 1):
        print(f"  [EMOJI:6D4B][EMOJI:8BD5] {i}: {input_text[:30]}...")
        
        # [EMOJI:6B63][EMOJI:5F0F][EMOJI:6D4B][EMOJI:8BD5]
        start_time = time.time()
        optimizer.optimize_prompt(input_text)
        end_time = time.time()
        
        response_time = end_time - start_time
        response_times.append(response_time)
        
        print(f"    [EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4]: {response_time:.3f}[EMOJI:79D2]")
    
    # [EMOJI:8BA1][EMOJI:7B97][EMOJI:7EDF][EMOJI:8BA1]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print(f"\n  [EMOJI:6027][EMOJI:80FD][EMOJI:7EDF][EMOJI:8BA1]:")
        print(f"    [EMOJI:5E73][EMOJI:5747][EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4]: {avg_time:.3f}[EMOJI:79D2]")
        print(f"    [EMOJI:6700][EMOJI:77ED][EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4]: {min_time:.3f}[EMOJI:79D2]")
        print(f"    [EMOJI:6700][EMOJI:957F][EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4]: {max_time:.3f}[EMOJI:79D2]")
        print(f"    [EMOJI:6D4B][EMOJI:8BD5][EMOJI:6B21][EMOJI:6570]: {len(response_times)}")
        
        # [EMOJI:6027][EMOJI:80FD][EMOJI:6807][EMOJI:51C6][EMOJI:FF1A][EMOJI:5E73][EMOJI:5747][EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4] < 3[EMOJI:79D2]
        performance_passed = avg_time < 3.0
        print(f"    [EMOJI:6027][EMOJI:80FD][EMOJI:8BC4][EMOJI:4F30]: {'[EMOJI:901A][EMOJI:8FC7]' if performance_passed else '[EMOJI:5931][EMOJI:8D25]'} ([EMOJI:6807][EMOJI:51C6]: <3[EMOJI:79D2])")
        
        return performance_passed
    else:
        print("  [EMOJI:65E0][EMOJI:6709][EMOJI:6548][EMOJI:54CD][EMOJI:5E94][EMOJI:65F6][EMOJI:95F4][EMOJI:6570][EMOJI:636E]")
        return False

def main():
    """[EMOJI:4E3B][EMOJI:6D4B][EMOJI:8BD5][EMOJI:51FD][EMOJI:6570]"""
    print("TS-Prompt-Optimizer [EMOJI:6838][EMOJI:5FC3][EMOJI:529F][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5]")
    print("=" * 60)
    print("[EMOJI:4E3A][EMOJI:51AC][EMOJI:51AC][EMOJI:4E3B][EMOJI:4EBA][EMOJI:9A8C][EMOJI:8BC1][EMOJI:6838][EMOJI:5FC3][EMOJI:529F][EMOJI:80FD]...")
    
    # [EMOJI:8FD0][EMOJI:884C][EMOJI:6240][EMOJI:6709][EMOJI:6D4B][EMOJI:8BD5]
    test_results = []
    
    test_results.append(("[EMOJI:524D][EMOJI:7F00][EMOJI:68C0][EMOJI:6D4B]", test_prefix_detection()))
    test_results.append(("[EMOJI:4F18][EMOJI:5316][EMOJI:5668][EMOJI:57FA][EMOJI:672C][EMOJI:529F][EMOJI:80FD]", test_optimizer_basic()))
    test_results.append(("[EMOJI:914D][EMOJI:7F6E][EMOJI:7CFB][EMOJI:7EDF]", test_config_system()))
    test_results.append(("[EMOJI:547D][EMOJI:4EE4][EMOJI:884C][EMOJI:5DE5][EMOJI:5177]", test_command_line()))
    test_results.append(("[EMOJI:4F18][EMOJI:5316][EMOJI:5DE5][EMOJI:4F5C][EMOJI:6D41]", test_optimization_workflow()))
    test_results.append(("[EMOJI:6027][EMOJI:80FD][EMOJI:6D4B][EMOJI:8BD5]", run_performance_test()))
    
    # [EMOJI:6C47][EMOJI:603B][EMOJI:7ED3][EMOJI:679C]
    print("\n" + "=" * 60)
    print("[EMOJI:6D4B][EMOJI:8BD5][EMOJI:7ED3][EMOJI:679C][EMOJI:6C47][EMOJI:603B]")
    print("=" * 60)
    
    passed_count = 0
    total_count = len(test_results)
    
    for test_name, passed in test_results:
        status = "[EMOJI:901A][EMOJI:8FC7]" if passed else "[EMOJI:5931][EMOJI:8D25]"
        symbol = "[OK]" if passed else "[FAIL]"
        print(f"  {symbol} {test_name}: {status}")
        
        if passed:
            passed_count += 1
    
    # [EMOJI:603B][EMOJI:4F53][EMOJI:8BC4][EMOJI:4F30]
    success_rate = (passed_count / total_count) * 100 if total_count > 0 else 0
    
    print("\n" + "=" * 60)
    print("[EMOJI:603B][EMOJI:4F53][EMOJI:8BC4][EMOJI:4F30]")
    print("=" * 60)
    print(f"  [EMOJI:603B][EMOJI:6D4B][EMOJI:8BD5][EMOJI:6570]: {total_count}")
    print(f"  [EMOJI:901A][EMOJI:8FC7][EMOJI:6570]: {passed_count}")
    print(f"  [EMOJI:5931][EMOJI:8D25][EMOJI:6570]: {total_count - passed_count}")
    print(f"  [EMOJI:6210][EMOJI:529F][EMOJI:7387]: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:7ED3][EMOJI:679C]: [EMOJI:4F18][EMOJI:79C0][EMOJI:FF01]TS-Prompt-Optimizer [EMOJI:6838][EMOJI:5FC3][EMOJI:529F][EMOJI:80FD][EMOJI:5B8C][EMOJI:6574]")
        print("[EMOJI:5EFA][EMOJI:8BAE]: [EMOJI:53EF][EMOJI:4EE5][EMOJI:5F00][EMOJI:59CB][EMOJI:5168][EMOJI:9762][EMOJI:8BD5][EMOJI:7528]")
    elif success_rate >= 60:
        print("\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:7ED3][EMOJI:679C]: [EMOJI:826F][EMOJI:597D][EMOJI:FF01][EMOJI:4E3B][EMOJI:8981][EMOJI:529F][EMOJI:80FD][EMOJI:6B63][EMOJI:5E38]")
        print("[EMOJI:5EFA][EMOJI:8BAE]: [EMOJI:53EF][EMOJI:4EE5][EMOJI:8BD5][EMOJI:7528][EMOJI:FF0C][EMOJI:6CE8][EMOJI:610F][EMOJI:89C2][EMOJI:5BDF][EMOJI:5931][EMOJI:8D25][EMOJI:9879]")
    else:
        print("\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:7ED3][EMOJI:679C]: [EMOJI:9700][EMOJI:8981][EMOJI:6539][EMOJI:8FDB]")
        print("[EMOJI:5EFA][EMOJI:8BAE]: [EMOJI:4F18][EMOJI:5148][EMOJI:4FEE][EMOJI:590D][EMOJI:6838][EMOJI:5FC3][EMOJI:529F][EMOJI:80FD][EMOJI:95EE][EMOJI:9898]")
    
    # [EMOJI:751F][EMOJI:6210][EMOJI:6D4B][EMOJI:8BD5][EMOJI:62A5][EMOJI:544A]
    report = {
        "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total_count,
        "passed_tests": passed_count,
        "failed_tests": total_count - passed_count,
        "success_rate": success_rate,
        "test_results": {name: passed for name, passed in test_results},
        "recommendation": "[EMOJI:53EF][EMOJI:4EE5][EMOJI:8BD5][EMOJI:7528]" if success_rate >= 60 else "[EMOJI:9700][EMOJI:8981][EMOJI:4FEE][EMOJI:590D]"
    }
    
    # [EMOJI:4FDD][EMOJI:5B58][EMOJI:6D4B][EMOJI:8BD5][EMOJI:62A5][EMOJI:544A]
    report_file = script_dir / "test_report_simple.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:62A5][EMOJI:544A][EMOJI:5DF2][EMOJI:4FDD][EMOJI:5B58]: {report_file}")
    
    return success_rate >= 60

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:88AB][EMOJI:7528][EMOJI:6237][EMOJI:4E2D][EMOJI:65AD]")
        sys.exit(1)
    except Exception as e:
        print(f"\n[EMOJI:6D4B][EMOJI:8BD5][EMOJI:6267][EMOJI:884C][EMOJI:5F02][EMOJI:5E38]: {e}")
        sys.exit(1)
"""
tests/run_tests.py - 简易测试运行器
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.test_cases import load_test_case, list_test_cases
from ziwei_verify import calibrate, run


def run_test_case(case_id: str, verbose: bool = True) -> dict:
    """
    运行单个测试案例
    
    返回：测试结果字典
    """
    case = load_test_case(case_id)
    if not case:
        return {"case_id": case_id, "status": "ERROR", "error": "测试案例不存在"}
    
    input_packet = case["input"]
    params = case.get("parameters", {})
    expected = case.get("expected", {})
    
    # 准备参数
    birth_dt_str = input_packet["data"]["birth_info"]["birth_dt"]
    from ziwei_verify.utils import parse_birth_datetime
    birth_dt = parse_birth_datetime(birth_dt_str)
    
    max_shifts = params.get("max_shifts", 2)
    interactive = params.get("interactive", False)
    
    # 执行
    start = datetime.utcnow()
    try:
        result = calibrate(
            packet=input_packet,
            birth_dt=birth_dt,
            max_shifts=max_shifts,
            interactive=interactive
        )
    except Exception as e:
        result = {"status": "ERROR", "error": str(e)}
    elapsed = (datetime.utcnow() - start).total_seconds()
    
    # 验证
    passed = True
    failures = []
    
    if expected:
        if "status" in expected and result.get("status") != expected["status"]:
            passed = False
            failures.append(f"状态不匹配: 期望 {expected['status']}, 实际 {result.get('status')}")
        
        if "confidence_min" in expected:
            conf = result.get("confidence", 0)
            if conf < expected["confidence_min"]:
                passed = False
                failures.append(f"置信度过低: {conf} < {expected['confidence_min']}")
        
        if "candidates_count" in expected:
            count = len(result.get("data", {}).get("candidates", []))
            if count != expected["candidates_count"]:
                passed = False
                failures.append(f"候选数量不匹配: {count} != {expected['candidates_count']}")
    
    test_result = {
        "case_id": case_id,
        "description": case.get("description", ""),
        "status": "PASS" if passed else "FAIL",
        "elapsed_seconds": round(elapsed, 4),
        "failures": failures,
        "result_status": result.get("status"),
        "result_confidence": result.get("confidence")
    }
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"案例: {case_id} - {case.get('description', '')}")
        print(f"结果: {'✅ PASS' if passed else '❌ FAIL'}")
        print(f"耗时: {elapsed:.3f}s")
        if failures:
            for f in failures:
                print(f"  - {f}")
    
    return test_result


def run_all_tests(verbose: bool = True) -> list:
    """运行所有测试案例"""
    results = []
    case_ids = list_test_cases()
    
    if verbose:
        print(f"开始运行 {len(case_ids)} 个测试案例...")
    
    for cid in case_ids:
        result = run_test_case(cid, verbose=verbose)
        results.append(result)
    
    # 汇总
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed
    
    print(f"\n{'='*60}")
    print(f"测试完成: {passed}/{total} 通过, {failed} 失败")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ziwei_verify 测试运行器")
    parser.add_argument("--case", help="运行单个测试案例ID")
    parser.add_argument("--all", action="store_true", help="运行所有案例")
    parser.add_argument("--quiet", action="store_true", help="静默模式")
    args = parser.parse_args()
    
    if args.case:
        run_test_case(args.case, verbose=not args.quiet)
    elif args.all or len(sys.argv) == 1:
        run_all_tests(verbose=not args.quiet)
    else:
        parser.print_help()

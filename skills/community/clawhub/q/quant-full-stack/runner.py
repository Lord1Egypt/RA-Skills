#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 股票量化全流程技能执行器
"""
import sys
import os
import json
import subprocess

# 固定路径配置，无需修改
HOME_DIR = os.path.expanduser("~")
VENV_PYTHON = os.path.join(HOME_DIR, "quant_trading", "venv", "bin", "python3")
PROJECT_DIR = os.path.join(HOME_DIR, "quant_trading")

def run_quant_script(task_num, script_name, args):
    """执行量化模块脚本"""
    try:
        script_path = os.path.join(PROJECT_DIR, task_num, script_name)
        if not os.path.exists(script_path):
            return {"status": "error", "error": f"脚本不存在：{script_path}"}
        
        # 构造执行命令
        cmd = [VENV_PYTHON, script_path] + args
        # 执行命令，超时2分钟，避免卡死
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_DIR
        )
        
        if result.returncode == 0:
            return {"status": "success", "result": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": f"执行失败：{str(e)}"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "help": "使用方法: python3 runner.py [任务编号] [命令] [参数]",
            "task_map": {
                "01_data_system": "数据体系建设",
                "02_factor_engineering": "Alpha因子挖掘",
                "03_strategy_build": "策略构建",
                "04_backtest_verify": "回测验证",
                "05_trade_execution": "模拟交易",
                "06_risk_iteration": "风险管理"
            }
        }, ensure_ascii=False, indent=2))
        return
    
    # 解析参数
    task_num = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else ""
    args = sys.argv[3:] if len(sys.argv) > 3 else []
    
    # 任务与脚本映射
    script_mapping = {
        "01_data_system": "data_system.py",
        "02_factor_engineering": "factor_engineering.py",
        "03_strategy_build": "strategy_build.py",
        "04_backtest_verify": "backtest_verify.py",
        "05_trade_execution": "trade_execution.py",
        "06_risk_iteration": "risk_iteration.py"
    }
    
    if task_num not in script_mapping:
        print(json.dumps({"status": "error", "error": f"未知任务编号：{task_num}"}, ensure_ascii=False))
        return
    
    script_name = script_mapping[task_num]
    full_args = [command] + args if command else args
    result = run_quant_script(task_num, script_name, full_args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

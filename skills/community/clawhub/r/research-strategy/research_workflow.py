#!/usr/bin/env python3
"""
Research Strategy 主脚本

功能：
- 监听回测完成
- 自动评估结果
- 自动决策
- 自动移动文件
- 自动记录
- 自动汇报

使用方法：
    python3 research_workflow.py
    
    # 后台运行
    nohup python3 research_workflow.py > logs/research_workflow.log &
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, '/Users/allenbot/.openclaw/workspace/project/auto-trading')

# 常量
WORKSPACE = '/Users/allenbot/.openclaw/workspace/project/auto-trading'
LOG_FILE = f'{WORKSPACE}/logs/research_workflow.log'
MEMORY_FILE = f'{WORKSPACE}/MEMORY.md'
TEST_DIR = f'{WORKSPACE}/core/strategy/test'
FORMAL_DIR = f'{WORKSPACE}/core/strategy'
REPORTS_DIR = f'{WORKSPACE}/backtest/reports'


def log(message):
    """日志记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[{timestamp}] {message}"
    print(msg)
    with open(LOG_FILE, 'a') as f:
        f.write(msg + '\n')


def get_latest_report():
    """获取最新的回测报告"""
    reports = Path(REPORTS_DIR).glob('*.json')
    reports = sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)
    if reports:
        return str(reports[0])
    return None


def evaluate_result(report_path):
    """评估回测结果"""
    try:
        with open(report_path) as f:
            data = json.load(f)
        
        results = data.get('results', {})
        
        return {
            'strategy': data.get('strategy', ''),
            'coin': data.get('coin', ''),
            'total_return': results.get('total_return', 0),
            'max_drawdown': results.get('max_drawdown', 0),
            'total_trades': results.get('total_trades', 0),
            'win_rate': results.get('win_rate', 0)
        }
    except Exception as e:
        log(f"❌ 评估错误: {e}")
        return None


def decide(result):
    """决策"""
    trades = result['total_trades']
    ret = result['total_return']
    dd = result['max_drawdown']
    
    # 决策规则（简化版，全自主）
    if trades >= 50 and ret > 0:
        return 'MOVE_TO_FORMAL', '交易量达标，收益为正，移到正式文件夹'
    elif trades >= 50 and ret < 0:
        return 'REVERSE_LOGIC', '交易量大但亏损，调换逻辑'
    elif trades < 10:
        return 'ABANDON', '交易量太少，放弃'
    else:
        return 'ABANDON', '其他情况放弃'


def move_to_formal(strategy_name):
    """移动到正式文件夹"""
    src = f'{TEST_DIR}/{strategy_name}.py'
    dst = f'{FORMAL_DIR}/{strategy_name}.py'
    
    if os.path.exists(src):
        os.rename(src, dst)
        return True
    return False


def reverse_logic(strategy_name):
    """调换买卖逻辑"""
    src = f'{TEST_DIR}/{strategy_name}.py'
    
    if not os.path.exists(src):
        return False
    
    with open(src, 'r') as f:
        content = f.read()
    
    # 调换 BUY 和 SELL
    new_content = content.replace('Signal.BUY', 'TEMP_BUY')
    new_content = new_content.replace('Signal.SELL', 'Signal.BUY')
    new_content = new_content.replace('TEMP_BUY', 'Signal.SELL')
    
    # 调换 "BUY" 和 "SELL" 字符串
    new_content = new_content.replace('"BUY"', 'TEMP_BUY')
    new_content = new_content.replace('"SELL"', '"BUY"')
    new_content = new_content.replace('TEMP_BUY', '"SELL"')
    
    with open(src, 'w') as f:
        f.write(new_content)
    
    return True


def record_to_memory(strategy_name, result, decision, reason):
    """记录到 MEMORY.md"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    entry = f"""

## {strategy_name}（{timestamp}）

### 评估结果
- 交易量：{result['total_trades']}
- 回撤：{result['max_drawdown']:.2f}%
- 收益：{result['total_return']:.2f}%
- 结论：{decision} - {reason}

"""
    
    with open(MEMORY_FILE, 'a') as f:
        f.write(entry)
    
    return entry


def report_to_father(result, decision, reason):
    """向爸爸汇报"""
    log(f"\n{'='*60}")
    log(f"📢 向爸爸汇报")
    log(f"{'='*60}")
    log(f"策略：{result['strategy']}")
    log(f"币种：{result['coin']}")
    log(f"交易量：{result['total_trades']}")
    log(f"回撤：{result['max_drawdown']:.2f}%")
    log(f"收益：{result['total_return']:.2f}%")
    log(f"决策：{decision} - {reason}")
    log(f"{'='*60}\n")


def process_report(report_path):
    """处理单个回测报告"""
    log(f"\n📊 检测到新报告: {report_path}")
    
    # 评估
    result = evaluate_result(report_path)
    if not result:
        return
    
    # 决策
    decision, reason = decide(result)
    log(f"📈 评估: {result['strategy']} + {result['coin']}")
    log(f"   交易量: {result['total_trades']} | 收益: {result['total_return']:.2f}% | 回撤: {result['max_drawdown']:.2f}%")
    log(f"   决策: {decision} - {reason}")
    
    # 执行决策
    if decision == 'MOVE_TO_FORMAL':
        if move_to_formal(result['strategy']):
            log(f"✅ 已移到正式文件夹")
    
    elif decision == 'REVERSE_LOGIC':
        if reverse_logic(result['strategy']):
            log(f"🔄 已调换逻辑，等待重新回测")
            # 注意：调换后不会立即重新回测，需要等待
    
    # 记录
    record_to_memory(result['strategy'], result, decision, reason)
    
    # 汇报
    report_to_father(result, decision, reason)


def main():
    """主函数"""
    log(f"\n{'='*60}")
    log(f"🚀 Auto-Coding-Workflow 启动")
    log(f"{'='*60}")
    log(f"工作目录: {WORKSPACE}")
    log(f"监听目录: {REPORTS_DIR}")
    log(f"测试目录: {TEST_DIR}")
    log(f"正式目录: {FORMAL_DIR}")
    log(f"{'='*60}\n")
    
    processed = set()
    
    while True:
        try:
            report = get_latest_report()
            
            if report and report not in processed:
                processed.add(report)
                process_report(report)
            
            time.sleep(30)  # 每 30 秒检查一次
        
        except KeyboardInterrupt:
            log(f"\n🛑 收到中断信号，停止运行")
            break
        except Exception as e:
            log(f"❌ 错误: {e}")
            time.sleep(60)  # 错误时等待更长时间


if __name__ == '__main__':
    main()

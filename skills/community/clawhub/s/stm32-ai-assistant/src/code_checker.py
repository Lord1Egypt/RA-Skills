#!/usr/bin/env python3
"""STM32代码检查器 — 检查HAL代码常见错误"""

import re
from typing import List, Dict


def check_hal_code(code: str) -> List[Dict]:
    """检查HAL代码中的常见问题"""
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # 1. 直接操作寄存器（应该用HAL库）
        if re.search(r'->\w+\s*[|&^]=', stripped) and 'HAL_' not in stripped:
            issues.append({
                'line': i,
                'severity': 'warning',
                'message': '直接操作寄存器，建议使用HAL库函数',
                'code': stripped
            })
        
        # 2. 缺少时钟使能
        if 'GPIO_Init' in stripped or 'HAL_GPIO_Init' in stripped:
            # 检查前面是否有 __HAL_RCC_xxx_CLK_ENABLE
            if i > 5:
                prev = '\n'.join(lines[max(0,i-10):i])
                if 'CLK_ENABLE' not in prev:
                    issues.append({
                        'line': i,
                        'severity': 'error',
                        'message': 'GPIO初始化前需要使能时钟: __HAL_RCC_GPIOx_CLK_ENABLE()',
                        'code': stripped
                    })
        
        # 3. UART波特率过高
        if 'BaudRate' in stripped:
            m = re.search(r'BaudRate\s*=\s*(\d+)', stripped)
            if m and int(m.group(1)) > 115200:
                issues.append({
                    'line': i,
                    'severity': 'warning',
                    'message': f'波特率 {m.group(1)} 较高，可能不稳定，建议 ≤115200',
                    'code': stripped
                })
        
        # 4. I2C缺少上拉
        if 'I2C' in stripped and 'GPIO_InitStruct.Pull' in stripped:
            if 'GPIO_PULLUP' not in stripped and 'PULLUP' not in stripped:
                issues.append({
                    'line': i,
                    'severity': 'warning',
                    'message': 'I2C引脚需要上拉电阻，建议 Pull=GPIO_PULLUP',
                    'code': stripped
                })
        
        # 5. 中断优先级问题
        if 'NVIC_SetPriority' in stripped:
            m = re.search(r'SetPriority\(\w+,\s*(\d+)', stripped)
            if m and int(m.group(1)) > 15:
                issues.append({
                    'line': i,
                    'severity': 'error',
                    'message': f'优先级 {m.group(1)} 超出范围(0-15)，STM32F4只有4位优先级',
                    'code': stripped
                })
        
        # 6. ADC采样时间过短
        if 'SamplingTime' in stripped and 'ADC_SAMPLETIME_3CYCLES' in stripped:
            issues.append({
                'line': i,
                'severity': 'warning',
                'message': '3周期采样时间很短，高精度测量建议用84CYCLES或更长',
                'code': stripped
            })
        
        # 7. DMA方向错误
        if 'Direction' in stripped and 'DMA_PERIPH_TO_MEMORY' in stripped:
            if 'UART_Transmit' in code or 'USART_Transmit' in code:
                issues.append({
                    'line': i,
                    'severity': 'error',
                    'message': 'UART发送应使用 DMA_MEMORY_TO_PERIPH',
                    'code': stripped
                })
        
        # 8. 缺少HAL_Delay
        if 'HAL_UART_Transmit' in stripped and 'IT' not in stripped and 'DMA' not in stripped:
            if 'timeout' in stripped.lower() or 'HAL_MAX_DELAY' in stripped:
                pass  # OK
            else:
                issues.append({
                    'line': i,
                    'severity': 'info',
                    'message': '轮询传输会阻塞，考虑使用中断或DMA模式',
                    'code': stripped
                })
        
        # 9. 未检查返回值
        if 'HAL_' in stripped and '=' in stripped and '==' not in stripped:
            if 'if' not in stripped and 'ret' not in stripped and 'status' not in stripped:
                issues.append({
                    'line': i,
                    'severity': 'info',
                    'message': '建议检查HAL函数返回值: if(HAL_xxx() != HAL_OK)',
                    'code': stripped
                })
        
        # 10. 时钟配置检查
        if 'SystemClock_Config' in stripped:
            if 'RCC_OscInitStruct.PLL.PLLState' not in code:
                issues.append({
                    'line': i,
                    'severity': 'info',
                    'message': '确认PLL配置正确，F407最大168MHz',
                    'code': stripped
                })
    
    return issues


def format_issues(issues: List[Dict]) -> str:
    """格式化检查结果"""
    if not issues:
        return "✅ 代码检查通过，未发现明显问题。"
    
    result = f"发现 {len(issues)} 个潜在问题:\n\n"
    
    errors = [i for i in issues if i['severity'] == 'error']
    warnings = [i for i in issues if i['severity'] == 'warning']
    infos = [i for i in issues if i['severity'] == 'info']
    
    if errors:
        result += "❌ 错误:\n"
        for e in errors:
            result += f"  行{e['line']}: {e['message']}\n"
            result += f"    代码: {e['code'][:80]}\n\n"
    
    if warnings:
        result += "⚠️ 警告:\n"
        for w in warnings:
            result += f"  行{w['line']}: {w['message']}\n"
            result += f"    代码: {w['code'][:80]}\n\n"
    
    if infos:
        result += "💡 建议:\n"
        for info in infos:
            result += f"  行{info['line']}: {info['message']}\n\n"
    
    return result

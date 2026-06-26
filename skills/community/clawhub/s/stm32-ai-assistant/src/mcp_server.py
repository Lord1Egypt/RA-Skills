#!/usr/bin/env python3
"""STM32智能助手 MCP Server — 让AI编码助手理解嵌入式硬件"""
import json
import sys
from pathlib import Path
from typing import Optional

# MCP Server实现（兼容OpenClaw/Claude Code/Codex）
# 提供4个核心工具：
# 1. lookup_register — 查寄存器定义
# 2. generate_code — 自然语言→HAL代码
# 3. list_peripherals — 列出外设信息
# 4. get_peripheral_detail — 获取外设全部寄存器

KNOWLEDGE_DIR = Path(__file__).parent.parent / 'knowledge'
TEMPLATES_DIR = Path(__file__).parent.parent / 'templates'
try:
    from quick_ref import get_quick_ref
except ImportError:
    from src.quick_ref import get_quick_ref
try:
    from code_checker import check_hal_code, format_issues
except ImportError:
    from src.code_checker import check_hal_code, format_issues
try:
    from pin_mapper import find_pins
except ImportError:
    from src.pin_mapper import find_pins


def load_kb(chip: str = 'STM32F407') -> dict:
    """加载知识库"""
    kb_path = KNOWLEDGE_DIR / f'{chip.lower()}_kb.json'
    if not kb_path.exists():
        raise FileNotFoundError(f"知识库不存在: {kb_path}")
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def lookup_register(peripheral: str, register: str, chip: str = 'STM32F407') -> dict:
    """查询寄存器详细信息"""
    kb = load_kb(chip)
    
    # 查找外设（支持大小写模糊匹配）
    pkey = None
    for k in kb['peripherals']:
        if k.upper() == peripheral.upper():
            pkey = k
            break
    
    if not pkey:
        # 尝试从实例名查找外设类型
        for inst_name, inst_info in kb['instances'].items():
            if inst_name.upper() == peripheral.upper():
                pkey = inst_info['type']
                break
    
    if not pkey:
        return {'error': f'未找到外设: {peripheral}', 'available': list(kb['peripherals'].keys())}
    
    pdata = kb['peripherals'][pkey]
    
    # 查找寄存器
    rdata = None
    for reg in pdata['registers']:
        if reg['name'].upper() == register.upper():
            rdata = reg
            break
    
    if not rdata:
        return {
            'error': f'外设 {pkey} 中未找到寄存器: {register}',
            'available_registers': [r['name'] for r in pdata['registers']]
        }
    
    # 构建基地址信息
    instances = {
        name: info for name, info in kb['instances'].items()
        if info['type'] == pkey
    }
    
    return {
        'peripheral': pkey,
        'peripheral_desc': pdata['description'],
        'register': rdata['name'],
        'access': rdata['access'],
        'comment': rdata.get('comment', ''),
        'bits': rdata.get('bits', {}),
        'instances': instances
    }


def list_peripherals(chip: str = 'STM32F407') -> list:
    """列出所有外设"""
    kb = load_kb(chip)
    result = []
    for ptype, pdata in kb['peripherals'].items():
        instances = [k for k, v in kb['instances'].items() if v['type'] == ptype]
        result.append({
            'type': ptype,
            'description': pdata['description'],
            'registers': len(pdata['registers']),
            'instances': instances
        })
    return sorted(result, key=lambda x: x['type'])


def get_peripheral_detail(peripheral: str, chip: str = 'STM32F407') -> dict:
    """获取外设全部寄存器详情"""
    kb = load_kb(chip)
    
    pkey = None
    for k in kb['peripherals']:
        if k.upper() == peripheral.upper():
            pkey = k
            break
    
    if not pkey:
        for inst_name, inst_info in kb['instances'].items():
            if inst_name.upper() == peripheral.upper():
                pkey = inst_info['type']
                break
    
    if not pkey:
        return {'error': f'未找到外设: {peripheral}'}
    
    pdata = kb['peripherals'][pkey]
    instances = {
        name: info for name, info in kb['instances'].items()
        if info['type'] == pkey
    }
    
    return {
        'peripheral': pkey,
        'description': pdata['description'],
        'registers': pdata['registers'],
        'instances': instances
    }


TEMPLATE_MAP = {
    'GPIO': 'gpio_init.c', 'LED': 'gpio_init.c',
    'USART': 'usart_init.c', 'UART': 'usart_init.c', 'SERIAL': 'usart_init.c',
    'TIM': 'tim_pwm_init.c', 'TIMER': 'tim_pwm_init.c', 'PWM': 'tim_pwm_init.c',
    'SPI': 'spi_init.c',
    'I2C': 'i2c_init.c',
    'ADC': 'adc_init.c',
    'EXTI': 'exti_init.c', 'INTERRUPT': 'exti_init.c', 'KEY': 'exti_init.c',
    'DMA': 'dma_init.c',
    'RTC': 'rtc_init.c',
    'IWDG': 'iwdg_init.c', 'WATCHDOG': 'iwdg_init.c',
    'CAN': 'can_init.c',
    'DAC': 'dac_init.c',
    'PWR': 'pwr_init.c',
    'POWER': 'pwr_init.c',
    'FLASH': 'flash_init.c',
    'WWDG': 'wwdg_init.c',
    'CRC': 'crc_init.c',
    'RCC': 'rcc_init.c',
    'KEY': 'gpio_io.c',
    'BUTTON': 'gpio_io.c',
    'SYSTICK': 'systick_init.c',
    'DELAY': 'systick_init.c',
    'FREERTOS': 'freertos_init.c',
    'RTOS': 'freertos_init.c',
    'TASK': 'freertos_init.c',
    'PRINTF': 'printf_init.c',
    'DEBUG': 'printf_init.c',
    'LOG': 'printf_init.c',
    'NVIC': 'nvic_init.c',
    'INTERRUPT': 'nvic_init.c',
    'GPIO_EXTI': 'gpio_exti.c',
    'KEY_EXTI': 'gpio_exti.c',
    'TIM_IC': 'tim_ic.c',
    'INPUT_CAPTURE': 'tim_ic.c',
    'CAPTURE': 'tim_ic.c',
    'ENCODER': 'tim_encoder.c',
    'TIM_ENCODER': 'tim_encoder.c',
    'PWM_INPUT': 'tim_pwm_input.c',
    'TIM_PWM_INPUT': 'tim_pwm_input.c',
    'FREQUENCY': 'tim_pwm_input.c',
    'SPI_DMA': 'spi_dma.c',
    'UART_DMA': 'uart_dma.c',
    'USART_DMA': 'uart_dma.c',
    'I2C_DMA': 'i2c_dma.c',
    'ADC_DMA': 'adc_dma.c',
    'TIM_OC': 'tim_oc.c',
    'OUTPUT_COMPARE': 'tim_oc.c',
    'ONEPULSE': 'tim_onepulse.c',
    'ONE_PULSE': 'tim_onepulse.c',
    'RTC_ALARM': 'rtc_alarm.c',
    'ALARM': 'rtc_alarm.c',
    'LPTIM': 'lptim.c',
    'LOW_POWER': 'lptim.c',
    'STANDBY': 'lptim.c',
    'IWDG_WWDG': 'iwdg_wwdg.c',
    'WATCHDOG_COMPARE': 'iwdg_wwdg.c',
    'RELAY': 'gpio_od_ext.c',
    'BUZZER': 'gpio_od_ext.c',
    'BUZZ': 'gpio_od_ext.c',
    'HALL': 'tim_hall.c',
    'BLDC': 'tim_hall.c',
    'MOTOR': 'tim_hall.c',
    'BITBAND': 'gpio_bitband.c',
    'BIT': 'gpio_bitband.c',
    'EXTCLK': 'tim_extclk.c',
    'COUNTER': 'tim_extclk.c',
    'PULSE_COUNT': 'tim_extclk.c',
    'DAC': 'dac_init.c',
}


def generate_code(peripheral: str, config: str, chip: str = 'STM32F407') -> str:
    """根据自然语言描述生成HAL初始化代码"""
    import re as _re
    
    periph_upper = peripheral.upper()
    template_file = TEMPLATE_MAP.get(periph_upper, f'{peripheral.lower()}_init.c')
    template_path = TEMPLATES_DIR / template_file
    
    if template_path.exists():
        template = template_path.read_text()
        
        # 智能参数替换
        # 引脚替换
        pin_m = _re.search(r'P([A-K])(\d+)', config.upper())
        if pin_m:
            port, pin_num = pin_m.group(1), pin_m.group(2)
            template = template.replace('GPIOA', f'GPIO{port}')
            template = template.replace('PIN_5', f'PIN_{pin_num}')
            template = template.replace('PA5', f'P{port}{pin_num}')
        
        # 波特率替换
        baud_m = _re.search(r'(\d+)\s*(?:波特|baud|bps)', config.lower())
        if baud_m and 'USART' in periph_upper:
            template = template.replace('115200', baud_m.group(1))
        
        # 通道替换
        ch_m = _re.search(r'(?:ch|通道)\s*(\d)', config.lower())
        if ch_m:
            ch = ch_m.group(1)
            template = template.replace('TIM_CHANNEL_1', f'TIM_CHANNEL_{ch}')
        
        # 占空比替换
        duty_m = _re.search(r'(\d+)\s*%', config)
        if duty_m and '占空' in config:
            duty = int(duty_m.group(1))
            pulse = int(999 * duty / 100) - 1
            template = _re.sub(r'Pulse = \d+', f'Pulse = {pulse}', template)
        
        return f"// 基于模板: {peripheral} | 配置: {config}\n\n{template}"
    
    # 无模板时，基于知识库生成框架
    kb = load_kb(chip)
    pkey = None
    for k in kb['peripherals']:
        if k.upper() == peripheral.upper():
            pkey = k
            break
    
    if not pkey:
        return f"// 错误: 未找到外设 {peripheral}"
    
    pdata = kb['peripherals'][pkey]
    code = f"// {pkey} 初始化框架 | {config}\n#include \"stm32f4xx_hal.h\"\n\nvoid {pkey}_Init(void) {{\n"
    for reg in pdata['registers']:
        bits = list(reg.get('bits', {}).keys())[:3]
        hint = f" [{', '.join(bits)}]" if bits else ""
        code += f"    // {pkey}->{reg['name']}{hint}\n"
    code += "}\n"
    return code


# MCP协议处理
def handle_mcp_request(request: dict) -> dict:
    """处理MCP协议请求"""
    method = request.get('method', '')
    params = request.get('params', {})
    req_id = request.get('id')
    
    if method == 'initialize':
        return {
            'jsonrpc': '2.0',
            'id': req_id,
            'result': {
                'protocolVersion': '2024-11-05',
                'capabilities': {'tools': {}},
                'serverInfo': {
                    'name': 'stm32-ai-assistant',
                    'version': '1.0.0'
                }
            }
        }
    
    elif method == 'tools/list':
        return {
            'jsonrpc': '2.0',
            'id': req_id,
            'result': {
                'tools': [
                    {
                        'name': 'lookup_register',
                        'description': '查询STM32外设寄存器的详细定义，包括访问类型、位定义、功能描述',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'peripheral': {'type': 'string', 'description': '外设名称，如 GPIO, USART, TIM'},
                                'register': {'type': 'string', 'description': '寄存器名称，如 MODER, CR1, SR'},
                                'chip': {'type': 'string', 'description': '芯片型号，默认STM32F407'}
                            },
                            'required': ['peripheral', 'register']
                        }
                    },
                    {
                        'name': 'list_peripherals',
                        'description': '列出STM32芯片的所有外设类型、寄存器数量和实例',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'chip': {'type': 'string', 'description': '芯片型号，默认STM32F407'}
                            }
                        }
                    },
                    {
                        'name': 'get_peripheral_detail',
                        'description': '获取指定外设的全部寄存器详情',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'peripheral': {'type': 'string', 'description': '外设名称'},
                                'chip': {'type': 'string', 'description': '芯片型号'}
                            },
                            'required': ['peripheral']
                        }
                    },
                    {
                        'name': 'quick_reference',
                        'description': 'STM32常用操作速查表，包括GPIO模式、USART配置、TIM计算、SPI模式等',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'peripheral': {'type': 'string', 'description': '外设名称，如 GPIO, USART, TIM, SPI, I2C, ADC, RCC'}
                            }
                        }
                    },
                    {
                        'name': 'find_pins',
                        'description': '查找STM32外设的可用引脚和复用功能（支持F407/F103）',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'peripheral': {'type': 'string', 'description': '外设名称，如 USART1, SPI1, I2C1, TIM2'},
                                'signal': {'type': 'string', 'description': '信号名称，如 TX, RX, SCK, MOSI, CH1（可选）'},
                                'chip': {'type': 'string', 'description': '芯片型号，默认STM32F407'}
                            },
                            'required': ['peripheral']
                        }
                    },
                    {
                        'name': 'check_code',
                        'description': '检查STM32 HAL代码的常见错误（缺少时钟使能、优先级超限、DMA方向错误等）',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'code': {'type': 'string', 'description': '要检查的C代码'}
                            },
                            'required': ['code']
                        }
                    },
                    {
                        'name': 'generate_code',
                        'description': '根据自然语言描述生成STM32 HAL初始化代码',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'peripheral': {'type': 'string', 'description': '外设名称，如 GPIO, USART, TIM'},
                                'config': {'type': 'string', 'description': '配置需求描述，如"PA5配置为推挽输出"'},
                                'chip': {'type': 'string', 'description': '芯片型号'}
                            },
                            'required': ['peripheral', 'config']
                        }
                    }
                ]
            }
        }
    
    elif method == 'tools/call':
        tool_name = params.get('name', '')
        args = params.get('arguments', {})
        
        try:
            if tool_name == 'lookup_register':
                result = lookup_register(**args)
            elif tool_name == 'list_peripherals':
                result = list_peripherals(**args)
            elif tool_name == 'get_peripheral_detail':
                result = get_peripheral_detail(**args)
            elif tool_name == 'quick_reference':
                result = get_quick_ref(**args)
            elif tool_name == 'find_pins':
                result = find_pins(**args)
            elif tool_name == 'check_code':
                issues = check_hal_code(args.get('code', ''))
                result = format_issues(issues)
            elif tool_name == 'generate_code':
                result = generate_code(**args)
            else:
                result = {'error': f'未知工具: {tool_name}'}
            
            return {
                'jsonrpc': '2.0',
                'id': req_id,
                'result': {
                    'content': [{'type': 'text', 'text': json.dumps(result, ensure_ascii=False, indent=2)}]
                }
            }
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'id': req_id,
                'result': {
                    'content': [{'type': 'text', 'text': f'错误: {str(e)}'}],
                    'isError': True
                }
            }
    
    return {'jsonrpc': '2.0', 'id': req_id, 'error': {'code': -32601, 'message': f'未知方法: {method}'}}


def main():
    """MCP Server stdio主循环"""
    print("STM32 AI Assistant MCP Server v1.0.0", file=sys.stderr)
    print(f"知识库: {KNOWLEDGE_DIR}", file=sys.stderr)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            request = json.loads(line)
            response = handle_mcp_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError:
            error_resp = {
                'jsonrpc': '2.0',
                'error': {'code': -32700, 'message': 'Parse error'}
            }
            print(json.dumps(error_resp))
            sys.stdout.flush()


if __name__ == '__main__':
    main()

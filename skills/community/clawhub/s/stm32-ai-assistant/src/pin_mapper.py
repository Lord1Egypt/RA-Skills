#!/usr/bin/env python3
"""STM32引脚映射工具 — 根据功能查找可用引脚"""

# STM32F407 引脚复用映射表 (简化版)
# 完整版需要从CMSIS头文件解析
PIN_MAP = {
    'USART1': {
        'TX': [{'pin': 'PA9', 'af': 'AF7'}, {'pin': 'PB6', 'af': 'AF7'}],
        'RX': [{'pin': 'PA10', 'af': 'AF7'}, {'pin': 'PB7', 'af': 'AF7'}],
    },
    'USART2': {
        'TX': [{'pin': 'PA2', 'af': 'AF7'}, {'pin': 'PD5', 'af': 'AF7'}],
        'RX': [{'pin': 'PA3', 'af': 'AF7'}, {'pin': 'PD6', 'af': 'AF7'}],
    },
    'USART3': {
        'TX': [{'pin': 'PB10', 'af': 'AF7'}, {'pin': 'PD8', 'af': 'AF7'}],
        'RX': [{'pin': 'PB11', 'af': 'AF7'}, {'pin': 'PD9', 'af': 'AF7'}],
    },
    'SPI1': {
        'SCK':  [{'pin': 'PA5', 'af': 'AF5'}],
        'MISO': [{'pin': 'PA6', 'af': 'AF5'}],
        'MOSI': [{'pin': 'PA7', 'af': 'AF5'}],
    },
    'SPI2': {
        'SCK':  [{'pin': 'PB13', 'af': 'AF5'}],
        'MISO': [{'pin': 'PB14', 'af': 'AF5'}],
        'MOSI': [{'pin': 'PB15', 'af': 'AF5'}],
    },
    'I2C1': {
        'SCL': [{'pin': 'PB6', 'af': 'AF4'}, {'pin': 'PB8', 'af': 'AF4'}],
        'SDA': [{'pin': 'PB7', 'af': 'AF4'}, {'pin': 'PB9', 'af': 'AF4'}],
    },
    'I2C2': {
        'SCL': [{'pin': 'PB10', 'af': 'AF4'}],
        'SDA': [{'pin': 'PB11', 'af': 'AF4'}],
    },
    'TIM2': {
        'CH1': [{'pin': 'PA0', 'af': 'AF1'}, {'pin': 'PA5', 'af': 'AF1'}, {'pin': 'PA15', 'af': 'AF1'}],
        'CH2': [{'pin': 'PA1', 'af': 'AF1'}, {'pin': 'PB3', 'af': 'AF1'}],
        'CH3': [{'pin': 'PA2', 'af': 'AF1'}, {'pin': 'PB10', 'af': 'AF1'}],
        'CH4': [{'pin': 'PA3', 'af': 'AF1'}, {'pin': 'PB11', 'af': 'AF1'}],
    },
    'TIM3': {
        'CH1': [{'pin': 'PA6', 'af': 'AF2'}, {'pin': 'PB4', 'af': 'AF2'}, {'pin': 'PC6', 'af': 'AF2'}],
        'CH2': [{'pin': 'PA7', 'af': 'AF2'}, {'pin': 'PB5', 'af': 'AF2'}, {'pin': 'PC7', 'af': 'AF2'}],
        'CH3': [{'pin': 'PB0', 'af': 'AF2'}, {'pin': 'PC8', 'af': 'AF2'}],
        'CH4': [{'pin': 'PB1', 'af': 'AF2'}, {'pin': 'PC9', 'af': 'AF2'}],
    },
    'TIM4': {
        'CH1': [{'pin': 'PB6', 'af': 'AF2'}, {'pin': 'PD12', 'af': 'AF2'}],
        'CH2': [{'pin': 'PB7', 'af': 'AF2'}, {'pin': 'PD13', 'af': 'AF2'}],
        'CH3': [{'pin': 'PB8', 'af': 'AF2'}, {'pin': 'PD14', 'af': 'AF2'}],
        'CH4': [{'pin': 'PB9', 'af': 'AF2'}, {'pin': 'PD15', 'af': 'AF2'}],
    },
    
    'TIM5': {
        'CH1': [{'pin': 'PA0', 'af': 'AF2'}],
        'CH2': [{'pin': 'PA1', 'af': 'AF2'}],
        'CH3': [{'pin': 'PA2', 'af': 'AF2'}],
        'CH4': [{'pin': 'PA3', 'af': 'AF2'}],
    },
    'TIM9': {
        'CH1': [{'pin': 'PA2', 'af': 'AF3'}, {'pin': 'PE5', 'af': 'AF3'}],
        'CH2': [{'pin': 'PA3', 'af': 'AF3'}, {'pin': 'PE6', 'af': 'AF3'}],
    },
    'TIM10': {
        'CH1': [{'pin': 'PB8', 'af': 'AF3'}],
    },
    'TIM11': {
        'CH1': [{'pin': 'PB9', 'af': 'AF3'}],
    },
    'TIM12': {
        'CH1': [{'pin': 'PB14', 'af': 'AF9'}],
        'CH2': [{'pin': 'PB15', 'af': 'AF9'}],
    },
    'TIM13': {
        'CH1': [{'pin': 'PA6', 'af': 'AF9'}],
    },
    'TIM14': {
        'CH1': [{'pin': 'PA7', 'af': 'AF9'}],
    },
    'SPI3': {
        'SCK':  [{'pin': 'PB3', 'af': 'AF6'}, {'pin': 'PC10', 'af': 'AF6'}],
        'MISO': [{'pin': 'PB4', 'af': 'AF6'}, {'pin': 'PC11', 'af': 'AF6'}],
        'MOSI': [{'pin': 'PB5', 'af': 'AF6'}, {'pin': 'PC12', 'af': 'AF6'}],
    },
    'UART4': {
        'TX': [{'pin': 'PA0', 'af': 'AF8'}, {'pin': 'PC10', 'af': 'AF8'}],
        'RX': [{'pin': 'PA1', 'af': 'AF8'}, {'pin': 'PC11', 'af': 'AF8'}],
    },
    'UART5': {
        'TX': [{'pin': 'PC12', 'af': 'AF8'}],
        'RX': [{'pin': 'PD2', 'af': 'AF8'}],
    },
    'USART6': {
        'TX': [{'pin': 'PC6', 'af': 'AF8'}],
        'RX': [{'pin': 'PC7', 'af': 'AF8'}],
    },
        'ADC2': {
        'CH0': [{'pin': 'PA0'}],
        'CH1': [{'pin': 'PA1'}],
        'CH2': [{'pin': 'PA2'}],
        'CH3': [{'pin': 'PA3'}],
        'CH4': [{'pin': 'PA4'}],
        'CH5': [{'pin': 'PA5'}],
        'CH6': [{'pin': 'PA6'}],
        'CH7': [{'pin': 'PA7'}],
        'CH10': [{'pin': 'PC0'}],
        'CH11': [{'pin': 'PC1'}],
        'CH12': [{'pin': 'PC2'}],
        'CH13': [{'pin': 'PC3'}],
        'CH14': [{'pin': 'PC4'}],
        'CH15': [{'pin': 'PC5'}],
    },
    'ADC3': {
        'CH0': [{'pin': 'PA0'}],
        'CH1': [{'pin': 'PA1'}],
        'CH2': [{'pin': 'PA2'}],
        'CH3': [{'pin': 'PA3'}],
        'CH10': [{'pin': 'PC0'}],
        'CH11': [{'pin': 'PC1'}],
        'CH12': [{'pin': 'PC2'}],
        'CH13': [{'pin': 'PC3'}],
    },
    'ADC1': {
        'CH0': [{'pin': 'PA0'}, {'pin': 'PA0'}],
        'CH1': [{'pin': 'PA1'}],
        'CH2': [{'pin': 'PA2'}],
        'CH3': [{'pin': 'PA3'}],
        'CH4': [{'pin': 'PA4'}],
        'CH5': [{'pin': 'PA5'}],
        'CH6': [{'pin': 'PA6'}],
        'CH7': [{'pin': 'PA7'}],
        'CH10': [{'pin': 'PC0'}],
        'CH11': [{'pin': 'PC1'}],
        'CH12': [{'pin': 'PC2'}],
        'CH13': [{'pin': 'PC3'}],
        'CH14': [{'pin': 'PC4'}],
        'CH15': [{'pin': 'PC5'}],
    },
}


def find_pins(peripheral: str, signal: str = None, chip: str = 'STM32F407') -> dict:
    """查找外设的可用引脚"""
    periph_upper = peripheral.upper()
    
    # 根据芯片选择映射表
    if 'F103' in chip.upper() or 'F1' in chip.upper():
        pin_map = PIN_MAP_F103
    else:
        pin_map = PIN_MAP
    
    if periph_upper not in pin_map:
        return {
            'error': f'未找到 {peripheral} 的引脚映射',
            'available': list(pin_map.keys())
        }
    
    pmap = pin_map[periph_upper]
    
    if signal:
        sig_upper = signal.upper()
        if sig_upper in pmap:
            return {
                'peripheral': periph_upper,
                'signal': sig_upper,
                'pins': pmap[sig_upper]
            }
        return {
            'error': f'未找到信号 {signal}',
            'available_signals': list(pmap.keys())
        }
    
    return {
        'peripheral': periph_upper,
        'signals': {
            sig: pins for sig, pins in pmap.items()
        }
    }

# STM32F103 引脚复用映射 (简化版)
PIN_MAP_F103 = {
    'USART1': {
        'TX': [{'pin': 'PA9', 'af': 'AF7'}],
        'RX': [{'pin': 'PA10', 'af': 'AF7'}],
    },
    'USART2': {
        'TX': [{'pin': 'PA2', 'af': 'AF7'}],
        'RX': [{'pin': 'PA3', 'af': 'AF7'}],
    },
    'SPI1': {
        'SCK':  [{'pin': 'PA5', 'af': 'AF5'}],
        'MISO': [{'pin': 'PA6', 'af': 'AF5'}],
        'MOSI': [{'pin': 'PA7', 'af': 'AF5'}],
    },
    'I2C1': {
        'SCL': [{'pin': 'PB6', 'af': 'AF4'}],
        'SDA': [{'pin': 'PB7', 'af': 'AF4'}],
    },
    'TIM2': {
        'CH1': [{'pin': 'PA0', 'af': 'AF1'}],
        'CH2': [{'pin': 'PA1', 'af': 'AF1'}],
        'CH3': [{'pin': 'PA2', 'af': 'AF1'}],
        'CH4': [{'pin': 'PA3', 'af': 'AF1'}],
    },
    'TIM3': {
        'CH1': [{'pin': 'PA6', 'af': 'AF2'}],
        'CH2': [{'pin': 'PA7', 'af': 'AF2'}],
        'CH3': [{'pin': 'PB0', 'af': 'AF2'}],
        'CH4': [{'pin': 'PB1', 'af': 'AF2'}],
    },
    
    'TIM4': {
        'CH1': [{'pin': 'PB6', 'af': 'AF2'}],
        'CH2': [{'pin': 'PB7', 'af': 'AF2'}],
        'CH3': [{'pin': 'PB8', 'af': 'AF2'}],
        'CH4': [{'pin': 'PB9', 'af': 'AF2'}],
    },
    'SPI2': {
        'SCK':  [{'pin': 'PB13', 'af': 'AF5'}],
        'MISO': [{'pin': 'PB14', 'af': 'AF5'}],
        'MOSI': [{'pin': 'PB15', 'af': 'AF5'}],
    },
    'I2C2': {
        'SCL': [{'pin': 'PB10', 'af': 'AF4'}],
        'SDA': [{'pin': 'PB11', 'af': 'AF4'}],
    },
    'USART3': {
        'TX': [{'pin': 'PB10', 'af': 'AF7'}],
        'RX': [{'pin': 'PB11', 'af': 'AF7'}],
    },
    'ADC1': {
        'CH0': [{'pin': 'PA0'}],
        'CH1': [{'pin': 'PA1'}],
        'CH2': [{'pin': 'PA2'}],
        'CH3': [{'pin': 'PA3'}],
        'CH4': [{'pin': 'PA4'}],
        'CH5': [{'pin': 'PA5'}],
        'CH6': [{'pin': 'PA6'}],
        'CH7': [{'pin': 'PA7'}],
    },
}

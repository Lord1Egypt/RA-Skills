#!/usr/bin/env python3
"""STM32快速参考 — 常用操作速查表"""

QUICK_REF = {
    'GPIO': {
        '推挽输出': {'config': 'Mode=GPIO_MODE_OUTPUT_PP, Pull=GPIO_NOPULL', 'example': 'HAL_GPIO_WritePin(GPIOx, GPIO_PIN_x, GPIO_PIN_SET);'},
        '开漏输出': {'config': 'Mode=GPIO_MODE_OUTPUT_OD, Pull=GPIO_PULLUP', 'example': '常用于I2C、单总线'},
        '上拉输入': {'config': 'Mode=GPIO_MODE_INPUT, Pull=GPIO_PULLUP', 'example': 'uint8_t val = HAL_GPIO_ReadPin(GPIOx, GPIO_PIN_x);'},
        '模拟输入': {'config': 'Mode=GPIO_MODE_ANALOG, Pull=GPIO_NOPULL', 'example': '用于ADC输入'},
        '复用推挽': {'config': 'Mode=GPIO_MODE_AF_PP, Alternate=GPIO_AFx', 'example': '用于USART/SPI等外设'},
        '外部中断': {'config': 'Mode=GPIO_MODE_IT_FALLING, Pull=GPIO_PULLUP', 'example': 'HAL_GPIO_EXTI_Callback()'},
    },
    'USART': {
        '波特率': '9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600',
        '数据格式': '8N1 = 8位数据, 无校验, 1位停止',
        '轮询': 'HAL_UART_Transmit(&huart, data, len, timeout);',
        '中断': 'HAL_UART_Receive_IT(&huart, buf, 1);',
        'DMA': 'HAL_UART_Transmit_DMA(&huart, data, len);',
        'printf': 'int fputc(int ch, FILE *f) { HAL_UART_Transmit(&huart, (uint8_t*)&ch, 1, 10); return ch; }',
    },
    'TIM': {
        'PWM频率': 'freq = TIM_CLK / (PSC+1) / (ARR+1)',
        '占空比': 'duty = CCR / (ARR+1) * 100%',
        '84MHz': 'PSC=83, ARR=999 → 1kHz; CCR=500 → 50%',
        '编码器': 'Mode=TIM_ENCODERMODE_TI12',
        '输入捕获': 'Mode=TIM_INPUTCHANNELPOLARITY_RISING',
    },
    'SPI': {
        'Mode0': 'CPOL=0, CPHA=0 (最常用)',
        'Mode1': 'CPOL=0, CPHA=1',
        'Mode2': 'CPOL=1, CPHA=0',
        'Mode3': 'CPOL=1, CPHA=1',
        '时钟': 'SCK = PCLK / Prescaler',
        'CS': 'HAL_GPIO_WritePin(GPIOx, CS_PIN, GPIO_PIN_RESET);',
    },
    'I2C': {
        '地址': '7位地址左移1位: 0xA0 (写), 0xA1 (读)',
        '速率': '100kHz(标准), 400kHz(快速)',
        '上拉': 'SCL/SDA需要外部上拉(4.7kΩ)',
        'EEPROM': 'HAL_I2C_Mem_Write(&hi2c, 0xA0, addr, I2C_MEMADD_SIZE_8BIT, data, len, 100);',
    },
    'ADC': {
        '分辨率': '12位(0-4095), 10位(0-1023), 8位(0-255)',
        '电压': 'V = adc_value * Vref / 4096',
        '采样': '总时间 = 采样周期 + 12.5个周期',
        'DMA': 'HAL_ADC_Start_DMA(&hadc, buf, count);',
    },
    'DMA': {
        '方向': 'PERIPH_TO_MEMORY (外设→内存), MEMORY_TO_PERIPH (内存→外设)',
        '模式': 'NORMAL (单次), CIRCULAR (循环)',
        '宽度': 'BYTE (8位), HALFWORD (16位), WORD (32位)',
        '优先级': 'LOW, MEDIUM, HIGH, VERY_HIGH',
    },
    'CAN': {
        '波特率': 'APB1_CLK / (Prescaler * (BS1 + BS2 + 1))',
        '500kbps': 'Prescaler=6, BS1=13TQ, BS2=2TQ',
        '过滤器': 'ID掩码模式: FilterIdHigh/Low + FilterMaskIdHigh/Low',
        '发送': 'HAL_CAN_AddTxMessage(&hcan, &header, data, &mailbox)',
        '接收': 'HAL_CAN_GetRxMessage(&hcan, &header, data)',
    },
    'DAC': {
        '分辨率': '12位 (0-4095)',
        '电压': 'Vout = Vref * DOR / 4096',
        '触发': 'NONE (软件), TIMx, EXTIx',
    },
    'FLASH': {
        '扇区': 'S0-3: 16KB, S4: 64KB, S5-6: 128KB, S7: 128KB',
        '流程': '解锁 → 擦除 → 写入 → 锁定',
    },
    'PWR': {
        '模式': 'RUN → SLEEP → STOP → STANDBY',
        'STOP': 'HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI)',
        'STANDBY': 'HAL_PWR_EnterSTANDBYMode() — 唤醒后复位',
    },
    'RCC': {
        'HSE': '外部高速晶振(8MHz)',
        'HSI': '内部高速RC(16MHz)',
        'PLL': 'HSE/PLL_M*PLL_N/PLL_P = 168MHz',
        'AHB': 'HCLK = 168MHz',
        'APB1': 'PCLK1 = 42MHz (低速外设)',
        'APB2': 'PCLK2 = 84MHz (高速外设)',
    },
}


def get_quick_ref(peripheral: str = None) -> dict:
    if peripheral:
        key = peripheral.upper()
        if key in QUICK_REF:
            return {'peripheral': key, 'reference': QUICK_REF[key]}
        return {'error': f'未找到 {peripheral}', 'available': list(QUICK_REF.keys())}
    return {'all_peripherals': list(QUICK_REF.keys())}

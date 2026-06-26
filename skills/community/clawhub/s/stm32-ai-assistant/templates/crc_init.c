/**
 * STM32F407 CRC 校验 初始化模板
 * 配置: CRC-32 校验
 */
#include "stm32f4xx_hal.h"

CRC_HandleTypeDef hcrc;

void CRC_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_CRC_CLK_ENABLE();
    
    // 2. CRC配置
    hcrc.Instance = CRC;
    hcrc.Init.DefaultPolynomialUse = DEFAULT_POLYNOMIAL_ENABLE;    // 默认多项式
    hcrc.Init.DefaultInitValueUse = DEFAULT_INIT_VALUE_ENABLE;     // 默认初始值
    hcrc.Init.InputDataInversionMode = CRC_INPUTDATA_INVERSION_NONE;
    hcrc.Init.OutputDataInversionMode = CRC_OUTPUTDATA_INVERSION_NONE;
    hcrc.InputDataFormat = CRC_INPUTDATA_FORMAT_WORDS;             // 32位输入
    HAL_CRC_Init(&hcrc);
}

// 计算CRC-32
uint32_t CRC_Calculate(uint32_t *data, uint32_t len) {
    return HAL_CRC_Calculate(&hcrc, data, len);
}

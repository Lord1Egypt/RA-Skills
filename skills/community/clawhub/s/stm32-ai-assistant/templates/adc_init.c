/**
 * STM32F407 ADC 初始化模板
 * 配置示例: ADC1 CH0 单次转换 (PA0)
 */
#include "stm32f4xx_hal.h"

ADC_HandleTypeDef hadc1;

void ADC1_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_ADC1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为模拟输入
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;          // 模拟模式
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. ADC配置
    hadc1.Instance = ADC1;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;        // 12位分辨率
    hadc1.Init.ScanConvMode = DISABLE;                 // 单通道
    hadc1.Init.ContinuousConvMode = DISABLE;           // 单次转换
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE; // 软件触发
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;        // 右对齐
    hadc1.Init.NbrOfConversion = 1;
    hadc1.Init.DMAContinuousRequests = DISABLE;
    hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
    HAL_ADC_Init(&hadc1);
    
    // 4. 配置通道0
    ADC_ChannelConfTypeDef sConfig = {0};
    sConfig.Channel = ADC_CHANNEL_0;                   // CH0 = PA0
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_84CYCLES;    // 采样时间
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
}

// 使用:
// HAL_ADC_Start(&hadc1);
// HAL_ADC_PollForConversion(&hadc1, 100);
// uint16_t adc_value = HAL_ADC_GetValue(&hadc1);  // 0-4095 (12bit)
// float voltage = adc_value * 3.3f / 4096;         // 转电压

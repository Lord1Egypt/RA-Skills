/**
 * STM32F407 ADC DMA 连续采集模板
 * 配置: ADC1 + DMA2 Stream0 CH0
 */
#include "stm32f4xx_hal.h"

ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;

uint16_t adc_buffer[4];  // 4通道DMA缓冲

void ADC1_DMA_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_ADC1_CLK_ENABLE();
    __HAL_RCC_DMA2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0-PA3为模拟输入
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. DMA配置 (DMA2 Stream0 Channel0 = ADC1)
    hdma_adc1.Instance = DMA2_Stream0;
    hdma_adc1.Init.Channel = DMA_CHANNEL_0;
    hdma_adc1.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_adc1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_adc1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_adc1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
    hdma_adc1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_adc1.Init.Mode = DMA_CIRCULAR;
    hdma_adc1.Init.Priority = DMA_PRIORITY_HIGH;
    hdma_adc1.Init.FIFOMode = DMA_FIFOMODE_DISABLE;
    HAL_DMA_Init(&hdma_adc1);
    __HAL_LINKDMA(&hadc1, DMA_Handle, hdma_adc1);
    
    // 4. ADC配置
    hadc1.Instance = ADC1;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = ENABLE;
    hadc1.Init.ContinuousConvMode = ENABLE;
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 4;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    hadc1.Init.EOCSelection = ADC_EOC_SEQ_CONV;
    HAL_ADC_Init(&hadc1);
    
    // 5. 配置4个通道
    ADC_ChannelConfTypeDef sConfig = {0};
    sConfig.Channel = ADC_CHANNEL_0; sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_84CYCLES;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    sConfig.Channel = ADC_CHANNEL_1; sConfig.Rank = 2;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    sConfig.Channel = ADC_CHANNEL_2; sConfig.Rank = 3;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    sConfig.Channel = ADC_CHANNEL_3; sConfig.Rank = 4;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // 6. 配置NVIC
    HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);
    
    // 7. 启动DMA采集
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, 4);
}

// DMA中断
void DMA2_Stream0_IRQHandler(void) {
    HAL_DMA_IRQHandler(&hdma_adc1);
}

// DMA采集完成回调
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    if (hadc->Instance == ADC1) {
        // 4通道数据已更新到adc_buffer[0-3]
    }
}

// 使用:
// while(1) {
//     float v0 = adc_buffer[0] * 3.3f / 4096;
//     float v1 = adc_buffer[1] * 3.3f / 4096;
//     float v2 = adc_buffer[2] * 3.3f / 4096;
//     float v3 = adc_buffer[3] * 3.3f / 4096;
// }

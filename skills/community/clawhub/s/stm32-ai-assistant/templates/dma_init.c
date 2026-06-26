/**
 * STM32F407 DMA 初始化模板
 * 配置示例: DMA2 Stream0 CH0 ADC1 传输
 */
#include "stm32f4xx_hal.h"

DMA_HandleTypeDef hdma_adc1;

void DMA_ADC_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_DMA2_CLK_ENABLE();
    __HAL_RCC_ADC1_CLK_ENABLE();
    
    // 2. DMA配置 (DMA2 Stream0 Channel0 = ADC1)
    hdma_adc1.Instance = DMA2_Stream0;
    hdma_adc1.Init.Channel = DMA_CHANNEL_0;              // ADC1
    hdma_adc1.Init.Direction = DMA_PERIPH_TO_MEMORY;     // 外设→内存
    hdma_adc1.Init.PeriphInc = DMA_PINC_DISABLE;         // 外设地址不自增
    hdma_adc1.Init.MemInc = DMA_MINC_ENABLE;             // 内存地址自增
    hdma_adc1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;  // 16位
    hdma_adc1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_adc1.Init.Mode = DMA_CIRCULAR;                  // 循环模式
    hdma_adc1.Init.Priority = DMA_PRIORITY_HIGH;
    hdma_adc1.Init.FIFOMode = DMA_FIFOMODE_DISABLE;
    HAL_DMA_Init(&hdma_adc1);
    
    // 3. 关联DMA到ADC
    __HAL_LINKDMA(&hadc1, DMA_Handle, hdma_adc1);
    
    // 4. 配置NVIC
    HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);
}

// 中断服务函数
void DMA2_Stream0_IRQHandler(void) {
    HAL_DMA_IRQHandler(&hdma_adc1);
}

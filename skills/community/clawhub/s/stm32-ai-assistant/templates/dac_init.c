/**
 * STM32F407 DAC 初始化模板
 * 配置示例: DAC1 CH1 (PA4)
 */
#include "stm32f4xx_hal.h"

DAC_HandleTypeDef hdac;

void DAC1_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_DAC_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA4为模拟输入
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_4;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. DAC配置
    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);
    
    // 4. 通道配置
    DAC_ChannelConfTypeDef sConfig = {0};
    sConfig.DAC_TRIGGER = DAC_TRIGGER_NONE;           // 软件触发
    sConfig.DAC_OUTPUTBUFFER = DAC_OUTPUTBUFFER_ENABLE;
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
    
    // 5. 启动DAC
    HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
}

// 输出电压 (12位, 0-4095)
void DAC_SetValue(uint16_t value) {
    HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, value);
}

// 输出电压 (0-3.3V)
void DAC_SetVoltage(float voltage) {
    uint16_t value = (uint16_t)(voltage * 4095 / 3.3f);
    DAC_SetValue(value);
}

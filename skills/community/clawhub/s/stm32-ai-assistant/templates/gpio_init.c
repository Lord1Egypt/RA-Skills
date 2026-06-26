/**
 * STM32F407 GPIO 初始化模板
 * 配置示例: PA5 推挽输出 (LED)
 */
#include "stm32f4xx_hal.h"

void GPIO_LED_Init(void) {
    // 1. 使能GPIOA时钟
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA5为推挽输出
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;      // 推挽输出
    GPIO_InitStruct.Pull = GPIO_NOPULL;               // 无上下拉
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;      // 低速
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 初始输出低电平
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
}

// 使用:
// HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // 翻转
// HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);  // 置高

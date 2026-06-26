/**
 * STM32F407 GPIO外部中断模板
 * 配置: PA0下降沿中断 + PA1上升沿中断
 */
#include "stm32f4xx_hal.h"

void GPIO_EXTI_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为下降沿中断 (按键按下)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 配置PA1为上升沿中断 (传感器触发)
    GPIO_InitStruct.Pin = GPIO_PIN_1;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 4. 配置NVIC
    HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
    
    HAL_NVIC_SetPriority(EXTI1_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(EXTI1_IRQn);
}

// 中断服务函数 (在stm32f4xx_it.c中)
void EXTI0_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

void EXTI1_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_1);
}

// 中断回调函数
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_0) {
        // PA0下降沿中断处理 (按键按下)
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
    if (GPIO_Pin == GPIO_PIN_1) {
        // PA1上升沿中断处理 (传感器触发)
        // 添加你的处理代码
    }
}

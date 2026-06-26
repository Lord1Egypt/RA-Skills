/**
 * STM32F407 外部中断 初始化模板
 * 配置示例: PA0 下降沿触发外部中断 (按键)
 */
#include "stm32f4xx_hal.h"

void EXTI_Key_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为外部中断输入
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;       // 下降沿触发
    GPIO_InitStruct.Pull = GPIO_PULLUP;                // 上拉
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 配置NVIC (在HAL_GPIO_Init中已自动调用HAL_NVIC_SetPriority)
    HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);           // 优先级2
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);                    // 使能中断
}

// 4. 中断服务函数 (在stm32f4xx_it.c中)
void EXTI0_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

// 5. 回调函数 (用户代码)
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_0) {
        // 按键按下处理
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // 翻转LED
    }
}

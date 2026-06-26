/**
 * STM32F407 GPIO 输入输出组合模板
 * 配置: PA0上拉输入 + PA5推挽输出 (按键控制LED)
 */
#include "stm32f4xx_hal.h"

void GPIO_Key_LED_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为上拉输入 (按键)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 配置PA5为推挽输出 (LED)
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

// 按键扫描 (带消抖)
uint8_t Key_Scan(void) {
    if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {
        HAL_Delay(20);  // 消抖
        if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {
            while (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET);  // 等待释放
            return 1;
        }
    }
    return 0;
}

// 使用示例:
// if (Key_Scan()) {
//     HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
// }

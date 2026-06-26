/**
 * STM32F407 USART 初始化模板
 * 配置示例: USART1 115200 8N1 (PA9-TX PA10-RX)
 */
#include "stm32f4xx_hal.h"

UART_HandleTypeDef huart1;

void USART1_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_USART1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置TX(PA9)和RX(PA10)引脚
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_9 | GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;          // 复用推挽
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART1;     // AF7 = USART1
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 配置USART1参数
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    HAL_UART_Init(&huart1);
}

// 使用:
// HAL_UART_Transmit(&huart1, (uint8_t*)"Hello\n", 6, 100);
// HAL_UART_Receive(&huart1, buf, 1, 1000);
// HAL_UART_Transmit_IT(&huart1, data, len);  // 中断发送
// HAL_UART_Receive_IT(&huart1, buf, 1);       // 中断接收

/**
 * STM32F407 printf 重定向模板
 * 配置: USART1 115200, 重定向printf到串口
 */
#include "stm32f4xx_hal.h"
#include <stdio.h>

extern UART_HandleTypeDef huart1;

// 重定向printf到USART1
int fputc(int ch, FILE *f) {
    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 100);
    return ch;
}

// 重定向scanf到USART1
int fgetc(FILE *f) {
    uint8_t ch = 0;
    HAL_UART_Receive(&huart1, &ch, 1, HAL_MAX_DELAY);
    return ch;
}

// 使用示例:
// printf("Hello STM32!\r\n");
// printf("ADC value: %d\r\n", adc_value);
// printf("Temperature: %.1f C\r\n", temp);

/**
 * STM32F407 TIM 输入捕获模板
 * 配置: TIM2 CH1 输入捕获 (PA0)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim2;
volatile uint32_t capture_value = 0;
volatile uint32_t capture_flag = 0;

void TIM2_IC_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_TIM2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为TIM2_CH1输入捕获
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF1_TIM2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 时基配置: 84MHz/84 = 1MHz (1us分辨率)
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 83;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 0xFFFFFFFF;
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    HAL_TIM_IC_Init(&htim2);
    
    // 4. 输入捕获配置
    TIM_IC_InitTypeDef sConfigIC = {0};
    sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
    sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
    sConfigIC.ICFilter = 0;
    HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_1);
    
    // 5. 启动输入捕获中断
    HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
}

// 捕获回调函数
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2 && htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
        capture_value = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
        capture_flag = 1;
    }
}

// 中断服务函数 (在stm32f4xx_it.c中)
void TIM2_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim2);
}

// 使用示例: 测量脉冲宽度
// if (capture_flag) {
//     float pulse_us = capture_value;  // 1MHz时钟, 1tick = 1us
//     printf("Pulse: %.1f us\r\n", pulse_us);
//     capture_flag = 0;
// }

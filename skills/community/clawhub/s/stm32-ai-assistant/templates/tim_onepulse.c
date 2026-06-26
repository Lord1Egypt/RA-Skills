/**
 * STM32F407 TIM 单脉冲模式模板
 * 配置: TIM2 CH1 单脉冲输出 (触发后输出一个脉冲)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim2;

void TIM2_OnePulse_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_TIM2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为TIM2_CH1
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF1_TIM2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 时基配置
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 83;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 999;
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
    HAL_TIM_PWM_Init(&htim2);
    
    // 4. 单脉冲配置
    TIM_OnePulse_InitTypeDef sConfig = {0};
    sConfig.OCMode = TIM_OCMODE_PWM1;
    sConfig.Pulse = 499;  // 脉冲宽度 5ms (1kHz时钟)
    sConfig.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfig.OCIdleState = TIM_OCIDLESTATE_RESET;
    sConfig.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfig.ICSelection = TIM_ICSELECTION_DIRECTTI;
    sConfig.ICPrescaler = TIM_ICPSC_DIV1;
    sConfig.ICFilter = 0;
    HAL_TIM_OnePulse_Init(&htim2, TIM_OPMODE_SINGLE);
    
    // 5. 配置触发输入 (PA1触发)
    HAL_TIM_IC_Start(&htim2, TIM_CHANNEL_2);
}

// 启动单脉冲
void TIM2_OnePulse_Start(void) {
    HAL_TIM_OnePulse_Start(&htim2, TIM_CHANNEL_1);
}

// 使用: 触发PA1上升沿后，PA0输出一个5ms脉冲

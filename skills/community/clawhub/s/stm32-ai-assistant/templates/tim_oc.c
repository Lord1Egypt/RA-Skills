/**
 * STM32F407 TIM 输出比较模板
 * 配置: TIM2 CH1 输出比较模式 (PA0)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim2;

void TIM2_OC_Init(void) {
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
    
    // 3. 时基配置: 84MHz/84/1000 = 1kHz
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 83;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 999;
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_PWM_Init(&htim2);
    
    // 4. 输出比较配置
    TIM_OC_InitTypeDef sConfigOC = {0};
    sConfigOC.OCMode = TIM_OCMODE_TOGGLE;
    sConfigOC.Pulse = 500;  // 在500时翻转
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    HAL_TIM_OC_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_1);
    
    // 5. 启动
    HAL_TIM_OC_Start(&htim2, TIM_CHANNEL_1);
}

// 输出比较模式说明:
// TIM_OCMODE_FROZEN: 冻结，不输出
// TIM_OCMODE_ACTIVE: 匹配时输出有效电平
// TIM_OCMODE_INACTIVE: 匹配时输出无效电平
// TIM_OCMODE_TOGGLE: 匹配时翻转
// TIM_OCMODE_PWM1: CNT < CCR时输出有效电平 (PWM模式1)
// TIM_OCMODE_PWM2: CNT < CCR时输出无效电平 (PWM模式2)

/**
 * STM32F407 TIM PWM 初始化模板
 * 配置示例: TIM2 CH1 PWM 1kHz 50%占空比 (PA0)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim2;

void TIM2_PWM_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_TIM2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为TIM2_CH1复用功能
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF1_TIM2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 时基配置: 84MHz / (83+1) / (999+1) = 1kHz
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 83;           // 预分频器
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 999;             // 自动重装载值
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_PWM_Init(&htim2);
    
    // 4. PWM通道配置: 50%占空比
    TIM_OC_InitTypeDef sConfigOC = {0};
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 499;               // 占空比 = Pulse/(Period+1) = 50%
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_1);
    
    // 5. 启动PWM
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
}

// 使用:
// __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, 749);  // 改为75%占空比
// HAL_TIM_PWM_Stop(&htim2, TIM_CHANNEL_1);             // 停止PWM

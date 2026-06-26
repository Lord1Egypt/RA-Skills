/**
 * STM32F407 TIM Hall传感器模板
 * 配置: TIM1 Hall传感器接口 (PA8/PA9/PA10)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim1;
volatile uint32_t hall_state = 0;
volatile uint32_t hall_speed = 0;

void TIM1_Hall_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_TIM1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置Hall引脚 (PA8=CH1, PA9=CH2, PA10=CH3)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_8 | GPIO_PIN_9 | GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF1_TIM1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. Hall传感器配置
    TIM_HallSensor_InitTypeDef sHallConfig = {0};
    sHallConfig.IC1Polarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sHallConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sHallConfig.IC1Filter = 15;
    sHallConfig.Commutation_Delay = 10;  // 换相延迟
    HAL_TIMEx_HallSensor_Init(&htim1, &sHallConfig);
    
    // 4. 启动Hall传感器
    HAL_TIMEx_HallSensor_Start_IT(&htim1);
}

// Hall状态变化回调
void HAL_TIMEx_CommutationCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM1) {
        hall_state = TIM1->CR2 & TIM_CR2_CCPC;
        hall_speed = __HAL_TIM_GET_COUNTER(&htim1);
    }
}

// Hall传感器应用场景:
// - 无刷电机(BLDC)换相
// - 直流电机速度测量
// - 位置传感器读取

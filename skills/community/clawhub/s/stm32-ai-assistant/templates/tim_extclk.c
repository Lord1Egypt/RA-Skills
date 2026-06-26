/**
 * STM32F407 TIM 外部时钟计数器模板
 * 配置: TIM2 计数外部脉冲 (PA0)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim2;

void TIM2_ExtClk_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_TIM2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA0为TIM2_CH1外部时钟输入
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF1_TIM2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 外部时钟模式配置
    TIM_SlaveConfigTypeDef sSlaveConfig = {0};
    sSlaveConfig.SlaveMode = SLAVEMODE_EXTERNAL1;
    sSlaveConfig.InputTrigger = TIM_TS_TI1FP1;
    sSlaveConfig.TriggerPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sSlaveConfig.TriggerPrescaler = TIM_ICPSC_DIV1;
    sSlaveConfig.TriggerFilter = 0;
    HAL_TIM_SlaveConfigSynchronization(&htim2, &sSlaveConfig);
    
    // 4. 时基配置 (计数器)
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 0;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 0xFFFFFFFF;  // 32位计数器
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
    HAL_TIM_Base_Init(&htim2);
    
    // 5. 启动计数
    HAL_TIM_Base_Start(&htim2);
}

// 读取计数值
uint32_t TIM2_GetCount(void) {
    return TIM2->CNT;
}

// 外部时钟计数器应用:
// - 流量计脉冲计数
// - 编码器脉冲计数
// - 事件计数
// - 频率测量 (配合定时器中断)

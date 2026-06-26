/**
 * STM32F407 TIM PWM输入模式模板
 * 配置: TIM2 CH1 PWM输入 (PA0) - 测量频率和占空比
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim2;
volatile uint32_t ic_value1 = 0;
volatile uint32_t ic_value2 = 0;
volatile uint32_t ic_value3 = 0;
volatile uint32_t frequency = 0;
volatile uint32_t duty_cycle = 0;
volatile uint8_t capture_done = 0;

void TIM2_PWM_Input_Init(void) {
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
    
    // 3. 时基配置: 84MHz/84 = 1MHz
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 83;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 0xFFFF;
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    HAL_TIM_IC_Init(&htim2);
    
    // 4. PWM输入配置 (TI1FP1直连, TI1FP2交叉)
    TIM_IC_InitTypeDef sConfigIC = {0};
    sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
    sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
    sConfigIC.ICFilter = 0;
    HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_1);
    
    sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_FALLING;
    sConfigIC.ICSelection = TIM_ICSELECTION_INDIRECTTI;
    HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_2);
    
    // 5. 从模式: 复位模式
    TIM_SlaveConfigTypeDef sSlaveConfig = {0};
    sSlaveConfig.SlaveMode = SLAVEMODE_RESET;
    sSlaveConfig.InputTrigger = TIM_TS_TI1FP1;
    sSlaveConfig.TriggerPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sSlaveConfig.TriggerPrescaler = TIM_ICPSC_DIV1;
    sSlaveConfig.TriggerFilter = 0;
    HAL_TIM_SlaveConfigSynchronization(&htim2, &sSlaveConfig);
    
    // 6. 启动PWM输入
    HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
    HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_2);
}

// 捕获回调
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2) {
        if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
            ic_value1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            if (ic_value1 != 0) {
                frequency = 1000000 / ic_value1;  // 1MHz / 周期
                duty_cycle = (ic_value2 * 100) / ic_value1;
                capture_done = 1;
            }
        }
        if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_2) {
            ic_value2 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_2);
        }
    }
}

// 中断服务函数
void TIM2_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim2);
}

// 使用示例:
// if (capture_done) {
//     printf("Freq: %lu Hz, Duty: %lu%%\r\n", frequency, duty_cycle);
//     capture_done = 0;
// }

/**
 * STM32F407 TIM 编码器模式模板
 * 配置: TIM3 编码器模式 (PA6=CH1, PA7=CH2)
 */
#include "stm32f4xx_hal.h"

TIM_HandleTypeDef htim3;

void TIM3_Encoder_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_TIM3_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置PA6/PA7为TIM3_CH1/CH2
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF2_TIM3;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. 时基配置
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 0;
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 0xFFFF;
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_IC_Init(&htim3);
    
    // 4. 编码器配置
    TIM_Encoder_InitTypeDef sConfig = {0};
    sConfig.EncoderMode = TIM_ENCODERMODE_TI12;
    sConfig.IC1Polarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC1Filter = 0;
    sConfig.IC2Polarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC2Filter = 0;
    HAL_TIM_Encoder_Init(&htim3, &sConfig);
    
    // 5. 启动编码器
    HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
}

// 读取编码器计数值
int16_t Encoder_GetCount(void) {
    return (int16_t)TIM3->CNT;
}

// 重置编码器计数
void Encoder_Reset(void) {
    TIM3->CNT = 0;
}

// 计算转速 (RPM)
// 假设编码器1000脉冲/转, 采样周期10ms
// RPM = (count_diff / 1000) * (60 / 0.01) = count_diff * 6
float Encoder_GetRPM(int16_t count_diff) {
    return (float)count_diff * 6.0f;
}

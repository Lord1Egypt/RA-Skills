/**
 * STM32F407 GPIO开漏输出驱动外部设备模板
 * 配置: PB0开漏输出驱动继电器/蜂鸣器
 */
#include "stm32f4xx_hal.h"

void GPIO_OD_Ext_Init(void) {
    __HAL_RCC_GPIOB_CLK_ENABLE();
    
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;  // 开漏输出
    GPIO_InitStruct.Pull = GPIO_PULLUP;          // 需要外部上拉
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    
    // 初始状态: 高电平(不驱动)
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);
}

// 继电器控制
void Relay_On(void)  { HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET); }  // 低电平有效
void Relay_Off(void) { HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET); }

// 蜂鸣器控制
void Buzzer_On(void)  { HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET); }
void Buzzer_Off(void) { HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET); }

// LED驱动 (低电平点亮)
void LED_On(void)  { HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET); }
void LED_Off(void) { HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET); }

// 开漏输出说明:
// - 高阻态输出: 只能拉低，不能拉高
// - 需要外部上拉电阻
// - 适合驱动: 继电器、蜂鸣器、LED、电平转换
// - 可驱动不同电压设备 (3.3V/5V/12V)

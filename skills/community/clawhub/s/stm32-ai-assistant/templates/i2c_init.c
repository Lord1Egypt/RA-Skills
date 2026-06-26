/**
 * STM32F407 I2C 初始化模板
 * 配置示例: I2C1 100kHz (PB6-SCL PB7-SDA)
 */
#include "stm32f4xx_hal.h"

I2C_HandleTypeDef hi2c1;

void I2C1_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_I2C1_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    
    // 2. 配置I2C引脚 (PB6=SCL, PB7=SDA)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;           // 开漏输出
    GPIO_InitStruct.Pull = GPIO_PULLUP;                // 需要上拉
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF4_I2C1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    
    // 3. I2C配置
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 100000;                   // 100kHz标准模式
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;           // Tlow/Thigh = 2
    hi2c1.Init.OwnAddress1 = 0;                       // 主机地址
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
    HAL_I2C_Init(&hi2c1);
}

// 使用:
// uint8_t data[] = {0x01, 0x02};
// HAL_I2C_Master_Transmit(&hi2c1, 0xA0, data, 2, 100);  // 写
// HAL_I2C_Master_Receive(&hi2c1, 0xA0, buf, 2, 100);     // 读
// HAL_I2C_Mem_Write(&hi2c1, 0xA0, 0x00, I2C_MEMADD_SIZE_8BIT, data, 2, 100);

/**
 * STM32F407 SPI 初始化模板
 * 配置示例: SPI1 全双工主机 Mode0 (PA5-SCK PA6-MISO PA7-MOSI)
 */
#include "stm32f4xx_hal.h"

SPI_HandleTypeDef hspi1;

void SPI1_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_SPI1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // 2. 配置SPI引脚 (PA5=SCK, PA6=MISO, PA7=MOSI)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // 3. SPI配置
    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;              // 主机模式
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;     // 全双工
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;         // 8位数据
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;       // CPOL=0
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;           // CPHA=0 (Mode 0)
    hspi1.Init.NSS = SPI_NSS_SOFT;                   // 软件CS
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16; // 84MHz/16=5.25MHz
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;          // MSB先发
    hspi1.Init.TIMode = SPI_TIMODE_DISABLE;          // 非TI模式
    hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
    HAL_SPI_Init(&hspi1);
}

// 使用:
// uint8_t tx = 0xAA, rx;
// HAL_SPI_Transmit(&hspi1, &tx, 1, 100);            // 发送
// HAL_SPI_Receive(&hspi1, &rx, 1, 100);              // 接收
// HAL_SPI_TransmitReceive(&hspi1, &tx, &rx, 1, 100); // 收发

/**
 * STM32F407 CAN 初始化模板
 * 配置示例: CAN1 500kbps (PB8-RX PB9-TX)
 */
#include "stm32f4xx_hal.h"

CAN_HandleTypeDef hcan1;

void CAN1_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_CAN1_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    
    // 2. 配置CAN引脚 (PB8=RX, PB9=TX)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_8 | GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF9_CAN1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    
    // 3. CAN配置
    hcan1.Instance = CAN1;
    hcan1.Init.Prescaler = 6;              // 42MHz/6/8 = 875kbps (近似500kbps)
    hcan1.Init.Mode = CAN_MODE_NORMAL;
    hcan1.Init.SyncJumpWidth = CAN_SJW_1TQ;
    hcan1.Init.TimeSeg1 = CAN_BS1_13TQ;
    hcan1.Init.TimeSeg2 = CAN_BS2_2TQ;
    hcan1.Init.TimeTriggeredMode = DISABLE;
    hcan1.Init.AutoBusOff = DISABLE;
    hcan1.Init.AutoWakeUp = DISABLE;
    hcan1.Init.AutoRetransmission = ENABLE;
    hcan1.Init.ReceiveFifoLocked = DISABLE;
    hcan1.Init.TransmitFifoPriority = DISABLE;
    HAL_CAN_Init(&hcan1);
    
    // 4. 配置过滤器 (接收所有消息)
    CAN_FilterTypeDef sFilterConfig = {0};
    sFilterConfig.FilterBank = 0;
    sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
    sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
    sFilterConfig.FilterIdHigh = 0x0000;
    sFilterConfig.FilterIdLow = 0x0000;
    sFilterConfig.FilterMaskIdHigh = 0x0000;
    sFilterConfig.FilterMaskIdLow = 0x0000;
    sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
    sFilterConfig.FilterActivation = ENABLE;
    HAL_CAN_ConfigFilter(&hcan1, &sFilterConfig);
    
    // 5. 启动CAN
    HAL_CAN_Start(&hcan1);
}

// 发送CAN消息
HAL_StatusTypeDef CAN_Send(uint32_t id, uint8_t *data, uint8_t len) {
    CAN_TxHeaderTypeDef header = {0};
    header.StdId = id;
    header.DLC = len;
    header.IDE = CAN_ID_STD;
    header.RTR = CAN_RTR_DATA;
    
    uint32_t mailbox;
    return HAL_CAN_AddTxMessage(&hcan1, &header, data, &mailbox);
}

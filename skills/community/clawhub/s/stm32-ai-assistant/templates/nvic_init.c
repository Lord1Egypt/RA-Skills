/**
 * STM32F407 NVIC 中断管理模板
 * 配置: 中断优先级分组和使能
 */
#include "stm32f4xx_hal.h"

void NVIC_Init(void) {
    // 1. 配置中断优先级分组 (4位抢占优先级, 0位子优先级)
    HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);
    
    // 2. 配置系统中断优先级
    // SysTick (最低优先级)
    HAL_NVIC_SetPriority(SysTick_IRQn, 15, 0);
    
    // 3. 配置外设中断
    // EXTI0 (按键中断, 最高优先级)
    HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
    
    // USART1 (串口中断)
    HAL_NVIC_SetPriority(USART1_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(USART1_IRQn);
    
    // DMA2 Stream0 (ADC DMA)
    HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 2, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);
}

// 中断优先级说明:
// STM32F407: 4位优先级 = 0-15 (0最高, 15最低)
// NVIC_PRIORITYGROUP_4: 4位抢占, 0位子优先级
// NVIC_PRIORITYGROUP_3: 3位抢占, 1位子优先级
// NVIC_PRIORITYGROUP_2: 2位抢占, 2位子优先级
// NVIC_PRIORITYGROUP_1: 1位抢占, 3位子优先级
// NVIC_PRIORITYGROUP_0: 0位抢占, 4位子优先级

// 中断服务函数示例 (在stm32f4xx_it.c中):
// void EXTI0_IRQHandler(void) {
//     HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
// }
//
// void USART1_IRQHandler(void) {
//     HAL_UART_IRQHandler(&huart1);
// }
//
// void DMA2_Stream0_IRQHandler(void) {
//     HAL_DMA_IRQHandler(&hdma_adc1);
// }

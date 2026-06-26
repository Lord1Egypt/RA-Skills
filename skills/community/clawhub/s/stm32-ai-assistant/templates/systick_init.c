/**
 * STM32F407 SysTick 定时器 初始化模板
 * 配置: 1ms系统滴答定时器
 */
#include "stm32f4xx_hal.h"

volatile uint32_t sys_tick_ms = 0;

void SysTick_Init(void) {
    // HAL库已经配置了SysTick (1ms中断)
    // 在stm32f4xx_hal.c中: HAL_InitTick() 配置 SysTick
    
    // 如果需要自定义:
    // SysTick_Config(SystemCoreClock / 1000);  // 1ms中断
}

// 毫秒延时 (非阻塞)
void Delay_ms(uint32_t ms) {
    uint32_t start = sys_tick_ms;
    while ((sys_tick_ms - start) < ms) {
        // 可以在这里处理其他任务
    }
}

// 微秒延时 (阻塞)
void Delay_us(uint32_t us) {
    uint32_t start = SysTick->VAL;
    uint32_t ticks = us * (SystemCoreClock / 1000000);
    while ((start - SysTick->VAL) < ticks);
}

// SysTick中断回调 (在stm32f4xx_it.c中调用)
void SysTick_Callback(void) {
    sys_tick_ms++;
}

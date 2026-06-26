/**
 * STM32F407 看门狗 初始化模板
 * IWDG 独立看门狗, 超时约1秒
 */
#include "stm32f4xx_hal.h"

IWDG_HandleTypeDef hiwdg;

void IWDG_Init(void) {
    // IWDG配置: LSI 32kHz / 64 / 500 = 1秒超时
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_64;   // 分频64
    hiwdg.Init.Reload = 500;                     // 重装载值
    hiwdg.Init.Window = IWDG_WINDOW_DISABLE;     // 窗口模式关闭
    HAL_IWDG_Init(&hiwdg);
    
    // 启动看门狗
    HAL_IWDG_Start(&hiwdg);
}

// 喂狗 (在主循环中定期调用)
// HAL_IWDG_Refresh(&hiwdg);

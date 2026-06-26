/**
 * STM32F407 WWDG 窗口看门狗 初始化模板
 * 配置: 窗口看门狗，超时约50ms
 */
#include "stm32f4xx_hal.h"

WWDG_HandleTypeDef hwwdg;

void WWDG_Init(void) {
    // WWDG配置: PCLK1/4096/8 = 42MHz/4096/8 ≈ 1.28ms/step
    // 窗口: 0x50-0x7F (80-127), 超时: 0x7F (127) = 162ms
    hwwdg.Instance = WWDG;
    hwwdg.Init.Prescaler = WWDG_PRESCALER_8;
    hwwdg.Init.Window = 0x50;              // 窗口下限
    hwwdg.Init.Counter = 0x7F;             // 计数器初始值
    hwwdg.Init.EWIMode = WWDG_EWI_ENABLE;  // 提前唤醒中断
    HAL_WWDG_Init(&hwwdg);
}

// 喂狗 (必须在窗口内: 0x50 < counter < 0x7F)
// HAL_WWDG_Refresh(&hwwdg);

// 提前唤醒中断回调
void HAL_WWDG_EarlyWakeupCallback(WWDG_HandleTypeDef *hwwdg) {
    // 在这里喂狗
    HAL_WWDG_Refresh(hwwdg);
}

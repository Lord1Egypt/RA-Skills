/**
 * STM32F407 看门狗配置模板 (IWDG + WWDG)
 * IWDG: 独立看门狗，LSI时钟，超时较长
 * WWDG: 窗口看门狗，APB1时钟，超时较短
 */
#include "stm32f4xx_hal.h"

IWDG_HandleTypeDef hiwdg;
WWDG_HandleTypeDef hwwdg;

void IWDG_Init(uint32_t timeout_ms) {
    // IWDG: LSI ≈ 32kHz
    // 超时 = (Prescaler * Reload) / LSI
    // Prescaler: /4, /8, /16, /32, /64, /128, /256
    // Reload: 0-4095
    
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_128;  // 32kHz/128 = 250Hz
    hiwdg.Init.Reload = (timeout_ms * 250) / 1000;  // 自动计算
    hiwdg.Init.Window = IWDG_WINDOW_DISABLE;
    HAL_IWDG_Init(&hiwdg);
}

void WWDG_Init(uint8_t window, uint8_t counter) {
    // WWDG: PCLK1/4096/8 ≈ 1.28ms/step
    // 超时 = counter * 1.28ms
    // 窗口 = window * 1.28ms
    
    hwwdg.Instance = WWDG;
    hwwdg.Init.Prescaler = WWDG_PRESCALER_8;
    hwwdg.Init.Window = window;
    hwwdg.Init.Counter = counter;
    hwwdg.Init.EWIMode = WWDG_EWI_ENABLE;
    HAL_WWDG_Init(&hwwdg);
}

// 使用:
// IWDG_Init(5000);   // 5秒超时 (适合低频主循环)
// WWDG_Init(80, 127); // 162ms超时 (适合高频主循环)

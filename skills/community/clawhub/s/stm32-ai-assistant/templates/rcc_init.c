/**
 * STM32F407 RCC 时钟配置模板
 * 配置: HSE 8MHz → PLL → 168MHz系统时钟
 */
#include "stm32f4xx_hal.h"

void SystemClock_Config(void) {
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
    
    // 1. 配置电源和电压调节器
    __HAL_RCC_PWR_CLK_ENABLE();
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
    
    // 2. 配置HSE和PLL
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    RCC_OscInitStruct.PLL.PLLM = 8;      // HSE/8 = 1MHz
    RCC_OscInitStruct.PLL.PLLN = 336;    // 1MHz*336 = 336MHz
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;  // 336/2 = 168MHz
    RCC_OscInitStruct.PLL.PLLQ = 7;      // 336/7 = 48MHz (USB)
    HAL_RCC_OscConfig(&RCC_OscInitStruct);
    
    // 3. 配置总线时钟
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;      // HCLK = 168MHz
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;       // APB1 = 42MHz
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;       // APB2 = 84MHz
    HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5);
}

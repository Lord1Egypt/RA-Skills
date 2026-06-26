/**
 * STM32F407 电源管理 初始化模板
 * 配置: 低功耗模式配置
 */
#include "stm32f4xx_hal.h"

void PWR_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_PWR_CLK_ENABLE();
    
    // 2. 配置电压调节器
    // PWR_CR: 电压调节器输出Scale 1模式
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
    
    // 3. 配置唤醒引脚 (PA0)
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
}

// 进入STOP模式 (低功耗)
void Enter_Stop_Mode(void) {
    HAL_SuspendTick();
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
    // 唤醒后继续执行
    HAL_ResumeTick();
    SystemClock_Config();  // 重新配置时钟
}

// 进入STANDBY模式 (最低功耗)
void Enter_Standby_Mode(void) {
    HAL_PWR_EnterSTANDBYMode();
    // 唤醒后复位
}

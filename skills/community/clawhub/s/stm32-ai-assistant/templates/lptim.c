/**
 * STM32F407 LPTIM 低功耗定时器模板
 * 配置: LPTIM 唤醒定时器 (1秒周期)
 */
#include "stm32f4xx_hal.h"

// LPTIM仅在STM32L4等低功耗系列有
// F407没有LPTIM，这里提供通用低功耗定时器配置思路

// F407替代方案: 使用RTC作为低功耗定时器
#include "stm32f4xx_hal.h"

void LowPower_Wakeup_Init(void) {
    // 1. 配置RTC闹钟作为唤醒源
    RTC_HandleTypeDef hrtc;
    hrtc.Instance = RTC;
    hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
    hrtc.Init.AsynchPrediv = 127;
    hrtc.Init.SynchPrediv = 255;
    HAL_RTC_Init(&hrtc);
    
    // 2. 配置闹钟: 1分钟后唤醒
    RTC_TimeTypeDef sTime;
    HAL_RTC_GetTime(&hrtc, &sTime, RTC_FORMAT_BIN);
    
    RTC_AlarmTypeDef sAlarm = {0};
    sAlarm.AlarmTime.Hours = sTime.Hours;
    sAlarm.AlarmTime.Minutes = sTime.Minutes + 1;
    sAlarm.AlarmTime.Seconds = sTime.Seconds;
    sAlarm.Alarm = RTC_ALARM_A;
    HAL_RTC_SetAlarm(&hrtc, &sAlarm, RTC_FORMAT_BIN);
    
    // 3. 使能RTC闹钟中断
    HAL_NVIC_SetPriority(RTC_Alarm_IRQn, 2, 0);
    HAL_NVIC_EnableIRQ(RTC_Alarm_IRQn);
}

// 进入低功耗模式
void Enter_LowPower(void) {
    HAL_SuspendTick();
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
    // 唤醒后重新配置时钟
    HAL_ResumeTick();
    SystemClock_Config();
}

// 低功耗应用场景:
// 1. 电池供电设备定时采集
// 2. 传感器节点定期上报
// 3. 遥控器/门锁等低功耗设备

/**
 * STM32F407 RTC 闹钟模板
 * 配置: RTC闹钟A，每天12:00:00触发
 */
#include "stm32f4xx_hal.h"

RTC_HandleTypeDef hrtc;

void RTC_Alarm_Init(void) {
    // RTC初始化 (在rtc_init.c中)
    hrtc.Instance = RTC;
    hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
    hrtc.Init.AsynchPrediv = 127;
    hrtc.Init.SynchPrediv = 255;
    hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
    HAL_RTC_Init(&hrtc);
    
    // 配置闹钟A: 每天12:00:00
    RTC_AlarmTypeDef sAlarm = {0};
    sAlarm.AlarmTime.Hours = 12;
    sAlarm.AlarmTime.Minutes = 0;
    sAlarm.AlarmTime.Seconds = 0;
    sAlarm.AlarmTime.TimeFormat = RTC_HOURFORMAT24_AM;
    sAlarm.AlarmMask = RTC_ALARMMASK_NONE;  // 完全匹配
    sAlarm.AlarmSubSecondMask = RTC_ALARMSUBSECONDMASK_NONE;
    sAlarm.Alarm = RTC_ALARM_A;
    HAL_RTC_SetAlarm(&hrtc, &sAlarm, RTC_FORMAT_BIN);
}

// 闹钟中断回调
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc) {
    if (hrtc->Instance == RTC) {
        // 闹钟A触发处理
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}

// 中断服务函数
void RTC_Alarm_IRQHandler(void) {
    HAL_RTC_AlarmIRQHandler(&hrtc);
}

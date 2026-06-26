/**
 * STM32F407 RTC 初始化模板
 * 配置: LSE 32.768kHz, 24小时制
 */
#include "stm32f4xx_hal.h"

RTC_HandleTypeDef hrtc;

void RTC_Init(void) {
    // 1. 使能时钟
    __HAL_RCC_RTC_ENABLE();
    
    // 2. RTC配置
    hrtc.Instance = RTC;
    hrtc.Init.HourFormat = RTC_HOURFORMAT_24;            // 24小时制
    hrtc.Init.AsynchPrediv = 127;                        // LSE异步分频
    hrtc.Init.SynchPrediv = 255;                         // LSE同步分频
    hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
    hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
    hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
    HAL_RTC_Init(&hrtc);
    
    // 3. 设置日期: 2026年6月3日 星期二
    RTC_DateTypeDef sDate = {0};
    sDate.Year = 26;
    sDate.Month = RTC_MONTH_JUNE;
    sDate.Date = 3;
    sDate.WeekDay = RTC_WEEKDAY_TUESDAY;
    HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BIN);
    
    // 4. 设置时间: 12:00:00
    RTC_TimeTypeDef sTime = {0};
    sTime.Hours = 12;
    sTime.Minutes = 0;
    sTime.Seconds = 0;
    HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BIN);
}

// 读取时间
void RTC_GetTime(RTC_TimeTypeDef *time, RTC_DateTypeDef *date) {
    HAL_RTC_GetTime(&hrtc, time, RTC_FORMAT_BIN);
    HAL_RTC_GetDate(&hrtc, date, RTC_FORMAT_BIN);  // 必须同时读日期
}

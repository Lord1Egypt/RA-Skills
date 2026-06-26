/**
 * STM32F407 FreeRTOS 初始化模板
 * 配置: 基本任务创建和调度
 */
#include "stm32f4xx_hal.h"
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

// 任务句柄
TaskHandle_t Task1_Handle = NULL;
TaskHandle_t Task2_Handle = NULL;

// 任务函数
void Task1(void *pvParameters) {
    while(1) {
        // 任务1: LED闪烁
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void Task2(void *pvParameters) {
    while(1) {
        // 任务2: 串口输出
        HAL_UART_Transmit(&huart1, (uint8_t*)"Task2\r\n", 7, 100);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void FreeRTOS_Init(void) {
    // 创建任务
    xTaskCreate(Task1, "LED_Task", 128, NULL, 2, &Task1_Handle);
    xTaskCreate(Task2, "UART_Task", 256, NULL, 1, &Task2_Handle);
    
    // 启动调度器
    vTaskStartScheduler();
}

// FreeRTOS钩子函数
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
    // 栈溢出处理
    while(1);
}

void vApplicationMallocFailedHook(void) {
    // 内存分配失败处理
    while(1);
}

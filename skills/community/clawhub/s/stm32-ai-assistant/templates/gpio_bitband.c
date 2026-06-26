/**
 * STM32F407 GPIO 位带操作模板
 * 位带别名区: 直接操作单个位，无需读-改-写
 */
#include "stm32f4xx_hal.h"

// 位带操作宏定义
// GPIOA输出: 0x42000000 + (PAx_offset) * 32 + bit * 4
// GPIOA输入: 0x42200000 + (PAx_offset) * 32 + bit * 4

// 示例: PA5 位带操作
#define PA5_ODR    (*((volatile unsigned long *)0x42212094))  // PA5输出
#define PA5_IDR    (*((volatile unsigned long *)0x422120A4))  // PA5输入

// 更通用的方式
#define BITBAND(addr, bitnum) ((addr & 0xF0000000) + 0x02000000 + ((addr & 0xFFFFF) << 5) + (bitnum << 2))
#define BIT_ADDR(addr, bitnum) (*(volatile unsigned long *)BITBAND(addr, bitnum))

// GPIO输出位带
#define GPIOA_ODR_Addr (GPIOA_BASE + 12)
#define GPIOB_ODR_Addr (GPIOB_BASE + 12)
#define GPIOC_ODR_Addr (GPIOC_BASE + 12)

// GPIO输入位带
#define GPIOA_IDR_Addr (GPIOA_BASE + 8)
#define GPIOB_IDR_Addr (GPIOB_BASE + 8)
#define GPIOC_IDR_Addr (GPIOC_BASE + 8)

// 宏定义
#define PAout(n) BIT_ADDR(GPIOA_ODR_Addr, n)
#define PAin(n)  BIT_ADDR(GPIOA_IDR_Addr, n)
#define PBout(n) BIT_ADDR(GPIOB_ODR_Addr, n)
#define PBin(n)  BIT_ADDR(GPIOB_IDR_Addr, n)
#define PCout(n) BIT_ADDR(GPIOC_ODR_Addr, n)
#define PCin(n)  BIT_ADDR(GPIOC_IDR_Addr, n)

// 使用示例:
// PA5 = 1;          // 设置PA5高电平
// PA5 = 0;          // 设置PA5低电平
// if (PA5 == 1)     // 读取PA5
// volatile bit = PA5;  // 读取单个位
//
// 位带操作优点:
// 1. 原子操作，无需关中断
// 2. 执行速度更快
// 3. 代码更简洁

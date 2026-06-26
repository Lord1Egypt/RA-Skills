/**
 * STM32F407 FLASH 操作模板
 * 配置: 内部Flash读写
 */
#include "stm32f4xx_hal.h"

// Flash扇区地址 (STM32F407)
#define FLASH_SECTOR7_ADDR  0x08060000  // 128KB扇区7

// 写入数据到Flash
HAL_StatusTypeDef Flash_Write(uint32_t addr, uint32_t *data, uint32_t len) {
    HAL_FLASH_Unlock();
    
    // 擦除扇区
    FLASH_EraseInitTypeDef erase = {0};
    erase.TypeErase = FLASH_TYPEERASE_SECTORS;
    erase.Sector = FLASH_SECTOR_7;
    erase.NbSectors = 1;
    erase.VoltageRange = FLASH_VOLTAGE_RANGE_3;
    
    uint32_t error;
    HAL_FLASHEx_Erase(&erase, &error);
    
    // 写入数据
    for (uint32_t i = 0; i < len; i++) {
        HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, addr + i*4, data[i]);
    }
    
    HAL_FLASH_Lock();
    return HAL_OK;
}

// 从Flash读取数据
void Flash_Read(uint32_t addr, uint32_t *buf, uint32_t len) {
    for (uint32_t i = 0; i < len; i++) {
        buf[i] = *(__IO uint32_t*)(addr + i*4);
    }
}

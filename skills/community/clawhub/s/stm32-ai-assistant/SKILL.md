---
name: stm32-ai-assistant
description: STM32嵌入式开发AI助手MCP Server。让AI编码助手直接查询STM32寄存器定义、生成HAL初始化代码。支持GPIO/USART/SPI/I2C/ADC/TIM/EXTI等外设。触发词：STM32、嵌入式、单片机、寄存器、HAL代码生成。
version: 1.0.0
author: zhaohe
tags: [stm32, embedded, mcu, mcp-server, hal, register, 嵌入式, 单片机]
---

# STM32 AI Assistant — MCP Server

> 让 AI 编码助手直接理解 STM32 寄存器，生成正确的 HAL 代码。

## 功能

- 📖 **寄存器查询** — "GPIO 的 MODER 寄存器有哪些位？" → 返回完整定义
- 📋 **外设列表** — "STM32F407 有哪些外设？" → 32个外设、81个实例
- 🔧 **代码生成** — "PA5 配置为推挽输出" → 完整 HAL 初始化代码
- 📊 **外设详情** — "USART 的所有寄存器" → 全部寄存器+访问类型

## 已支持芯片

| 芯片 | 外设 | 实例 | 寄存器 |
|------|------|------|--------|
| STM32F407 | 32 | 81 | 317 |

## 代码模板

GPIO / USART / TIM PWM / SPI / I2C / ADC / EXTI

## 使用方式

### 作为 MCP Server

```json
{
  "mcpServers": {
    "stm32": {
      "command": "python3",
      "args": ["stm32-ai-assistant/src/mcp_server.py"]
    }
  }
}
```

### 通过 OpenClaw 对话

```
帮我配置 STM32F407 的 USART1，115200 波特率，PA9 TX PA10 RX
```

## 安装

```bash
clawhub install stm32-ai-assistant
```

## 完整版

完整版含更多芯片（STM32F103/H743/ESP32）、位域定义、代码校验。

- 微信咨询：a175311344（备注：嵌入式AI）

## License

MIT

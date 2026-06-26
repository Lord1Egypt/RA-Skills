# STM32 AI Assistant 🤖

> 让 Codex / Claude Code / Cursor 直接理解 STM32 硬件，生成正确代码。

## 为什么需要这个？

当前 AI 编程工具写嵌入式代码时：
- ❌ 不知道寄存器位定义，靠"猜"
- ❌ 翻 1000 页数据手册才能配一个外设
- ❌ 生成的 HAL 代码经常有错

**本工具让 AI 像嵌入式工程师一样思考。**

## 7 个工具

| 工具 | 功能 | 示例 |
|------|------|------|
| `lookup_register` | 查寄存器位定义 | "GPIO MODER 有哪些位？" |
| `list_peripherals` | 列出芯片外设 | "STM32F407 有哪些外设？" |
| `get_peripheral_detail` | 外设全部寄存器 | "USART 的所有寄存器" |
| `generate_code` | 自然语言→代码 | "PA5 推挽输出" → HAL 代码 |
| `quick_reference` | 速查表 | "GPIO 有哪几种模式？" |
| `find_pins` | 查找可用引脚 | "USART1 TX 可以用哪些引脚？" |
| `check_code` | 代码检查 | 检查 HAL 常见错误 |

## 智能代码生成

```
输入: "PC13 推挽输出"
→ 自动识别引脚 PC13，替换模板中的 PA5
→ 输出完整 HAL 初始化代码

输入: "USART2 9600波特率"
→ 自动替换波特率
→ 输出正确配置
```

## 知识库

| 芯片 | 外设 | 实例 | 寄存器 | 位定义 |
|------|------|------|--------|--------|
| STM32F407 | 32 | 81 | 317 | 1,757 |
| STM32F103 | 24 | 41 | 170 | 1,065 |

## 代码模板

GPIO / USART / TIM PWM / SPI / I2C / ADC / EXTI / DMA / RTC / IWDG

## 引脚映射

支持 USART1/2/3, SPI1/2, I2C1/2, TIM2/3/4, ADC1

## 安装

```bash
clawhub install stm32-ai-assistant
```

## 配置 MCP Server

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

## 完整版

完整版含更多芯片、工业协议、数据手册RAG。

微信: a175311344（备注：嵌入式AI）

## License

MIT

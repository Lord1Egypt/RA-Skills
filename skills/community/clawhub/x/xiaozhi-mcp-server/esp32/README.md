# ESP32 WebSocket客户端

## 文件说明

| 文件 | 说明 |
|------|------|
| `xiaozhi_websocket_client.ino` | 完整Arduino示例 |
| `OpenClawMCP.h` | 可复用的类库 |

## 依赖库

在Arduino IDE中安装：

```
WebSocketsClient by Markus Sattler
ArduinoJson by Benoit Blanchon
```

## 使用方法

### 方式1：直接使用示例

1. 打开 `xiaozhi_websocket_client.ino`
2. 修改配置：
   ```cpp
   const char* WIFI_SSID = "你的WiFi";
   const char* WIFI_PASSWORD = "WiFi密码";
   const char* MCP_SERVER_HOST = "你的服务器IP";
   const char* MCP_TOKEN = "你的Token";
   ```
3. 上传到ESP32

### 方式2：集成到xiaozhi-esp32项目

1. 复制 `OpenClawMCP.h` 到项目目录
2. 在代码中引用：
   ```cpp
   #include "OpenClawMCP.h"
   
   OpenClawMCP mcp;
   
   void setup() {
       mcp.begin("服务器IP", 9000, "你的Token");
       mcp.setCallback(onMCPMessage);
   }
   
   void loop() {
       mcp.loop();
   }
   
   void onMCPMessage(const char* type, const char* taskId, const char* result) {
       // 收到任务结果，调用TTS播报
       if (strcmp(type, "task_completed") == 0) {
           speakText(result);  // 你的TTS函数
       }
   }
   ```

## 流程

```
用户说话
    ↓
调用 mcp.callTool("run_agent", "用户说的话", true)
    ↓
返回 task_id
    ↓
TTS播报 "任务进行中"
    ↓
WebSocket收到推送
    ↓
回调 onMCPMessage()
    ↓
TTS播报结果
```

## 测试

```bash
# 编译上传
arduino-cli compile --board esp32:esp32:esp32 .
arduino-cli upload --board esp32:esp32:esp32 --port /dev/ttyUSB0 .

# 查看日志
arduino-cli monitor --port /dev/ttyUSB0
```
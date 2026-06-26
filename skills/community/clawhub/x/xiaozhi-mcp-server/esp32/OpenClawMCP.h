/**
 * OpenClawMCP.h - OpenClaw MCP Client for ESP32
 * 
 * 用法：
 * 1. 在 xiaozhi-esp32 项目中添加此文件
 * 2. 修改配置参数
 * 3. 在主程序中调用 OpenClawMCP::begin()
 * 4. 在 loop() 中调用 OpenClawMCP::loop()
 */

#ifndef OPENCLAW_MCP_H
#define OPENCLAW_MCP_H

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

class OpenClawMCP {
private:
    String host;
    int port;
    String token;
    WebSocketsClient webSocket;
    bool connected;
    unsigned long lastHeartbeat;
    
    // 心跳间隔
    const unsigned long HEARTBEAT_INTERVAL = 30000;
    
    // 回调函数
    typedef void (*MessageCallback)(const char* type, const char* taskId, const char* result);
    MessageCallback onMessage;
    
    // WebSocket事件处理
    static void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
        OpenClawMCP* instance = (OpenClawMCP*)payload; // 简化处理
    }
    
public:
    OpenClawMCP() : connected(false), lastHeartbeat(0), onMessage(nullptr) {}
    
    /**
     * 初始化MCP客户端
     * @param serverHost 服务器IP
     * @param serverPort 服务器端口
     * @param authToken 认证Token
     */
    void begin(const char* serverHost, int serverPort, const char* authToken) {
        host = serverHost;
        port = serverPort;
        token = authToken;
        
        // 设置WebSocket
        String url = "/ws?token=" + String(token);
        webSocket.begin(host.c_str(), port, url);
        webSocket.onEvent([this](WStype_t type, uint8_t * payload, size_t length) {
            this->handleWsEvent(type, payload, length);
        });
        webSocket.setReconnectInterval(5000);
        webSocket.enableHeartbeat(30000, 10000, 2);
        
        Serial.println("[OpenClawMCP] 初始化完成");
    }
    
    /**
     * 主循环，需要在Arduino loop()中调用
     */
    void loop() {
        webSocket.loop();
        
        // 心跳
        unsigned long now = millis();
        if (connected && (now - lastHeartbeat > HEARTBEAT_INTERVAL)) {
            sendPing();
            lastHeartbeat = now;
        }
    }
    
    /**
     * 设置消息回调
     */
    void setCallback(MessageCallback callback) {
        onMessage = callback;
    }
    
    /**
     * 调用MCP工具
     * @param toolName 工具名称
     * @param message 消息内容
     * @param asyncMode 是否异步
     * @return 响应JSON字符串
     */
    String callTool(String toolName, String message, bool asyncMode = true) {
        HTTPClient http;
        String url = "http://" + host + ":" + String(port) + "/mcp";
        
        http.begin(url);
        http.addHeader("Authorization", "Bearer " + token);
        http.addHeader("Content-Type", "application/json");
        http.setTimeout(10000);
        
        // 构建请求
        StaticJsonDocument<512> doc;
        doc["jsonrpc"] = "2.0";
        doc["id"] = 1;
        doc["method"] = "tools/call";
        
        JsonObject params = doc.createNestedObject("params");
        params["name"] = toolName;
        
        JsonObject arguments = params.createNestedObject("arguments");
        arguments["message"] = message;
        arguments["async"] = asyncMode;
        
        String body;
        serializeJson(doc, body);
        
        int code = http.POST(body);
        String response = "";
        
        if (code == HTTP_CODE_OK) {
            response = http.getString();
        } else {
            Serial.printf("[OpenClawMCP] HTTP错误: %d\n", code);
        }
        
        http.end();
        return response;
    }
    
    /**
     * 是否已连接
     */
    bool isConnected() {
        return connected;
    }
    
private:
    void handleWsEvent(WStype_t type, uint8_t * payload, size_t length) {
        switch(type) {
            case WStype_CONNECTED:
                Serial.println("[OpenClawMCP] WebSocket连接成功");
                connected = true;
                break;
                
            case WStype_DISCONNECTED:
                Serial.println("[OpenClawMCP] WebSocket断开");
                connected = false;
                break;
                
            case WStype_TEXT:
                processMessage((char*)payload);
                break;
                
            default:
                break;
        }
    }
    
    void processMessage(const char* message) {
        StaticJsonDocument<4096> doc;
        deserializeJson(doc, message);
        
        const char* type = doc["type"];
        
        if (strcmp(type, "task_completed") == 0) {
            const char* taskId = doc["task_id"];
            const char* result = doc["result"];
            
            Serial.printf("[OpenClawMCP] 任务完成: %s\n", taskId);
            
            // 回调
            if (onMessage) {
                onMessage(type, taskId, result);
            }
        }
    }
    
    void sendPing() {
        if (!connected) return;
        
        StaticJsonDocument<64> doc;
        doc["type"] = "ping";
        
        char buffer[64];
        serializeJson(doc, buffer);
        webSocket.sendTXT(buffer);
        
        Serial.println("[OpenClawMCP] 发送心跳");
    }
};

#endif // OPENCLAW_MCP_H
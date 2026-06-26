# OpenClaw 常用配置示例

## 模型配置

### 切换主模型
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "siliconflow/Pro/MiniMaxAI/MiniMax-M2.5"
      }
    }
  }
}
```

### 添加视觉模型
```json
{
  "agents": {
    "defaults": {
      "models": {
        "siliconflow/Pro/MiniMaxAI/MiniMax-M2.5": {
          "alias": "MiniMax"
        },
        "siliconflow/Qwen/Qwen3-VL-8B-Instruct": {
          "alias": "Qwen3 VL"
        }
      }
    }
  }
}
```

### 在 SiliconFlow 添加新模型
```json
{
  "models": {
    "providers": {
      "siliconflow": {
        "models": [
          {
            "id": "Pro/moonshotai/Kimi-K2.5",
            "name": "Kimi K2.5",
            "contextWindow": 32000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

## 搜索配置

### ❌ 错误格式（常见误区）
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "kimi",
        "apiKey": "sk-xxx"  // ❌ 这是一个常见的错误写法
      }
    }
  }
}
```

### ✅ 正确格式 - Kimi 搜索
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "kimi",
        "kimi": {
          "apiKey": "sk-xxx"
        }
      }
    }
  }
}
```

### ✅ 正确格式 - Brave 搜索
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "brave",
        "apiKey": "xxx"
      }
    }
  }
}
```

## Channel 配置

### Telegram
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "xxx",
      "dmPolicy": "pairing"
    }
  }
}
```

### Kimi
```json
{
  "channels": {
    "kimi-claw": {
      "enabled": true,
      "config": {
        "bridge": {
          "token": "sk-xxx"
        }
      }
    }
  }
}
```

## Skills 目录

当前已安装的 skills：
- `~/.openclaw/skills/safe-config/` - 安全修改配置
- `~/.openclaw/skills/bocha-search/` - 博查搜索

## Gateway 管理

```bash
# 查看状态
openclaw gateway status

# 重启
openclaw gateway restart

# 停止
openclaw gateway stop

# 启动
openclaw gateway start
```
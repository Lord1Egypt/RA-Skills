# 📚 基础使用示例

## 概述

本文档提供Telegram语音消息技能的基础使用示例，帮助你快速上手。

## 示例1：最简单的使用流程

### 场景
发送一条简单的语音消息："你好，世界！"

### 步骤

#### 1. 设置环境变量
```bash
# 设置Telegram配置
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# 设置TTS服务配置（以阿里云为例）
export ALIYUN_TTS_API_KEY="your_aliyun_api_key_here"
```

#### 2. 生成音频
```bash
# 使用TTS生成脚本
./scripts/tts_generator.sh "你好，世界！"

# 输出示例：
# ℹ️  生成音频: 你好，世界！...
# ✅ 生成成功: /tmp/telegram_voice_1741584000/audio_1741584001.wav
# ✅ 转换成功: /tmp/telegram_voice_1741584000/output.ogg
# /tmp/telegram_voice_1741584000/output.ogg
```

#### 3. 发送消息
```bash
# 使用发送脚本
./scripts/telegram_sender.sh /tmp/telegram_voice_1741584000/output.ogg

# 输出示例：
# ℹ️  发送语音消息: output.ogg
# ℹ️  文件信息:
# ℹ️    大小: 0MB
# ℹ️    时长: 1.5秒
# ℹ️  尝试发送 (1/3)...
# ✅ 发送成功！
```

### 完整脚本
```bash
#!/bin/bash
# simple_voice_message.sh

# 设置配置
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export ALIYUN_TTS_API_KEY="your_api_key"

# 生成音频
audio_file=$(./scripts/tts_generator.sh "你好，世界！")

# 发送消息
./scripts/telegram_sender.sh "$audio_file"

echo "✅ 语音消息发送完成！"
```

## 示例2：带错误处理的完整流程

### 场景
发送语音消息，并处理可能出现的错误。

### 完整脚本
```bash
#!/bin/bash
# robust_voice_message.sh

set -e  # 遇到错误立即退出

# 配置检查函数
check_config() {
    local missing_vars=()
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        missing_vars+=("TELEGRAM_BOT_TOKEN")
    fi
    
    if [ -z "$TELEGRAM_CHAT_ID" ]; then
        missing_vars+=("TELEGRAM_CHAT_ID")
    fi
    
    if [ -z "$ALIYUN_TTS_API_KEY" ]; then
        missing_vars+=("ALIYUN_TTS_API_KEY")
    fi
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo "❌ 缺少环境变量: ${missing_vars[*]}"
        echo "💡 请设置: export 变量名=\"值\""
        exit 1
    fi
    
    echo "✅ 配置检查通过"
}

# 生成音频函数（带重试）
generate_audio_with_retry() {
    local text="$1"
    local max_retries=3
    
    for attempt in $(seq 1 $max_retries); do
        echo "尝试生成音频 ($attempt/$max_retries)..."
        
        local audio_file
        if audio_file=$(./scripts/tts_generator.sh "$text" 2>/dev/null); then
            echo "✅ 音频生成成功: $audio_file"
            echo "$audio_file"
            return 0
        fi
        
        if [ $attempt -lt $max_retries ]; then
            echo "等待2秒后重试..."
            sleep 2
        fi
    done
    
    echo "❌ 音频生成失败，已达到最大重试次数"
    return 1
}

# 发送消息函数（带重试）
send_message_with_retry() {
    local audio_file="$1"
    
    if ./scripts/telegram_sender.sh "$audio_file"; then
        echo "✅ 消息发送成功"
        return 0
    else
        echo "❌ 消息发送失败"
        return 1
    fi
}

# 清理函数
cleanup() {
    echo "🧹 清理临时文件..."
    # 脚本会自动清理，这里可以添加额外清理
}

# 主函数
main() {
    local text="你好，这是带错误处理的测试消息"
    
    echo "========================================"
    echo "Telegram语音消息发送示例"
    echo "文本: $text"
    echo "========================================"
    
    # 检查配置
    check_config
    
    # 生成音频
    echo ""
    echo "步骤1: 生成音频"
    local audio_file
    audio_file=$(generate_audio_with_retry "$text") || exit 1
    
    # 发送消息
    echo ""
    echo "步骤2: 发送消息"
    send_message_with_retry "$audio_file" || exit 1
    
    # 完成
    echo ""
    echo "========================================"
    echo "✅ 流程完成！语音消息已发送"
    echo "========================================"
}

# 设置退出时清理
trap cleanup EXIT

# 运行主函数
main "$@"
```

### 使用方式
```bash
# 设置环境变量
export TELEGRAM_BOT_TOKEN="xxx"
export TELEGRAM_CHAT_ID="yyy"
export ALIYUN_TTS_API_KEY="zzz"

# 运行脚本
./robust_voice_message.sh
```

## 示例3：批量发送消息

### 场景
批量发送多条语音消息。

### 脚本
```bash
#!/bin/bash
# batch_voice_messages.sh

# 消息列表
messages=(
    "早上好！今天是美好的一天。"
    "记得吃早餐，保持健康。"
    "工作顺利，加油！"
    "午休时间到了，放松一下。"
    "下班了，好好休息。"
)

echo "批量发送 ${#messages[@]} 条语音消息"
echo "========================================"

# 遍历消息列表
for i in "${!messages[@]}"; do
    message="${messages[$i]}"
    index=$((i + 1))
    
    echo ""
    echo "消息 $index/${#messages[@]}: ${message:0:30}..."
    
    # 生成音频
    audio_file=$(./scripts/tts_generator.sh "$message")
    if [ $? -ne 0 ]; then
        echo "❌ 生成失败，跳过此消息"
        continue
    fi
    
    # 发送消息
    if ./scripts/telegram_sender.sh "$audio_file"; then
        echo "✅ 发送成功"
    else
        echo "❌ 发送失败"
    fi
    
    # 短暂延迟，避免请求过快
    if [ $index -lt ${#messages[@]} ]; then
        echo "等待1秒..."
        sleep 1
    fi
done

echo ""
echo "========================================"
echo "批量发送完成！"
echo "========================================"
```

### 使用方式
```bash
# 设置环境变量
export TELEGRAM_BOT_TOKEN="xxx"
export TELEGRAM_CHAT_ID="yyy"
export ALIYUN_TTS_API_KEY="zzz"

# 运行批量脚本
./batch_voice_messages.sh
```

## 示例4：集成到现有系统

### 场景
将Telegram语音消息功能集成到现有的AI助手系统中。

### Python集成示例
```python
#!/usr/bin/env python3
# telegram_voice_integration.py

import os
import subprocess
import tempfile
import json

class TelegramVoiceSender:
    def __init__(self, config_file=None):
        """初始化Telegram语音消息发送器"""
        self.load_config(config_file)
        
    def load_config(self, config_file=None):
        """加载配置"""
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # 从环境变量加载
            self.config = {
                'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
                'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
                'aliyun_tts_api_key': os.getenv('ALIYUN_TTS_API_KEY')
            }
        
        # 验证配置
        self.validate_config()
    
    def validate_config(self):
        """验证配置"""
        required_keys = ['telegram_bot_token', 'telegram_chat_id']
        missing_keys = [key for key in required_keys if not self.config.get(key)]
        
        if missing_keys:
            raise ValueError(f"缺少必要配置: {missing_keys}")
    
    def send_voice_message(self, text, lang='zh'):
        """发送语音消息
        
        Args:
            text: 要发送的文本
            lang: 语言代码 (zh/en等)
        
        Returns:
            bool: 是否发送成功
        """
        try:
            print(f"发送语音消息: {text[:50]}...")
            
            # 设置环境变量
            env = os.environ.copy()
            env.update({
                'TELEGRAM_BOT_TOKEN': self.config['telegram_bot_token'],
                'TELEGRAM_CHAT_ID': self.config['telegram_chat_id']
            })
            
            if self.config.get('aliyun_tts_api_key'):
                env['ALIYUN_TTS_API_KEY'] = self.config['aliyun_tts_api_key']
            
            # 生成音频
            print("生成音频...")
            result = subprocess.run(
                ['./scripts/tts_generator.sh', text],
                capture_output=True,
                text=True,
                env=env,
                cwd=os.path.dirname(__file__)
            )
            
            if result.returncode != 0:
                print(f"音频生成失败: {result.stderr}")
                return False
            
            audio_file = result.stdout.strip()
            print(f"音频文件: {audio_file}")
            
            # 发送消息
            print("发送到Telegram...")
            result = subprocess.run(
                ['./scripts/telegram_sender.sh', audio_file],
                capture_output=True,
                text=True,
                env=env,
                cwd=os.path.dirname(__file__)
            )
            
            if result.returncode == 0:
                print("✅ 发送成功！")
                return True
            else:
                print(f"❌ 发送失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 发送过程中出错: {e}")
            return False

# 使用示例
if __name__ == "__main__":
    # 创建发送器实例
    sender = TelegramVoiceSender()
    
    # 发送测试消息
    success = sender.send_voice_message("你好，这是Python集成的测试消息")
    
    if success:
        print("测试通过！")
    else:
        print("测试失败！")
```

### Node.js集成示例
```javascript
// telegram_voice_integration.js
const { spawn } = require('child_process');
const path = require('path');

class TelegramVoiceSender {
    constructor(config = {}) {
        this.config = {
            telegramBotToken: process.env.TELEGRAM_BOT_TOKEN || config.telegramBotToken,
            telegramChatId: process.env.TELEGRAM_CHAT_ID || config.telegramChatId,
            aliyunTtsApiKey: process.env.ALIYUN_TTS_API_KEY || config.aliyunTtsApiKey
        };
        
        this.validateConfig();
    }
    
    validateConfig() {
        const required = ['telegramBotToken', 'telegramChatId'];
        const missing = required.filter(key => !this.config[key]);
        
        if (missing.length > 0) {
            throw new Error(`Missing required config: ${missing.join(', ')}`);
        }
    }
    
    /**
     * 发送语音消息
     * @param {string} text - 要发送的文本
     * @returns {Promise<boolean>} - 是否发送成功
     */
    async sendVoiceMessage(text) {
        return new Promise((resolve, reject) => {
            console.log(`Sending voice message: ${text.substring(0, 50)}...`);
            
            // 设置环境变量
            const env = {
                ...process.env,
                TELEGRAM_BOT_TOKEN: this.config.telegramBotToken,
                TELEGRAM_CHAT_ID: this.config.telegramChatId
            };
            
            if (this.config.aliyunTtsApiKey) {
                env.ALIYUN_TTS_API_KEY = this.config.aliyunTtsApiKey;
            }
            
            // 生成音频
            this.runScript('./scripts/tts_generator.sh', [text], env)
                .then(audioFile => {
                    console.log(`Audio generated: ${audioFile}`);
                    
                    // 发送消息
                    return this.runScript('./scripts/telegram_sender.sh', [audioFile.trim()], env);
                })
                .then(() => {
                    console.log('✅ Message sent successfully!');
                    resolve(true);
                })
                .catch(error => {
                    console.error(`❌ Failed to send message: ${error}`);
                    resolve(false);
                });
        });
    }
    
    /**
     * 运行shell脚本
     * @param {string} script - 脚本路径
     * @param {string[]} args - 参数
     * @param {Object} env - 环境变量
     * @returns {Promise<string>} - 脚本输出
     */
    runScript(script, args, env) {
        return new Promise((resolve, reject) => {
            const child = spawn(script, args, {
                cwd: path.dirname(__dirname),
                env: env
            });
            
            let output = '';
            let error = '';
            
            child.stdout.on('data', data => {
                output += data.toString();
            });
            
            child.stderr.on('data', data => {
                error += data.toString();
            });
            
            child.on('close', code => {
                if (code === 0) {
                    resolve(output);
                } else {
                    reject(new Error(`Script failed with code ${code}: ${error}`));
                }
            });
            
            child.on('error', reject);
        });
    }
}

// 使用示例
async function main() {
    try {
        const sender = new TelegramVoiceSender();
        const success = await sender.sendVoiceMessage('Hello from Node.js integration!');
        
        if (success) {
            console.log('Test passed!');
        } else {
            console.log('Test failed!');
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// 运行测试
if (require.main === module) {
    main();
}

module.exports = TelegramVoiceSender;
```

## 示例5：命令行工具封装

### 场景
创建简单的命令行工具，方便日常使用。

### 脚本
```bash
#!/bin/bash
# telegram-voice-cli.sh

VERSION="1.0.0"
CONFIG_FILE="$HOME/.telegram_voice_config"

# 显示帮助
show_help() {
    cat << EOF
Telegram语音消息命令行工具 v${VERSION}

用法:
  $0 [命令] [选项]

命令:
  send <文本>          发送语音消息
  config               配置工具
  test                 测试连接
  version              显示版本
  help                 显示帮助

选项:
  -c, --chat <ID>      指定聊天ID
  -f, --file <文件>    从文件读取文本
  -l, --lang <语言>    指定语言 (zh/en)
  -q, --quiet          安静模式
  -v, --verbose        详细模式

示例:
  $0 send "你好，世界！"
  $0 send -c "123456789" "测试消息"
  $0 send -f message.txt
  $0 config
  $0 test
EOF
}

# 加载配置
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    fi
    
    # 检查必要配置
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "❌ 未配置TELEGRAM_BOT_TOKEN"
        echo "💡 请运行: $0 config"
        exit 1
    fi
    
    if [ -z "$TELEGRAM_CHAT_ID" ]; then
        echo "❌ 未配置TELEGRAM_CHAT_ID"
        echo "💡 请运行: $0 config"
        exit 1
    fi
}

# 保存配置
save_config() {
    cat > "$CONFIG_FILE" << EOF
# Telegram语音消息配置
# 生成时间: $(date)

# Telegram配置
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID"

# TTS服务配置
ALIYUN_TTS_API_KEY="$ALIYUN_TTS_API_KEY"
OPENAI_API_KEY="$OPENAI_API_KEY"

# 音频配置
AUDIO_BITRATE="64k"
AUDIO_SAMPLE_RATE="48000"
EOF
    
    chmod 600 "$CONFIG_FILE"
    echo "✅ 配置已保存到: $CONFIG_FILE"
}

# 配置命令
config_command() {
    echo "🔧 Telegram语音消息配置"
    echo "========================================"
    
    # 读取现有配置
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    fi
    
    # Telegram配置
    echo ""
    echo "1. Telegram配置:"
    read -p "Bot Token [${TELEGRAM_BOT_TOKEN:-未设置}]: " token
    if [ -n "$token" ]; then
        TELEGRAM_BOT_TOKEN="$token"
    fi
    
    read -p "Chat ID [${TELEGRAM_CHAT_ID:-未设置}]: " chat_id
    if [ -n "$chat_id" ]; then
        TELEGRAM_CHAT_ID="$chat_id"
    fi
    
    # TTS配置
    echo ""
    echo "2. TTS服务配置:"
    read -p "阿里云TTS API Key [${ALIYUN_TTS_API_KEY:-未设置}]: " aliyun_key
    if [ -n "$aliyun_key" ]; then
        ALIYUN_TTS_API_KEY="$aliyun_key"
    fi
    
    read -p "OpenAI API Key [${OPENAI_API_KEY:-未设置}]: " openai_key
    if [ -n "$openai_key" ]; then
        OPENAI_API_KEY="$openai_key"
    fi
    
    # 保存配置
    save_config
}

# 发送命令
send_command() {
    local text="$1"
    local chat_id="$TELEGRAM_CHAT_ID"
    
    # 检查文本
    if [ -z "$text" ]; then
        echo "❌ 未指定要发送的文本"
        show_help
        exit 1
    fi
    
    # 设置环境变量
    export TELEGRAM_BOT_TOKEN
    export TELEGRAM_CHAT_ID="$chat_id"
    
    if [ -n "$ALIYUN_TTS_API_KEY" ]; then
        export ALIYUN_TTS_API_KEY
    fi
    
    if [ -n "$OPENAI_API_KEY" ]; then
        export OPENAI_API_KEY
    fi
    
    echo "📤 发送语音消息..."
    echo "   文本: ${text:0:50}..."
    echo "   接收者: $chat_id"
    
    # 生成音频
    audio_file=$(./scripts/tts_generator.sh "$text")
    if [ $? -ne 0 ]; then
        echo "❌ 音频生成失败"
        exit 1
    fi
    
    # 发送消息
    if ./scripts/telegram_sender.sh "$audio_file"; then
        echo "✅ 消息发送成功！"
    else
        echo "❌ 消息发送失败"
        exit 1
    fi
}

# 测试命令
test_command() {
    echo "🧪 测试Telegram连接..."
    
    load_config
    
    # 测试配置
    echo "1. 配置测试:"
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        echo "   ✅ TELEGRAM_BOT_TOKEN: 已设置"
    else
        echo "   ❌ TELEGRAM_BOT_TOKEN: 未设置"
    fi
    
    if [ -n "$TELEGRAM_CHAT_ID" ]; then
        echo "   ✅ TELEGRAM_CHAT_ID: 已设置"
    else
        echo "   ❌ TELEGRAM_CHAT_ID: 未设置"
    fi
    
    # 测试发送
    echo ""
    echo "2. 发送测试消息..."
    send_command "这是一条测试消息。如果收到此消息，说明配置正确。"
}

# 主函数
main() {
    local command="$1"
    
    case "$command" in
        send)
            shift
            load_config
            send_command "$@"
            ;;
        config)
            config_command
            ;;
        test)
            test_command
            ;;
        version)
            echo "Telegram语音消息命令行工具 v${VERSION}"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            if [ -z "$command" ]; then
                show_help
            else
                echo "❌ 未知命令: $command"
                show_help
                exit 1
            fi
            ;;
    esac
}

# 运行主函数
main "$@"
```

### 使用方式
```bash
# 1. 配置工具
./telegram-voice-cli.sh config

# 2. 测试连接
./telegram-voice-cli.sh test

# 3. 发送消息
./telegram-voice-cli.sh send "你好，这是命令行工具测试！"

# 4. 从文件发送
echo "这是文件中的消息" > message.txt
./telegram-voice-cli.sh send -f message.txt
```

## 总结

这些示例展示了Telegram语音消息技能的不同使用方式：

1. **基础使用**: 最简单的发送流程
2. **错误处理**: 健壮的生产环境脚本
3. **批量发送**: 处理多条消息
4. **系统集成**: Python和Node.js集成示例
5. **命令行工具**: 方便日常使用

选择适合你需求的示例，根据实际情况进行调整。所有示例都遵循最佳实践，确保消息发送的可靠性和安全性。

---
**示例版本**: 1.0.0  
**创建日期**: 2026-03-09  
**更新日期**: 2026-03-09  

*"好的示例是成功的一半"*
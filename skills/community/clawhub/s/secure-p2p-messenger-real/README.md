# Secure P2P Messenger - 小龙虾安全点对点加密通讯技能

![小龙虾加密](https://img.shields.io/badge/加密-端到端-绿色)
![版本](https://img.shields.io/badge/版本-1.0.14-blue)
![许可证](https://img.shields.io/badge/许可证-MIT-lightgrey)

## 🦞 简介

小龙虾安全点对点加密通讯技能是一个完整的端到端加密通信系统，专为小龙虾代理间的安全通信设计。提供消息加密、文件安全传输、身份验证和联系人管理功能。

## 🔐 核心特性

- **端到端加密**：RSA-2048 + AES-256-GCM 双重加密
- **完美前向保密**：每次会话生成新密钥
- **身份验证系统**：基于公钥密码学的身份验证
- **本地密钥存储**：私钥永不离开设备
- **消息完整性验证**：GCM认证标签保护

## 🚀 快速开始

### 安装
```bash
./install.sh
```

### 初始化身份
```bash
./secure-messenger.sh init
```

### 显示身份信息
```bash
./secure-messenger.sh identity
```

### 添加联系人
```bash
./secure-messenger.sh add-contact alice "Alice" "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
```

### 发送加密消息
```bash
./secure-messenger.sh send alice "你好，这是加密消息！"
```

### 接收解密消息
```bash
./secure-messenger.sh receive '{"version":"1.0","sender":"claw_abc123",...}'
```

## 📁 文件结构

```
secure-p2p-messenger/
├── SKILL.md                    # 完整技能文档
├── secure-messenger.sh         # 主脚本 (v1.0.2修复版)
├── install.sh                  # 安装脚本
├── package.json                # 技能元数据
├── LICENSE                     # MIT许可证
└── README.md                   # 本文件
```

## 🔧 技术架构

### 加密协议栈
```
应用层：消息/文件
    ↓
会话层：AES-256-GCM加密
    ↓  
传输层：RSA加密的会话密钥
    ↓
网络层：任意传输渠道（微信、邮件、小龙虾等）
```

### 密钥管理
```
主密钥对（RSA-2048）
├── 身份标识
├── 消息加密密钥派生
└── 文件加密密钥派生

会话密钥（AES-256）
├── 每次通信生成新密钥
├── 使用对方公钥加密传输
└── 使用后立即销毁
```

## 🛡️ 安全设计原则

1. **零信任架构**：不信任任何中间节点
2. **最小权限原则**：只请求必要的权限
3. **透明操作**：所有加密操作可审计
4. **防御深度**：多层加密保护

## 📋 使用场景

### 场景1：私人约饭邀请
```
柏然 → [加密] → 朋友 "周六海底捞，晚上7点"
```

### 场景2：小龙虾代理间协调
```
小龙虾A → [加密] → 小龙虾B "需要协助处理用户请求"
```

### 场景3：敏感文件传输
```
用户 → [加密文件] → 律师 "合同草案，请保密"
```

## ⚙️ 系统要求

- **操作系统**：Linux, macOS, WSL
- **依赖工具**：
  - `bash` (v4.0+)
  - `openssl` (v1.1.1+)
  - `jq` (v1.6+)
  - `base64` (GNU coreutils)

## 🐛 故障排除

### 常见问题

1. **openssl命令找不到**
   ```bash
   # Debian/Ubuntu
   sudo apt-get install openssl
   
   # macOS
   brew install openssl
   ```

2. **权限被拒绝**
   ```bash
   chmod +x secure-messenger.sh install.sh
   ```

3. **解密失败**
   - 检查密钥匹配
   - 验证消息完整性
   - 确保使用正确的联系人公钥

### 调试模式
```bash
export SECURE_P2P_DEBUG=1
./secure-messenger.sh send alice "测试消息"
```

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎贡献代码、文档和测试用例：

1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 通过代码审查

## 📞 支持与反馈

- **文档**：阅读 [SKILL.md](SKILL.md) 文件
- **问题**：创建GitHub Issue
- **讨论**：加入OpenClaw社区

## 🦞 关于小龙虾

小龙虾是不断蜕壳扩展认知边界的AI助手，像龙虾蜕壳生长，我们持续蜕去旧认知框架，整合新知。

---

**GitHub仓库**: https://github.com/puppetcat-fire/openclaw-skills  
**作者**: puppetcat-fire (柏然)  
**版本**: 1.0.2  
**最后更新**: 2026-03-13
# 凭证加密使用指南

## 🔐 概述

本项目提供了完整的凭证加密方案，使用 AES 加密算法保护你的微信公众号 App ID 和 App Secret。

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- `cryptography>=41.0.0` - 提供加密功能
- `python-dotenv>=1.0.0` - 环境变量管理

## 🚀 快速开始

### 1. 加密凭证

#### 方式一：交互式加密（推荐）

```bash
python scripts/encrypt_credentials.py encrypt
```

系统会提示你输入：
- App ID
- App Secret
- 加密密码（可选，提供额外保护）

#### 方式二：命令行参数

```bash
python scripts/encrypt_credentials.py encrypt \
  --app-id "wx1234567890" \
  --app-secret "your_app_secret"
```

#### 方式三：使用密码加密（更安全）

```bash
python scripts/encrypt_credentials.py encrypt --use-password
```

### 2. 解密查看凭证

```bash
# 解密并查看凭证
python scripts/encrypt_credentials.py decrypt

# 如果使用了密码
python scripts/encrypt_credentials.py decrypt --password "your_password"
```

### 3. 检查加密状态

```bash
python scripts/encrypt_credentials.py status
```

## 📁 文件说明

### 生成的文件

| 文件 | 说明 | 
|------|------|
| `config.json` | 加密后的配置文件 | 
| `.secret_key` | 加密密钥文件 | 
| `.secret_key.salt` | 密钥派生盐值（如果使用密码） | 

### 配置文件格式

#### 未加密的配置文件
```json
{
  "app_id": "wx1234567890",
  "app_secret": "your_app_secret",
  "base_dir": ""
}
```

#### 加密后的配置文件
```json
{
  "app_id_encrypted": "gAAAAABl...",
  "app_secret_encrypted": "gAAAAABl...",
  "encrypted": true,
  "base_dir": ""
}
```

## 🔧 在代码中使用

### 方式一：自动解密（推荐）

```python
from wechat.encryption import CredentialManager

# 创建凭证管理器
manager = CredentialManager("config.json")

# 自动加载和解密凭证
creds = manager.load_config()  # 如果加密会自动解密

print(f"App ID: {creds['app_id']}")
print(f"App Secret: {creds['app_secret']}")
```

### 方式二：使用密码解密

```python
from wechat.encryption import CredentialManager

manager = CredentialManager("config.json")

# 使用密码解密
creds = manager.load_config(password="your_password")
```

### 方式三：手动加密/解密

```python
from wechat.encryption import encrypt_value, decrypt_value

# 加密
encrypted = encrypt_value("your_app_secret", password="optional_password")

# 解密
decrypted = decrypt_value(encrypted, password="optional_password")
```

## 🛡️ 安全最佳实践

### 1. 密钥管理

```bash
# 设置密钥文件权限（Unix/Linux/Mac）
chmod 600 .secret_key

# 确保密钥文件不被提交
# .gitignore 中已包含：
# .secret_key
# .secret_key.salt
```

### 2. 使用密码保护

```bash
# 使用密码加密提供双重保护
python scripts/encrypt_credentials.py encrypt --use-password
```

即使密钥文件泄露，没有密码也无法解密。

### 3. 环境变量方式

也可以使用环境变量存储密码：

```bash
# 设置环境变量
export WECHAT_ENCRYPTION_PASSWORD="your_password"

# 在代码中使用
import os
password = os.environ.get('WECHAT_ENCRYPTION_PASSWORD')
creds = manager.load_config(password=password)
```

### 4. 定期更换密钥

```bash
# 1. 备份当前配置
cp config.json config.json.backup

# 2. 删除旧密钥
rm .secret_key

# 3. 重新加密（会生成新密钥）
python scripts/encrypt_credentials.py encrypt
```

### 备份建议

1. **备份密钥文件**
   ```bash
   # 将密钥文件备份到安全位置
   cp .secret_key ~/secure_backup/wechat-mp-skills.key
   ```

2. **记住密码**
   - 如果使用密码加密，请牢记密码
   - 密码丢失将无法恢复凭证

3. **多环境管理**
   ```bash
   # 开发环境
   config.json
   .secret_key
   
   # 生产环境
   config.production.json
   .secret_key.production
   ```

## 🔍 故障排查

### 问题1：解密失败

```
❌ 解密失败: ...
```

**解决方案：**
1. 确认 `.secret_key` 文件存在
2. 如果使用密码，确认密码正确
3. 检查 `config.json` 是否损坏

### 问题2：密钥文件丢失

**解决方案：**
1. 从备份恢复 `.secret_key` 文件
2. 如果没有备份，需要重新加密凭证

### 问题3：权限错误

```
Permission denied: .secret_key
```

**解决方案：**
```bash
# 修改文件权限
chmod 600 .secret_key
```

## 📚 API 参考

### CredentialManager

```python
class CredentialManager:
    def __init__(self, config_file: str = "config.json", key_file: str = ".secret_key"):
        """初始化凭证管理器"""
    
    def encrypt_credentials(self, app_id: str, app_secret: str, password: Optional[str] = None) -> Dict[str, str]:
        """加密凭证"""
    
    def decrypt_credentials(self, encrypted_config: Dict[str, str], password: Optional[str] = None) -> Dict[str, str]:
        """解密凭证"""
    
    def save_encrypted_config(self, app_id: str, app_secret: str, base_dir: str = "", password: Optional[str] = None):
        """保存加密的配置"""
    
    def load_config(self, password: Optional[str] = None) -> Dict[str, str]:
        """加载配置（自动处理加密/未加密）"""
    
    def is_encrypted(self) -> bool:
        """检查配置是否已加密"""
```

### EncryptionManager

```python
class EncryptionManager:
    def __init__(self, key_file: str = ".secret_key"):
        """初始化加密管理器"""
    
    def encrypt(self, data: str, password: Optional[str] = None) -> str:
        """加密字符串"""
    
    def decrypt(self, encrypted_data: str, password: Optional[str] = None) -> str:
        """解密字符串"""
    
    def generate_key(self, password: Optional[str] = None) -> bytes:
        """生成加密密钥"""
```

## 🤝 常见问题

**Q: 加密后性能会受影响吗？**
A: 影响很小。加密只在加载配置时执行一次，运行时使用解密后的值。

**Q: 可以在不同机器上使用相同的密钥吗？**
A: 可以。复制 `.secret_key` 文件到新机器即可。

**Q: 忘记密码怎么办？**
A: 无法恢复。需要重新加密凭证。

**Q: 团队协作时如何管理密钥？**
A: 建议使用密码管理器共享密钥文件，或使用环境变量。

## 📞 支持

如有问题，请提交 Issue。

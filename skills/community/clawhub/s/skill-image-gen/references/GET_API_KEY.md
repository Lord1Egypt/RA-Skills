# 获取 Gitee AI API Key 说明文档

本文档详细说明如何获取 Gitee AI 的免费 API Key，并配置到 free-image-gen 技能中。

## 📋 目录

- [什么是 Gitee AI](#什么是-gitee-ai)
- [注册账号](#注册账号)
- [获取 API Key](#获取-api-key)
- [配置到技能](#配置到技能)
- [测试验证](#测试验证)
- [常见问题](#常见问题)

---

## 什么是 Gitee AI

Gitee AI 是 Gitee 推出的 AI 开发平台，提供：
- 🆓 **免费额度**：新用户有免费调用额度
- 🎨 **图片生成**：支持 Kolors 等多种图片生成模型
- 🚀 **快速接入**：简单的 API 接口，易于集成

官网：https://ai.gitee.com/

---

## 注册账号

### 第一步：访问 Gitee AI

打开浏览器，访问：https://ai.gitee.com/

### 第二步：注册账号

**如果你已有 Gitee 账号：**
- 直接点击右上角"登录"
- 使用你的 Gitee 账号登录

**如果你没有 Gitee 账号：**
1. 点击"注册"按钮
2. 填写注册信息：
   - 用户名
   - 邮箱
   - 密码
3. 完成邮箱验证
4. 登录成功

---

## 获取 API Key

### 第一步：进入控制台

登录后，点击右上角的头像或用户名，选择"控制台"或"个人中心"。

或者直接访问：https://ai.gitee.com/dashboard

### 第二步：找到 API 管理页面

在控制台中，找到以下选项之一：
- "API 管理"
- "密钥管理"
- "访问令牌"
- "API Keys"

通常在左侧菜单或顶部导航栏中。

### 第三步：创建新的 API Key

1. 点击"创建新密钥"或"生成 API Key"按钮
2. 输入密钥名称（可选），例如：`free-image-gen`
3. 选择权限（如果有选项）
4. 点击"确认"或"创建"按钮

### 第四步：复制 API Key

**⚠️ 重要提示：创建成功后，API Key 只会显示一次！**

1. 看到生成的 API Key（一长串字符）
2. 立即点击"复制"按钮，或手动选择复制
3. 保存到安全的地方

**API Key 格式示例：**
```
EXXSO8UHNBKI8AHK9TXM5KOILPDUISI25HIKOJ73
```

**⚠️ 安全提示：**
- 不要分享给其他人
- 不要提交到 GitHub 等公开仓库
- 不要在公开场合展示

---

## 配置到技能

### 方法一：手动配置（推荐）

**步骤 1：创建配置目录**

```bash
# Linux/macOS
mkdir -p ~/.openclaw/skills/free-image-gen

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.openclaw\skills\free-image-gen"
```

**步骤 2：创建配置文件**

创建文件：`~/.openclaw/skills/free-image-gen/config.json`

**Linux/macOS：**
```bash
cat > ~/.openclaw/skills/free-image-gen/config.json << 'EOF'
{
  "gitee": {
    "api_key": "你的API_Key_粘贴到这里",
    "model": "Kolors",
    "base_url": "https://ai.gitee.com/v1"
  },
  "cos": {
    "enabled": false
  },
  "output": {
    "path": "./output",
    "format": "png"
  }
}
EOF
```

**Windows：**
```powershell
$config = @"
{
  "gitee": {
    "api_key": "你的API_Key_粘贴到这里",
    "model": "Kolors",
    "base_url": "https://ai.gitee.com/v1"
  },
  "cos": {
    "enabled": false
  },
  "output": {
    "path": "./output",
    "format": "png"
  }
}
"@
$config | Out-File -FilePath "$env:USERPROFILE\.openclaw\skills\free-image-gen\config.json" -Encoding utf8
```

**步骤 3：编辑配置文件**

用文本编辑器打开配置文件，把 `你的API_Key_粘贴到这里` 替换成你的实际 API Key。

### 方法二：通过对话配置

如果你使用 OpenClaw 的 AI Agent，可以直接告诉 AI 你的 API Key：

```
我的 Gitee AI API Key 是：EXXSO8UHNBKI8AHK9TXM5KOILPDUISI25HIKOJ73
```

AI 会自动帮你更新配置文件。

### 方法三：复制示例文件

```bash
# 复制示例文件
cp references/config.example.json ~/.openclaw/skills/free-image-gen/config.json

# 编辑配置文件
nano ~/.openclaw/skills/free-image-gen/config.json
```

---

## 测试验证

### 测试配置是否正确

**方法一：运行测试脚本**

```bash
cd <技能目录>
python -c "from scripts.config import Config; c = Config(interactive=False); print(f'API Key: {c.get(\"gitee.api_key\")}')"
```

如果输出你的 API Key，说明配置成功。

**方法二：生成测试图片**

```bash
cd <技能目录>
python scripts/main.py --prompt "一只可爱的小狗" --output ./test.png
```

如果成功生成图片，说明配置完全正确。

### 验证成功标志

- ✅ 配置文件路径正确
- ✅ API Key 显示正确
- ✅ 图片生成成功

---

## 常见问题

### Q1: API Key 在哪里查看？

**A:** API Key 创建后只会显示一次，建议立即保存。如果忘记了，可以：
1. 在控制台中查看是否有"查看密钥"选项
2. 如果没有，只能删除旧密钥，重新创建一个

### Q2: API Key 有使用限制吗？

**A:** 是的，Gitee AI 有以下限制：
- **免费额度**：新用户有一定免费额度
- **调用频率**：有 API 调用频率限制
- **并发数**：同时请求数量有限制

具体限制请查看 Gitee AI 控制台的"用量"或"配额"页面。

### Q3: API Key 泄露了怎么办？

**A:** 立即采取以下措施：
1. 登录 Gitee AI 控制台
2. 找到泄露的 API Key
3. 点击"删除"或"禁用"
4. 创建新的 API Key
5. 更新配置文件

### Q4: 提示"API Key 无效"怎么办？

**A:** 检查以下几点：
1. API Key 是否正确复制（没有多余空格）
2. API Key 是否已激活
3. 账号是否欠费或被限制
4. API Key 是否已过期或被删除

### Q5: 免费额度用完了怎么办？

**A:** 有以下选择：
1. **等待重置**：有些额度会定期重置
2. **充值**：在控制台中充值购买额度
3. **使用其他平台**：考虑使用其他免费图片生成服务

### Q6: 配置文件找不到？

**A:** 检查配置文件是否在正确位置：
- **推荐位置**：`~/.openclaw/skills/free-image-gen/config.json`
- **项目位置**：`./config.json` 或 `./.free-image-gen/config.json`

### Q7: 如何查看剩余额度？

**A:** 登录 Gitee AI 控制台，在"用量"或"配额"页面查看：
- 已使用额度
- 剩余额度
- 额度重置时间

---

## 🔗 相关链接

- [Gitee AI 官网](https://ai.gitee.com/)
- [Gitee AI 文档](https://ai.gitee.com/docs)
- [Gitee AI 控制台](https://ai.gitee.com/dashboard)
- [技能主文档](../SKILL.md)
- [配置文件示例](./config.example.json)

---

## 📝 更新日志

- 2026-03-10：创建文档，添加详细的获取步骤和常见问题

---

**需要帮助？**

如果遇到问题，可以：
1. 查看 [技能主文档](../SKILL.md)
2. 查看 [配置说明](./README.md)
3. 联系技能开发者

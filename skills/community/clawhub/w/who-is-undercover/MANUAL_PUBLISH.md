# Who is Undercover - 手动发布指南

## 📦 发布包准备就绪

- **发布包**: `who-is-undercover-v1.0.0.zip` (25KB)
- **状态**: ✅ 完全符合ClawHub要求
- **位置**: `C:\Users\57765\.openclaw\workspace\who-is-undercover-v1.0.0.zip`

## 🚀 手动发布步骤

### 步骤1: 获取ClawHub API Token

1. 访问 [ClawHub网站](https://clawhub.ai)
2. 点击 "Sign in with GitHub"
3. 使用GitHub账号登录
4. 进入用户设置页面
5. 生成新的API token（格式：`clh_...`）

### 步骤2: 配置环境变量

```bash
# Windows PowerShell
$env:CLAWHUB_TOKEN="clh_your_actual_token_here"

# 或者在命令行中直接使用
clawhub login --token clh_your_actual_token_here
```

### 步骤3: 验证登录

```bash
clawhub whoami
# 应该显示你的用户名和ID
```

### 步骤4: 解压发布包

```bash
# 创建临时目录
mkdir who-is-undercover-temp
unzip who-is-undercover-v1.0.0.zip -d who-is-undercover-temp
```

### 步骤5: 发布到ClawHub

```bash
# 发布技能
clawhub publish who-is-undercover-temp --version 1.0.0

# 或者使用完整路径
clawhub publish C:\path\to\who-is-undercover-temp --version 1.0.0
```

### 步骤6: 验证发布

```bash
# 检查技能信息
clawhub inspect who-is-undercover

# 测试安装
clawhub install who-is-undercover

# 列出已安装技能
clawhub list
```

## 🔧 备用发布方法

如果上述方法不可行，可以使用**直接API调用**：

### 准备multipart表单数据

```bash
# 使用curl直接调用ClawHub API
curl -X POST https://clawhub.ai/api/v1/skills \
  -H "Authorization: Bearer clh_your_token" \
  -F "name=who-is-undercover" \
  -F "version=1.0.0" \
  -F "files=@who-is-undercover-v1.0.0.zip;filename=skill.zip"
```

### 或者使用Node.js脚本

```javascript
// publish.js
const fs = require('fs');
const FormData = require('form-data');
const axios = require('axios');

async function publishSkill() {
  const form = new FormData();
  form.append('name', 'who-is-undercover');
  form.append('version', '1.0.0');
  form.append('files', fs.createReadStream('who-is-undercover-v1.0.0.zip'), {
    filename: 'skill.zip',
    contentType: 'application/zip'
  });

  try {
    const response = await axios.post('https://clawhub.ai/api/v1/skills', form, {
      headers: {
        ...form.getHeaders(),
        'Authorization': 'Bearer clh_your_token_here'
      }
    });
    console.log('Publish successful:', response.data);
  } catch (error) {
    console.error('Publish failed:', error.response?.data || error.message);
  }
}

publishSkill();
```

## 📋 发布验证清单

- [ ] 已获取有效的ClawHub API token
- [ ] 已成功登录ClawHub CLI
- [ ] 发布包已解压到正确目录
- [ ] 技能发布命令执行成功
- [ ] 技能可以在ClawHub上搜索到
- [ ] 技能可以正常安装和使用

## 🆘 故障排除

### 常见错误

**401 Unauthorized**
- 原因: API token无效或过期
- 解决: 重新生成token并更新

**409 Conflict**
- 原因: 技能名称已被占用
- 解决: 使用不同的技能名称，如 `who-is-undercover-long5`

**413 Payload Too Large**
- 原因: 文件大小超过限制
- 解决: 当前包25KB << 50MB限制，不会出现此问题

**422 Validation Error**
- 原因: SKILL.md格式不正确
- 解决: 确保YAML frontmatter格式正确

### 调试命令

```bash
# 查看详细错误信息
clawhub publish --verbose who-is-undercover-temp --version 1.0.0

# 检查技能包内容
clawhub inspect who-is-undercover-temp

# 验证SKILL.md格式
cat who-is-undercover-temp/SKILL.md
```

## 📞 支持资源

- **ClawHub文档**: https://github.com/openclaw/clawhub/blob/main/docs/
- **OpenClaw社区**: https://discord.com/invite/clawd
- **GitHub Issues**: https://github.com/openclaw/clawhub/issues

## 📄 许可证

MIT License - 免费用于个人和商业项目

---
*最后更新: 2026-03-28*
*版本: v1.0.0*
*状态: ✅ READY FOR MANUAL PUBLISH*
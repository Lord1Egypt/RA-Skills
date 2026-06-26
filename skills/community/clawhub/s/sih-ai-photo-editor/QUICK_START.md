# Sih.Ai - 快速开始指南

## 🚀 5分钟上手测试

### 1. 测试API连接

```bash
cd /Users/chensong/.openclaw/workspace/sih-ai-photo-changer

# 测试API
python3 scripts/sih_api.py <图片路径> "把衣服换成bikini"
```

### 2. 测试配额系统

```bash
# 查看用户信息（首次会创建新用户并赠送5次免费）
python3 scripts/quota_checker.py info

# 模拟充值（测试用）
python3 scripts/quota_checker.py add 100

# 查看使用历史
python3 scripts/quota_checker.py history

# 显示充值链接
python3 scripts/quota_checker.py topup
```

### 3. 完整流程测试

```python
from scripts.sih_api import SihClient
from scripts.quota_checker import QuotaChecker

# 初始化
quota = QuotaChecker()
client = SihClient()

# 显示当前用户信息
quota.show_user_info()

# 示例：处理图片
prompt = "把衣服换成红色连衣裙"
image_path = "test.jpg"

# 估算费用
cost = quota.estimate_cost(prompt)
print(f"预估消耗: {cost}积分")

# 检查余额
if not quota.has_balance(cost):
    quota.show_topup_url()
else:
    # 扣费并处理
    result = quota.deduct(cost, operation="change_clothes", prompt=prompt)
    print(f"✅ 扣费成功，剩余: {result['remaining']}积分")

    # 调用API
    api_result = client.edit_image(image_path, prompt)
    print(f"🎨 处理完成: {api_result['url']}")
```

---

## 📦 发布检查清单

### 打包前测试
- [ ] API连接正常（测试sih_api.py）
- [ ] 配额系统正常（测试quota_checker.py）
- [ ] Python脚本无语法错误
- [ ] 所有文档齐全

### 打包命令
```bash
cd /Users/chensong/.openclaw/workspace
python3 /Users/chensong/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py sih-ai-photo-changer
```

### 上传到ClawHub
1. 访问 https://clawhub.com/upload
2. 上传 `sih-ai-photo-changer.skill`
3. 填写上架信息：
   - **标题:** Sih.Ai - AI Photo Changer
   - **描述:** 见 PUBLISH.md
   - **分类:** 图片处理 / AI工具
   - **标签:** #AI #换装 #换背景 #换脸 #风格转换

---

## 🔧 配置说明

### API Key配置
API Key已预设在 `scripts/config.py`：
```python
SIH_API_KEY = "sk-w4YfLvoXwIEM0I3uNcOOOclfHkBDiR19Md9ixabWv1XMNPhn"
```

生产环境建议使用环境变量：
```bash
export SIH_API_KEY="your-production-key"
```

### 用户数据位置
配额数据存储在：
```
~/.sih_ai/
├── current_user.json     # 当前用户信息
└── usage_history.jsonl   # 使用历史记录
```

---

## 📝 用户使用流程

1. **首次使用**
   - OpenClaw自动创建用户ID
   - 赠送5次免费体验

2. **余额不足时**
   - 显示充值链接（包含用户ID）
   - 用户跳转到 https://sih.ai/topup?user=xxx

3. **充值完成后**
   - 用户返回OpenClaw
   - 发送消息"已充值"或继续使用
   - 系统自动检查余额更新

---

## 🐛 常见问题

### Q1: API调用失败
**A:** 检查网络连接和API Key是否正确

### Q2: 配额文件损坏
**A:** 删除 `~/.sih_ai/` 目录，重新初始化

### Q3: 充值后余额未更新
**A:** 当前版本需要手动触发刷新（发送"已充值"消息）

---

**技术支持:** support@sih.ai
**文档更新:** 2026-03-13

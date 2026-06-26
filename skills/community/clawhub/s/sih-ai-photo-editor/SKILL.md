---
name: sih-ai-photo-changer
description: AI图片编辑工具，支持自然语言驱动的换装、换背景、换脸、风格转换（动漫/粘土/油画等）、美颜修图。当用户需要AI图片处理、人像编辑、背景替换、风格迁移、服装更换、脸部融合时使用此skill。支持用户通过描述性prompt（如"把衣服换成bikini"、"背景换成海边"、"转换成动漫风格"）进行图片编辑。
---

# Sih.Ai - AI Photo Changer

**让图片听你的话** —— 用自然语言描述，AI自动完成编辑

---

## 🚀 快速开始

用户上传图片 → 用一句话描述想要的改变 → AI处理 → **自动下载并预览**

```python
# 示例调用
from scripts.sih_api import SihClient

client = SihClient(api_key="your-api-key")
result = client.edit_image(
    image_url="https://example.com/photo.jpg",
    prompt="把衣服换成红色连衣裙，背景换成海边"
)
# 自动下载到 Desktop/Sih_Ai_Results/
# 自动在Finder中显示
# 自动在预览中打开
```

### ✨ 新功能：自动下载和预览

**处理完成后，图片会自动：**
1. 📥 下载到 `~/Desktop/Sih_Ai_Results/` 文件夹
2. 📂 在Finder中高亮显示
3. 👁️ 在预览app中打开

**无需手动下载或二次处理，直接查看效果！**

---

## ✨ 核心功能

### 人像编辑
- **换服装** - "把衣服换成bikini"、"穿上西装"、"换成汉服"
- **换发型** - "把头发剪短"、"染成金色"、"烫卷发"
- **换妆容** - "化个烟熏妆"、"加个口红"

### 背景处理
- **换背景** - "背景换成海边"、"背景改成城市夜景"、"背景换成咖啡厅"
- **移除背景** - "去掉背景"、"只保留人物"、"透明背景"
- **虚化背景** - "背景虚化"、"突出人物"

### 风格转换
- **艺术风格** - "转换成油画风格"、"水彩画效果"、"素描风格"
- **动漫/二次元** - "动漫化"、"二次元风格"、" manga style"
- **特效风格** - "粘土风"、"赛博朋克"、"复古胶片"

### 智能修图
- **人脸融合** - "把脸换成[明星名字]"、"换脸到这张图"
- **身材调整** - "瘦身"、"增高"、"调整身材比例"
- **美颜** - "磨皮"、"美白"、"去痘痘"

---

## 🔧 使用流程

### 1. 初始化客户端

```python
from scripts.sih_api import SihClient
from scripts.quota_checker import QuotaChecker

# 使用Sih.Ai的API（需要用户提供API Key）
client = SihClient(api_key="sk-xxxxx")

# 或使用统一服务（需要用户ID和配额验证）
quota = QuotaChecker(user_id="user123")
if not quota.has_balance():
    print("余额不足，请充值：https://sih.ai/topup?user=user123")
```

### 2. 支持的输入格式

```python
# URL格式
client.edit_image(
    image_url="https://example.com/photo.jpg",
    prompt="换服装成bikini"
)

# Base64格式
client.edit_image(
    image_base64="data:image/jpeg;base64,/9j/4AAQ...",
    prompt="背景换成海边"
)

# 本地文件（会自动转Base64）
client.edit_image(
    image_path="/path/to/photo.jpg",
    prompt="动漫化"
)
```

### 3. 高级参数

```python
client.edit_image(
    image_url="...",
    prompt="换服装成bikini",
    model="sihai-image-27",  # 可选：模型选择
    size="1024x1024"  # 可选：输出尺寸
)
```

---

## 📝 Prompt最佳实践

### ✅ 好的Prompt

```
"把衣服换成红色bikini，背景换成海边沙滩"
"换装成白色婚纱，背景改成教堂"
"转换成动漫风格，背景改成樱花树下"
"脸换成Angelababy，保持原姿势"
"去掉背景，只保留人物"
```

### ❌ 避免的Prompt

```
"P一下"          # 太模糊，AI不知道具体要做什么
"好看一点"        # 主观描述不够具体
"修一修"          # 需要明确具体修改内容
```

### 💡 Prompt技巧

1. **具体描述** - "红色连衣裙" 比 "好看的裙子" 更好
2. **组合操作** - 可以同时要求换装+换背景+换风格
3. **保留元素** - "保持原姿势"、"保持面部表情"
4. **风格明确** - "日系动漫"、"美式漫画"、"3D渲染"

---

## 💰 配额与计费

### 用户自带API Key模式
```python
client = SihClient(api_key="user_provided_key")
# 直接调用，计费由用户自己在Sih.Ai后台处理
```

### 统一服务模式（推荐）
```python
from scripts.quota_checker import QuotaChecker

quota = QuotaChecker(user_id="user123")

# 检查余额
if not quota.check_balance():
    # 返回充值链接
    quota.show_topup_url()
    # https://sih.ai/topup?user=user123&return=xxx
else:
    # 扣除配额并处理
    quota.deduct(credits=10)
    result = client.edit_image(...)
```

### 计费建议
- **基础操作** - 5-10积分（换背景、简单换装）
- **复杂操作** - 15-20积分（换脸、风格转换）
- **批量处理** - 按图片数量累加

---

## 🎯 触发场景

**优先使用此skill当用户提到：**

### 直接触发
- "换服装"、"换背景"、"换脸"、"换发型"
- "P图"、"修图"、"美颜"、"精修"
- "动漫化"、"二次元"、"粘土风"、"风格转换"
- "AI处理图片"、"图片生成"、"图片编辑"

### 场景触发
- "这张照片帮我修一下"
- "能不能把背景换成xxx"
- "我想试试xxx风格的照片"
- "帮我P成动漫角色"
- "照片里的人能不能换成xxx"

### 关键词
```
人像：换装、换脸、换发型、化妆、美颜、瘦身、增高
背景：换背景、去背景、虚化、替换场景
风格：动漫、油画、水彩、素描、粘土、赛博朋克、复古
操作：修图、P图、美化、精修、处理、转换、生成
```

---

## 🛠️ 技术细节

### API Endpoint
```
POST https://api.vwu.ai/v1/images/generations/
```

### 认证方式
```
Authorization: Bearer sk-xxxxx
```

### 请求参数
```json
{
  "image": ["https://example.com/photo.jpg"],
  "prompt": "把衣服换成bikini",
  "model": "sihai-image-27"
}
```

### 响应格式
```json
{
  "model": "sihai-image-27",
  "created": 1773386658,
  "data": [
    {
      "url": "https://...",
      "size": "2048x2048"
    }
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 16384,
    "total_tokens": 16384
  }
}
```

---

## 📚 参考资料

- **完整API文档** - 见 `references/api_guide.md`
- **Prompt示例** - 见 `assets/examples/prompts.txt`
- **配额验证API** - 需要Sih.Ai提供余额查询endpoint

---

## ⚠️ 注意事项

1. **图片限制** - 确保图片URL可公网访问，或使用Base64格式
2. **API Key安全** - 不要在代码中硬编码API Key
3. **配额管理** - 每次操作前验证余额，避免处理失败
4. **错误处理** - API失败时返回友好提示给用户

---

**Sih.Ai官网：** https://sih.ai  
**充值中心：** https://sih.ai/topup  
**技术支持：** support@sih.ai

---
name: xiaohongshu-image-gen
description: 【爆款标题】小红书图片太难做？AI一键生成爆款配图，3个赛道任选！

你是不是觉得小红书配图难弄？要找图、要修图、要符合平台调性...没专业技能做不出那种"网红感"？

本工具用 AI 生成技术（DALL-E 3 / SDXL），输入文字自动生成高质量图片，专注家装/美食/穿搭 3 大热门赛道，竖屏/横屏/正方形规格全适配！

✨ **核心亮点**：
- AI一键生成：文字 → 高质量图片（支持 DALL-E 3 + SDXL）
- 赛道专精：家装、美食、穿搭、旅行 4大热门赛道
- 规格优化：竖屏/横屏/正方形，适配不同笔记类型
- 提示词增强：自动添加小红书风格前缀后缀

📁 **典型场景**：
- 小红书博主：快速生成爆款配图
- 电商卖家：产品图、场景图
- 个人品牌：打造统一视觉风格

🎯 **为什么选我**：
✅ 专注小红书，赛道优化最懂平台
✅ 多模型支持（DALL-E 3 + SDXL），质量有保障
✅ 无需设计技能，AI 全自动

👉 立即体验：`clawhub install xiaohongshu-image-gen`
---

# 小红书图片生成技能

为小红书爆款笔记生成高质量图片，专注家装、美食、穿搭、旅行等热门赛道。

## 核心功能

### 1. 智能提示词增强
- 自动添加小红书风格的前缀和后缀
- 针对不同赛道优化提示词
- 提升图片生成质量

### 2. 多赛道支持

| 赛道 | 风格选项 | 特点 |
|------|---------||------|
| **家装** | 现代简约、北欧、日式、美式、中式、轻奢、法式 | 竖屏为主，注重空间感 |
| **美食** | 精致摆盘、家常菜、烘焙、饮品、甜点、日料、西餐 | 高清摄影，食欲感 |
| **穿搭** | 春夏季、秋冬、休闲、职场、约会、运动 | 模特拍摄，ins风 |
| **旅行** | 海边、山景、城市、古镇、日出日落 | 风景摄影，网红打卡 |

### 3. 多种生成方式

**优先级从高到低：**
1. **OpenAI DALL-E 3**（推荐，质量最高）
   - 配置：`export OPENAI_API_KEY="sk-..."`
   - 支持：1024x1792（竖屏）、1792x1024（横屏）、1024x1024（正方形）

2. **Stability AI Stable Diffusion XL**
   - 配置：`export STABILITY_API_KEY="sk-..."`
   - 支持：自定义尺寸

3. **本地 image-generate**（降级方案）
   - 无需 API Key
   - 自动调用已安装的 image-generate 技能

### 4. 小红书规格优化
- 默认竖屏 9:16（最适合笔记）
- 正方形 1:1（适合封面）
- 横屏 16:9（适合拼图）

## 使用方法

### 基础用法
```bash
# 家装风格（默认）
xiaohongshu-image-gen --prompt "客厅白色沙发搭配原木色地板"

# 美食风格
xiaohongshu-image-gen --prompt "日式拉面汤浓面劲道" --style "美食"

# 穿搭风格
xiaohongshu-image-gen --prompt "米色风衣搭配白色直筒裤" --style "穿搭"

# 旅行风格
xiaohongshu-image-gen --prompt "海边日落" --style "旅行"
```

### 指定具体风格
```bash
xiaohongshu-image-gen \
  --prompt "开放式厨房设计" \
  --style "家装" \
  --substyle "现代简约"

xiaohongshu-image-gen \
  --prompt "春季穿搭" \
  --style "穿搭" \
  --substyle "职场"
```

### 指定宽高比
```bash
# 竖屏（笔记正文，默认）
xiaohongshu-image-gen --prompt "客厅设计" --aspect "竖屏"

# 正方形（封面图）
xiaohongshu-image-gen --prompt "客厅设计" --aspect "正方形"

# 横屏（拼图）
xiaohongshu-image-gen --prompt "客厅设计" --aspect "横屏"
```

### 使用本地生成（无需 API Key）
```bash
xiaohongshu-image-gen --prompt "现代简约客厅" --use-local
```

### 查看所有可用风格
```bash
xiaohongshu-image-gen --list-styles
```

## 典型场景

### 家装博主
```bash
# 生成装修效果图
xiaohongshu-image-gen --prompt "90平现代简约三居室" --style "家装" --substyle "现代简约"

# 生成细节图
xiaohongshu-image-gen --prompt "北欧风卧室床头柜搭配" --style "家装" --substyle "北欧"
```

### 美食博主
```bash
# 生成诱人美食图
xiaohongshu-image-gen --prompt "日式便当摆盘" --style "美食" --substyle "日料"

# 生成烘焙成品图
xiaohongshu-image-gen --prompt "草莓奶油蛋糕" --style "美食" --substyle "烘焙"
```

### 穿搭博主
```bash
# 生成穿搭示范
xiaohongshu-image-gen --prompt "春季职场穿搭" --style "穿搭" --substyle "职场"

# 生成约会穿搭
xiaohongshu-image-gen --prompt "法式连衣裙" --style "穿搭" --substyle "约会"
```

## 技术细节

### 提示词增强逻辑
```
前缀 + 具体风格 + 用户提示词 + 后缀
```

**家装示例：**
```
输入：客厅白色沙发
输出：装修设计，现代简约风格，客厅白色沙发，高清摄影
```

**美食示例：**
```
输入：日式拉面
输出：美食摄影，精致摆盘风格，日式拉面，美食拍摄
```

### 降级机制
1. 检查 `OPENAI_API_KEY` → 使用 DALL-E 3
2. 检查 `STABILITY_API_KEY` → 使用 Stable Diffusion XL
3. 都没有 → 自动降级到本地 image-generate

## 与其他技能配合

### 配合 xiaohongshu-content
```bash
# 1. 生成笔记内容（使用 xiaohongshu-content 技能）
# 2. 生成配图（使用本技能）
xiaohongshu-image-gen --prompt "90平现代简约客厅" --style "家装"
```

### 配合 social-publisher
```bash
# 生成多张图片后，使用 social-publisher 发布
xiaohongshu-image-gen --prompt "封面图" --aspect "正方形" --output "cover.png"
xiaohongshu-image-gen --prompt "正文图1" --output "img1.png"
xiaohongshu-image-gen --prompt "正文图2" --output "img2.png"
```

## 故障排查

### 问题：提示"未找到 image-generate 脚本"
**解决**：先安装 image-generate 技能
```bash
clawhub install image-generate
```

### 问题：OpenAI API 调用失败
**解决**：检查 API Key 是否正确
```bash
echo $OPENAI_API_KEY
```

### 问题：图片质量不够好
**建议**：
- 使用更具体的提示词（如"北欧风白色布艺沙发"而不是"沙发"）
- 尝试使用 OpenAI DALL-E（质量最高）
- 指定宽高比为"竖屏"

## 安全说明
- API Key 从环境变量读取，不会记录到日志
- 支持降级到本地生成，无需暴露凭证
- 所有生成过程在本地完成，不上传用户图片

## License
MIT

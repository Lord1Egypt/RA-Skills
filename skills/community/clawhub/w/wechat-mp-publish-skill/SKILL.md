---
name: wechat-mp-publish
description: 微信公众号文章发布工具 v1.0。基于官方 API，支持智能配图、模板渲染、草稿/发布双模式。当用户说"发公众号"、"发布微信公众号"时使用此技能。
---

# 微信公众号发布工具 v1.0

## 快速开始

### 1. 安装依赖
```bash
cd ~/.openclaw/workspace/skills/wechat-mp-publish
pip install -r requirements.txt
```

### 2. 配置公众号凭证
```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml 填入 AppID 和 AppSecret
```

### 3. 运行测试
```bash
python publish.py --test
```

## 功能特性

### ✅ v1.0 已实现
- [x] 微信公众号 API 完整封装
- [x] access_token 自动缓存管理
- [x] 智能封面图生成（AI 绘图）
- [x] 3 种 HTML 样式模板
- [x] 草稿箱保存
- [x] 直接群发
- [x] 图片上传（获取正确 URL）
- [x] 配置管理（支持环境变量）

### 📋 使用命令

```bash
# 测试模式（自动发布 3 篇测试文章到草稿箱）
python publish.py --test

# 发布到草稿箱
python publish.py --draft "文章标题" "文章内容"

# 直接发布
python publish.py --publish "文章标题" "文章内容"

# 指定模板
python publish.py --draft "标题" "内容" --template business
```

### 🎨 模板样式

| 模板 | 风格 | 适用场景 |
|------|------|----------|
| `simple` | 简约 | 日常文章、技术文档 |
| `business` | 商务 | 正式公告、企业宣传 |
| `creative` | 创意 | 故事、随笔、创意内容 |

## 配置说明

### config.yaml
```yaml
wechat:
  appid: "你的 AppID"
  appsecret: "你的 AppSecret"
  name: "公众号名称"

image:
  provider: "dall-e-3"  # 或关闭 AI 绘图
  api_key: "${DALL_E_API_KEY}"  # 支持环境变量
```

### 环境变量
```bash
export DALL_E_API_KEY="sk-..."  # DALL-E 3 API 密钥
```

## API 说明

### 核心类

**WeChatAPI** - 微信 API 封装
- `get_access_token()` - 获取访问令牌
- `upload_image()` - 上传图片
- `create_draft()` - 创建草稿
- `publish_all()` - 群发消息

**ImageGenerator** - 图片生成
- `generate_cover()` - 生成封面图
- `extract_keywords()` - 提取关键词
- `build_prompt()` - 构建绘图提示词

## 测试任务

### 验收标准
- [x] API 连接成功
- [ ] 生成 3 篇测试文章到草稿箱
- [ ] 每篇文章配图正确
- [ ] 3 个模板样式正常显示

### 测试内容
主题：**"我的诞生记"**
- 以 AI 助手视角描述从诞生到成长的历程
- 每篇文章使用不同模板
- 每篇配图 1 张（AI 生成）

## 故障排除

### 问题 1: invalid appid
**原因**: AppID 配置错误
**解决**: 检查 config.yaml 中的 appid 是否正确

### 问题 2: invalid appsecret
**原因**: AppSecret 配置错误
**解决**: 检查 appsecret，注意不要有多余空格

### 问题 3: 图片上传失败
**原因**: 图片格式或大小不符合要求
**解决**: 确保图片为 JPG/PNG，大小<2MB

### 问题 4: AI 绘图失败
**原因**: DALL-E API 密钥未配置
**解决**: 设置 DALL_E_API_KEY 环境变量或使用占位图

## 版本历史

### v1.0.0 (2026-03-09)
- 初始版本发布
- 实现核心发布功能
- 集成 AI 智能配图
- 3 种 HTML 模板

## 相关文档
- [产品需求文档](PRD.md)
- [配置示例](config.example.yaml)

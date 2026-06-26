---
name: qianfan-tools
description: 百度千帆工具箱 - 集成百度千帆平台多种免费 API | Baidu Qianfan Tools - Integrate Baidu Qianfan Platform APIs
metadata:
  author: 寇助理
  openclaw:
    emoji: 🔧
    category: tools
    tags: [qianfan, baidu, search, ai, tools, text-generation]
    requires:
      env: [BAIDU_API_KEY]
    primaryEnv: BAIDU_API_KEY
---

# 百度千帆工具箱 | Baidu Qianfan Tools

> 集成百度千帆平台 API，一个技能搞定多个工具！
> Integrate Baidu Qianfan Platform APIs - one skill for multiple tools!

## 📋 功能列表 | Features

### ✅ 已测试可用 | Tested & Working
| 功能 | 脚本 | 描述 |
|------|------|------|
| 智能搜索 | `ai-search.js` | 搜索 + AI 总结，返回结构化结果 |
| 百度热搜 | `hotword.js` | 获取实时热搜榜单 |

### 🔧 支持的 API (需开通) | Supported APIs (Requires Activation)
| 功能 | 脚本 | 描述 | 赠送额度 |
|------|------|------|---------|
| 文本生成 | `chat.js` | 文心大模型对话 | - |
| 续写 | `continue.js` | 文本续写 | - |
| 图像生成 | `image.js` | AI 绘图 | - |
| 通用 OCR | `ocr.js` | 图片文字识别 | - |
| 作文识别 | `ocr-essay.js` | 手写作文 OCR | 10次/天 |
| PPT生成 | `ppt.js` | 智能 PPT | 5次/天 |
| 百度学术 | `academic.js` | 学术搜索 | 1000次/天 |

## 🚀 快速开始 | Quick Start

### 1. 配置 API Key | Configure API Key

在 Skills 配置页面填写 `BAIDU_API_KEY`，或编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "qianfan-tools": {
        "env": {
          "BAIDU_API_KEY": "你的百度千帆 API Key"
        }
      }
    }
  }
}
```

本地使用 | Local usage:
```bash
cp config.example.json config.json
# 编辑 config.json 填入 apiKey
```

### 2. 使用方式 | Usage

```bash
cd skills/qianfan-tools
export BAIDU_API_KEY="你的APIKey"

# 智能搜索 | Smart Search
node scripts/ai-search.js "查询内容" [数量]

# 百度热搜 | Baidu Hot Search
node scripts/hotword.js

# 文本对话 (需开通) | Text Chat (requires activation)
node scripts/chat.js "你好"

# 图像生成 (需开通) | Image Generation (requires activation)
node scripts/image.js "一只可爱的猫"

# OCR 文字识别 (需开通) | OCR (requires activation)
node scripts/ocr.js <图片URL>

# PPT生成 (需开通) | PPT Generation (requires activation)
node scripts/ppt.js "主题内容"

# 百度学术 (需开通) | Academic Search (requires activation)
node scripts/academic.js "关键词" [数量]
```

## 📊 API 额度参考 | API Quota Reference

| API | 每日赠送 | 基础定价 |
|-----|---------|---------|
| 智能搜索生成 | 100次 | 0.036元/次 |
| 百度搜索 | 1000次 | 0.036元/次 |
| 百度百科 | 1000次 | 0.036元/次 |
| 百度热搜 | 10次 | 0.06元/次 |
| PPT生成 | 5次 | 2.5元/次 |
| 初中作文识别 | 10次 | 0.03元/次 |
| 高中作文识别 | 10次 | 0.05元/次 |
| 百度学术 | 1000次 | 0.07-0.66元/次 |

## ⚠️ 注意事项 | Notes

1. **API Key 获取**: 访问 [百度千帆控制台](https://console.bce.baidu.com/qianfan/) 创建 API Key
2. **额度查询**: 部分 API 需要在千帆平台开通才能使用
3. **免费额度**: 每日赠送额度用完后将按量计费

## 📁 项目结构 | Project Structure

```
qianfan-tools/
├── SKILL.md              # 本文档
├── _meta.json            # 元数据
├── package.json          # 依赖
├── config.example.json   # 配置模板
└── scripts/
    ├── shared.js         # 共享工具
    ├── ai-search.js      # 智能搜索 ✅
    ├── hotword.js        # 百度热搜 ✅
    ├── chat.js           # 文本对话
    ├── continue.js       # 文本续写
    ├── image.js          # 图像生成
    ├── ocr.js            # 通用 OCR
    ├── ocr-essay.js     # 作文 OCR
    ├── ppt.js            # PPT生成
    └── academic.js       # 百度学术
```

## 🔗 相关链接 | Links

- [百度千帆控制台](https://console.bce.baidu.com/qianfan/)
- [API 文档](https://cloud.baidu.com/doc/qianfan-api/s/3m9b5lqft)
- [ClawHub 技能市场](https://clawhub.com/skill/qianfan-tools)

---

**提示**: 本技能复用一个 API Key，统一管理更方便！
**Tip**: This skill uses one API Key for all tools - unified management!

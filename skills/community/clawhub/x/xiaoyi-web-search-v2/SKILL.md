---
name: xiaoyi-web-search
description: 使用华为云AI联网增强API进行网页内容检索，获取实时网络信息
---

# 小艺联网搜索 Skill

## 简介

通过华为云 AI 联网增强 API 实时获取最新的网页信息、新闻、资料等内容。

## 使用场景描述

### ✅ 适合场景

1. 需要获取**最新网络信息**时
2. 需要查询**实时新闻、资料**时
3. 需要**验证或补充已过时**的信息时
4. 用户**明确要求联网获取搜索结果**时
5. 需要中文优化的搜索结果时

### ❌ 不适合场景

1. 纯计算或本地数据处理
2. 用户要求不使用网络
3. 已有可靠本地信息

### 优势

- ✅ **智能联网增强** - 支持自定义搜索结果数量
- ✅ **简洁输出** - 清晰展示搜索结果
- ✅ **中文优化** - 适合中文搜索场景

## ⚙️ 安装后必读：配置 TOKEN

这个 skill 需要**华为云 AI 联网增强服务**的 TOKEN 才能工作。安装后首次使用前，务必完成以下三步配置。

### 📋 配置步骤（共3步，约10分钟）

#### 第1步：开通华为云服务

访问以下链接开通"AI 联网增强"服务：

👉 <https://developer.huawei.com/consumer/cn/doc/AppGallery-connect-Guides/agc-ainetworking-serviceopen-0000002370503878>

在华为开发者后台操作流程：
1. 登录账号（如无账号则先注册）
2. 找到 **AppGallery Connect** → **AI 联网增强服务**
3. 点击 **立即开通**
4. 记录系统生成的 **Token**

#### 第2步：找到配置文件

开通后，用文本编辑器打开本 skill 的配置文件：

```bash
# 找到 skill 目录
cd ~/.openclaw/workspace/skills/xiaoyi-web-search

# 用编辑器打开 web-access.js
vim scripts/web-access.js
```

#### 第3步：填入 TOKEN

在 `web-access.js` 文件中找到这两行（约第13-17行）：

```javascript
// 👇 把你的 TOKEN 填入下面引号中
const TOKEN = '';
```

改为：

```javascript
// 👇 把你的 TOKEN 填入下面引号中
const TOKEN = '你的TOKEN值';  // 替换为第1步获取的Token
```

保存文件即可。

### ✅ 验证配置是否生效

运行一条测试搜索：

```bash
cd ~/.openclaw/workspace/skills/xiaoyi-web-search
node ./scripts/web-access.js "测试" -n 3
```

- ✅ **配置成功** → 正常返回搜索结果
- ❌ **未配置** → 报错：`401 - Don't match authenticationService`
- ❌ **Token 过期** → 重新执行第2、3步更新 Token

## 使用方法

### 文件结构

```
xiaoyi-web-search/
├── SKILL.md             # 使用说明（本文档）
├── scripts/
│   └── web-access.js    # 主程序（执行联网搜索）
├── _meta.json           # Skill 元数据
└── package.json         # 项目配置
```

### 命令行调用

```bash
# 进入 skill 目录
cd ~/.openclaw/workspace/skills/xiaoyi-web-search

# 默认搜索（10条结果）
node ./scripts/web-access.js "人工智能最新进展"

# 指定返回数量
node ./scripts/web-access.js "ChatGPT 新闻" -n 10
```

### Node.js 代码调用

```javascript
const { webSearch } = require('./scripts/web-access.js');

async function searchExample() {
  const results = await webSearch('人工智能最新进展', 10);
  console.log(results);
}
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | ✅ | - | 搜索关键词 |
| count | number | ❌ | 10 | 返回结果数量（建议 5-15） |

## 注意事项

1. **Token 有效期**：Token 会过期，如遇 `401` 错误，需重新获取并更新
2. **搜索优化**：使用准确、具体的关键词可获得更好的结果
3. **结果数量**：建议 count 设置在 5-15 之间，平衡信息量和处理速度
4. **内容安全**：返回的结果可能包含各种信息，请根据实际需求过滤和验证

## 总结

当需要联网搜索时：
1. ✅ 先确认 TOKEN 已正确配置
2. ✅ 明确搜索目标，构建准确的关键词
3. ✅ 调用华为云 AI 联网增强 API
4. ✅ 整理和总结搜索结果
5. ✅ 以用户友好的方式呈现

记住：联网搜索是获取最新信息的强大工具，但要确保关键词准确、结果可信。✅

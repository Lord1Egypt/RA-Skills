---
name: rumour-buster-setup
description: Rumour Buster 初始化设置子技能。通过对话交互完成配置，检查依赖、设置 Tavily API、选择搜索引擎。
version: 0.2.0
---

# Rumour Buster Setup - 对话式初始化设置

## 触发方式

### 自动触发
- 首次安装 rumour-buster 时
- 首次运行主技能时（如 setup 未完成）

### 手动触发
用户输入：
- `setup`
- `重新设置`
- `/rumour-buster setup`

---

## 对话流程

### 第一步：欢迎与依赖检查

**系统**：
```
🔧 Rumour Buster 初始化设置

你好！我是 Rumour Buster（谣言终结者），一个帮你验证消息真假的 AI 助手。

让我先检查一下必需的依赖...
```

**检查 multi-search-engine**：
- 如果已安装：
  ```
  ✅ multi-search-engine 已安装
  ```
- 如果未安装：
  ```
  ❌ 缺少必需依赖：multi-search-engine
  
  请执行以下命令安装：
    clawhub install api-multi-search-engine
  
  安装完成后，发送 "继续" 继续设置，或 "退出" 稍后设置。
  ```

---

### 第二步：检测已有搜索技能

**系统**：
```
🔍 正在检测已安装的搜索引擎...

发现以下可用引擎：
  ✅ kimi_search（中文聚合搜索）
  ✅ multi-search-engine（多引擎搜索）
    - 中文：搜狗、搜狗微信、头条
    - 英文：DuckDuckGo、Startpage
```

---

### 第三步：配置 Tavily（对话式）

**系统**：
```
📚 关于 Tavily（英文深度搜索）

Tavily 是专为 AI 设计的搜索引擎：
  ✅ 每月 1000 次免费查询
  ✅ AI 智能总结答案
  ✅ 可信度评分
  ✅ 覆盖 WHO、NIH、BBC 等国际权威来源

是否启用 Tavily 搜索？（推荐启用）
回复 "是" 或 "否"：
```

**用户回复 "是"**：
```
太好了！请按以下步骤申请 Tavily API Key：

1️⃣ 访问 https://tavily.com/
2️⃣ 点击 "Sign Up" 注册账号
3️⃣ 进入 Dashboard → API Keys
4️⃣ 点击 "Create New Key"
5️⃣ 复制生成的 Key（格式：tvly-xxxxxxxx）

申请完成后，请直接粘贴你的 API Key：
```

**用户粘贴 API Key**：
- 如果格式正确（以 tvly- 开头）：
  ```
  ✅ API Key 格式正确！
  
  正在验证...
  ✅ Tavily 连接成功！
  免费额度：1000 次/月
  ```
- 如果格式不正确：
  ```
  ⚠️ API Key 格式不正确，应以 "tvly-" 开头
  请重新输入，或发送 "跳过" 暂不配置：
  ```

**用户回复 "否" 或 "跳过"**：
```
⏭️  已跳过 Tavily 配置

你仍然可以使用以下英文搜索引擎：
  - DuckDuckGo（隐私保护）
  - Startpage（Google 结果 + 隐私）

之后如需添加 Tavily，发送 "重新设置" 即可。
```

---

### 第四步：确认搜索引擎组合

**系统**：
```
📊 配置摘要

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 已启用以下搜索引擎：

中文搜索：
  • kimi_search（原生）
  • 搜狗（网页搜索）
  • 搜狗微信（公众号文章）
  • 头条搜索（今日头条）

英文搜索：
  • Tavily（AI 深度搜索）✨
  • DuckDuckGo（隐私保护）
  • Startpage（国际综合）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提示：
  • 发送 /验证 "消息内容" 开始事实核查
  • 发送 "重新设置" 可修改配置

是否保存以上配置？
回复 "保存" 或 "重新配置"：
```

**用户回复 "保存"**：
```
✅ 配置已保存！

Rumour Buster 已就绪！
现在可以发送 /验证 "消息内容" 开始验证消息真假了。

例如试试：/验证 "柠檬水可以抗癌"
```

---

## 配置存储

对话完成后，生成配置文件 `~/.rumour-buster-config`：

```json
{
  "setup_completed": true,
  "setup_time": "2026-04-03T06:47:00Z",
  "version": "0.3.0",
  "search_engines": {
    "chinese": {
      "kimi_search": {"available": true},
      "multi_search_engine": {
        "available": true,
        "engines": ["sogou", "sogou_wechat", "toutiao"]
      }
    },
    "english": {
      "tavily": {
        "available": true,
        "api_key": "tvly-xxxxx",
        "free_quota": 1000
      },
      "multi_search_engine": {
        "available": true,
        "engines": ["duckduckgo", "startpage"]
      }
    }
  }
}
```

---

## 重新设置流程

用户发送 "重新设置" 或 "setup"：

```
🔧 Rumour Buster 重新设置

当前配置：
  • Tavily：已启用（API: tvly-xxxxx）
  • 中文引擎：kimi + 搜狗 + 搜狗微信 + 头条
  • 英文引擎：Tavily + DuckDuckGo + Startpage

可执行操作：
  1. 修改 Tavily API Key
  2. 添加/移除搜索引擎
  3. 重置为默认配置
  4. 查看当前配置
  5. 退出

请回复数字 1-5：
```

---

## 错误处理

### API Key 验证失败
```
❌ Tavily API Key 验证失败

可能原因：
  • Key 已过期
  • 免费额度已用完（1000次/月）
  • 网络连接问题

是否重新输入？回复 "是" 或 "跳过"：
```

### 依赖未安装
```
⚠️ multi-search-engine 未安装

Rumour Buster 需要这个依赖才能工作。

请执行：clawhub install api-multi-search-engine

安装完成后发送 "继续"：
```

---

## 交互示例

### 完整设置示例

**用户**：安装 rumour-buster

**系统**：
```
🔧 Rumour Buster 初始化设置

你好！我是 Rumour Buster...
[欢迎语]

✅ multi-search-engine 已安装

📚 关于 Tavily...
是否启用 Tavily 搜索？
回复 "是" 或 "否"：
```

**用户**：是

**系统**：
```
太好了！请按以下步骤申请...
[申请步骤]

申请完成后，请直接粘贴你的 API Key：
```

**用户**：tvly-dev-3QAy8g-xxxxxx

**系统**：
```
✅ API Key 格式正确！
✅ Tavily 连接成功！

📊 配置摘要...
是否保存以上配置？
回复 "保存" 或 "重新配置"：
```

**用户**：保存

**系统**：
```
✅ 配置已保存！Rumour Buster 已就绪！
```

---

## 主技能集成

主技能启动时检查配置：

```python
def check_setup():
    config_file = "~/.rumour-buster-config"
    
    if not os.path.exists(config_file):
        print("首次使用，请先完成设置...")
        # 调用 setup 子技能对话流程
        run_setup_dialog()
        return False
    
    return load_config(config_file)
```

---

*对话式 Setup - 让配置更简单*

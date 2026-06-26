---
name: rumor-buster-setup
description: Rumor Buster 初始化设置子技能。检测所有可用搜索工具，配置 Tavily API，生成配置文件。支持中英文自动检测。检测范围包括：kimi_search, web_search, web_fetch, multi-search-engine 等。
version: 0.4.0
---

# Rumor Buster Setup - 对话式初始化设置

## 🌐 多语言支持

Setup 子技能支持**自动语言检测**，根据用户输入语言自动切换中英文交互。

### 语言检测

```python
def detect_language(text):
    """检测用户输入语言"""
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    if total_chars > 0 and chinese_chars / total_chars > 0.3:
        return "zh"
    return "en"

# 会话级语言状态
setup_session_lang = "zh"  # 默认中文，根据用户输入自动切换
```

### 文本资源

```python
TEXTS = {
    "zh": {
        "title": "🔧 Rumor Buster 设置",
        "first_time": "🆕 首次配置 Rumor Buster",
        "detected_config": "📁 检测到现有配置文件",
        "detecting_engines": "正在检测已安装的搜索引擎...",
        "native_search": "原生搜索技能",
        "multi_search_engine": "聚合搜索引擎",
        "kimi_available": "✅ kimi_search 已安装",
        "kimi_unavailable": "❌ kimi_search 未安装",
        "web_search_available": "✅ web_search (Brave) 已安装",
        "web_search_unavailable": "❌ web_search 未安装",
        "web_fetch_available": "✅ web_fetch 已安装",
        "web_fetch_unavailable": "❌ web_fetch 未安装",
        "multi_available": "✅ multi-search-engine 已安装",
        "multi_unavailable": "❌ multi-search-engine 未安装",
        "tavily_configured": "✅ Tavily API Key 已配置",
        "tavily_skipped": "⏭️  Tavily 未配置（可选）",
        "detection_complete": "📊 检测完成！",
        "available": "可用",
        "not_installed": "未安装",
        "configured": "已配置",
        "quota_remaining": "次/月剩余",
        "invalid": "无效",
        "optional_not_configured": "未配置（可选）",
        "available_engines": "可用搜索引擎：",
        "configure_tavily": "是否配置 Tavily 以获得更好的英文搜索体验？",
        "skip_tavily": "⏭️  跳过 Tavily 配置",
        "save_success": "✅ 配置已保存！",
        "ready_to_use": "现在可以开始验证消息了！",
        "choose_action": "请选择操作：",
        "option_modify": "1. 修改部分配置",
        "option_reset": "2. 重新配置（删除现有配置）",
        "option_view": "3. 查看当前配置",
        "option_exit": "4. 退出",
        "enter_api_key": "请粘贴 Tavily API Key（格式：tvly-xxxxxx）：",
        "api_key_valid": "✅ API Key 格式正确",
        "api_key_success": "✅ Tavily 连接测试成功！",
        "confirm_reset": "⚠️  确定要重新配置吗？",
        "config_deleted": "🗑️  删除现有配置...",
        "start_fresh": "🆕 开始全新配置...",
    },
    "en": {
        "title": "🔧 Rumor Buster Setup",
        "first_time": "🆕 First-time Setup",
        "detected_config": "📁 Existing config detected",
        "detecting_engines": "Detecting installed search engines...",
        "native_search": "Native Search Tools",
        "multi_search_engine": "Multi-Search Engine",
        "kimi_available": "✅ kimi_search installed",
        "kimi_unavailable": "❌ kimi_search not installed",
        "web_search_available": "✅ web_search (Brave) installed",
        "web_search_unavailable": "❌ web_search not installed",
        "web_fetch_available": "✅ web_fetch installed",
        "web_fetch_unavailable": "❌ web_fetch not installed",
        "multi_available": "✅ multi-search-engine installed",
        "multi_unavailable": "❌ multi-search-engine not installed",
        "tavily_configured": "✅ Tavily API Key configured",
        "tavily_skipped": "⏭️  Tavily not configured (optional)",
        "detection_complete": "📊 Detection complete!",
        "available": "available",
        "not_installed": "not installed",
        "configured": "configured",
        "quota_remaining": "queries remaining",
        "invalid": "invalid",
        "optional_not_configured": "not configured (optional)",
        "available_engines": "Available engines:",
        "configure_tavily": "Configure Tavily for better English search?",
        "skip_tavily": "⏭️  Skipping Tavily config",
        "save_success": "✅ Configuration saved!",
        "ready_to_use": "Ready to verify messages!",
        "choose_action": "Choose action:",
        "option_modify": "1. Modify configuration",
        "option_reset": "2. Reset (delete existing config)",
        "option_view": "3. View current config",
        "option_exit": "4. Exit",
        "enter_api_key": "Paste Tavily API Key (format: tvly-xxxxxx):",
        "api_key_valid": "✅ API Key format valid",
        "api_key_success": "✅ Tavily connection successful!",
        "confirm_reset": "⚠️  Confirm reset?",
        "config_deleted": "🗑️  Deleting existing config...",
        "start_fresh": "🆕 Starting fresh setup...",
    }
}

def get_text(key):
    """获取当前语言的文本"""
    return TEXTS[setup_session_lang].get(key, key)
```

---

## 触发方式

### 自动触发
- 首次运行主技能时（无配置文件）

### 手动触发
- `setup` / `设置`
- `重新设置` / `reset`
- `/rumor-buster setup`

---

## 检测流程

### 第一步：检查现有配置（带语言检测）

```python
CONFIG_FILE = "~/.rumor-buster-config"

def check_existing_config(user_input):
    # 检测用户输入语言
    detected_lang = detect_language(user_input)
    if detected_lang:
        setup_session_lang = detected_lang
    
    if os.path.exists(CONFIG_FILE):
        current_config = load_config(CONFIG_FILE)
        print(get_text("detected_config"))
        
        # 根据语言输出选项
        print(get_text("choose_action"))
        if setup_session_lang == "zh":
            print("  1. 修改部分配置")
            print("  2. 重新配置（删除现有配置）")
            print("  3. 查看当前配置")
            print("  4. 退出")
        else:
            print("  1. Modify configuration")
            print("  2. Reset (delete existing)")
            print("  3. View current config")
            print("  4. Exit")
    else:
        print(get_text("first_time"))
        run_full_setup()
```

### 第二步：实际检测搜索引擎（扩大检测范围）

**检测所有可用的搜索工具**：

```python
def detect_all_search_engines():
    """
    检测所有可用的搜索工具
    包括：原生搜索技能、multi-search-engine、web_search、web_fetch 等
    """
    engines = {
        "native": {},
        "multi_search_engine": {"available": False, "engines": []},
        "tavily": {"available": False, "configured": False}
    }
    
    print(get_text("detecting_engines"))
    
    # ========== 1. 检测原生搜索技能 ==========
    print(f"\n{get_text('native_search')}:")
    
    # 检测 kimi_search
    try:
        result = kimi_search("test", limit=1)
        engines["native"]["kimi_search"] = {"available": True, "type": "native"}
        print(f"  {get_text('kimi_available')}")
    except:
        engines["native"]["kimi_search"] = {"available": False}
        print(f"  {get_text('kimi_unavailable')}")
    
    # 检测 web_search (Brave Search)
    try:
        result = web_search("test", count=1)
        engines["native"]["web_search"] = {"available": True, "type": "native", "provider": "brave"}
        print(f"  {get_text('web_search_available')}")
    except:
        engines["native"]["web_search"] = {"available": False}
        print(f"  {get_text('web_search_unavailable')}")
    
    # 检测 web_fetch
    try:
        engines["native"]["web_fetch"] = {"available": True, "type": "utility"}
        print(f"  {get_text('web_fetch_available')}")
    except:
        engines["native"]["web_fetch"] = {"available": False}
        print(f"  {get_text('web_fetch_unavailable')}")
    
    # 检测其他可能的搜索技能
    other_searches = ["bing_search", "google_search", "duckduckgo_search"]
    for search in other_searches:
        try:
            module = globals().get(search)
            if module:
                engines["native"][search] = {"available": True, "type": "native"}
                print(f"  ✅ {search}")
        except:
            engines["native"][search] = {"available": False}
    
    # ========== 2. 检测 multi-search-engine ==========
    print(f"\n{get_text('multi_search_engine')}:")
    
    if check_multi_search_engine_installed():
        engines["multi_search_engine"]["available"] = True
        cn_engines, en_engines = test_multi_search_engines()
        engines["multi_search_engine"]["chinese"] = cn_engines
        engines["multi_search_engine"]["english"] = en_engines
        all_engines = cn_engines + en_engines
        print(f"  ✅ {get_text('multi_available')} ({get_text('available')}: {', '.join(all_engines)})")
    else:
        print(f"  {get_text('multi_unavailable')}")
    
    # ========== 3. 检测 Tavily ==========
    print(f"\nTavily:")
    
    tavily_key = os.getenv("TAVILY_API_KEY", "")
    if tavily_key and tavily_key.startswith("tvly-"):
        try:
            test_result = tavily_search("test", api_key=tavily_key, max_results=1)
            engines["tavily"] = {
                "available": True, 
                "configured": True,
                "api_key": tavily_key[:10] + "...",
                "quota": get_tavily_quota(tavily_key)
            }
            print(f"  ✅ Tavily {get_text('configured')}")
        except:
            engines["tavily"] = {"available": False, "error": "connection_failed"}
            print(f"  ⚠️  Tavily API Key {get_text('invalid')}")
    else:
        engines["tavily"] = {"available": False, "configured": False}
        print(f"  ⏭️  Tavily {get_text('optional_not_configured')}")
    
    return engines


def check_multi_search_engine_installed():
    """检查 multi-search-engine 技能是否安装"""
    try:
        skill_path = os.path.expanduser("~/.openclaw/workspace/skills/api-multi-search-engine")
        return os.path.exists(skill_path)
    except:
        return False


def test_multi_search_engines():
    """测试 multi-search-engine 中具体哪些引擎可用"""
    cn_engines = []
    en_engines = []
    
    chinese_engines = ["sogou", "sogou_wechat", "toutiao", "baidu", "bing_cn"]
    english_engines = ["duckduckgo", "startpage", "google", "bing_int", "brave"]
    
    for engine in chinese_engines:
        try:
            if test_engine_available(engine):
                cn_engines.append(engine)
        except:
            pass
    
    for engine in english_engines:
        try:
            if test_engine_available(engine):
                en_engines.append(engine)
        except:
            pass
    
    return cn_engines, en_engines


def test_engine_available(engine_name):
    """测试特定搜索引擎是否可用"""
    try:
        engine_urls = {
            "sogou": "https://sogou.com",
            "sogou_wechat": "https://wx.sogou.com",
            "toutiao": "https://so.toutiao.com",
            "duckduckgo": "https://duckduckgo.com",
            "startpage": "https://startpage.com",
        }
        if engine_name in engine_urls:
            result = web_fetch(url=engine_urls[engine_name], maxChars=100)
            return result is not None
        return False
    except:
        return False
```

### 第三步：配置流程

#### 场景A：全新配置

```
🆕 Rumor Buster 首次配置

1. 检测原生搜索技能...
   ❌ kimi_search 未安装
   ✅ web_search (Brave) 已安装
   ✅ web_fetch 已安装

2. 检测聚合搜索引擎...
   ✅ multi-search-engine 已安装
      - 可用：搜狗, 搜狗微信, 头条, DuckDuckGo, Startpage

3. 检测 Tavily...
   ⏭️  Tavily 未配置（可选）

4. 配置 Tavily（可选）...
   是否启用 Tavily？(yes/no): 

5. 生成配置文件
   ✅ 配置完成！
```

#### 场景B：修改现有配置

```
📁 当前配置：

原生搜索技能：
  ❌ kimi_search（未安装）
  ✅ web_search (Brave)
  ✅ web_fetch

聚合搜索引擎：
  ✅ sogou ✓
  ✅ sogou_wechat ✓
  ✅ 头条 ✓
  ✅ DuckDuckGo ✓
  ✅ Startpage ✓

Tavily：
  ⏭️  未配置（可选）

请选择要修改的项目：
  1. 添加/修改 Tavily API Key
  2. 测试搜索引擎可用性
  3. 返回主菜单
```

#### 场景C：重新配置

```
⚠️  确定要重新配置吗？
这将删除现有配置并重新检测所有搜索引擎。

当前配置将被删除：~/.rumor-buster-config

确认？(yes/no): yes

🗑️  删除现有配置...
🆕 开始全新配置...
[进入检测流程]
```

---

## 配置文件格式（更新版）

```json
{
  "setup_completed": true,
  "setup_time": "2026-04-03T08:30:00Z",
  "version": "0.4.0",
  "search_engines": {
    "native": {
      "kimi_search": {
        "available": false,
        "type": "native"
      },
      "web_search": {
        "available": true,
        "type": "native",
        "provider": "brave"
      },
      "web_fetch": {
        "available": true,
        "type": "utility"
      }
    },
    "multi_search_engine": {
      "available": true,
      "chinese": ["sogou", "sogou_wechat", "toutiao"],
      "english": ["duckduckgo", "startpage"]
    },
    "tavily": {
      "available": true,
      "configured": true,
      "api_key": "tvly-xxxxx...",
      "quota": 1000
    }
  },
  "detection_log": {
    "last_detection": "2026-04-03T08:30:00Z",
    "detected_engines": ["web_search", "web_fetch", "sogou", "duckduckgo"]
  }
}
```

---

## 交互示例

### 中文示例

#### 示例1：中文首次配置

**用户**：`/验证 "测试消息"`

**系统**：
```
⚠️ 首次使用 Rumor Buster，需要初始化配置。

🔧 Rumor Buster 设置

正在检测已安装的搜索引擎...

原生搜索技能：
  ❌ kimi_search 未安装
  ✅ web_search (Brave) 已安装
  ✅ web_fetch 已安装

聚合搜索引擎：
  ✅ multi-search-engine 已安装（可用：搜狗, 头条, DuckDuckGo）

Tavily：
  ⏭️  Tavily 未配置（可选）

是否配置 Tavily 以获得更好的英文搜索体验？(yes/no): 
```

**用户**：`no`

**系统**：
```
⏭️  跳过 Tavily 配置

✅ 配置已保存！
可用搜索引擎：
  原生：web_search (Brave), web_fetch
  聚合：搜狗, 头条, DuckDuckGo

现在可以开始验证消息了！
```

### 英文示例

#### Example 1: English First-time Setup

**User**: `/verify "test message"`

**System**:
```
⚠️ First time using Rumor Buster. Initial setup required.

🔧 Rumor Buster Setup

Detecting installed search engines...

Native Search Tools:
  ❌ kimi_search not installed
  ✅ web_search (Brave) installed
  ✅ web_fetch installed

Multi-Search Engine:
  ✅ multi-search-engine installed (available: sogou, startpage, duckduckgo)

Tavily:
  ⏭️  Tavily not configured (optional)

Configure Tavily for better English search? (yes/no):
```

---

## 检测范围说明

### 原生搜索技能（Native）
| 工具 | 类型 | 说明 |
|:---|:---|:---|
| kimi_search | native | Kimi AI 搜索 |
| web_search | native | Brave Search API |
| web_fetch | utility | 网页内容提取 |

### 聚合搜索引擎（Multi-Search）
| 引擎 | 语言 | 说明 |
|:---|:---|:---|
| sogou | 中文 | 搜狗搜索 |
| sogou_wechat | 中文 | 搜狗微信搜索 |
| toutiao | 中文 | 头条搜索 |
| duckduckgo | 英文 | 隐私搜索引擎 |
| startpage | 英文 | Google 代理搜索 |
| google | 英文 | Google 搜索 |
| bing | 双语 | 必应搜索 |

### 增强搜索（Enhanced）
| 工具 | 类型 | 说明 |
|:---|:---|:---|
| Tavily | API | AI 搜索增强 |

---

*Rumor Buster Setup - 智能检测，灵活配置 / Smart detection, flexible configuration*

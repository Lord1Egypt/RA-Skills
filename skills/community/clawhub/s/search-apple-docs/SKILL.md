---
name: 苹果开发者文档搜索服务
description: 通过模型上下文协议（MCP）访问苹果官方开发者文档、框架、API及WWDC视频，支持AI驱动的自然语言查询，提供Swift/Objective-C代码示例和技术指南。
version: 1.0.0
---

# 苹果开发者文档搜索服务

通过模型上下文协议（MCP）访问苹果官方开发者文档、框架、API及WWDC视频，支持AI驱动的自然语言查询，提供Swift/Objective-C代码示例和技术指南。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Search Apple Developer Documentation for APIs, frameworks, guides, and samples. Best for finding specific APIs, classes, or methods. For browsing sample code projects, use get_sample_code. For WWDC videos, use the dedicated WWDC tools (list_wwdc_videos, search_wwdc_content). | `scripts.tools.search_apple_docs` |
| Get detailed content from a specific Apple Developer Documentation page. Use this after search_apple_docs to get full documentation. Supports enhanced analysis options for comprehensive API understanding. Best for: reading API details, understanding usage, checking availability. | `scripts.tools.get_apple_doc_content` |
| Browse all Apple technologies and frameworks by category. Essential for discovering available frameworks and understanding Apple's technology ecosystem. Use this when: exploring what's available, finding framework identifiers for search_framework_symbols, checking beta status. | `scripts.tools.list_technologies` |
| Browse and search symbols within a specific Apple framework. Perfect for exploring framework APIs, finding all views/controllers/delegates in a framework, or discovering available types. Use after list_technologies to get framework identifiers. | `scripts.tools.search_framework_symbols` |
| Analyze API relationships and discover related functionality. Shows inheritance, protocol conformances, and Apple's recommended alternatives. Essential for understanding how APIs work together. Use when: learning API hierarchy, finding protocol requirements, discovering related functionality. | `scripts.tools.get_related_apis` |
| Deep dive into all types and APIs referenced in a documentation page. Resolves all mentioned types, methods, and properties to understand dependencies. Use when: analyzing complex APIs, understanding type requirements, exploring API ecosystems. | `scripts.tools.resolve_references_batch` |
| Check API availability across Apple platforms and OS versions. Shows minimum deployment targets, deprecations, and platform-specific features. Critical for cross-platform development. Use when: planning app requirements, checking API availability, finding platform alternatives. | `scripts.tools.get_platform_compatibility` |
| Discover alternative and related APIs. Finds APIs with similar functionality, modern replacements for deprecated APIs, and platform-specific alternatives. Perfect when looking for better ways to implement functionality. | `scripts.tools.find_similar_apis` |
| Track latest Apple platform updates, new APIs, and changes. Shows WWDC announcements, framework updates, and release notes. Essential for staying current with Apple development. For detailed WWDC videos, use WWDC-specific tools. | `scripts.tools.get_documentation_updates` |
| Access comprehensive guides and tutorials for Apple technologies. Includes getting started guides, architectural overviews, best practices, and implementation patterns. Perfect for learning new frameworks or understanding Apple's recommended approaches. | `scripts.tools.get_technology_overviews` |
| Browse complete sample projects from Apple. Full working examples demonstrating best practices and implementation patterns. Different from search_apple_docs which returns code snippets. Use for learning by example. | `scripts.tools.get_sample_code` |
| Browse WWDC session videos with full offline access to transcripts and code. Shows all available sessions with filtering options. Use this to discover WWDC content, find sessions by topic, or identify videos with code examples. | `scripts.tools.list_wwdc_videos` |
| Full-text search across all WWDC video transcripts and code examples. Find specific discussions, API mentions, or implementation examples. More powerful than list_wwdc_videos for finding specific content. | `scripts.tools.search_wwdc_content` |
| Access complete WWDC session content including full transcript, code examples, and resources. Use after finding videos with list_wwdc_videos or search_wwdc_content. Provides offline access to entire session content. | `scripts.tools.get_wwdc_video` |
| Browse all code examples from WWDC sessions. Perfect for finding implementation patterns, seeing new API usage, or learning by example. Each result includes the code and its session context. | `scripts.tools.get_wwdc_code_examples` |
| List all WWDC topic categories with their IDs. Essential first step before using list_wwdc_videos with topic filtering. Returns topic IDs like "swiftui-ui-frameworks" that can be used in other tools. | `scripts.tools.browse_wwdc_topics` |
| Discover WWDC sessions related to a specific video. Finds prerequisite sessions, follow-up content, and thematically similar talks. Essential for creating learning paths. | `scripts.tools.find_related_wwdc_videos` |
| List all available WWDC years with video counts and statistics. Shows which years have content available and how many videos each year contains. | `scripts.tools.list_wwdc_years` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.search_apple_docs
工具描述：Search Apple Developer Documentation for APIs, frameworks, guides, and samples. Best for finding specific APIs, classes, or methods. For browsing sample code projects, use get_sample_code. For WWDC videos, use the dedicated WWDC tools (list_wwdc_videos, search_wwdc_content).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search query for Apple Developer Documentation. Tips: Use specific API names (e.g., "UIViewController"), framework names (e.g., "SwiftUI"), or technical terms. Avoid generic terms like "how to" or "tutorial". Examples: "NSPredicate", "SwiftUI List", "Core Data migration", "URLSession authentication".|
|type|string|false| |Type of content to filter. Use "all" for comprehensive results, "documentation" for API references/guides, "sample" for code snippets. Note: "sample" returns individual code examples, not full projects. For complete sample projects, use get_sample_code instead. Default: "all".|

---

## scripts.tools.get_apple_doc_content
工具描述：Get detailed content from a specific Apple Developer Documentation page. Use this after search_apple_docs to get full documentation. Supports enhanced analysis options for comprehensive API understanding. Best for: reading API details, understanding usage, checking availability.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|url|string|true| |Full URL of the Apple Developer Documentation page. Must start with https://developer.apple.com/documentation/. Example: "https://developer.apple.com/documentation/uikit/uiviewcontroller"|
|includeRelatedApis|boolean|false| |Include inheritance hierarchy and protocol conformances. Useful for understanding API relationships. Default: false|
|includeReferences|boolean|false| |Resolve and include all referenced types and APIs. Helps understand dependencies. Default: false|
|includeSimilarApis|boolean|false| |Discover APIs with similar functionality. Great for finding alternatives. Default: false|
|includePlatformAnalysis|boolean|false| |Analyze platform availability and version requirements. Essential for cross-platform development. Default: false|

---

## scripts.tools.list_technologies
工具描述：Browse all Apple technologies and frameworks by category. Essential for discovering available frameworks and understanding Apple's technology ecosystem. Use this when: exploring what's available, finding framework identifiers for search_framework_symbols, checking beta status.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|false| |Filter by category (case-sensitive). Popular: "App frameworks" (SwiftUI, UIKit), "Graphics and games" (Metal, SpriteKit), "App services" (CloudKit, StoreKit), "Media" (AVFoundation), "System" (Foundation). Leave empty to see all categories.|
|language|string|false| |Filter by language support. "swift" for Swift-compatible frameworks, "occ" for Objective-C. Leave empty for all.|
|includeBeta|boolean|false| |Include beta/preview technologies. Set to false to see only stable frameworks. Default: true|
|limit|number|false| |Max results per category. Useful for quick overviews. Default: 200|

---

## scripts.tools.search_framework_symbols
工具描述：Browse and search symbols within a specific Apple framework. Perfect for exploring framework APIs, finding all views/controllers/delegates in a framework, or discovering available types. Use after list_technologies to get framework identifiers.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|framework|string|true| |Framework identifier in lowercase. Common: "uikit", "swiftui", "foundation", "combine", "coredata". Get exact names from list_technologies. Example: "swiftui" for SwiftUI framework.|
|symbolType|string|false| |Filter by symbol type. Use "class" for UIViewController subclasses, "protocol" for delegates, "struct" for value types. Default: "all" shows everything.|
|namePattern|string|false| |Filter by name pattern. Use "*View" for all views, "UI*" for UI-prefixed symbols, "*Delegate" for delegates. Case-sensitive. Leave empty for all symbols.|
|language|string|false| |Language preference. Some APIs differ between Swift and Objective-C. Default: "swift"|
|limit|number|false| |Results limit (default: 50, max: 200). Includes nested symbols.|

---

## scripts.tools.get_related_apis
工具描述：Analyze API relationships and discover related functionality. Shows inheritance, protocol conformances, and Apple's recommended alternatives. Essential for understanding how APIs work together. Use when: learning API hierarchy, finding protocol requirements, discovering related functionality.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|apiUrl|string|true| |Apple documentation URL to analyze. Example: "https://developer.apple.com/documentation/uikit/uiview"|
|includeInherited|boolean|false| |Show inherited methods/properties from superclasses. Helps understand full API surface. Default: true|
|includeConformance|boolean|false| |Show protocol conformances and requirements. Essential for protocol-oriented programming. Default: true|
|includeSeeAlso|boolean|false| |Show Apple's recommended related APIs. Great for finding better alternatives or complementary APIs. Default: true|

---

## scripts.tools.resolve_references_batch
工具描述：Deep dive into all types and APIs referenced in a documentation page. Resolves all mentioned types, methods, and properties to understand dependencies. Use when: analyzing complex APIs, understanding type requirements, exploring API ecosystems.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|sourceUrl|string|true| |Documentation URL to analyze for references. Example: "https://developer.apple.com/documentation/swiftui/view"|
|maxReferences|number|false| |Limit resolved references (default: 20, max: 50). Higher values = more comprehensive but slower.|
|filterByType|string|false| |Filter by reference type. Use "protocol" for protocol requirements, "class" for class hierarchies. Default: "all"|

---

## scripts.tools.get_platform_compatibility
工具描述：Check API availability across Apple platforms and OS versions. Shows minimum deployment targets, deprecations, and platform-specific features. Critical for cross-platform development. Use when: planning app requirements, checking API availability, finding platform alternatives.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|apiUrl|string|true| |API URL to check compatibility. Example: "https://developer.apple.com/documentation/swiftui/list"|
|compareMode|string|false| |Check single API or entire framework. "framework" shows all APIs in the framework. Default: "single"|
|includeRelated|boolean|false| |Also check related APIs' compatibility. Useful for finding platform-specific alternatives. Default: false|

---

## scripts.tools.find_similar_apis
工具描述：Discover alternative and related APIs. Finds APIs with similar functionality, modern replacements for deprecated APIs, and platform-specific alternatives. Perfect when looking for better ways to implement functionality.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|apiUrl|string|true| |Starting API URL. Example: "https://developer.apple.com/documentation/uikit/uialertview" (finds modern alternatives)|
|searchDepth|string|false| |How thoroughly to search. "shallow" = direct recommendations only, "medium" = topic siblings, "deep" = full relationship analysis. Default: "medium"|
|filterByCategory|string|false| |Focus on specific functionality like "Animation", "Navigation", "Data". Case-sensitive partial match.|
|includeAlternatives|boolean|false| |Include functionally similar APIs that might be better choices. Default: true|

---

## scripts.tools.get_documentation_updates
工具描述：Track latest Apple platform updates, new APIs, and changes. Shows WWDC announcements, framework updates, and release notes. Essential for staying current with Apple development. For detailed WWDC videos, use WWDC-specific tools.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|false| |Update type filter. "wwdc" = conference highlights, "technology" = API updates, "release-notes" = version changes. Default: "all"|
|technology|string|false| |Filter by framework (case-sensitive). Examples: "SwiftUI", "UIKit", "ARKit". Get names from list_technologies.|
|year|string|false| |WWDC year filter ("2025", "2024", etc.). Only for wwdc category.|
|searchQuery|string|false| |Search keywords. Examples: "async", "performance", "widgets". Case-insensitive.|
|includeBeta|boolean|false| |Include beta/preview features. Default: true|
|limit|number|false| |Max results (default: 50). Sorted by relevance and date.|

---

## scripts.tools.get_technology_overviews
工具描述：Access comprehensive guides and tutorials for Apple technologies. Includes getting started guides, architectural overviews, best practices, and implementation patterns. Perfect for learning new frameworks or understanding Apple's recommended approaches.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|false| |Topic category. Popular: "app-design-and-ui", "games", "ai-machine-learning", "augmented-reality", "privacy-and-security". Leave empty to browse all.|
|platform|string|false| |Target platform. "all" for cross-platform content. Default: "all"|
|searchQuery|string|false| |Search terms. Try: "getting started", "best practices", "architecture", "performance".|
|includeSubcategories|boolean|false| |Include nested topics for comprehensive results. Set false for overview only. Default: true|
|limit|number|false| |Max results (default: 50). Includes subcategories when enabled.|

---

## scripts.tools.get_sample_code
工具描述：Browse complete sample projects from Apple. Full working examples demonstrating best practices and implementation patterns. Different from search_apple_docs which returns code snippets. Use for learning by example.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|framework|string|false| |Framework filter (case-insensitive). Examples: "SwiftUI", "ARKit", "CoreML". Note: Some samples are under generic categories - use searchQuery for better results.|
|beta|string|false| |Beta samples: "include" = all, "exclude" = stable only, "only" = beta only. Default: "include"|
|searchQuery|string|false| |Search keywords. Most effective approach. Examples: "animation", "camera", "machine learning", "widgets".|
|limit|number|false| |Max results (default: 50).|

---

## scripts.tools.list_wwdc_videos
工具描述：Browse WWDC session videos with full offline access to transcripts and code. Shows all available sessions with filtering options. Use this to discover WWDC content, find sessions by topic, or identify videos with code examples.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|year|string|false| |WWDC year ("2025", "2024", etc.) or "all". Available: 2020-2025. Example: "2025" for latest.|
|topic|string|false| |Topic ID for exact filtering or keyword for title search. Available topic IDs: "accessibility-inclusion", "app-services", "app-store-distribution-marketing", "audio-video", "business-education", "design", "developer-tools", "essentials", "graphics-games", "health-fitness", "machine-learning-ai", "maps-location", "photos-camera", "privacy-security", "safari-web", "spatial-computing", "swift", "swiftui-ui-frameworks", "system-services". Use exact ID for topic filtering, or any keyword to search in video titles.|
|hasCode|boolean|false| |Filter by code availability. true = sessions with code, false = without code. Leave empty for all.|
|limit|number|false| |Max videos to show (default: 50). Videos include title, duration, and content indicators.|

---

## scripts.tools.search_wwdc_content
工具描述：Full-text search across all WWDC video transcripts and code examples. Find specific discussions, API mentions, or implementation examples. More powerful than list_wwdc_videos for finding specific content.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search terms. Examples: "async await", "@Observable", "Vision Pro", "performance optimization".|
|searchIn|string|false| |Search scope. "transcript" = spoken content, "code" = code examples only, "both" = everything. Default: "both"|
|year|string|false| |Limit to specific year ("2025", "2024", etc.). Leave empty for all years.|
|language|string|false| |Code language filter ("swift", "objc", "javascript"). Only for code search.|
|limit|number|false| |Max results (default: 20). Results include context snippets.|

---

## scripts.tools.get_wwdc_video
工具描述：Access complete WWDC session content including full transcript, code examples, and resources. Use after finding videos with list_wwdc_videos or search_wwdc_content. Provides offline access to entire session content.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|year|string|true| |WWDC year. Example: "2025"|
|videoId|string|true| |Session ID. Example: "10101" for keynote, "238" for session 238.|
|includeTranscript|boolean|false| |Include full session transcript with timestamps. Default: true|
|includeCode|boolean|false| |Include all code examples from the session. Default: true|

---

## scripts.tools.get_wwdc_code_examples
工具描述：Browse all code examples from WWDC sessions. Perfect for finding implementation patterns, seeing new API usage, or learning by example. Each result includes the code and its session context.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|framework|string|false| |Framework to find examples for. Examples: "SwiftUI", "SwiftData", "RealityKit".|
|topic|string|false| |Topic ID or concept keyword. Can use exact topic IDs ("swiftui-ui-frameworks", "machine-learning-ai", etc.) for precise filtering, or general keywords like "animation", "performance", "concurrency" for broader search.|
|year|string|false| |WWDC year filter ("2025", "2024", etc.).|
|language|string|false| |Programming language: "swift", "objc", "javascript", "metal".|
|limit|number|false| |Max examples (default: 30). Each includes code and source video info.|

---

## scripts.tools.browse_wwdc_topics
工具描述：List all WWDC topic categories with their IDs. Essential first step before using list_wwdc_videos with topic filtering. Returns topic IDs like "swiftui-ui-frameworks" that can be used in other tools.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|topicId|string|false| |Topic ID to explore. Available IDs: "accessibility-inclusion", "app-services", "app-store-distribution-marketing", "audio-video", "business-education", "design", "developer-tools", "essentials", "graphics-games", "health-fitness", "machine-learning-ai", "maps-location", "photos-camera", "privacy-security", "safari-web", "spatial-computing", "swift", "swiftui-ui-frameworks", "system-services". Leave empty to see all topics with video counts.|
|includeVideos|boolean|false| |List videos in the topic. Set false for topic structure only. Default: true|
|year|string|false| |Filter topic videos by year. Only when browsing specific topic.|
|limit|number|false| |Max videos per topic (default: 20).|

---

## scripts.tools.find_related_wwdc_videos
工具描述：Discover WWDC sessions related to a specific video. Finds prerequisite sessions, follow-up content, and thematically similar talks. Essential for creating learning paths.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|videoId|string|true| |Source video ID. Example: "10101" for keynote.|
|year|string|true| |Source video year. Example: "2025"|
|includeExplicitRelated|boolean|false| |Include Apple's recommended related videos. Usually prerequisites or follow-ups. Default: true|
|includeTopicRelated|boolean|false| |Include videos from same topic categories. Good for comprehensive learning. Default: true|
|includeYearRelated|boolean|false| |Include other videos from same WWDC. Default: false|
|limit|number|false| |Max related videos (default: 15).|

---

## scripts.tools.list_wwdc_years
工具描述：List all available WWDC years with video counts and statistics. Shows which years have content available and how many videos each year contains.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据
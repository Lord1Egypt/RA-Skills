# 增量更新（阶段 4 详细）

> 适用于：知识库已有该主题旧版本导览，需要增量更新。

## 1. 读取旧版本

```bash
# 导出旧版本笔记内容
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<旧版note_id>","target_content_format":1}' | \
python3 -c "import sys,json,urllib.request; d=json.load(sys.stdin); url=d['data']['content_url']; req=urllib.request.Request(url); resp=urllib.request.urlopen(req); print(resp.read().decode('utf-8'))"
```

## 2. 提取版本信息

从标题下方的版本行提取：

```
**版本**：v1.0 | 创建于 2026-05-08 | 更新于 2026-05-08
**更新日志**：v1.0 - 初始版本
```

## 3. 对比知识库增量

获取文件夹最新文件列表，与旧版本对比：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 100}' | \
python3 -c "import sys,json; data=json.load(sys.stdin); print([f['title'] for f in data.get('data',{}).get('list',[])])"
```

## 4. 识别增量内容

| 类型 | 判断方式 | 更新方式 |
|------|---------|---------|
| 新增文章 | 旧版本"四、知识卡片"中不存在 | 补充到对应核心概念的关键要素中 |
| 删除文章 | 旧版本提及但知识库中已不存在 | 从列表中移除 |
| 概念变化 | 知识库中出现新的核心概念分类 | 新增核心概念卡片 |

## 5. 更新导览内容

更新原则：
- **保留原有结构**：不改变核心概念划分方式
- **更新关键要素**：补充/移除文章引用
- **更新实践建议**：根据新增内容调整实践建议
- **更新学习路径**：如有新的依赖关系

**链接格式要求**（必须严格遵守，引用格式：`[《标题》](URL)`）：
- 所有引用必须提供**可点击的有效链接**
- 链接来源参考**第三步生成的链接特性表**，选择正确的写法：
  - 云文档类：使用相对路径格式 `[《标题》](路径)`
  - 网页链接：使用完整 URL 格式 `[《标题》](URL)`
  - 纯本地文件：使用文件路径格式并标注来源
- 禁止使用裸链接或纯 URL 文本，必须包装为引用格式

## 6. 版本号更新

```yaml
---
version: 1.1  # patch+0.0.1 或 minor+0.1 或 major+1.0
created: 2026-05-08
updated: 2026-05-08
changelog:
  - v1.1: 增量更新，补充了X篇新文章，更新了关键要素描述
  - v1.0: 初始版本
---
```

详见 [versioning.md](versioning.md) 的版本号规则。

## 7. 写入新版本

详见 [write-and-verify.md](write-and-verify.md)

> 💡 推荐使用"创建新笔记 + 标注替代旧版"模式，保留旧笔记作为历史版本（详见 [security.md](security.md) 第 3 节）。

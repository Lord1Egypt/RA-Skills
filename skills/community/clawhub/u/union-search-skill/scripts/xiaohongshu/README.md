# 小红书搜索模块

本模块提供小红书(Xiaohongshu)搜索API的生产级实现。

## 📁 项目结构

```
xiaohongshu/
├── xiaohongshu_search.py    # 生产级搜索客户端(主要使用)
├── tikhub_xhs_search.py     # 原始TikHub示例脚本
├── XIAOHONGSHU_README.md    # TikHub官方文档说明
├── README.md                # 本文档
└── responses/               # 搜索结果输出目录
    ├── *_full.json          # 完整API响应(用于调试)
    └── *_core.json          # 提取的核心信息(用于应用)
```

## 🚀 快速开始

### 1. 环境配置

创建 `.env` 文件:
```bash
TIKHUB_TOKEN=your_token_here
TIKHUB_HOST=api.tikhub.io
```

### 2. 基础使用

```python
from xiaohongshu_search import XiaohongshuSearcher, save_results

# 初始化搜索客户端
searcher = XiaohongshuSearcher()

# 搜索
result = searcher.search("猫粮", reset_session=True)
core_info = searcher.extract_core_info(result, "猫粮")

# 保存结果(自动生成2个文件)
full_path, core_path = save_results(result, core_info)

print(f"完整响应: {full_path}")
print(f"核心信息: {core_path}")
```

### 3. 运行示例

```bash
python xiaohongshu_search.py
```

## 📊 核心功能

### 搜索功能
- ✅ 关键词搜索
- ✅ 多种排序方式(综合/时间/热度/评论/收藏)
- ✅ 内容类型筛选(图文/视频)
- ✅ 时间筛选(一天内/一周内/半年内)
- ✅ 翻页支持

### 数据提取
- 自动提取20+核心字段
- 标签自动识别
- 作者信息提取
- 互动数据统计
- 媒体信息处理

### 双文件输出
1. **完整响应** (`*_full.json`)
   - 包含原始API响应
   - 用于调试和数据分析
   - 文件较大(~200KB)

2. **核心信息** (`*_core.json`)
   - 提取的关键数据
   - 用于应用集成
   - 数据缩减76%+

## 📖 核心字段说明

### 搜索信息
- `keyword`: 搜索关键词
- `search_time`: 搜索时间
- `search_id`: 搜索ID(用于翻页)
- `session_id`: 会话ID(用于翻页)

### 笔记信息
- `note_id`: 笔记ID
- `title`: 标题
- `desc`: 描述(截取200字)
- `tags`: 标签列表(自动提取)
- `note_type`: 笔记类型(normal/video)
- `note_type_cn`: 中文类型(图文笔记/视频笔记)

### 作者信息
- `user_id`: 用户ID
- `red_id`: 红书ID
- `nickname`: 昵称
- `avatar`: 头像URL

### 互动数据
- `liked_count`: 点赞数
- `collected_count`: 收藏数
- `comments_count`: 评论数
- `shared_count`: 分享数

### 媒体信息
- **图文笔记**: 图片URL(预览+高清)、尺寸
- **视频笔记**: 视频URL、编码格式(H264/H265)、质量

## 🔧 高级用法

### 翻页搜索
```python
searcher = XiaohongshuSearcher()

# 第一页
result1 = searcher.search("猫粮", page=1, reset_session=True)

# 第二页(使用相同的search_id和session_id)
result2 = searcher.search("猫粮", page=2, reset_session=False)
```

### 自定义排序和筛选
```python
result = searcher.search(
    keyword="猫粮",
    sort_type="popularity_descending",  # 按热度排序
    filter_note_type="视频笔记",         # 只看视频
    filter_note_time="一周内",          # 一周内的笔记
    reset_session=True
)
```

## 🛠️ 技术栈

- **Python**: 3.x
- **HTTP库**: http.client (标准库)
- **环境变量**: python-dotenv
- **数据格式**: JSON

## ✅ 生产就绪

本模块已完成测试并可用于生产环境:
- ✅ API功能完整验证
- ✅ 数据提取准确
- ✅ 错误处理完善
- ✅ 类型提示完整
- ✅ 文档清晰详细

---

**状态**: ✅ 生产就绪
**最后更新**: 2026-02-19

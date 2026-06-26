---
name: bilibili-video-analyzer
description: "B站视频评论与弹幕深度分析。输入B站视频链接或BV号，自动采集评论、弹幕数据，进行情感分析、关键词提取、热度分析，生成结构化分析报告。"
description_zh: "B站视频评论弹幕数据分析与报告生成"
description_en: "Bilibili video comment and danmaku analysis"
---

# B站视频深度分析 Skill

基于 **B站公开API** 实现的视频评论与弹幕深度分析工具，**无需登录即可使用**。自动采集弹幕、评论数据，进行多维度情感分析、关键词提取、热度分析，生成专业级分析报告。

## 核心特性

- ✅ **无需登录** - 仅需设置User-Agent请求头即可调用B站公开API
- ✅ **弹幕分析** - 支持XML弹幕抓取、内容分类、时间分布分析
- ✅ **评论分析** - 高赞评论提取、情感分析
- ✅ **深度洞察** - 互动热度、内容质量、用户画像
- ✅ **专业报告** - 对标专业分析报告格式

## 前置条件

### 1. 环境要求

- Python 3.8+
- 网络可访问 B站 API

### 2. 依赖安装

脚本已内置所有依赖，无需额外安装：

```python
# 所需库（内置）
import requests      # HTTP请求
import jieba         # 中文分词
from snownlp import SnowNLP  # 情感分析
import xml.etree.ElementTree as ET  # XML解析
```

## 使用方式

### 对话中使用

```
@skill://B站视频分析 请分析这个视频：https://www.bilibili.com/video/BV1ky97B9Efn
```

### 命令行使用

```bash
python analyze_video.py "https://www.bilibili.com/video/BV1ky97B9Efn"
python analyze_video.py "BV1ky97B9Efn" -o report.md
```

## 技术实现

### 核心API接口（无需登录）

| 数据 | 接口URL | 参数 |
|------|---------|------|
| 视频信息 | `https://api.bilibili.com/x/web-interface/view?bvid={bvid}` | bvid |
| 弹幕数据 | `https://api.bilibili.com/x/v1/dm/list.so?oid={cid}` | oid(视频cid) |
| 评论数据 | `https://api.bilibili.com/x/v2/reply/main?next={page}&type=1&oid={bvid}&mode=3` | oid, page |

### 请求头设置

```python
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}
```

## 分析流程

```
输入URL/BV号
    │
    ▼
1. 提取视频BV号 (正则匹配)
    │
    ▼
2. 获取视频信息 (标题、播放量、点赞等) + 获取CID
    │
    ▼
3. 弹幕采集 → XML解析 → 提取文本/时间/类型
    │
    ▼
4. 评论采集 → JSON解析 → 提取内容/用户/点赞
    │
    ▼
5. 多维度分析
    ├── 情感分析 (SnowNLP 0-1评分)
    ├── 关键词提取 (jieba分词+停用词过滤)
    ├── 内容分类 (技术型/情感型/玩梗型/疑问型)
    ├── 时间分布 (视频分段统计)
    └── 互动热度 (点赞率/评论率/弹幕率)
    │
    ▼
6. 生成Markdown专业报告
```

## 报告内容

### 完整报告结构

```
一、视频基本信息
   ├── 播放/点赞/投币/收藏/分享/评论/弹幕数量
   └── 视频简介

二、弹幕深度分析
   ├── 2.1 弹幕概况 (总数、类型分布)
   ├── 2.2 弹幕情感分析 (正面/中性/负面占比+综合评分)
   ├── 2.3 弹幕时间分布特征 (可视化柱状图)
   ├── 2.4 弹幕内容分类 (技术型/情感型/玩梗型/疑问型)
   └── 2.5 热门弹幕内容 (按长度排序+时间戳)

三、评论深度分析
   ├── 3.1 评论概况
   ├── 3.2 评论情感分析
   └── 3.3 高赞评论TOP10

四、关键词与话题提取
   └── 高频词TOP20

五、综合洞察
   ├── 5.1 用户情感倾向
   ├── 5.2 互动热度分析
   └── 5.3 内容质量观察

六、总结评价
   ├── 核心发现
   └── 总体评价

附录
   └── 数据来源、接口、工具说明
```

## 使用案例

### 案例：反导系统视频深度分析

**用户输入**：
```
@skill://B站视频分析 请分析这个视频："https://www.bilibili.com/video/BV1ky97B9Efn"
```

**视频信息**：
- 标题：花了天价造反导系统，为什么拦导弹还是像赌博？【差评君】
- 播放量：682,204
- 弹幕数：1,426条
- 评论数：1,566

**执行流程**：

1. **提取BV号**：`BV1ky97B9Efn`

2. **获取视频信息**：
   ```python
   GET https://api.bilibili.com/x/web-interface/view?bvid=BV1ky97B9Efn
   → 返回: title, stat, duration, cid=xxx
   ```

3. **采集弹幕**（通过XML接口）：
   ```python
   GET https://api.bilibili.com/x/v1/dm/list.so?oid={cid}
   → 解析XML获取1426条弹幕
   ```

4. **采集评论**：
   ```python
   GET https://api.bilibili.com/x/v2/reply/main?next=1&type=1&oid=BV1ky97B9Efn&mode=3
   → 获取20条热评
   ```

5. **分析结果**：

   | 分析维度 | 结果 |
   |---------|------|
   | 弹幕情感 | 0.53/1.0 (中性偏正) |
   | 评论情感 | 0.78/1.0 (正向) |
   | 高频词 | 导弹(97)、拦截(92)、反导(68)、核弹(63)、苏联(53) |
   | 弹幕密集时段 | 4-7分钟 (488条) |

6. **生成报告**：导出完整Markdown分析报告

**输出成果**：《[花了天价造反导系统...]视频深度分析报告.md》

## 脚本参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `url` | B站视频链接或BV号 | `BV1ky97B9Efn` |
| `-o, --output` | 输出报告路径 | `-o report.md` |

## 注意事项

1. **无需登录**: 脚本使用B站公开API，设置User-Agent即可
2. **评论限制**: 未登录状态评论获取受限(20条)，完整评论需登录凭证
3. **频率限制**: 建议控制请求频率，避免触发风控
4. **数据完整性**: 弹幕需视频有弹幕才能采集

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| 弹幕为0 | CID获取失败或视频无弹幕 | 检查网络或视频有效性 |
| 评论为0 | 未登录限制或API变更 | 正常现象，不影响分析 |
| 412/403错误 | 风控拦截 | 添加延时或更换User-Agent |

## 文件结构

```
B站视频分析/
├── SKILL.md                 # 本说明文件
├── _skillhub_meta.json      # Skill元数据
└── scripts/
    ├── analyze_video.py      # 核心分析脚本 (独立运行)
    └── requirements.txt      # 依赖列表
```

## 扩展定制

如需调整分析维度，可修改 `analyze_video.py` 中：
- `categorize_danmakus()` - 弹幕分类逻辑
- `analyze_sentiment()` - 情感分析阈值
- `extract_keywords()` - 停用词表
- `generate_professional_report()` - 报告模板

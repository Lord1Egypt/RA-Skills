---
name: bilibili-danmaku-extractor
description: "B站视频弹幕提取工具。输入B站视频链接，自动提取该视频的所有弹幕，输出JSON和Markdown两种格式的文件。"
description_zh: "B站弹幕提取，输出JSON和Markdown格式"
description_en: "Extract Bilibili video danmaku to JSON and Markdown"
---

# B站弹幕提取 Skill

专注于**弹幕提取**的轻量工具，输入B站视频链接，自动提取所有弹幕并输出为 **JSON** 和 **Markdown** 两种格式。

## 核心功能

- ✅ **弹幕提取** - 提取视频所有弹幕（滚动、底端、顶端等全部类型）
- ✅ **JSON导出** - 包含视频信息和完整弹幕数据
- ✅ **Markdown导出** - 按时间顺序排列的易读格式
- ✅ **无需登录** - 使用B站公开API，完全免费

## 前置条件

### 1. 环境要求

- Python 3.8+
- 网络可访问 B站 API

### 2. 依赖安装

```bash
pip install requests
```

## 使用方式

### 对话中使用

```
@skill://B站弹幕提取 请提取这个视频的弹幕：https://www.bilibili.com/video/BV1xx97xx9xx
```

### 命令行使用

```bash
# 提取弹幕并输出到当前目录
python main.py "https://www.bilibili.com/video/BV1xx97xx9xx"

# 指定输出目录
python main.py "https://www.bilibili.com/video/BV1xx97xx9xx" -o /path/to/output

# 使用BV号
python main.py "BV1xx97xx9xx"
```

## 技术实现

### 核心API接口

| 数据 | 接口URL | 参数 |
|------|---------|------|
| 视频信息 | `https://api.bilibili.com/x/web-interface/view?bvid={bvid}` | bvid |
| 弹幕数据 | `https://api.bilibili.com/x/v1/dm/list.so?oid={cid}` | oid(视频cid) |

### 请求头设置

```python
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}
```

## 输出文件

### JSON格式

```json
{
  "video_info": {
    "bvid": "BV1xx97xx9xx",
    "title": "视频标题",
    "owner": "UP主名称",
    "duration": 600,
    "stat": { "view": 123456, "like": 7890, ... },
    "pubdate": 1234567890
  },
  "export_time": "2024-01-01T12:00:00",
  "total_count": 1234,
  "danmakus": [
    {
      "text": "弹幕内容",
      "time": 12.5,
      "type": "滚动",
      "type_code": 1,
      "color": "ffffff",
      "timestamp": 1234567890
    },
    ...
  ]
}
```

### Markdown格式

```markdown
# 视频标题

> **BV号**: `BV1xx97xx9xx`
> **UP主**: UP主名称
> **弹幕总数**: 1234 条
> **导出时间**: 2024-01-01 12:00:00

---

## 全部弹幕 (共 1234 条)

`[00:12]` 这是第一条弹幕
`[00:15]` 这是第二条弹幕
`[00:20]` 这是第三条弹幕
...
```

## 工作流程

```
输入B站视频链接
    │
    ▼
1. 提取BV号 (正则匹配)
    │
    ▼
2. 获取视频信息 (标题、UP主、时长、CID等)
    │
    ▼
3. 获取弹幕数据 (XML/压缩格式)
    │
    ▼
4. 解析弹幕
   ├── 提取文本、时间、类型、颜色等
   └── 处理压缩弹幕 (zlib解压)
    │
    ▼
5. 导出文件
   ├── JSON: 完整数据 + 元信息
   └── Markdown: 易读格式
```

## 脚本参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `url` | B站视频链接或BV号 | `BV1ky97B9Efn` |
| `-o, --output` | 输出目录 | `-o ./output` |

## 弹幕字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `text` | string | 弹幕文本内容 |
| `time` | float | 出现时间（秒） |
| `type` | string | 弹幕类型（滚动/底端/顶端等） |
| `type_code` | int | 弹幕类型代码 |
| `color` | string | 弹幕颜色（十六进制） |
| `timestamp` | int | 发送时间戳 |

### 弹幕类型代码

| code | 类型 |
|------|------|
| 1 | 滚动弹幕 |
| 4 | 底部弹幕 |
| 5 | 顶部弹幕 |
| 6 | 逆向弹幕 |
| 7 | 高级弹幕 |
| 8 | 代码弹幕 |

## 注意事项

1. **无需登录**: 脚本使用B站公开API，无需登录即可提取弹幕
2. **弹幕完整性**: 获取的弹幕数量取决于视频实际弹幕数量
3. **频率限制**: 建议控制请求频率，避免触发风控
4. **编码处理**: 自动处理gzip压缩的弹幕数据

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| 获取弹幕为0 | CID获取失败或视频无弹幕 | 检查网络或视频有效性 |
| 412/403错误 | 风控拦截 | 添加延时或稍后重试 |
| 视频信息获取失败 | BV号无效 | 检查链接格式是否正确 |

## 实际案例

### 案例：萌娘百科消亡视频弹幕提取

**用户输入**：
```
@skill://B站弹幕提取 请提取这个视频的弹幕：https://www.bilibili.com/video/BV1Am9gBzEUb
```

**执行过程**：

1. **提取BV号**：`BV1Am9gBzEUb`

2. **获取视频信息**：
   - 标题：曾经"二次元入坑必备"的萌娘百科，为何一步步走向消亡？
   - UP主：BB姬Studio
   - 时长：约11分钟

3. **获取弹幕**：通过CID调用弹幕接口，获取到 **1063 条**弹幕

4. **导出文件**：
   - JSON: `BV1Am9gBzEUb_弹幕_1063条.json`
   - Markdown: `BV1Am9gBzEUb_弹幕_1063条.md`

**弹幕预览**：

| 时间 | 弹幕内容 |
|------|----------|
| `[07:24]` | 绿坝：没想到吧，老娘回来了 |
| `[03:03]` | 4千万身价指的是当时这玩意软件造价4,000万元人民币... |
| `[00:14]` | 萌娘百科方便是方便，不过有的时候会夹带私货或者玩梗误导人… |
| `[10:37]` | "不是我害了你，是这乱世害了你啊" |
| `[06:46]` | 啊？还有这么巧的事？ |

**输出成果**：
- ✅ 成功提取 1063 条弹幕
- ✅ JSON文件包含完整视频信息和弹幕数据
- ✅ Markdown文件按时间顺序排列，便于阅读

---

## 文件结构

```
B站弹幕提取/
├── SKILL.md                 # 本说明文件
├── _skillhub_meta.json      # Skill元数据
├── main.py                  # 核心脚本
└── requirements.txt         # Python依赖
```
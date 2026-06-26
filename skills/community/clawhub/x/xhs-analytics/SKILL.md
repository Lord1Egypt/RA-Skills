---
name: xhs-analytics
description: |
  小红书数据分析工具。用于采集笔记数据、分析热度、追踪竞品、生成报告。
  Activate when user mentions: 小红书, xiaohongshu, 笔记分析, 博主数据, 热度追踪, 竞品分析
---

# 小红书数据分析技能

用于采集和分析小红书平台数据，支持笔记搜索、博主分析、热度追踪等功能。

## 配置 (用户需要自行填写)

在使用前，用户需要在脚本中配置自己的 API 凭证:

```bash
# 在 scripts/config.sh 中设置
export XHS_API_KEY="your-api-key"
export XHS_COOKIE="your-cookie"
```

如无 API，可以使用备用方案:
- 第三方数据服务
- 手动输入
- 模拟数据测试

## 工具

### 1. 搜索笔记

根据关键词搜索小红书笔记:

```bash
# 基础搜索
python3 scripts/search_notes.py --keyword "美妆" --limit 50

# 筛选条件
python3 scripts/search_notes.py \
  --keyword "护肤" \
  --limit 100 \
  --sort "hot" \
  --category "笔记"
```

参数:
- `--keyword`: 搜索关键词 (必填)
- `--limit`: 返回数量，默认 50
- `--sort`: 排序方式 (hot/latest/time)
- `--category`: 笔记类型

输出: JSON 格式的笔记列表

### 2. 分析博主

获取博主基本信息和数据:

```bash
python3 scripts/analyze_author.py --user_id "用户ID"
```

输出:
- 粉丝数
- 笔记数
- 获赞与收藏
- 关注数
- 近期数据趋势

### 3. 热度分析

分析单篇笔记或话题的热度:

```bash
python3 scripts/analyze_trend.py --note_id "笔记ID"
```

输出:
- 点赞数
- 收藏数
- 评论数
- 分享数
- 发布时间
- 热度趋势

### 4. 竞品对比

对比多个博主或笔记的数据:

```bash
python3 scripts/compare.py --users "用户1,用户2,用户3"
python3 scripts/compare.py --notes "笔记1,笔记2,笔记3"
```

### 5. 生成报告

综合分析生成报告:

```bash
python3 scripts/generate_report.py \
  --keyword "美妆" \
  --output report.md \
  --format "markdown"
```

## 使用示例

### 示例1: 分析"护肤"关键词下的热门笔记

```
用户: 帮我分析"护肤"关键词下的前100篇热门笔记

帕瓦:
1. 搜索笔记: python3 scripts/search_notes.py --keyword "护肤" --limit 100 --sort "hot"
2. 分析热度: python3 scripts/analyze_trend.py --note_id "每个笔记ID"
3. 生成报告: python3 scripts/generate_report.py --keyword "护肤" --output 护肤分析报告.md
```

### 示例2: 对比竞品博主

```
用户: 对比"美妆护肤"领域的前5名博主

帕瓦:
1. 搜索领域关键词获取头部博主
2. 获取每个博主的数据
3. 生成对比表格和报告
```

### 示例3: 追踪热度趋势

```
用户: 追踪某个话题最近7天的热度变化

帕瓦:
1. 获取话题相关笔记
2. 按时间聚合数据
3. 生成趋势图表(文字描述)
```

## 数据来源

1. **官方API** (需要企业资质):
   - 需要用户自行申请
   - 配置: `scripts/config.sh`

2. **第三方服务** (可选):
   - 用户可接入自己的数据源
   - 修改: `scripts/api_client.py`

3. **手动/模拟** (测试用):
   - 使用示例数据进行功能测试

## 输出格式

所有脚本支持 JSON 输出，方便后续处理:

```bash
python3 scripts/search_notes.py --keyword "美妆" --format json
```

## 注意事项

1. **遵守平台规则**: 请勿高频请求，注意请求间隔
2. **数据安全**: 采集数据仅供分析使用，勿传播
3. **API限制**: 注意第三方 API 的调用限制
4. **隐私保护**: 勿采集个人隐私信息

## 故障排除

Q: 搜索返回空
A: 检查 API 凭证是否正确，或尝试减少 limit

Q: 请求被限制
A: 增加请求间隔，或使用代理

Q: 数据不准确
A: 第三方数据可能有时效性，建议交叉验证

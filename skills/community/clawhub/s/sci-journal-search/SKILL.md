# sci-journal-search - SCI 期刊查询

查询 SCI 期刊的详细信息，包括新锐分区（中科院分区）、JCR 分区等。

## ⚠️ 重要说明

**新锐分区 = 中科院分区**

自 2026 年起，中科院期刊分区表由新锐（XinRui）团队发布。

## 功能

- ✅ 期刊搜索（支持期刊名、ISSN）
- ✅ 新锐分区（中科院分区）查询
- ✅ JCR 小类分区查询
- ✅ Top 期刊标识
- ✅ 130+ 期刊简称自动识别
- ✅ HTTP 直接请求（快速，无需浏览器）
- 🔄 LetPub 查询（可选，需要浏览器，**查询后自动关闭**）

## 使用方式

### 1. 默认查询（推荐）

**只查询新锐分区**，快速返回结果：

```bash
python3 query.py "期刊名"
```

### 2. LetPub 查询（需要浏览器）

**查询新锐分区 + LetPub 详细指标**：

```bash
python3 query.py "期刊名" --letpub
```

**输出说明**：
1. 首先输出新锐分区结果
2. 然后输出 JSON 配置，格式如下：
```json
{
  "status": "need_browser",
  "journal": "期刊名",
  "search_url": "https://www.letpub.com.cn/...",
  "action": "open_and_parse",
  "close_browser_after": true
}
```
3. **Agent 解析 JSON**，调用 browser 工具打开 URL
4. 解析页面内容，输出 LetPub 详细指标
5. **查询完成后自动关闭浏览器**

### 3. 直接使用简称

支持 130+ 常见期刊简称：TPAMI, NC, JACS, TNNLS, ANGEW 等

## 输出示例

### 新锐分区查询

```
📊 Nature Communications
ISSN: - | EISSN: 2041-1723

【新锐分区（中科院分区）】
  • Multidisciplinary Science (综合性期刊): 1 区 🏆 Top

【JCR 小类分区】
  • MULTIDISCIPLINARY SCIENCES (综合性期刊): 1 区

💡 提示：如需查询更多详细信息（影响因子、自引率、审稿周期等），
   可以使用 --letpub 参数查询 LetPub 数据（需要浏览器）
```

### LetPub 查询

```
📊 Nature Communications

【影响因子】
  • 2024-2025: 14.7
  • 实时：16.2

【自引率】3.2%
【h-index】389
【审稿周期】网友：较快，2-3 个月

✅ LetPub 查询完成，浏览器已关闭
```

## 数据源

- **新锐分区**：https://www.xr-scholar.com（中科院分区官方）
- **LetPub**：https://www.letpub.com.cn（影响因子、审稿周期等）

## 注意事项

1. 新锐分区 = 中科院分区（2026 年起由新锐团队发布）
2. 默认只查询新锐分区，快速响应
3. LetPub 查询需要浏览器，**查询完成后自动关闭**
4. 期刊简称采用精确匹配

## 更新日志

- **v1.3.0**: 交互式 LetPub 查询，查询后自动关闭浏览器
- **v1.2.0**: 130+ 期刊简称映射表
- **v1.0**: 初始版本

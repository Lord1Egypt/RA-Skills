# 闲鱼搜索技能 - 严格筛选模式

## 技能描述

在闲鱼网站搜索商品时，自动应用严格筛选条件，确保搜索结果真实有效。用户只需提供搜索关键词，技能自动处理筛选逻辑。

## 激活条件

用户提及以下关键词时激活：
- "闲鱼搜索"
- "闲鱼找"
- "闲鱼买"
- "帮我找闲鱼"
- "闲鱼价格"
- "二手搜索"

## 默认筛选条件

### ✅ 必选条件

| 条件 | 说明 | 实现方式 |
|------|------|----------|
| 个人闲置 | 排除商家/鱼小铺/超赞鱼小铺 | 点击"个人闲置"筛选按钮 |
| 单一价格 | 排除价格区间/模糊定价 | 人工筛选排除"¥XXX-¥XXX" |
| 规格匹配 | 确保容量/频率/型号匹配 | 搜索关键词精确化 |
| 台式机 | 排除笔记本/服务器 | 关键词添加"台式机" |

### ❌ 排除条件

| 排除类型 | 识别特征 | 处理方式 |
|----------|----------|----------|
| 商家商品 | 鱼小铺/超赞鱼小铺/卖家信用极好 (批量) | 跳过 |
| 价格区间 | "¥XXX-¥XXX" / "XXX-XXX 元" | 跳过 |
| 套条价 | "标价为单根价格"但显示套条 | 标注说明 |
| 容量不符 | 8G/32G/64G (非目标容量) | 跳过 |
| 代数不符 | DDR3/DDR4 (非目标 DDR5) | 跳过 |
| 频率不符 | 4800/5200/5600 (非目标 6000) | 跳过 |
| 笔记本内存 | "笔记本"/"SO-DIMM" | 跳过 |
| 包装盒 | "包装盒"/"空盒" | 跳过 |
| 回收广告 | "回收"/"高价收" | 跳过 |

## 使用格式

```
用户输入：闲鱼搜索 [产品名称] [规格参数]
技能输出：TOP10 商品列表（含价格/地区/链接）
```

### 示例

**用户输入：**
```
闲鱼搜索 金士顿 DDR5 16G 6000 台式机内存
```

**技能处理流程：**
1. 打开闲鱼网站 `https://www.goofish.com/`
2. 搜索关键词 `金士顿 DDR5 16G 6000 台式机内存`
3. 点击"个人闲置"筛选
4. 抓取搜索结果前 50 条
5. 按筛选条件过滤
6. 按价格升序排列
7. 输出 TOP10 商品列表

## 输出格式

```markdown
## 🏆 [产品名称] 个人闲置 TOP10（单一价格）

已严格筛选：**仅限个人闲置** + **单一价格**

| 排名 | 价格 | 商品名称 | 地区 | 想要人数 | 购买链接 |
|:---:|------|----------|------|----------|----------|
| 🥇 | **¥XXX** | [商品简述] | [地区] | [X 人] | [🔗 查看](链接) |
| ... | ... | ... | ... | ... | ... |

---

### ✅ 筛选标准
- 个人闲置
- 单一价格
- [规格参数]
- [容量要求]
- [其他条件]

### 📊 价格统计
- **最低价：** ¥XXX
- **最高价：** ¥XXX
- **平均价：** ¥XXX
```

## 浏览器操作步骤

### 1. 打开闲鱼网站
```
browser(action=open, url="https://www.goofish.com/")
```

### 2. 执行搜索
```
browser(action=navigate, url="https://www.goofish.com/search?q=[关键词]")
```

### 3. 获取页面快照
```
browser(action=snapshot, refs="aria")
```

### 4. 点击个人闲置筛选
```
browser(action=act, kind="click", ref="[个人闲置按钮 ref]")
```

### 5. 再次获取快照并提取数据
```
browser(action=snapshot, refs="aria")
```

## 数据提取规则

### 商品链接提取
```
link[ref=eXXX][cursor=pointer]
  - /url: https://www.goofish.com/item?id=[商品 ID]
```

### 价格提取
```
generic [ref=eXXX]:
  - generic [ref=eXXX]: ¥
  - generic [ref=eXXX]: "[价格数字]"
```

### 地区提取
```
generic " [地区]" [ref=eXXX]:
  - paragraph [ref=eXXX]: [地区]
```

### 想要人数提取
```
generic "[X 人想要]" [ref=eXXX]
```

### 商品标题提取
```
link "[商品标题]" [ref=eXXX][cursor=pointer]:
  - /url: [商品链接]
```

## 价格验证逻辑

### 单一价格验证
```javascript
function isValidPrice(priceText) {
  // 排除价格区间
  if (priceText.includes('-') || priceText.includes('~')) {
    return false;
  }
  // 排除"XXX 起"
  if (priceText.includes('起')) {
    return false;
  }
  // 排除"面议"
  if (priceText.includes('面议')) {
    return false;
  }
  // 只保留纯数字价格
  return /^\d+$/.test(priceText.replace('¥', '').trim());
}
```

### 规格验证
```javascript
function matchesSpec(title, requiredSpecs) {
  // 必须包含所有必需规格
  for (const spec of requiredSpecs) {
    if (!title.includes(spec)) {
      return false;
    }
  }
  // 排除不符规格
  const excludeSpecs = ['笔记本', '包装盒', '回收', 'DDR4', 'DDR3'];
  for (const exclude of excludeSpecs) {
    if (title.includes(exclude)) {
      return false;
    }
  }
  return true;
}
```

## 排序规则

1. **主要排序：** 价格升序（从低到高）
2. **次要排序：** 想要人数降序（热门优先）
3. ** tertiary 排序：** 发布时间（新发布优先）

## 错误处理

### 无搜索结果
```
未找到符合条件的商品。

建议：
1. 放宽筛选条件（如接受商家商品）
2. 调整搜索关键词
3. 尝试不同频率/容量规格
```

### 筛选失败
```
⚠️ 筛选条件应用失败，显示全部结果。

可能原因：
- 闲鱼页面结构变更
- 网络加载超时
- 筛选按钮不可用

已显示原始搜索结果，请人工筛选。
```

### 价格解析失败
```
⚠️ 部分商品价格解析失败，已标记为"价格待确认"。

可能原因：
- 价格格式特殊
- 动态加载价格
- 商品已下架
```

## 技能配置

### 可配置参数

```json
{
  "xianyu_search": {
    "default_filters": {
      "personal_only": true,
      "single_price_only": true,
      "exclude_merchants": true,
      "exclude_price_range": true
    },
    "result_limit": 10,
    "sort_by": "price_asc",
    "timeout_ms": 10000,
    "retry_count": 3
  }
}
```

### 用户自定义筛选

用户可以在搜索时添加额外筛选条件：

```
闲鱼搜索 金士顿 DDR5 16G 6000 --max-price 1200 --region 广东 --condition 全新
```

支持的条件：
- `--max-price XXX` - 最高价格
- `--min-price XXX` - 最低价格
- `--region XXX` - 指定地区
- `--condition XXX` - 成色（全新/几乎全新/二手）
- `--shipping` - 仅包邮
- `--verified` - 仅验货宝

## 记忆记录

搜索完成后，记录到 `memory/YYYY-MM-DD.md`：

```markdown
### 闲鱼搜索记录

**时间：** 2026-03-06 13:37
**关键词：** 金士顿 DDR5 16G 6000 台式机内存
**结果数量：** 10 条
**价格区间：** ¥999 - ¥1200
**最低价商品：** [链接](https://www.goofish.com/item?id=...)
```

## 相关技能

- `playwright-browser` - 浏览器自动化
- `finder` - 文件浏览（保存搜索结果）
- `message` - 发送搜索结果到聊天

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03-06 | 初始版本，基础筛选功能 |

---

_此技能文件于 2026-03-06 创建。自动严格筛选，买二手不踩坑。_

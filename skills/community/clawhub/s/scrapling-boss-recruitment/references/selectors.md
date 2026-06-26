# Boss直聘 CSS选择器参考

> ⚠️ 注意：Boss直聘页面结构可能更新，请定期验证选择器有效性

## 候选人列表页 (搜索结果)

| 元素 | CSS选择器 | 说明 |
|------|-----------|------|
| 候选人卡片 | `.job-card-box` | 单个候选人卡片容器 |
| 候选人ID | `@data-lid` 或 `@data-jobid` | 候选人唯一标识 |
| 姓名 | `.name::text` | 候选人姓名 |
| 职位 | `.job-title::text` | 应聘职位 |
| 公司名 | `.company-name::text` | 当前/曾任职公司 |
| 城市 | `.city::text` | 所在城市 |
| 经验 | `.experience::text` | 工作年限 |
| 学历 | `.degree::text` | 最高学历 |
| 薪资 | `.salary::text` | 薪资范围 |
| 技能标签 | `.skill-tag::text` | 技能关键词列表 |
| 更新时间 | `.update-time::text` | 简历更新时间 |
| 头像 | `img.avatar@src` | 头像URL |
| 立即沟通 | `.btn-start-chat` | 打招呼按钮 |

## 简历详情页

| 元素 | CSS选择器 | 说明 |
|------|-----------|------|
| 姓名 | `.name::text` | 候选人姓名 |
| 性别 | `.gender::text` | 性别 |
| 年龄 | `.age::text` | 年龄 |
| 期望职位 | `.job-title::text` | 期望职位 |
| 期望城市 | `.city::text` | 期望城市 |
| 工作经验 | `.experience::text` | 工作年限 |
| 学历 | `.degree::text` | 最高学历 |
| 期望薪资 | `.salary-expectation::text` | 期望薪资 |
| 当前公司 | `.current-company::text` | 当前公司 |
| 当前职位 | `.current-position::text` | 当前职位 |
| 技能标签 | `.skill-tag::text` | 技能列表 |
| 自我介绍 | `.self-description::text` | 自我介绍 |

## 工作经历

| 元素 | CSS选择器 | 说明 |
|------|-----------|------|
| 容器 | `.work-history-item` | 单个工作经历 |
| 公司名 | `.company::text` | 公司名称 |
| 职位 | `.position::text` | 职位名称 |
| 时间 | `.duration::text` | 在职时间 |
| 描述 | `.description::text` | 工作描述 |

## 教育经历

| 元素 | CSS选择器 | 说明 |
|------|-----------|------|
| 容器 | `.education-item` | 单个教育经历 |
| 学校 | `.school::text` | 学校名称 |
| 专业 | `.major::text` | 所学专业 |
| 学历 | `.degree::text` | 学历 |
| 时间 | `.duration::text` | 就读时间 |

## 搜索参数

### URL参数说明

```
https://www.zhipin.com/web/candidate/search?
    query={关键词}           # 搜索关键词
    &city={城市代码}          # 城市，如101010100(北京)
    &experience={经验代码}    # 经验要求，如102（3-5年）
    &degree={学历代码}        # 学历要求，如205（本科）
    &salary={薪资代码}        # 薪资范围，如3（15K-25K）
    &page={页码}             # 页码
    &pageSize={每页数量}     # 每页数量，默认30
```

### 常用参数值

| 参数 | 值 | 说明 |
|------|-----|------|
| 经验 | 101 | 1年以下 |
| 经验 | 102 | 1-3年 |
| 经验 | 103 | 3-5年 |
| 经验 | 104 | 5-10年 |
| 经验 | 105 | 10年以上 |
| 学历 | 204 | 大专 |
| 学历 | 205 | 本科 |
| 学历 | 206 | 硕士 |
| 学历 | 207 | 博士 |

## 动态加载内容

Boss直聘使用Ajax动态加载内容，需要：

1. 使用 `DynamicFetcher` 或 `StealthyFetcher`
2. 设置 `network_idle=True` 等待请求完成
3. 或使用 `wait_for_selector` 等待特定元素出现

```python
from scrapling.fetchers import DynamicSession

with DynamicSession(headless=True, network_idle=True) as session:
    page = session.fetch(url)
    # 等待动态内容加载
    page.wait_for_selector('.job-card-box', timeout=10000)
```

## XPath备选方案

如CSS选择器失效，可使用XPath：

```python
# XPath示例
items = page.xpath('//div[@class="job-card-box"]')
name = page.xpath('//span[@class="name"]/text()').get()
```

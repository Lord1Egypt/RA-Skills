# 本地测试指南

本文档介绍如何在本地测试 qxbent-skills。

## 前置准备

1. 安装 Node.js (推荐 v18 或更高版本)
2. 获取启信宝 API Token

## 安装步骤

### 1. 安装依赖

```bash
cd d:\qxb_project\skill-ent-v8\qxbent-skills
npm install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Token：

```env
QXBENT_API_TOKEN=your_api_token_here
```

或者直接设置环境变量（Windows）：

```bash
set QXBENT_API_TOKEN=your_api_token_here
```

或者（Linux/Mac）：

```bash
export QXBENT_API_TOKEN=your_api_token_here
```

## 测试方法

### 方法 1: 快速测试（推荐新手）

运行自动化测试，一次性测试所有接口：

```bash
npm run test
```

输出示例：
```
=== 启信宝 API 测试 ===

1. 测试查询企业工商信息...
✓ 成功
  企业名称: 上海合合信息科技发展有限公司
  统一社会信用代码: 91310000779855085M
  法定代表人: 镇立新
  注册资本: 11111.1111万人民币

2. 测试查询股东信息...
✓ 成功
  共 10 个股东

...
```

### 方法 2: 交互式测试（推荐深度测试）

运行交互式测试，可以手动输入企业名称：

```bash
npm run interactive
```

使用流程：
1. 选择要测试的功能（1-5）
2. 输入企业名称
3. 查看返回结果
4. 继续测试或退出

示例交互：
```
可用操作：
1. 查询企业工商信息
2. 查询企业股东信息
3. 查询企业主要人员
4. 查询企业变更记录
5. 退出

请选择操作 (1-5): 1

请输入企业名称: 上海合合信息科技发展有限公司

查询企业工商信息...

查询成功！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
企业名称: 上海合合信息科技发展有限公司
统一社会信用代码: 91310000779855085M
法定代表人: 镇立新
...
```

### 方法 3: 测试多候选企业场景

测试企业名称不唯一的情况：

```bash
npx ts-node src/examples/multiple_match_example.ts
```

这会演示：
- 使用简称查询（如"胜宏科技"）
- 捕获 `MultipleMatchError` 错误
- 展示候选企业列表
- 使用完整名称重新查询

### 方法 4: 运行完整示例

查看详细的 API 使用示例：

```bash
npx ts-node qxbent/scripts/enterprise_info_example.ts
```

## 测试用例

### 推荐测试的企业名称

1. **完整名称测试**：
   - `上海合合信息科技发展有限公司`
   - `恒大地产集团有限公司`
   - `胜宏科技（惠州）股份有限公司`

2. **简称测试（会返回多个候选）**：
   - `胜宏科技`
   - `华为`
   - `腾讯`

3. **不存在的企业**：
   - `这是一个不存在的企业名称123456`

## 测试各个功能

### 1. 测试企业工商信息查询

```typescript
const client = createClient()
const info = await client.getEnterpriseInformation('上海合合信息科技发展有限公司')
console.log(info)
```

预期返回：企业名称、统一社会信用代码、法定代表人等 18 个字段

### 2. 测试股东信息查询

```typescript
const shareholders = await client.getPartnerList('上海合合信息科技发展有限公司')
console.log(shareholders)
```

预期返回：股东列表（最多 10 个），包含股东名称、持股比例等

### 3. 测试主要人员查询

```typescript
const personnel = await client.getEmployeesList('上海合合信息科技发展有限公司')
console.log(personnel)
```

预期返回：主要人员列表（最多 10 个），包含姓名、职务、持股比例等

### 4. 测试变更记录查询

```typescript
const changes = await client.getChangeRecords('上海合合信息科技发展有限公司')
console.log(changes)
```

预期返回：变更记录列表（最多 10 条），包含变更日期、变更事项等

## 错误处理测试

### 测试多个候选企业

```typescript
try {
  const info = await client.getEnterpriseInformation('胜宏科技')
} catch (error) {
  if (error instanceof MultipleMatchError) {
    console.log('找到多个候选企业：')
    error.candidates.forEach((c, i) => {
      console.log(`${i + 1}. ${c.ename}`)
    })
  }
}
```

### 测试企业未找到

```typescript
try {
  const info = await client.getEnterpriseInformation('不存在的企业')
} catch (error) {
  if (error instanceof EnterpriseNotFoundError) {
    console.log('企业未找到')
  }
}
```

## 常见问题

### Q: 提示 "请提供 API Token"

A: 确保已设置环境变量 `QXBENT_API_TOKEN`，或在 `.env` 文件中配置。

### Q: 报错 "Request failed with status code 401"

A: API Token 无效或已过期，请检查 Token 是否正确。

### Q: 报错 "Request failed with status code 429"

A: 超过 API 调用频次限制，请稍后再试。

### Q: TypeScript 编译错误

A: 确保已安装依赖：`npm install`

## 性能测试

如果需要测试性能，可以运行批量查询：

```bash
# 创建性能测试脚本
# 批量查询多个企业，统计耗时
```

## 下一步

测试通过后，你可以：
1. 将 skills 发布到 ClawHub
2. 在 AI 智能体中加载使用
3. 向他人分享

## 反馈

如果发现问题，请提交 Issue 或 Pull Request。

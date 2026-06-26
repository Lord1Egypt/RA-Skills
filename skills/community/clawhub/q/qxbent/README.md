# 启信宝企业信息查询 Skill

启信宝（QiXinBao）企业信息查询 AI Skill，提供企业工商信息、股东信息、主要人员、变更记录等查询功能。

> 📖 **首次使用？** 请先阅读 [用户指南](USER_GUIDE.md) 了解如何配置 API Token

## 特性

- 💬 **自然语言交互** - 直接用中文描述需求即可获取数据
- 🏢 **丰富的企业数据** - 工商信息、股东、人员、变更记录等
- 🚀 **开箱即用** - AI Skill 即插即用
- 📚 **完整的接口文档** - 包含 4 个核心企业查询接口
- ✨ **符合官方标准** - 遵循 AI Skills 最佳实践

## 安装

### 1. 安装依赖

```bash
cd qxbent-skills
npm install
```

### 2. 配置 API Token

**⚠️ 安全提示**：Token 是敏感凭证，必须使用环境变量配置，不要在对话中提供。

**环境变量配置：**

Windows 永久配置：
```bash
# 在系统环境变量中添加
变量名：QXBENT_API_TOKEN
变量值：your_token_here
```

Linux/Mac 永久配置：
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export QXBENT_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

配置成功后，AI 会自动从环境变量读取 token。

详细配置方法请查看 [用户指南](USER_GUIDE.md)。

### 3. 安装 Skill

将 `qxbent` 目录复制到本地的 skills 目录，或通过 skills 管理工具安装。

## 使用方法

安装后在本地智能体中加载该技能，之后可以用自然语言直接交流。

支持 Claude Code, OpenClaw, Trae 等所有的通用智能体。

### 交互示例

**查询企业工商信息**：
```
查询上海合合信息科技发展有限公司的工商信息
```

**查询股东信息**：
```
帮我查一下恒大地产集团有限公司的股东情况
```

**查询主要人员**：
```
查询上海合合信息科技发展有限公司的主要人员和高管
```

**查询变更记录**：
```
查看上海合合信息科技发展有限公司最近的变更记录
```

### 代码示例

```typescript
import { createClient } from './src/client'

const client = createClient()

// 查询企业工商信息
const info = await client.getEnterpriseInformation('上海合合信息科技发展有限公司')
console.log('企业名称:', info.企业名称)
console.log('法定代表人:', info.法定代表人)

// 查询股东信息
const shareholders = await client.getPartnerList('上海合合信息科技发展有限公司')
console.log('股东列表:', shareholders)

// 查询主要人员
const personnel = await client.getEmployeesList('上海合合信息科技发展有限公司')
console.log('主要人员:', personnel)

// 查询变更记录
const changes = await client.getChangeRecords('上海合合信息科技发展有限公司')
console.log('变更记录:', changes)
```

### 错误处理

当企业名称不唯一时，会抛出 `MultipleMatchError`，包含候选企业列表：

```typescript
import { createClient, MultipleMatchError } from './src/client'

const client = createClient()

try {
  // 使用简称查询
  const info = await client.getEnterpriseInformation('胜宏科技')
  console.log(info)
} catch (error) {
  if (error instanceof MultipleMatchError) {
    console.log('找到多个匹配的企业：')
    error.candidates.forEach((candidate, index) => {
      console.log(`${index + 1}. ${candidate.ename}`)
    })
    // AI 可以引导用户选择，然后使用完整名称重新查询
  }
}
```

## API 接口

| 接口名 | 描述 | 文档 |
|--------|------|------|
| getEnterpriseInformation | 查询企业工商信息 | [查看文档](qxbent/references/getEnterpriseInformation.md) |
| getPartnerListV3 | 查询企业股东信息 | [查看文档](qxbent/references/getPartnerListV3.md) |
| getEmployeesListV4 | 查询企业主要人员 | [查看文档](qxbent/references/getEmployeesListV4.md) |
| getPagingEntBasicInfo | 查询企业变更记录 | [查看文档](qxbent/references/getPagingEntBasicInfo.md) |

## 开发

### 构建项目

```bash
npm run build
```

### 运行示例

```bash
npm run test
```

或直接运行示例脚本：

```bash
npx ts-node qxbent/scripts/enterprise_info_example.ts
```

## 项目结构

```
qxbent-skills/
├── src/                    # 源代码
│   ├── types.ts           # 类型定义
│   ├── client.ts          # API 客户端
│   ├── utils.ts           # 工具函数
│   └── index.ts           # 入口文件
├── qxbent/                # Skill 定义
│   ├── SKILL.md          # Skill 描述文件
│   ├── scripts/          # 示例脚本
│   └── references/       # API 文档
├── package.json
├── tsconfig.json
└── README.md
```

## 工具权限

- `Bash(node:*)`: 允许执行 Node.js/TypeScript 代码
- `Read`: 允许读取接口文档

## 注意事项

本项目仅供学习和研究使用，请勿用于商业用途。使用时请遵守启信宝 API 的使用条款。

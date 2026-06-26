---
name: searchOnlineAssets
version: 1.0.9
description: '在线素材搜索工具：调用公共素材库（Pixabay）检索高质量图片、插画、矢量图与视频，返回素材元数据与 URL 供当前工作流使用。'
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.0.9',
        'installAlternative': 'npx @dlazy/cli@1.0.9',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': '当调用此技能时，请使用 searchOnlineAssets 工具检索公共素材库（Pixabay）。' },
  }
---

# searchOnlineAssets

[English](./SKILL.md) · [中文](./SKILL-cn.md)

在线素材搜索工具：调用公共素材库（Pixabay）检索高质量图片、插画、矢量图与视频，返回素材元数据与 URL 供当前工作流使用。

## 触发关键词

- searchOnlineAssets
- pixabay
- 在线素材搜索

## 身份验证 (Authentication)

所有请求都需要 dLazy API key，通过 CLI 配置：

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把 key 保存在你的用户配置目录（macOS/Linux 上为 `~/.dlazy/config.json`，Windows 上为 `%USERPROFILE%\.dlazy\config.json`），文件权限仅限当前操作系统用户访问。你也可以用 `DLAZY_API_KEY` 环境变量按次传入。

### 获取你的 API Key

1. 登录或在 [dlazy.com](https://dlazy.com) 创建账号
2. 访问 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

每个 key 都属于你自己的 dLazy 组织，可在同一控制面板**随时轮换或吊销**。

## 关于与来源 (Provenance)

- **CLI 源代码**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.8` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.0.9 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.0.9`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理

本技能是 Pixabay 公共搜索 API 的轻量封装，运行在 dLazy 的工具运行时之内。调用时：

- 你提供的关键词与筛选参数会被转发到 Pixabay API。
- Pixabay 返回 hits 列表，工具会将每条结果映射为稳定结构（id、tags、preview/webformat/large URL、宽高）。
- 技能本身不会越权访问网络或文件系统，仅在 dLazy 工具运行时内发起一次到 Pixabay 的 HTTP 请求。

这是标准的 SaaS 调用模式；返回的素材 URL 由 Pixabay（`pixabay.com`）托管，不经过 dLazy。完整服务条款请参见 [dlazy.com](https://dlazy.com)。

## 使用方法

**CRITICAL INSTRUCTION FOR AGENT**:
通过结构化输入对象调用 `searchOnlineAssets` 工具。它是一个内部 AI 工具，不是 CLI 命令——通过模型的 tool-call 通道执行。

输入参数：

```ts
{
  query: string;                                            // 必填，搜索关键词；建议优先使用英文以提高召回率
  imageType?: "all" | "photo" | "illustration" | "vector";  // 默认 "all"
  orientation?: "all" | "horizontal" | "vertical";          // 默认 "all"
  page?: number;                                            // 默认 1
  perPage?: number;                                         // 默认 10（Pixabay 上限 200）
  lang?: string;                                            // 默认 "zh"，需要英文标签时传 "en"
}
```

行为说明：

- `safesearch` 在服务端被强制为 `true`，自动过滤敏感内容。
- Pixabay 对英文关键词召回更好。中文关键词（如"咖啡"）建议先翻译为英文（"coffee"）再检索。
- 拿到结果后，挑选最匹配的 `largeImageURL`（或视频预览 URL）+ `tags` 提供给用户，**不要**整段返回原始 `hits`。
- 若 `total === 0`，告知用户未找到匹配素材，并建议放宽关键词。

## 输出格式

```json
{
  "total": 1234,
  "hits": [
    {
      "id": 5179107,
      "tags": "coffee, cup, latte art",
      "previewURL": "https://cdn.pixabay.com/.../preview.jpg",
      "webformatURL": "https://pixabay.com/.../webformat.jpg",
      "largeImageURL": "https://pixabay.com/.../large.jpg",
      "imageWidth": 6000,
      "imageHeight": 4000
    }
  ]
}
```

## 命令示例

```ts
// 搜索横版城市风景照片
searchOnlineAssets({
  query: 'cityscape skyline',
  imageType: 'photo',
  orientation: 'horizontal',
  perPage: 6,
})
```

```ts
// 搜索自然主题的矢量图标
searchOnlineAssets({
  query: 'leaf nature icon',
  imageType: 'vector',
  perPage: 12,
})
```

## 错误处理

| Code | 错误类型               | 示例信息                               |
| ---- | ---------------------- | -------------------------------------- |
| 401  | 未授权（缺少 API Key） | `Pixabay API key is not configured`    |
| 502  | 上游 API 调用失败      | `Pixabay API error: <statusText>`      |
| 503  | 网络 / fetch 失败      | `Failed to search images from Pixabay` |

> **智能体关键指令**:
>
> 1. 如果工具抛出 `Pixabay API key is not configured`，说明工作区未配置 Pixabay 凭证——请直接告知用户并停止重试。
> 2. 如果返回 `Pixabay API error`，请用更简短的关键词重试一次，仍失败再告知用户未找到素材。

## Tips

Visit https://dlazy.com for more information.

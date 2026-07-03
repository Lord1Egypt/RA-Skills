---
slug: skillhub-upload-guide
displayName: SkillHub.cn 技能上传操作指南
version: 1.0.0
summary: 在 skillhub.cn/dashboard 上传新技能的完整操作指南，含发布包/运行包分离原则与 API Key 安全规范
license: MIT
---

# SkillHub.cn 技能上传操作指南

> 适用场景：在 skillhub.cn/dashboard 上传自制新技能的完整操作流程
>
> 支持方式：Web 界面上传 + CLI 上传（clawhub / skillhub 均支持）
>
> 核心原则：**发布包与运行包必须分离**

---

## ⚠️ 核心原则：发布包与运行包必须分离

这是最容易踩的坑，**必须严格遵守**，否则会造成 API Key 泄露。

### 两类文件对比

| 类型 | 存放位置 | 内容 | 上传 skillhub.cn |
|:---|:---|:---|:---|
| **发布包** | `D:\openclaw-data\workspace\skills\<slug>\` | API Key 清空、路径用占位符 | ✅ 必须上传 |
| **运行包** | 真实运行路径（如 `D:\ollama-intel\`、`D:\openclaw-data\scripts\`） | 真实 API Key、真实路径 | ❌ 禁止上传 |

### 为什么必须分离？

1. **skillhub.cn 是公开/团队内部分发平台**，API Key 一旦上传无法删除
2. 发布包只是模板，使用者安装后自行配置
3. 真实路径（如 `D:\ollama-intel\`）对他人无意义，不能写进发布包

### 发布包三条铁律

1. **API Key**：一律清空默认值，用 `os.environ.get("KEY") or ""`
2. **真实路径**：全部替换为占位符 `<真实运行路径>`
3. **SKILL.md**：环境变量表格写"必填"，不写真实默认值

---

## 第一阶段：准备发布包

### 1.1 创建发布包目录

```
D:\openclaw-data\workspace\skills\<你的技能slug>\
├── SKILL.md          # 必须：技能元数据
├── <技能名>.cjs      # 必须：核心代码（清空版）
├── <技能名>.py       # 可选：Python 版本
└── README.md         # 可选：使用说明
```

### 1.2 编写 SKILL.md

```yaml
---
slug: my-brand-new-skill           # 唯一标识，不能以 "clawhub-" 开头
displayName: 我的全新技能           # 显示名称
version: 1.0.0                     # 语义化版本
summary: 一句话描述技能功能          # 摘要
license: MIT                       # 推荐 MIT
---
```

正文必须包含：
- 技能用途
- 核心函数签名和示例
- 配置要求（**写清楚"安装后需自行配置 API Key"**）
- 路由触发词

### 1.3 编写核心代码（发布包版本）

**JavaScript 版本：**

```javascript
// my-skill.cjs（发布包，API Key 清空）
/**
 * 我的全新技能 v1.0.0
 * 2026-06-27
 *
 * 注意：这是发布包，真实 API Key 在运行包中配置。
 */

const API_KEY = proces…_KEY || "";  // ← 清空，无默认值
const REAL_PATH = "<真实运行路径>";  // ← 占位符

async function myFunction(params) {
  return result;
}

module.exports = { myFunction };
```

**Python 版本：**

```python
# my_bridge.py（发布包）
"""
我的桥接技能 v1.0.0
2026-06-27
注意：这是发布包，真实 API Key 在运行包中配置。
"""
import os

API_KEY = ***"MY_API_KEY") or ""  # ← 清空默认值
REAL_PATH = "<真实运行路径>"                   # ← 占位符

# ...
```

---

## 第二阶段：Web 界面上传（skillhub.cn/dashboard）

### 2.1 登录 skillhub.cn

1. 访问 [https://skillhub.cn/dashboard](https://skillhub.cn/dashboard)
2. 注册/登录账号
3. 进入 **个人设置 → API Tokens**，创建新 Token（用于 CLI 认证）

### 2.2 创建团队空间（如需）

1. 点击 **团队空间** → **创建团队**
2. 设置团队名称和可见性
3. 团队成员可在该命名空间下发布技能

### 2.3 上传技能包

1. 进入 **开发者中心** 或 **发布技能** 页面
2. 填写技能信息：

| 字段 | 说明 | 示例 |
|:---|:---|:---|
| 技能名称 | 显示名称 | DeepSeek Bridge |
| Slug | 唯一标识 | deepseek-bridge |
| 版本号 | 语义化版本 | 1.0.0 |
| 简介 | 一句话描述 | DeepSeek API 本地桥接服务 |
| 分类 | 技能分类 | 工具类 / AI 类 / 开发类 |
| 可见性 | public / namespace-only / private | public |
| 技能包 | 打包好的 zip 文件 | deepseek-bridge.zip |

3. 上传 `SKILL.md` + 核心代码文件（zip 打包）
4. 点击 **发布**

### 2.4 通过 CLI 上传（可选）

**方式一：使用 skillhub CLI**

```bash
# 安装
npm install -g @astron-team/skillhub

# 登录（使用 API Token）
skillhub login --token sk_your_token_here

# 发布（到 global 空间）
skillhub publish ./my-skill --namespace global

# 发布（到团队空间）
skillhub publish ./my-skill --namespace my-team
```

**方式二：使用 clawhub CLI（兼容 SkillHub）**

```bash
# 设置 registry 为 skillhub.cn
$env:CLAWHUB_REGISTRY = "https://skill.xfyun.cn"

# 或 export CLAWHUB_REGISTRY=https://skill.xfyun.cn  (Linux/macOS)

# 登录
clawhub login --token sk_your_token_here

# 发布（slug 格式：namespace--slug）
clawhub publish ./my-skill \
  --slug my-team--my-skill \
  --name "My Skill" \
  --version 1.0.0 \
  --changelog "初始版本"
```

**slug 映射规则（ClawHub 兼容格式）：**

| 目标 | Canonical Slug 格式 |
|:---|:---|
| global 空间 | `my-skill` |
| my-team 空间 | `my-team--my-skill` |

---

## 第三阶段：发布后验证

### Web 验证

1. 进入技能详情页，确认版本号和描述正确
2. 检查 API Key 字段是否为空（没有泄露）
3. 检查路径是否为占位符（没有写真实路径）

### CLI 验证

```bash
# 搜索技能
clawhub search my-skill

# 查看技能详情
clawhub inspect my-skill

# 安装测试（另开目录）
clawhub install my-skill
```

---

## 第四阶段：存档到 IMA

### 凭证

- ClientID：`66f4b780fc9d552fb2d6bb1a785fda3f`
- API Key：`+3mGg42wQRJga5eDYvGzMSBF6xn9k4q6HGFAjcM1864WOX8np0UYvBBHiWtspRPkAJA3dh04Bg==`
- 模块路径：`D:\openclaw-data\workspace\skills\skills\ima-skills\ima_api.cjs`

### 新建笔记

```javascript
const { imaApi } = require('D:\\openclaw-data\\workspace\\skills\\skills\\ima-skills\\ima_api.cjs');
const fs = require('fs');
const content = fs.readFileSync('D:\\openclaw-data\\workspace\\skills\\skillhub-upload-guide\\SKILL.md', 'utf8');
const body = content.replace(/^---\n[\s\S]*?---\n/, '');

imaApi('openapi/note/v1/import_doc', {
  content_format: 1,
  title: 'SkillHub.cn 技能上传操作指南',
  content: body
}, {
  clientId: '66f4b780fc9d552fb2d6bb1a785fda3f',
  apiKey: '+3mGg42wQRJga5eDYvGzMSBF6xn9k4q6HGFAjcM1864WOX8np0UYvBBHiWtspRPkAJA3dh04Bg=='
}).then(r => { console.log(r); });
```

### 追加内容到已有笔记

```javascript
await imaApi('openapi/note/v1/append_doc', {
  note_id: '<笔记ID>',
  content: '## 新增章节\n\n内容...'
}, {
  clientId: '66f4b780fc9d552fb2d6bb1a785fda3f',
  apiKey: '+3mGg42wQRJga5eDYvGzMSBF6xn9k4q6HGFAjcM1864WOX8np0UYvBBHiWtspRPkAJA3dh04Bg=='
});
```

**注意：** append_doc 只接受纯 Markdown，内容不要以 `\n\n` 开头。

---

## 第五阶段：通知 main

```javascript
sessions_send({
  sessionKey: "agent:main:main",
  message: "[技能发布完成]\n- 技能名称：<name>\n- 版本：x.x.x\n- skillhub.cn：<URL>\n- IMA 笔记 ID：<note_id>"
});
```

---

## 发布包检查清单（publish 前必查）

逐项确认，**全部通过才能上传**：

- [ ] 代码中无硬编码 API Key（用 `os.environ.get("KEY") or ""`）
- [ ] SKILL.md 环境变量表格无默认值（或写"必填"）
- [ ] 真实路径全部替换为占位符（如 `<真实路径>`）
- [ ] SKILL.md 中没有真实 API Key 片段
- [ ] README.md 无真实凭证
- [ ] 压缩包中不包含运行包（如 `D:\ollama-intel\` 下的真实文件）

---

## 真实案例：deepseek-bridge 教训

首次发布 deepseek-bridge 时，将真实 API Key 写进了 skill 文件上传，造成泄露。处理方式：

1. **立即修复**：重新发布 v1.0.1，API Key 改为空值
2. **本地同步**：skill 文件和运行包同步修正
3. **创建勘误**：在 IMA 创建勘误笔记说明情况
4. **更新指南**：将此次教训写入发布指南，作为真实案例

---

## 完整流程示例（以 my-skill 为例）

```bash
# 1. 创建发布包（API Key 清空版）
mkdir D:\openclaw-data\workspace\skills\my-skill
# 写入 SKILL.md + my-skill.cjs + README.md

# 2. 创建真实运行包（不放进 skills 目录）
mkdir D:\openclaw-data\scripts\my-skill
# 写入含真实 API Key 的 my-skill.py

# 3. Web 上传：访问 skillhub.cn/dashboard → 开发者中心 → 发布技能
#    或 CLI 上传：
skillhub login --token sk_xxx
skillhub publish ./my-skill --namespace my-team

# 4. 验证上传结果（Web 检查 / CLI inspect）

# 5. 存档到 IMA
node -e "const {imaApi}=require('./ima_api.cjs'); ..."

# 6. 通知 main
sessions_send({ sessionKey: "agent:main:main", message: "..." })
```

---

## 常见问题

| 问题 | 解决方法 |
|:---|:---|
| API Key 泄露到 skillhub.cn | 立即重新发布清空版本 v1.x.y，创建 IMA 勘误笔记 |
| slug 被占用 | 换一个（如加 v2 后缀） |
| slug 以 "clawhub-" 开头 | 换一个，受保护命名空间 |
| 上传后技能不可见 | 检查可见性设置，确认是 public 或有权限的 namespace |
| CLI 登录失败 | 确认 Token 有效，在 skillhub.cn 个人设置中重新生成 |
| IMA 写入失败（code: 210001） | append_doc 只接受纯 Markdown，内容不以 `\n\n` 开头 |

---

*Created by Worker-A · 2026-06-27 · SkillHub.cn 技能上传完整指南*
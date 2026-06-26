---
name: ui-prototype-generator
description: 从参考图片或描述生成交互式原型。默认输出 HTML 格式，仅在用户明确要求时使用 Figma。支持 (1) 用于网页预览和测试的 HTML 原型，(2) 通过 API 生成 Figma 设计文件用于设计交接和协作，(3) 基于组件架构的可复用 UI 元素，(4) 响应式布局和交互状态，(5) 基于反馈的快速迭代。
---

# UI 原型生成器

将参考图片或描述转化为交互式原型。**默认：HTML 格式**。仅在用户明确要求时使用 Figma。

## 输出格式选择

### 默认：HTML 格式
**使用场景**：用户未指定格式或泛称"原型"时
- 基于浏览器的网页预览
- 交互元素（悬停、点击、表单验证）
- 可通过文件或 URL 轻松分享
- 快速迭代和修改
- 无需外部工具

### 可选：Figma 格式
**使用场景**：用户明确提到 "Figma"、"设计文件" 或 "给设计师"
- 与 UI/UX 团队的设计交接
- 在 Figma 生态系统中协作
- 设计系统文档
- 需要 Figma API 访问令牌

## 快速开始

### HTML 原型（默认）

1. **分析参考** → 2. **生成 HTML** → 3. **交付文件**

```
用户："从这个截图创建原型"
→ 生成 HTML 文件（默认）
```

### Figma 原型（按需）

1. **检查认证** → 2. **分析参考** → 3. **调用 Figma API** → 4. **返回文件 URL**

```
用户："从这个截图创建 Figma 原型"
→ 使用 Figma API（明确请求）
```

## 核心能力

### 1. 界面分析
- 解析截图提取 UI 组件
- 识别设计模式和布局
- 提取调色板和字体
- 识别间距和网格系统

### 2. HTML 原型生成（默认）
- 语义化 HTML5 结构
- 现代 CSS（Flexbox、Grid）
- 交互状态和动画
- 响应式设计
- 独立的单文件

### 3. Figma 设计生成（按需）
- 基于 API 的自动化创建
- 组件和样式生成
- 自动布局配置
- 设计系统结构

### 4. 组件库
- 表单、表格、导航
- 模态框、卡片、按钮
- 状态徽章和指示器
- 工具提示和弹出框

## 工作流程

### 工作流程 1：HTML 原型（默认）

**触发条件**：用户未指定格式提供参考

```
用户："从这个图片创建原型"
        ↓
[默认] 生成 HTML
        ↓
保存到工作区
        ↓
提供文件路径
```

**处理流程**：
1. 分析参考图片
2. 提取设计令牌（颜色、字体、间距）
3. 创建语义化 HTML 结构
4. 使用变量实现 CSS
5. 添加交互状态
6. 保存为 `.html` 文件
7. 提供使用说明

**示例**：
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>UI 原型</title>
    <style>
        :root {
            --primary: #1890ff;
            --text-dark: #333;
        }
        /* 完整的 CSS 实现 */
    </style>
</head>
<body>
    <!-- 语义化 HTML 结构 -->
</body>
</html>
```

### 工作流程 2：Figma 原型（仅明确请求）

**触发条件**：用户明确提到 "Figma"、"设计文件" 或 "给设计师"

```
用户："创建 Figma 原型" / "在 Figma 中制作"
        ↓
检查 Figma 认证 (auth-profiles.json)
        ↓
[如果认证存在] 调用 Figma API
        ↓
生成设计文件
        ↓
返回 Figma 文件 URL
```

**处理流程**：
1. **检查认证**：
   ```python
   # 从 auth-profiles.json 读取
   auth = load_auth_profile('figma')
   if not auth:
       prompt_user_for_figma_token()
   ```

2. **分析参考**（与 HTML 工作流程相同）

3. **转换为 Figma 节点**：
   ```json
   {
     "type": "FRAME",
     "name": "Header",
     "width": 1440,
     "height": 50,
     "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0.08, "b": 0.16}}]
   }
   ```

4. **调用 Figma API**：
   ```python
   headers = {"X-Figma-Token": auth['access_token']}
   response = requests.post(
       "https://api.figma.com/v1/files",
       json={"name": "Prototype", "nodes": nodes},
       headers=headers
   )
   ```

5. **返回 Figma URL**：
   ```
   https://www.figma.com/file/[FILE_ID]/Prototype
   ```

## 认证

### Figma API 访问令牌

**存储位置**：`auth-profiles.json`

**格式**：
```json
{
  "profiles": {
    "figma": {
      "provider": "figma",
      "access_token": "figd_xxxxxxxxxxxxxxxx",
      "token_type": "Bearer",
      "created_at": "2024-01-15T10:30:00Z"
    }
  }
}
```

**设置流程**：
1. 用户请求 Figma 原型
2. 检查 auth-profiles.json 中是否存在令牌
3. 如果缺失，引导用户：
   - 访问 figma.com → 设置 → 个人访问令牌
   - 生成新令牌
   - 向智能体提供令牌
4. 安全保存令牌
5. 继续 API 调用

## 脚本和工具

### HTML 生成器（默认）

**位置**：`scripts/html_generator.py`

**用法**：
```bash
python3 scripts/html_generator.py --input reference.png --output prototype.html
```

### Figma 生成器（按需）

**位置**：`scripts/figma_generator.py`

**用法**：
```bash
export FIGMA_ACCESS_TOKEN=$(cat auth-profiles.json | jq -r '.profiles.figma.access_token')
python3 scripts/figma_generator.py --input reference.png --name "My Prototype"
```

### Figma 插件（捆绑）

**位置**：`plugins/figma-plugin/`

**用途**：将生成的设计导入 Figma

**安装**：
1. 打开 Figma → 插件 → 开发 → 从清单导入插件
2. 选择 `plugins/figma-plugin/manifest.json`
3. 使用插件导入生成的 JSON

## 组件库

### HTML 组件

参见 [HTML_COMPONENTS.md](references/HTML_COMPONENTS.md)

### Figma 组件

参见 [FIGMA_COMPONENTS.md](references/FIGMA_COMPONENTS.md)

## 格式决策树

```
用户请求
    ↓
包含 "Figma" 或 "设计文件"？
    ↓ 是                           ↓ 否
使用 Figma API                   默认：HTML
    ↓                               ↓
检查认证                        生成 HTML
    ↓                               ↓
[如果认证正常]                  保存 .html 文件
调用 API                        在浏览器中打开
    ↓                               ↓
返回 Figma URL                  完成
```

## 最佳实践

### HTML 原型
- 独立的单文件
- 嵌入式 CSS 和最小化 JS
- 语义化 HTML 结构
- 移动端响应式
- 跨浏览器兼容

### Figma 原型
- 有组织的图层结构
- 命名组件和样式
- 自动布局以提高灵活性
- 设计系统令牌
- 适当的约束

## 示例

### 示例 1：HTML 原型（默认）

**输入**：管理后台截图
**输出**：`admin-dashboard.html`
**结果**：在浏览器中打开，完全可交互

### 示例 2：Figma 原型（明确请求）

**输入**："为这个表单创建 Figma 原型"
**流程**：
1. 在 auth-profiles.json 中检查 Figma 令牌
2. 生成 Figma 兼容的 JSON
3. 调用 Figma API
4. 返回：`https://figma.com/file/abc123/Form-Prototype`

## 故障排除

### HTML 问题
- **无法渲染**：检查浏览器控制台错误
- **样式损坏**：验证 CSS 是否嵌入在 `<style>` 中
- **非响应式**：添加 viewport meta 标签

### Figma 问题
- **认证失败**：检查 auth-profiles.json 中的令牌
- **API 错误**：验证令牌权限
- **导入失败**：使用捆绑的 Figma 插件

## 迁移：HTML 到 Figma

如果用户有 HTML 并想要 Figma：

1. 解析 HTML 结构
2. 提取 CSS 样式
3. 转换为 Figma 节点
4. 调用 Figma API
5. 提供 Figma URL

**脚本**：`scripts/html_to_figma.py`

## 资源

- [HTML 组件](references/HTML_COMPONENTS.md)
- [Figma 组件](references/FIGMA_COMPONENTS.md)
- [Figma API 文档](https://www.figma.com/developers/api)
- [设计令牌](references/DESIGN_TOKENS.md)

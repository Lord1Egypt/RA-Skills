# UI 原型生成器

从参考图片或描述生成交互式原型。默认生成 HTML 格式，明确指定时可通过 Figma API 生成设计稿。

## 概述

**技能名称**: `ui-prototype-generator`

**版本**: 1.0.0

**作者**: OpenClaw 社区

**许可证**: MIT

## 功能描述

UI 原型生成器是一个综合性技能，用于从参考图片或文本描述创建交互式原型。支持两种输出格式：

1. **HTML（默认）**: 包含 CSS/JS 的独立网页原型
2. **Figma（可选）**: 通过 API 生成设计文件

## 主要特性

### 核心能力

- ✅ **图像分析**: 解析截图提取 UI 组件
- ✅ **HTML 生成**: 语义化 HTML5 + 现代 CSS
- ✅ **Figma 集成**: 基于 API 的设计生成
- ✅ **组件库**: 表单、表格、弹窗、导航等
- ✅ **响应式设计**: 移动端友好的布局
- ✅ **交互状态**: 悬停、聚焦、激活状态
- ✅ **快速迭代**: 基于反馈快速修改

### 输出格式对比

| 格式 | 默认 | 适用场景 | 要求 |
|------|------|----------|------|
| HTML | ✅ 是 | 网页预览、测试、分享 | 无 |
| Figma | ❌ 否 | 设计交付、团队协作 | Figma API Token |

## 安装方法

### 通过 OpenClaw CLI 安装

```bash
openclaw skills install ui-prototype-generator
```

### 手动安装

1. 下载 `ui-prototype-generator.skill`
2. 复制到 OpenClaw 技能目录：
   ```bash
   cp ui-prototype-generator.skill ~/.openclaw/skills/
   ```
3. 重启 OpenClaw：
   ```bash
   openclaw gateway restart
   ```

## 配置说明

### Figma API 设置（可选）

如需使用 Figma 输出格式：

1. 获取 Figma 个人访问令牌：
   - 访问：https://www.figma.com/settings
   - 生成新令牌

2. 创建 auth-profiles.json：
   ```bash
   # 位置：~/.openclaw/agents/main/agent/auth-profiles.json
   {
     "profiles": {
       "figma": {
         "provider": "figma",
         "access_token": "你的令牌",
         "token_type": "Bearer"
       }
     }
   }
   ```

## 使用方式

### 基础用法（HTML - 默认）

```
用户："根据这张截图生成原型"
→ 生成 HTML 文件
```

### Figma 用法（需明确指定）

```
用户："用 Figma 生成这个原型"
→ 调用 Figma API → 返回 Figma 文件链接
```

### 示例

#### 示例 1：管理后台

**输入**: 管理面板截图

**输出**: `admin-dashboard.html`

**特性**:
- 侧边栏导航
- 带筛选的数据表格
- 响应式布局

#### 示例 2：表单弹窗

**输入**: "创建一个包含姓名、邮箱和提交按钮的弹窗表单"

**输出**: `modal-form.html`

**特性**:
- 表单验证
- 交互按钮
- 简洁样式

#### 示例 3：Figma 设计

**输入**: "为这个登录页生成 Figma 设计"

**输出**: Figma 文件链接

**特性**:
- 组件结构
- 自动布局
- 设计令牌

## 文件结构

```
ui-prototype-generator/
├── SKILL.md                          # 技能定义
├── README.md                         # 本文档
├── CHANGELOG.md                      # 版本历史
├── LICENSE                           # MIT 许可证
├── auth-profiles.template.json       # 认证模板
├── references/
│   ├── EXAMPLES.md                   # 使用示例
│   ├── HTML_COMPONENTS.md            # HTML 组件文档
│   └── FIGMA_COMPONENTS.md           # Figma 组件文档
├── scripts/
│   ├── html_generator.py             # HTML 生成
│   └── figma_generator.py            # Figma API 集成
└── plugins/
    └── figma-plugin/                 # Figma 导入插件
        ├── manifest.json
        ├── code.js
        └── ui.html
```

## API 参考

### HTML 生成器

```python
from scripts.html_generator import HTMLPrototypeGenerator

generator = HTMLPrototypeGenerator()
generator.generate_from_description(
    description="带侧边栏的管理后台",
    output_name="dashboard"
)
```

### Figma 生成器

```python
from scripts.figma_generator import FigmaPrototypeGenerator

generator = FigmaPrototypeGenerator()
generator.create_prototype(
    name="我的设计",
    nodes=[...]
)
```

## 组件清单

### HTML 组件

- **表单**: 输入框、下拉框、单选、复选、文本域
- **表格**: 可排序、可筛选、带操作
- **导航**: 头部、侧边栏、面包屑、标签页
- **反馈**: 弹窗、提示、警告、进度条
- **数据展示**: 卡片、列表、徽章、标签

### Figma 组件

- **画框**: 布局容器
- **形状**: 矩形、椭圆、线条
- **文本**: 标签、标题、段落
- **效果**: 阴影、模糊
- **自动布局**: 响应式容器

## 设计系统

### 颜色

| 令牌 | 色值 | RGB | 用途 |
|------|------|-----|------|
| 主色 | #1890ff | rgb(24,144,255) | 按钮、链接 |
| 成功 | #52c41a | rgb(82,196,26) | 成功状态 |
| 警告 | #faad14 | rgb(250,173,20) | 警告提示 |
| 错误 | #ff4d4f | rgb(255,77,79) | 错误提示 |
| 文字 | #333333 | rgb(51,51,51) | 正文 |
| 边框 | #e8e8e8 | rgb(232,232,232) | 边框线 |

### 字体

- **字体族**: Inter, -apple-system, BlinkMacSystemFont
- **基础大小**: 14px
- **比例**: 12px, 14px, 16px, 18px, 20px, 24px

### 间距

- **基础单位**: 8px
- **比例**: 4px, 8px, 16px, 24px, 32px, 48px

## 故障排除

### 常见问题

#### HTML 无法渲染
- 检查浏览器控制台错误
- 确保 CSS 嵌入在 `<style>` 标签中
- 验证文件编码为 UTF-8

#### Figma API 错误
- 验证 auth-profiles.json 中的令牌
- 检查 Figma 设置中的令牌权限
- 确认令牌未过期

#### 插件无法工作
- 验证 manifest.json 格式
- 检查 Figma 插件 API 版本
- 查看浏览器控制台错误

### 调试模式

启用调试日志：

```bash
export UI_PROTOTYPE_DEBUG=1
python3 scripts/html_generator.py --input image.png
```

## 参与贡献

### 开发环境设置

```bash
git clone https://github.com/openclaw/ui-prototype-generator.git
cd ui-prototype-generator
pip install -r requirements.txt
```

### 测试

```bash
python3 -m pytest tests/
```

### 提交变更

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 添加测试
5. 提交 Pull Request

## 路线图

### v1.1.0（计划中）
- [ ] Sketch 格式支持
- [ ] Adobe XD 集成
- [ ] 组件变体
- [ ] 动画支持

### v1.2.0（计划中）
- [ ] 设计令牌导出
- [ ] 主题自定义
- [ ] 批量处理
- [ ] API 速率限制

## 获取支持

### 文档
- 完整文档：https://docs.openclaw.ai/skills/ui-prototype-generator
- 示例：参见 `references/EXAMPLES.md`

### 社区
- Discord：https://discord.gg/clawd
- GitHub Issues：https://github.com/openclaw/ui-prototype-generator/issues

### 商业支持
- 提供企业许可
- 定制开发服务
- 培训和咨询

## 致谢

### 贡献者
- OpenClaw 社区
- Figma API 团队
- 开源贡献者

### 第三方
- Inter 字体家族
- Figma 插件 API
- OpenClaw 框架

## 许可证

MIT 许可证 - 详见 LICENSE 文件

## 更新日志

参见 CHANGELOG.md 了解版本历史

---

**用 ❤️ 制作 - OpenClaw 社区**
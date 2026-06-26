# wiki2doc

将 Confluence Wiki 页面内容转换为 Word 文档 (.docx) 的工具。

## 功能特性

- ✅ 自动登录 Confluence（支持账号密码）
- ✅ 提取页面标题（#title-text）
- ✅ 提取 #splitter-content 中的全部文本和图片
- ✅ 过滤 CSS 隐藏的图片（display:none / visibility:hidden）
- ✅ 图片自动转为 JPG 格式
- ✅ 排除 GIF/SVG/视频等非图片文件
- ✅ 保持文本与图片原始顺序
- ✅ 生成可编辑的 .docx Word 文档
- ✅ 支持单个 URL 或批量 URL 处理
- ✅ 自动创建 demand/ 输出目录
- ✅ 需求分析（检测遗漏点、矛盾点、不明确点）
- ✅ 自动生成结构化测试用例（支持多种测试设计方法）
- ✅ 输出测试用例到Markdown和Excel格式
- ✅ 完整自动化工作流：从Wiki到Excel的一键生成

## 使用方式

### 工具概览

本技能提供两种使用模式：

#### 模式一：完整自动化流程（推荐）

一键完成从Wiki页面到测试用例Excel的完整转换：

```bash
/skill wiki2doc --auto http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
```

执行步骤：
1. ✓ 从Wiki提取内容生成Word文档
2. ✓ 分析需求检测遗漏点、矛盾点
3. ✓ 自动生成测试用例（Markdown格式）
4. ✓ 转换为Excel格式

#### 模式二：独立工具使用

可以单独使用各个工具模块：

##### 1. 基本用法：Wiki转Word（单个页面）

```bash
/skill wiki2doc http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
```

##### 2. 批量处理（多个页面）

```bash
/skill wiki2doc --batch "http://10.225.1.76:8090/page1,http://10.225.1.76:8090/page2"
```

##### 3. 需求分析

```bash
python bin/analyze/analyze_requirements.py demand/需求文档.docx
```

输出：
- JSON格式分析报告
- TXT格式人类可读报告

##### 4. 测试用例生成

```bash
python bin/generate/generate_testcases.py demand/需求文档.docx
```

输出：
- Markdown格式测试用例
- JSON格式测试用例

##### 5. Markdown转Excel

```bash
python bin/convert/md2excel.py demand/测试用例.md
```

输出：
- Excel格式测试用例表格

### 输出位置

所有生成的文件保存在：
```
~/.claude/skills/wiki2doc/demand/
```

文件命名规范：
- Word文档：`{页面标题}.docx`
- 分析报告：`{页面标题}_analysis_report.txt` / `.json`
- 测试用例MD：`{页面标题}_testcases.md` / `.json`
- 测试用例Excel：`{页面标题}_testcases.xlsx`

## 安装依赖

首次使用前请确保已安装依赖：

```bash
pip install playwright beautifulsoup4 python-docx requests Pillow lxml
```

## 注意事项

- 仅支持内网 Confluence（默认地址：http://10.225.1.76:8090/login.action）
- 默认账号：`yanghua`，密码：`Aa123123`
- 图片将自动转换为 JPG，保留原始顺序
- 如果页面无 `#splitter-content` 元素，将返回空文档
- 部分图片下载失败不影响其他内容
- 会话 Cookie 在运行期间保持，批量处理时无需重复登录

## 示例

```bash
# 单个页面
/skill wiki2doc http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052

# 批量处理三个页面
/skill wiki2doc --batch "http://10.225.1.76:8090/page1,http://10.225.1.76:8090/page2,http://10.225.1.76:8090/page3"
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 登录失败 | 检查账号密码是否正确，或手动登录后重试 |
| 页面加载超时 | 检查网络连接，或尝试访问 URL 是否正常 |
| 提示 `No such element: #splitter-content` | 该页面结构不同，无法提取内容 |
| 图片未显示 | 图片可能被 CSS 隐藏，或链接失效 |
| 生成空文档 | 页面无有效内容，或标题提取失败 |

> 本技能由 Claude Code 自动生成，适用于内部知识管理场景。
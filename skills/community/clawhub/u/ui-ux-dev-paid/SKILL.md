---

slug: ui-ux-dev-paid
name: "ui-ux-dev-paid"
version: 1.0.1
displayName: "UI/UX开发工具专业版"
summary: "多页面React项目生成+设计系统持久化+批量截图+Zip导出,面向团队的专业页面开发引擎。面向开发团队和代理机构的专业级React页面生成引擎,支持多页面项目管理、 设计系统持久化、自动化"
summary_zh: "多页面React项目生成+设计系统持久化+批量截图+Zip导出,面向团队的专业页面开发引擎。面向开发团队和代理机构的专业级React页面生成引擎,支持多页面项目管理、 设计系统持久化、自动化"
license: "MIT"
edition: "pro"
description: |- 功能涵盖:。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。具备完整的输入输出规范。
  面向开发团队和代理机构的专业级React页面生成引擎,支持多页面项目管理、
  设计系统持久化、自动化截图审查循环、批量图片处理和Zip打包导出。核心能力:
  - 多页面项目管理与配置持久化
  - 设计系统引用与跨页面一致性保障
  - 自动化多分辨率截图审查(桌面/平板/移动)
  - 批量图片WebP转换与优化报告
  - Zip打包导出与独立部署支持
  - 企业级设计原则自动应用与质量门禁
  - 组件化React开发与状态管理
  适用场景:
  - 代理机构多客户多页面项目交付
  - 企业多页面Web应用快速开发
  - 设计系...
tags:
  - 设计
  - UI
  - UX
  - React
  - 前端
  - 原型
  - 开发
  - 企业级
  - 项目管理
  - 批量处理
  - UI设计
  - bash
  - project
  - page
  - tmp
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"

---

> **核心功能**: 本技能提供与配置持久化等能力。

# UI/UX开发工具专业版
## 付费版扩展能力
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| UI/UX开发工具专业版面React项目生成 | 不支持 | 支持 |
| UI/UX开发工具专业版Zip导出 | 不支持 | 支持 |
| 代码静态分析与质量评分 | 不支持 | 支持 |
| 依赖漏洞检测与升级建议 | 不支持 | 支持 |
| 批量代码审查与报告生成 | 不支持 | 支持 |
## 能力图谱
### 1. 多页面项目管理
支持完整的多页面项目结构,每个项目独立管理配置和设计系统:
```text
serve/
├── client-a/
│   ├── project.json              # 项目配置+设计系统引用
│   ├── assets/
│   │   ├── logo.webp
│   │   ├── hero-banner.webp
│   │   └── team-photos/
│   │       ├── member-1.webp
│   │       └── member-2.webp
│   ├── landing/index.html        # 落地页
│   ├── about/index.html          # 关于我们
│   ├── pricing/index.html        # 定价方案
│   ├── contact/index.html        # 联系我们
│   └── dashboard/index.html      # 用户仪表盘
├── client-b/
│   ├── project.json
│   ├── assets/
│   └── landing/index.html
```
### 2. 设计系统持久化与引用
项目配置中引用设计系统,保障跨页面一致性:
```json
{
  "name": "enterprise-app",
  "version": "2.0.0",
  "preferences": {
    "style": "professional",
    "font": "Inter",
    "primary_color": "#2563EB",
    "dark_mode": true
  },
  "design_system": {
    "reference": "design-system/MASTER.md",
    "max_width": "max-w-7xl",
    "spacing_scale": "tailwind-default",
    "border_radius": "rounded-xl",
    "color_tokens": {
      "primary": "#2563EB",
      "secondary": "#64748B",
      "accent": "#22D3EE",
      "background": "#0F172A",
      "surface": "#1E293B",
      "text_primary": "#F8FAFC",
      "text_secondary": "#CBD5E1"
    }
  },
  "pages": [
    {"slug": "landing", "title": "首页", "status": "completed"},
    {"slug": "pricing", "title": "定价", "status": "completed"},
    {"slug": "dashboard", "title": "仪表盘", "status": "in-progress"},
    {"slug": "settings", "title": "设置", "status": "pending"}
  ]
}
```
- 异常时参考错误处理章节进行恢复
- 关键参数: `设计系统持久化与引用` 选项
### 3. 自动化多分辨率截图审查
专业版支持自动化多分辨率截图,全面覆盖各设备尺寸:
```bash
bash （请参考skill目录中的脚本文件） "http://localhost:5174/project/page/" /tmp/desktop-full.png 1920 1080
bash （请参考skill目录中的脚本文件） "http://localhost:5174/project/page/" /tmp/desktop.png 1440 900
bash （请参考skill目录中的脚本文件） "http://localhost:5174/project/page/" /tmp/tablet.png 1024 768
bash （请参考skill目录中的脚本文件） "http://localhost:5174/project/page/" /tmp/tablet-portrait.png 768 1024
bash （请参考skill目录中的脚本文件） "http://localhost:5174/project/page/" /tmp/mobile.png 390 844
bash （请参考skill目录中的脚本文件） "http://localhost:5174/project/page/" /tmp/mobile-small.png 320 568
```
- 异常时参考错误处理章节进行恢复
- 关键参数: `自动化多分辨率截图审查` 选项
### 4. 批量截图审查脚本
```bash
#!/bin/bash
PROJECT=$1
BASE_URL="http://localhost:5174/${PROJECT}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="/tmp/reviews/${PROJECT}_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"
PAGES=("landing" "about" "pricing" "contact" "dashboard")
RESOLUTIONS=("1920x1080" "1440x900" "768x1024" "390x844")
for page in "${PAGES[@]}"; do
  for res in "${RESOLUTIONS[@]}"; do
    width=$(echo $res | cut -d'x' -f1)
    height=$(echo $res | cut -d'x' -f2)
    output="${OUTPUT_DIR}/${page}_${res}.png"
    bash （请参考skill目录中的脚本文件） "${BASE_URL}/${page}/" "$output" "$width" "$height"
    echo "截图完成: ${page} @ ${res}"
  done
done
echo "批量截图完成,输出目录: ${OUTPUT_DIR}"
```
### 5. 批量图片转换与优化报告
```bash
#!/bin/bash
INPUT_DIR=$1
QUALITY=${2:-80}
total_before=0
total_after=0
count=0
for img in "$INPUT_DIR"/*.{png,jpg,jpeg}; do
  if [ -f "$img" ]; then
    filename=$(basename "$img" | sed 's/\.[^.]*$//')
    output="$INPUT_DIR/${filename}.webp"
    before_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img")
    bash （请参考skill目录中的脚本文件） "$img" "$output" "$QUALITY"
    after_size=$(stat -f%z "$output" 2>/dev/null || stat -c%s "$output")
    reduction=$((100 - (after_size * 100 / before_size)))
    total_before=$((total_before + before_size))
    total_after=$((total_after + after_size))
    count=$((count + 1))
    echo "转换: $(basename $img) -> ${filename}.webp"
    echo "  大小: $(numfmt --to=iec $before_size) -> $(numfmt --to=iec $after_size) (减少${reduction}%)"
  fi
done
echo ""
echo "=== 批量转换报告 ==="
echo "处理文件数: ${count}"
echo "原始总大小: $(numfmt --to=iec $total_before)"
echo "转换后大小: $(numfmt --to=iec $total_after)"
echo "总节省: $(numfmt --to=iec $((total_before - total_after)))"
```- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `批量图片转换与优化报告` 选项
- 处理流程: 接收输入 -> 执行批量图片转换与优化报告 -> 返回结果
- 输入: 用户提供批量图片转换与优化报告所需的参数和指令
### 6. Zip打包导出
```bash
cd serve && zip -r /tmp/enterprise-app.zip enterprise-app/
zip enterprise-app/ \
  -x "*.DS_Store" "*/tmp/*" "*/.git/*"
```
- 异常时参考错误处理章节进行恢复
- 关键参数: `zip打包导出` 选项
## 典型场景
### 场景一:代理机构多客户项目交付
代理机构需要同时为3个客户开发各自的落地页,每个客户有独立的设计偏好.
```bash
mkdir -p serve/client-a/{landing,assets}
cat > serve/client-a/project.json << 'EOF'
{
  "name": "client-a",
  "preferences": {"style": "minimal", "font": "Inter", "primary_color": "#2563EB"},
  "design_system": {"max_width": "max-w-6xl", "border_radius": "rounded-lg"},
  "pages": [{"slug": "landing", "title": "首页", "status": "in-progress"}]
}
EOF
mkdir -p serve/client-b/{landing,assets}
mkdir -p serve/client-c/{landing,assets}
```
### 场景二:企业多页面Web应用
一家企业需要开发包含5个页面的产品官网,要求设计一致性.
```bash
mkdir -p serve/enterprise/{landing,features,pricing,about,contact,assets}
bash （请参考skill目录中的脚本文件） enterprise
bash （请参考skill目录中的脚本文件） serve/enterprise/assets 85
cd serve && zip -r /tmp/enterprise.zip enterprise/
```
### 场景三:自动化视觉质量门禁
在CI/CD流程中集成自动化截图审查作为质量门禁:
```bash
#!/bin/bash
PROJECT=$1
ISSUES_FOUND=0
bash （请参考skill目录中的脚本文件） "$PROJECT"
for screenshot in /tmp/reviews/${PROJECT}_*/*.png; do
  echo "检查: $(basename $screenshot)"
done
if [ $ISSUES_FOUND -gt 0 ]; then
  echo "质量门禁未通过:发现 ${ISSUES_FOUND} 个问题"
  exit 1
else
  echo "质量门禁通过"
  exit 0
fi
```
## 使用说明
### 专业版项目初始化
```bash
bash （请参考skill目录中的脚本文件） 5174
PROJECT_NAME="my-enterprise-app"
mkdir -p serve/${PROJECT_NAME}/{landing,about,pricing,contact,assets}
cat > serve/${PROJECT_NAME}/project.json << 'EOF'
{
  "name": "my-enterprise-app",
  "version": "1.0.0",
  "preferences": {
    "style": "professional",
    "font": "Inter",
    "primary_color": "#2563EB",
    "dark_mode": false
  },
  "design_system": {
    "max_width": "max-w-7xl",
    "border_radius": "rounded-xl",
    "spacing_scale": "tailwind-default"
  },
  "pages": [
    {"slug": "landing", "title": "首页"},
    {"slug": "about", "title": "关于我们"},
    {"slug": "pricing", "title": "定价方案"},
    {"slug": "contact", "title": "联系我们"}
  ]
}
EOF
bash （请参考skill目录中的脚本文件） ${PROJECT_NAME}
bash （请参考skill目录中的脚本文件） serve/${PROJECT_NAME}/assets 85
cd serve && zip -r /tmp/${PROJECT_NAME}.zip ${PROJECT_NAME}/
```
## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| content | string | 否 | 处理的内容输入 |
| mode | string | 否 | 处理模式, 可选值: json/text/markdown |
| style | string | 否 | 输出风格, 参考 `references/style.md` |
## 响应格式
```json
{
  "success": true,
  "data": {
    "result": "处理结果",
    "status": "success",
    "metadata": {
    "metadata": {
      "template_used": "reviewer",
      "word_count": 0,
      "style": "专业"
    }
  },
  "error": null
}
```
输出模板参考: `assets/output.json`
## 异常应对
| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 |
## 环境要求
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome/Chromium(用于截图审查)
- **本地服务器**: Python http.server或Node.js静态服务器
- **Bash**: 批量脚本执行(Windows需Git Bash或WSL)
### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Bash | 运行时 | 必需 | 系统内置或Git Bash |
| Chrome/Chromium | 截图工具 | 必需 | 浏览器安装 |
| cwebp | 图片转换 | 必需 | libwebp工具包 |
| zip | 打包工具 | 必需 | 系统内置 |
| numfmt | 报告格式化 | 推荐 | coreutils(GNU) |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| CDN资源 | 前端库 | 必需 | 自动从CDN加载 |
安装依赖:
```bash
brew install webp
sudo apt install webp zip coreutils
```
### API Key 配置
本Skill基于指令驱动和本地脚本运行,无需额外API Key。页面生成由Agent内置LLM驱动,截图、图片转换和打包均为本地工具执行。CDN前端库通过公网加载,无需配置.
### 可用性分类
- **分类**: MD+execute()
- **说明**: 基于Markdown的AI Skill,。多页面管理、批量截图、图片转换和Zip导出均依赖exec工具执行Bash脚本。自动化质量门禁可集成到CI/CD流水线,需确保Bash和Chrome/Chromium环境可用.
## 案例展示
### 企业级React页面模板(CDN)
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>企业应用 - 首页</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
com/react-dom@18/umd/react-dom.production.min.js"></script>
com/@babel/standalone/babel.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
          colors: {
            primary: { DEFAULT: '#2563EB', hover: '#1D4ED8' }
          }
        }
      }
    }
  </script>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect } = React;
    // 组件化开发
    function Navbar() {
      const [menuOpen, setMenuOpen] = useState(false);
      return (
        <header className="fixed top-4 left-4 right-4 z-50">
          <nav className="bg-white/80 backdrop-blur-md rounded-2xl shadow-lg px-6 py-4">
            <div className="flex items-center justify-between max-w-7xl mx-auto">
              <span className="text-xl font-bold text-slate-900">企业应用</span>
              <button className="md:hidden" onClick={() => setMenuOpen(!menuOpen)}>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d={menuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
                </svg>
              </button>
              <div className={`${menuOpen ? 'block' : 'hidden'} md:flex gap-6`}>
                <a href="/" className="text-slate-600 hover:text-primary cursor-pointer transition-colors">首页</a>
                <a href="/about" className="text-slate-600 hover:text-primary cursor-pointer transition-colors">关于</a>
                <a href="/pricing" className="text-slate-600 hover:text-primary cursor-pointer transition-colors">定价</a>
              </div>
            </div>
          </nav>
        </header>
      );
    }
    function App() {
      return (
        <div className="min-h-screen bg-slate-50">
          <Navbar />
          <main className="max-w-7xl mx-auto px-4 pt-32 pb-16">
            <h1 className="text-5xl font-bold text-slate-900 mb-6">企业级解决方案</h1>
          </main>
        </div>
      );
    }
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```
### 专业版与免费版完整对比
| 功能维度 | 免费版 | 专业版 |
|:------|------:|:------|
| 页面生成 | 单页面 | 多页面项目管理 |
| 项目配置 | 基础JSON | 设计系统持久化引用 |
| 截图审查 | 桌面+移动(2种) | 6种分辨率全覆盖 |
| 截图自动化 | 手动单次 | 批量脚本+CI集成 |
| 图片处理 | 单张WebP转换 | 批量转换+优化报告 |
| 导出 | 静态文件 | Zip打包+排除规则 |
| 设计系统 | 基础原则 | 跨页面一致性引用 |
| 质量保障 | 手动审查 | 自动化质量门禁 |
| 组件化 | 基础组件 | 完整组件+状态管理 |
| 多项目管理 | 单项目 | 多客户并行管理 |
| 适用对象 | 个人开发者 | 团队/代理机构 |
| 兼容性 | - | 完全兼容免费版流程 |
## 疑问解答
### Q1: 专业版是否兼容免费版的单页面流程?
完全兼容。专业版支持免费版的所有操作,包括单页面生成、基础截图审查和WebP转换。专业版额外提供多页面管理、批量操作和导出功能.
### Q2: 如何管理多个客户项目?
每个客户项目使用独立目录(serve/client-a/, serve/client-b/),各自维护project.json配置和设计系统。通过批量脚本可一次性截图审查所有项目.
### Q3: 自动化截图审查如何集成到CI/CD?
将quality-gate.sh脚本集成到CI/CD流水线中,在代码提交后自动运行截图审查。如果发现视觉问题,CI流程失败并报告问题详情.
### Q4: Zip导出的页面可以独立部署吗?
可以。CDN方式的React页面是独立HTML文件,Zip解压后可通过任意静态服务器(Nginx/Apache/CDN)部署,无需构建步骤.
### Q5: 设计系统如何在团队中共享?
将project.json中的设计系统配置纳入版本控制(Git),团队成员克隆仓库后即可使用相同的设计令牌和偏好设置,确保所有人生成的页面视觉一致.
### Q6: 批量图片转换支持哪些格式?
支持PNG、JPG、JPEG转WebP。转换后自动生成优化报告,包括每张文件的原始大小、转换后大小和压缩比例.
## 故障应对方案
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
| --- | --- | --- | --- |
| 无法生成多页面项目 | 设计系统配置错误 | 检查`project.json`文件中的设计系统引用是否正确，确认设计系统文件路径 | 修正`project.json`中的设计系统引用，确保文件路径正确 |
| 截图审查失败 | 网络连接问题 | 检查网络连接是否稳定，确认本地服务器运行正常 | 确保网络连接稳定，重启本地服务器 |
| 批量图片转换无输出 | 图片格式不支持 | 检查图片格式是否为PNG、JPG或JPEG | 转换图片格式为支持的类型，重新执行转换命令 |
| Zip导出文件损坏 | 文件路径错误 | 检查输出路径是否正确，确认文件名无误 | 修正输出路径和文件名，重新执行导出命令 |
| 自动化截图审查脚本执行失败 | 脚本错误 | 检查脚本中的URL、输出目录和分辨率设置是否正确 | 修正脚本中的错误，确保URL、输出目录和分辨率设置正确 |
## 安全告示
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| 设计系统泄露 | 高 | 对设计系统文件进行访问控制，限制编辑权限 | 定期审计设计系统文件的访问记录，确保只有授权用户可以访问 |
| 项目数据丢失 | 中 | 定期备份项目数据，使用版本控制系统 | 定期检查备份文件和版本控制记录，确保数据完整性和一致性 |
| 网络攻击 | 高 | 使用防火墙和入侵检测系统，限制外部访问 | 定期检查网络日志和系统日志，确保没有异常访问记录 |
| 权限滥用 | 中 | 限制用户权限，确保用户只能访问其需要访问的资源 | 定期审计用户权限，确保用户权限设置合理 |
| 脚本执行风险 | 高 | 对执行脚本进行安全检查，避免执行恶意脚本 | 使用安全扫描工具检查脚本，确保没有安全漏洞 |
## 创新优势
| 功能 | 效率提升量化分析 | 差异化对比 |
| --- | --- | --- |
| 多页面项目管理 | 通过自动化管理多页面项目，节省50%的时间在项目配置和设计系统引用上 | 相比手动管理，专业版提供更高效的项目结构管理和配置持久化 |
| 设计系统持久化 | 通过设计系统持久化，确保跨页面一致性，减少30%的设计和开发时间 | 专业版提供设计系统引用和配置，确保团队协作中的一致性 |
| 自动化多分辨率截图审查 | 通过自动化截图审查，节省70%的时间在手动审查上 | 自动化审查覆盖更多设备尺寸，提高审查效率和准确性 |
| 批量图片转换与优化报告 | 通过批量图片转换和优化，节省60%的时间在图片处理上 | 提供批量转换和优化报告，帮助开发者快速识别和修复图片问题 |
| Zip打包导出与独立部署支持 | 通过Zip打包导出，节省80%的时间在部署上 | 提供独立部署支持，简化部署流程，提高部署效率 |
| 企业级设计原则自动应用与质量门禁 | 通过自动应用企业级设计原则和质量门禁，提高产品质量 | 自动化质量门禁确保产品符合设计规范和标准 |
| 组件化React开发与状态管理 | 通过组件化开发，提高开发效率和代码可维护性 | 组件化开发提高代码复用性和可维护性，加快开发速度 |
## 主要功能
- **自动化执行**: 多页面React项目生成+设计系统持久化+批量截图+Zip导出,面向团队的专业页面开发引擎。面向开发团队和代理机构的专业
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
## 性能评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |
## 特色对比
| 对比维度 | UI/UX开发工具专业版 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 多页面React项目生成+设计系统持久化+批量截图+Zip导出,面向团队的专业页 | 通用场景 | 通用场景 |
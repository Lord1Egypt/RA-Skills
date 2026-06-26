# 概念方案生成与设计说明撰写技能 - 完整安装使用手册

---

## 一、技能概述
`scheme_generation_design_writing` 是基于大模型驱动的专业设计文档自动生成技能，可基于历史项目资料、本地设计稿图片、Figma设计链接，快速生成符合行业规范的概念方案和设计说明文档，将设计文档产出时间从3-5天缩短至2分钟。

**核心能力：**
- ✅ 基于历史项目智能匹配设计风格和规范
- ✅ 支持本地PNG/JPG设计稿图片解析
- ✅ 支持Figma设计稿自动解析（组件、尺寸、色彩、布局）
- ✅ 自动生成结构化Markdown/Word格式设计说明
- ✅ 支持银行、电商、政务、教育等多行业方案生成

---

## 二、前置准备
### 2.1 环境要求
- OpenClaw 版本 ≥ 2026.4.22
- Python 3.7+（系统全局可用）
- 磁盘可用空间 ≥ 500MB
- 网络环境：可访问外网（用于Figma API调用，内网环境需配置代理白名单）

### 2.2 历史项目资料准备
1. 整理你的历史设计项目文件夹，按如下结构存放：
```
你的历史项目根目录/
├─ 2020.12 福建省农村信用社手机银行/
│  ├─ 设计稿/
│  ├─ 设计说明.docx
│  └─ 需求文档.pdf
├─ 2021.03 电商APP改版/
│  ├─ 设计稿/
│  └─ 设计说明.docx
└─ ...其他项目
```
2. 每个项目文件夹建议包含：设计说明文档、设计稿文件、需求文档，项目命名建议包含「行业+项目名称+时间」，匹配准确率更高。

---

## 三、技能安装与基础配置
### 3.1 安装技能
在OpenClaw中执行安装命令：
```bash
openclaw skills install scheme_generation_design_writing
```
安装完成后可通过以下命令验证安装成功：
```bash
openclaw skills list | findstr scheme_generation
```

### 3.2 基础配置（必须配置）
1. 找到技能配置文件路径：
   `~/.openclaw/workspace/skills/scheme_generation_design_writing/config.json`
2. 修改配置文件内容：
```json
{
  "projects_path": "C:\\nas\\你的历史项目根目录路径",  // 替换为你的历史项目资料实际路径，Windows用双反斜杠
  "output_path": "C:\\Users\\你的用户名\\.openclaw\\workspace\\output",  // 生成文档输出目录
  "max_related_projects": 5,  // 匹配相关项目最大数量
  "num_proposal_styles": 3,  // 生成概念方案的风格数量
  "enable_figma": true,  // 启用Figma集成
  "enable_image_analysis": true  // 启用本地图片分析
}
```
3. **配置说明**：
   - `projects_path`：**最重要配置**，指向你整理的历史项目资料根目录，使用绝对路径
   - `output_path`：生成的设计说明文档保存目录，建议设置为你方便查找的路径
   - 其他参数保持默认即可

### 3.3 建立项目索引（首次使用必须执行）
进入技能目录执行索引构建：
```bash
cd ~/.openclaw/workspace/skills/scheme_generation_design_writing
python scripts/index_projects.py
```
执行完成后会在`data/`目录下生成`project_index.json`索引文件，后续新增项目后重新执行即可更新索引。

---

## 四、Figma技能集成配置（可选但推荐）
如需支持Figma设计稿自动解析，需要完成以下配置：

### 4.1 安装Figma依赖技能
```bash
openclaw skills install figma
```

### 4.2 获取Figma个人访问令牌
1. 登录Figma官网：https://www.figma.com
2. 点击右上角头像 → 进入「Settings」设置页面
3. 下拉到「Personal access tokens」区域
4. 输入令牌名称（例如`OpenClaw-Design`）→ 点击「Create token」
5. **立即复制生成的令牌**（只会显示一次，关闭页面无法再次查看）
6. 权限建议：仅勾选`Files:Read`只读权限即可

### 4.3 配置Figma令牌
1. 打开Figma技能配置路径：`~/.openclaw/workspace/skills/figma/.env`（没有则新建）
2. 写入以下内容：
```env
FIGMA_ACCESS_TOKEN=你刚才复制的Figma令牌
```

### 4.4 代理问题处理（国内环境必须配置）
国内网络环境下需要修改Figma客户端代码跳过代理SSL验证：
1. 打开文件：`~/.openclaw/workspace/skills/figma/scripts/figma_client.py`
2. 在文件头部导入部分添加：
```python
import urllib3
# 禁用代理SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```
3. 找到`__init__`方法，修改会话配置：
```python
self.session = requests.Session()
self.session.verify = False  # 跳过代理SSL验证
self.session.trust_env = False  # 不读取系统代理配置
self.session.proxies = {'http': None, 'https': None}  # 强制不使用代理
```

### 4.5 验证Figma配置
执行以下命令验证配置成功：
```bash
cd ~/.openclaw/workspace/skills/figma
python -c "from scripts.figma_client import FigmaClient; client = FigmaClient(); print('✅ Figma配置成功！')"
```
输出`✅ Figma配置成功！`即表示配置完成。

---

## 五、使用方法
### 5.1 基于本地设计稿生成设计说明
**命令格式：**
```
/scheme_generation_design_writing 本地图片完整路径 项目说明文字
```
**使用示例：**
```
/scheme_generation_design_writing C:\设计稿\首页.png 这是一个手机银行APP的首页，需要生成设计说明
```
**输出：** 自动生成包含页面概述、布局结构、组件说明、交互逻辑、视觉规范的完整设计说明文档，保存到配置的`output_path`目录。

### 5.2 基于Figma设计稿生成设计说明
**命令格式：**
```
/scheme_generation_design_writing Figma文件链接 项目说明文字
```
**使用示例：**
```
/scheme_generation_design_writing https://www.figma.com/design/xxxxxxx 在线考试系统管理后台，生成完整设计说明
```
**输出：** 自动解析Figma设计稿中的画板尺寸、组件结构、色彩字体、布局结构，生成精确到像素级的专业设计说明文档。

### 5.3 生成概念方案（多风格对比）
**命令格式：**
```
/scheme_generation_design_writing 项目需求描述
```
**使用示例：**
```
/scheme_generation_design_writing 生成一个智能家居APP的概念方案，面向年轻用户群体，科技风设计
```
**输出：** 自动匹配3个不同风格的历史项目，生成3套不同方向的概念方案文档。

---

## 六、生成文档说明
### 6.1 设计说明文档标准结构（8个章节）：
1. **封面**：项目名称、文档类型、版本、日期、设计稿来源
2. **页面概述**：页面功能定位、所属模块、入口跳转关系
3. **页面布局结构**：分区域布局说明、精确尺寸标注
4. **组件清单与说明**：核心组件的尺寸、状态、交互规则、数据来源
5. **交互逻辑**：核心操作流程、异常处理逻辑
6. **视觉规范**：色彩系统、字体层级、间距系统、圆角阴影规范
7. **响应式适配说明**：多尺寸适配规则
8. **开发适配指南**：前端开发尺寸换算、切图规范

### 6.2 概念方案文档标准结构：
1. **项目概述**：项目背景、目标用户、核心功能
2. **设计目标与范围**：设计原则、范围边界
3. **用户画像与使用场景**：典型用户、核心场景
4. **信息架构**：页面层级、功能模块
5. **交互方案**：核心流程设计
6. **视觉风格方向**：3套不同风格的视觉方向建议
7. **技术可行性评估**：技术栈建议、开发周期估算

---

## 七、常见问题排查
### 7.1 匹配不到相关项目
- 检查`config.json`中的`projects_path`路径配置错误，确保使用绝对路径，Windows用双反斜杠
- 历史项目命名不规范，建议项目名称包含行业关键词
- 重新执行`python scripts/index_projects.py`更新项目索引

### 7.2 Figma连接失败
- 检查Figma令牌是否正确，是否有文件读取权限
- 国内环境确认已配置了代理跳过配置（参考4.4节）
- 确认Figma文件链接是否为公开可访问，或你的账号有该文件权限
- 令牌过期重新生成新的令牌更新到`.env`文件

### 7.3 生成文档内容不准确
- 增加历史项目数量不足，建议至少添加5个以上同行业项目
- 优化需求描述，增加行业、用户群体、功能定位等关键词
- 检查设计稿图片清晰度不够，建议使用≥72dpi以上分辨率

### 7.4 Python依赖报错
- 确认Python版本≥3.7，`python --version`检查版本
- 安装缺失依赖：`pip install requests python-docx`

---

## 八、更新维护
- **新增历史项目更新**：新增项目新增后重新执行`python scripts/index_projects.py`更新索引即可
- **Figma技能更新**：更新Figma技能后需要重新检查代理配置是否被覆盖
- **定期备份**：定期备份`data/project_index.json`索引文件

---

*本手册基于实际测试流程编写，所有步骤均已验证通过。*

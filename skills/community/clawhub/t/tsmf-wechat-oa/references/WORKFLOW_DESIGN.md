# 微信公众号写作工作流设计

## 两种写作模式

### 模式一：自动写作（全自动）
适合：有明确话题，需要快速出稿

```
用户输入话题
    ↓
[1] 话题分析
    - 理解用户意图
    - 确定文章类型（技术/生活/商业等）
    - 确定目标读者
    ↓
[2] 资料搜索
    - 搜索最新信息
    - 验证数据准确性
    - 收集案例和引用
    ↓
[3] 大纲生成
    - 确定文章结构
    - 规划章节内容
    - 预估字数分配
    ↓
[4] 自动写作
    - 按大纲逐段写作
    - 实时搜索验证事实
    - 确保内容准确
    ↓
[5] 排版优化
    - 转换为 HTML
    - 应用最佳排版样式
    - 优化移动端显示
    ↓
[6] 生成封面
    - 自动生成封面图
    - 添加"小爪制作，需要审核"
    ↓
[7] 推送草稿
    - 上传到公众号草稿箱
    - 返回 Media ID
    ↓
用户审核发布
```

### 模式二：指定主题写作（半自动）
适合：有明确方向，需要精细控制

```
用户输入话题 + 指定要求
    ↓
[1] 需求确认
    - 确认写作方向
    - 确定风格要求
    - 明确字数要求
    ↓
[2] 资料搜索（用户可参与）
    - 搜索相关资料
    - 用户可提供参考资料
    - 验证关键数据
    ↓
[3] 大纲确认（用户审核）
    - 生成详细大纲
    - 用户确认或修改
    - 确定最终结构
    ↓
[4] 分段写作（用户可干预）
    - 按大纲逐段写作
    - 每段完成后可调整
    - 用户可随时修改方向
    ↓
[5] 排版优化
    - 转换为 HTML
    - 精细调整样式
    - 确保最佳显示效果
    ↓
[6] 生成封面
    - 生成封面图
    - 或用户自定义封面
    ↓
[7] 推送草稿
    - 上传到公众号
    - 返回 Media ID
    ↓
用户审核发布
```

---

## 核心模块设计

### 模块 1：内容搜索与验证
```python
class ContentValidator:
    """内容搜索与验证模块"""
    
    def search_latest_info(self, topic):
        """搜索话题最新信息"""
        pass
    
    def verify_fact(self, statement):
        """验证事实准确性"""
        pass
    
    def collect_data(self, query):
        """收集数据支撑"""
        pass
    
    def check_sources(self, content):
        """检查引用来源"""
        pass
```

### 模块 2：智能大纲生成
```python
class OutlineGenerator:
    """大纲生成模块"""
    
    def analyze_topic(self, topic):
        """分析话题类型"""
        pass
    
    def generate_structure(self, topic_type, word_count):
        """生成文章结构"""
        pass
    
    def allocate_content(self, sections, word_count):
        """分配各段字数"""
        pass
```

### 模块 3：HTML 写作与排版
```python
class HTMLWriter:
    """HTML 写作模块"""
    
    def create_html_template(self):
        """创建 HTML 模板"""
        pass
    
    def write_section(self, title, content, style):
        """写作单个章节"""
        pass
    
    def apply_typography(self, html_content):
        """应用排版样式"""
        pass
    
    def optimize_mobile(self, html_content):
        """优化移动端显示"""
        pass
```

### 模块 4：封面生成
```python
class CoverGenerator:
    """封面生成模块"""
    
    def generate_default_cover(self, title):
        """生成默认封面"""
        pass
    
    def generate_custom_cover(self, title, style):
        """生成自定义封面"""
        pass
```

### 模块 5：草稿推送
```python
class DraftPublisher:
    """草稿推送模块"""
    
    def upload_cover(self, image_path):
        """上传封面图"""
        pass
    
    def push_draft(self, title, content, cover_id):
        """推送草稿"""
        pass
```

---

## 关键决策点

### 1. 写作模式选择
- 用户说"写一篇关于...的文章" → 自动模式
- 用户说"帮我写...，要求..." → 指定主题模式

### 2. 搜索验证策略
- 涉及数据/事实 → 必须搜索验证
- 涉及最新信息 → 实时搜索
- 个人观点/经验 → 无需验证

### 3. 排版样式选择
- 技术类 → 科技现代主题
- 生活类 → 温暖文艺/活泼清新
- 商业类 → 极简商务
- 特殊需求 → 自定义 HTML

### 4. 封面生成
- 默认 → "小爪制作，需要审核"
- 自定义 → 用户提供图片或描述

---

## 用户交互流程

### 自动模式交互
```
用户：写一篇关于 AI 发展趋势的文章

小爪：
1. 正在搜索 AI 发展趋势最新信息...
2. 已收集 5 篇权威资料，验证 3 个关键数据
3. 生成大纲：
   - 01 2024年AI重大突破
   - 02 技术趋势分析
   - 03 产业应用案例
   - 04 未来展望
4. 开始写作（预计 5 分钟）...
5. ✓ 写作完成，已转换为 HTML 排版
6. ✓ 生成封面图
7. ✓ 已推送至草稿箱
   Media ID: xxx
   请前往公众号后台审核发布
```

### 指定主题模式交互
```
用户：我想写一篇关于咖啡文化的文章，要文艺风格，1500字左右

小爪：
1. 确认需求：
   - 主题：咖啡文化
   - 风格：文艺
   - 字数：1500字
   确认吗？

用户：确认

小爪：
2. 搜索咖啡文化相关资料...
3. 生成大纲：
   - 01 咖啡的起源与传播（300字）
   - 02 第三波咖啡浪潮（400字）
   - 03 咖啡馆的文化意义（400字）
   - 04 结语（400字）
   这个结构可以吗？

用户：可以，但第三波咖啡那段可以短一点

小爪：
4. 调整大纲，开始写作...
5. [逐段展示，用户可实时调整]
6. ✓ 完成，已排版推送
```

---

## 技术实现要点

### 1. 搜索验证
- 使用 web_search 获取最新信息
- 使用 web_fetch 验证具体事实
- 标记不确定的内容，提醒用户核实

### 2. HTML 模板
- 预设 5 套主题样式
- 支持完全自定义 HTML
- 移动端优先的响应式设计

### 3. 错误处理
- 搜索失败 → 使用已有知识，标记待核实
- 推送失败 → 保存本地，提示重试
- 内容敏感 → 提醒用户审核

### 4. 进度反馈
- 每个步骤实时反馈
- 预估剩余时间
- 关键节点用户确认

---

## 下一步工作

1. 实现 ContentValidator 搜索验证模块
2. 实现 OutlineGenerator 大纲生成模块
3. 优化 HTMLWriter 排版模块
4. 集成 CoverGenerator 封面生成
5. 完善 DraftPublisher 推送模块
6. 编写完整的 SKILL.md 文档

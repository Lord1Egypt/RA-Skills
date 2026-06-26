# Resume Generator - AI简历生成器

为程序员和测试工程师打造的智能简历生成工具。输入个人信息，输出专业简历。

## 功能

- ✅ **多模板**：3种专业简历模板
- ✅ **多格式**：Markdown / HTML / PDF导出
- ✅ **岗位匹配**：根据JD优化简历关键词
- ✅ **AI自我介绍**：基于经历自动生成

## 使用方法

```bash
# 安装
pip install resume-generator

# 基本使用
resume-generator generate --name "张三" --email "zhangsan@example.com" --phone "13800138000"

# 从JSON文件导入
resume-generator generate --input resume_data.json --template modern

# 导出为HTML
resume-generator export --input resume.md --format html --output resume.html

# 导出为PDF
resume-generator export --input resume.html --format pdf --output resume.pdf

# 优化简历
resume-generator optimize --resume resume.md --jd "job_description.txt"
```

## 输入格式

```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "location": "北京",
  "education": [
    {
      "school": "北京大学",
      "major": "计算机科学",
      "degree": "硕士",
      "year": "2020"
    }
  ],
  "experience": [
    {
      "company": "字节跳动",
      "title": "高级工程师",
      "duration": "2020.06 - 至今",
      "description": "- 负责抖音核心功能开发\n- 主导性能优化，提升30%加载速度"
    }
  ],
  "projects": [
    {
      "name": "电商系统",
      "role": "技术负责人",
      "tech": "Python, Django, Redis",
      "description": "构建高并发电商平台，日均订单10万+",
      "outcome": "月GMV突破500万"
    }
  ],
  "skills": [
    {"category": "编程语言", "items": ["Python", "JavaScript", "SQL"]},
    {"category": "框架", "items": ["Django", "React", "Vue"]},
    {"category": "工具", "items": ["Git", "Docker", "Jenkins"]}
  ],
  "self_intro": "6年后端开发经验，擅长高并发系统设计"
}
```

## 输出模板

### 模板1：简约技术型
黑白配色，左侧技能栏，右侧详细内容。适合技术岗位。

### 模板2：经典专业型
顶部联系方式，双栏布局。适合求职申请。

### 模板3：现代简洁型
大字体姓名，卡片式布局。适合互联网公司。

## 价格

| 套餐 | 价格 | 功能 |
|:---|:---|:---|
| Free | 免费 | 基础模板、Markdown导出 |
| Pro | ¥19 | 3种模板、HTML+PDF导出、岗位匹配优化 |
| Team | ¥49 | 批量生成、API访问、自定义模板 |

## 适用场景

- 程序员客栈接单展示
- 求职申请（Boss直聘、猎聘、拉勾）
- 技术面试准备
- 个人品牌展示

## 案例

### 案例1：Python开发工程师
```json
{
  "name": "李明",
  "experience": [{"company": "美团", "title": "后端开发", "description": "- 负责订单系统\n- 日处理订单100万+"}],
  "skills": [{"category": "后端", "items": ["Python", "Go", "MySQL"]}]
}
```
输出：专业的技术简历，突出项目规模和业绩。

### 案例2：测试工程师
```json
{
  "name": "王芳",
  "experience": [{"company": "阿里云", "title": "测试开发", "description": "- 主导自动化测试框架开发\n- 覆盖率从60%提升到90%"}],
  "skills": [{"category": "测试", "items": ["Selenium", "Pytest", "Jenkins"]}]
}
```
输出：突出测试业绩和工具开发能力。

---

*让简历说话，用实力证明*
# Sum2Slides Lite 用户指南

## 🚀 快速开始

### 安装步骤
```bash
# 1. 下载安装包并解压
# 2. 进入目录
cd sum2slides-lite

# 3. 运行安装脚本
# 手动安装

# 4. 启动应用
python sum2slides_lite.py
```

### 第一次使用
```python
# 基本示例
from sum2slides import sum2slides

conversation = """
今天会议讨论了以下内容：
1. 决定开发新功能
2. 需要增加测试覆盖率
3. 关键决策：采用微服务架构
4. 行动项：下周完成设计
"""

result = sum2slides(conversation, title="会议总结")
if result['success']:
    print(f"✅ PPT已生成: {result['ppt_info']['file_path']}")
```

## 📋 核心功能

### 1. 对话分析
Sum2Slides 会自动分析对话内容，提取：
- ✅ 关键决策
- ✅ 行动项  
- ✅ 重要要点
- ✅ 问题列表
- ✅ 解决方案

### 2. PPT生成
支持两种生成方式：

#### 方式A: 标准生成（无需特殊权限）
```python
# 使用 python-pptx 生成标准 .pptx 文件
result = sum2slides(conversation, software="powerpoint")
```
✅ 无需授权，兼容性好

#### 方式B: 自动化生成（需要授权）
```python
# 自动化操作 PowerPoint/WPS
result = sum2slides(conversation, software="powerpoint")
# 需要 AppleScript 权限
```
✅ 功能更强大，需要授权

### 3. 文件处理
- **本地保存**: 自动保存到 `~/Desktop/Sum2Slides/`
- **飞书上传**: 自动上传并生成分享链接（需要配置）
- **模板选择**: 商务、技术、教育等多种模板

## ⚙️ 配置说明

### 基础配置
编辑 `config/config.yaml`:
```yaml
# 输出目录
output_dir: "~/Desktop/Sum2Slides"

# 默认软件
default_software: "powerpoint"  # powerpoint 或 wps

# 默认模板  
default_template: "business"    # business, technical, education

# 日志设置
logging:
  level: "INFO"
  file: "~/Desktop/Sum2Slides/logs/sum2slides.log"
```

### 飞书配置
1. 复制环境变量文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件：
```bash
# 飞书应用配置
FEISHU_APP_ID=your_app_id_here
FEISHU_APP_SECRET=your_app_secret_here

# 其他配置
OUTPUT_DIR=~/Desktop/Sum2Slides
LOG_LEVEL=INFO
```

3. 或在 `config/config.yaml` 中配置：
```yaml
feishu:
  enabled: true
  app_id: "your_app_id"
  app_secret: "your_app_secret"
```

## 🎯 使用示例

### 示例1: 会议总结
```python
from sum2slides import sum2slides

meeting = """
项目进度会议：
1. 前端开发完成80%
2. 后端API设计完成
3. 关键决策：采用React + Node.js技术栈
4. 行动项：本周完成测试用例
5. 风险：第三方服务延迟
"""

result = sum2slides(
    conversation_text=meeting,
    title="项目进度汇报",
    software="powerpoint",
    template="business"
)
```

### 示例2: 学习笔记整理
```python
learning = """
Python学习笔记：
• 函数定义和调用
• 类和对象的概念
• 异常处理机制
• 重点：理解装饰器原理
• 难点：异步编程
"""

result = sum2slides(
    conversation_text=learning,
    title="Python学习总结",
    software="wps",
    template="education"
)
```

### 示例3: 项目提案
```python
proposal = """
新产品提案：
1. 市场机会：AI助手需求增长
2. 产品特点：智能对话、多平台支持
3. 技术方案：微服务架构、云原生
4. 预期收益：年收入100万
5. 资源需求：3人团队，6个月
"""

result = sum2slides(
    conversation_text=proposal,
    title="新产品提案",
    software="powerpoint",
    template="technical",
    platform="feishu"  # 自动上传到飞书
)
```

## 🔧 高级功能

### 自定义模板
```python
from sum2slides import Sum2Slides

# 自定义颜色方案
custom_config = {
    "template": "business",
    "colors": {
        "primary": "#FF6B6B",
        "secondary": "#4ECDC4",
        "background": "#F7FFF7"
    }
}

processor = Sum2Slides()
result = processor.summarize_to_ppt(
    conversation_text="你的内容",
    title="自定义模板",
    software="powerpoint",
    template_config=custom_config
)
```

### 批量处理
```python
from sum2slides import Sum2Slides

processor = Sum2Slides()

# 处理多个对话
conversations = [
    ("会议1", "内容1..."),
    ("会议2", "内容2..."),
    ("会议3", "内容3..."),
]

for title, content in conversations:
    result = processor.summarize_to_ppt(
        conversation_text=content,
        title=title,
        software="powerpoint"
    )
    if result['success']:
        print(f"✅ {title}: {result['ppt_info']['file_path']}")
```

### 集成到其他应用
```python
import subprocess
import json

# 通过命令行调用
conversation = "你的对话内容..."
result = subprocess.run(
    ['python', '-c', f'''
from sum2slides import sum2slides
import json
result = sum2slides("{conversation}")
print(json.dumps(result))
    '''],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
print(f"生成的文件: {data['ppt_info']['file_path']}")
```

## 🛠️ 故障排除

### 常见问题

#### 问题1: 无法保存文件
**症状**: "Permission denied" 错误
**解决**:
1. 检查输出目录权限
2. 更改输出目录：修改 `config/config.yaml` 中的 `output_dir`
3. 手动创建目录：`mkdir -p ~/Desktop/Sum2Slides`

#### 问题2: 飞书上传失败
**症状**: "无法获取访问令牌" 错误
**解决**:
1. 检查 `.env` 文件配置
2. 验证飞书应用权限
3. 检查网络连接
4. 使用本地保存：设置 `platform=None`

#### 问题3: PPT软件无法打开文件
**症状**: 文件损坏或无法识别
**解决**:
1. 确保安装了 PowerPoint 或 WPS
2. 检查文件扩展名是否为 `.pptx`
3. 尝试用其他软件打开
4. 重新生成文件

#### 问题4: 权限检测失败
**症状**: AppleScript 权限问题
**解决**:
1. 运行 `python quick_permission_check.py`
2. 按照提示授权
3. 或使用标准生成模式

### 日志查看
```bash
# 查看日志文件
tail -f ~/Desktop/Sum2Slides/logs/sum2slides.log

# 或查看最近错误
grep ERROR ~/Desktop/Sum2Slides/logs/sum2slides.log
```

### 调试模式
```bash
# 设置调试级别
export LOG_LEVEL=DEBUG

# 重新运行
python your_script.py
```

## 📊 最佳实践

### 1. 对话格式优化
```python
# 良好的对话格式
good_conversation = """
会议主题：项目评审

讨论内容：
1. 进展：完成模块A开发
2. 问题：接口性能有待优化
3. 决策：采用缓存方案提升性能
4. 行动：下周进行压力测试
5. 总结：整体进度符合预期
"""

# 避免的格式
bad_conversation = "随便写的一些话没有结构很难分析"
```

### 2. 文件管理
```bash
# 定期清理旧文件
find ~/Desktop/Sum2Slides -name "*.pptx" -mtime +30 -delete

# 备份重要文件
cp ~/Desktop/Sum2Slides/重要汇报.pptx ~/备份/
```

### 3. 性能优化
```python
# 对于长对话，分段处理
long_conversation = "很长很长的对话..."

# 方法1: 自动分段
from sum2slides import Sum2Slides
processor = Sum2Slides()
processor.set_max_length(1000)  # 每段最多1000字符

# 方法2: 手动分段
sections = long_conversation.split('\n\n')
for i, section in enumerate(sections, 1):
    result = sum2slides(section, title=f"第{i}部分")
```

## 🔄 更新和维护

### 检查更新
```bash
# 查看当前版本
python -c "from sum2slides import __version__; print(__version__)"

# 检查更新（未来功能）
# git pull origin master
```

### 备份配置
```bash
# 备份重要文件
cp config/config.yaml config/config.yaml.backup
cp .env .env.backup
```

### 重新安装
```bash
# 完全重新安装
rm -rf ~/.openclaw/skills/sum2slides-lite
# 手动安装
```

## 🤝 获取帮助

### 文档资源
- **本文档**: 基础使用指南
- **权限说明**: 详细权限配置
- **API文档**: 高级编程接口
- **示例代码**: `examples/` 目录

### 社区支持
- **GitHub Issues**: 问题反馈和功能建议
- **Discord社区**: 实时交流和支持
- **邮件列表**: 更新通知和公告

### 问题报告
遇到问题时，请提供：
1. 错误信息全文
2. 使用的代码片段
3. 系统环境信息
4. 日志文件内容

## 🎉 成功案例

### 案例1: 周会自动化
```python
# 每周自动生成会议纪要PPT
import schedule
import time
from sum2slides import sum2slides

def weekly_meeting():
    # 从数据库或文件读取会议记录
    meeting_notes = get_meeting_notes()
    
    result = sum2slides(
        conversation_text=meeting_notes,
        title="周会纪要",
        software="powerpoint",
        platform="feishu"  # 自动分享到团队
    )
    
    if result['success']:
        send_notification(f"周会纪要已生成: {result['file_url']}")

# 每周一上午10点执行
schedule.every().monday.at("10:00").do(weekly_meeting)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 案例2: 学习笔记系统
```python
# 将学习内容自动整理成PPT
class LearningAssistant:
    def __init__(self):
        from sum2slides import Sum2Slides
        self.processor = Sum2Slides()
    
    def add_note(self, topic, content):
        # 保存到数据库
        save_to_db(topic, content)
        
        # 生成学习总结PPT
        result = self.processor.summarize_to_ppt(
            conversation_text=content,
            title=f"{topic}学习总结",
            template="education"
        )
        
        return result
```

### 案例3: 客户汇报自动化
```python
# 自动为客户生成项目汇报
def generate_client_report(project_data):
    # 整理项目数据
    report_content = format_project_data(project_data)
    
    # 生成专业汇报PPT
    result = sum2slides(
        conversation_text=report_content,
        title=f"{project_data['name']}项目汇报",
        template="business",
        software="powerpoint"
    )
    
    # 发送给客户
    if result['success']:
        send_email_to_client(
            subject="项目汇报",
            attachment=result['ppt_info']['file_path']
        )
```

---

**开始使用 Sum2Slides Lite，让对话总结变得简单高效！** 🚀

如有任何问题，请查阅文档或联系社区支持。
# OpenClaw 网页下载器技能

## 技能描述

网页读取器技能是一个强大的工具，允许您使用Google Chrome的无头浏览器读取和分析网页内容。此技能可以：

- 检查系统是否安装了Google Chrome
- 如果未找到Chrome，自动尝试安装（在支持的平台上）
- 使用Chrome的无头模式和优化参数下载网页内容
- 读取和处理下载的HTML内容
- 生成网页内容摘要
- 安全处理临时文件以保护您的隐私

## 安装指南

### 先决条件

- Python 3.8或更高版本
- Google Chrome浏览器（将被自动检测，如果缺少将提供安装协助）

### 安装步骤

1. **在OpenClaw中安装技能**：
   - 打开OpenClaw
   - 进入技能管理器
   - 点击"添加技能"
   - 选择您下载此技能的目录
   - 点击"安装"

### 平台特定说明

- **Windows**：Chrome安装需要从[Google Chrome](https://www.google.com/chrome/)手动下载
- **macOS**：自动安装需要Homebrew。如果未安装Homebrew，需要手动安装。
- **Linux**：支持在Ubuntu/Debian和Fedora/CentOS/RHEL发行版上自动安装。对于其他发行版，需要手动安装。

## 使用示例

### 基本用法

```python
from webpage_reader import main

result = main("https://example.com")

if result['success']:
    print("网页下载成功！")
    print("摘要：")
    print(result['summary'])
    print("\n内容预览：")
    print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
else:
    print(f"错误：{result['message']}")
```

### 命令行用法

```bash
python webpage_reader.py https://example.com
```

### OpenClaw界面用法

1. 打开OpenClaw
2. 选择网页读取器技能
3. 在输入字段中输入URL
4. 点击"运行"
5. 在输出面板中查看结果

## 技术详情

### Chrome命令参数

技能使用以下Chrome命令参数以获得最佳性能：

```bash
google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --virtual-time-budget=8000 --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" --hide-scrollbars --blink-settings=imagesEnabled=true --dump-dom <url>
```

### 输出格式

技能返回具有以下结构的字典：

```python
{
    "success": bool,          # 操作是否成功
    "message": str,           # 状态消息
    "content": str,           # 网页的完整HTML内容
    "summary": str            # 网页内容摘要
}
```

## 故障排除

### 常见问题

1. **未找到Chrome**
   - **解决方案**：从[https://www.google.com/chrome/](https://www.google.com/chrome/)手动安装Google Chrome

2. **权限错误**
   - **解决方案**：以适当的权限运行技能，尤其是在Linux上安装Chrome时

3. **超时错误**
   - **解决方案**：技能有60秒的超时。对于大型网页，这可能不够。您可以在`download_webpage`函数中修改超时时间。

4. **内容为空**
   - **解决方案**：检查URL是否可访问，且未被CAPTCHA或其他反爬措施阻止

5. **编码错误**
   - **解决方案**：技能使用UTF-8编码。对于使用不同编码的网页，您可能需要修改`read_webpage_content`函数中的编码处理。

### 日志记录

技能生成详细的日志以帮助诊断问题。日志默认输出到控制台，但可以配置为写入文件（如果需要）。

## 贡献

欢迎贡献！请随时提交Pull Request。

## 许可证

此技能以MIT许可证发布。有关详细信息，请参阅LICENSE文件。

## 支持

如果您遇到任何问题或有疑问，请在GitHub存储库上打开一个issue。
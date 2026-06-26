---
name: xiaohongshu-publish-kit
description: "Complete toolkit for publishing content to Xiaohongshu (小红书). Includes automated browser control, image generation, content formatting, and full publishing pipeline. Works with OpenClaw browser automation. 完整的小红书自动发布工具包，包含浏览器自动化、图片生成、内容格式化等全流程功能。"
metadata:
  {
    "openclaw": {
      "emoji": "📕",
      "requires": {
        "bins": ["python3"]
      },
      "recommends": {
        "config": ["browser.defaultProfile"]
      }
    }
  }
---

# 小红书自动发布工具包 (Xiaohongshu Publish Kit)

通过 OpenClaw 托管浏览器实现小红书图文笔记的完全自动化发布。支持AI内容生成、封面制作、格式化和一键发布。

## 功能特性

✨ **完整自动化流程**
- 自动登录检测和页面导航
- 智能图片上传（支持多张图片）
- 标题和正文自动填写
- 发布状态验证

🎨 **内容创作支持**
- 自动生成科技风封面图片
- AI内容格式化（适配小红书规范）
- 话题标签自动插入
- 字数限制自动检查

🔧 **开发者友好**
- 完整的Python脚本示例
- 详细的浏览器控制命令
- 错误处理和重试机制
- 可扩展的模块化设计

## 平台限制（严格遵守）

⚠️ **小红书平台规则**
- **标题**：最多 20 个字符（超出导致发布失败）
- **正文**：最多 1000 个字符
- **图片**：1-18张，最大32MB，推荐png/jpg/jpeg/webp
- **尺寸**：推荐3:4至2:1，分辨率≥720x960

## 快速开始

### 1. 环境准备

```bash
# 启动托管浏览器
browser --browser-profile openclaw start

# 创建图片上传目录
mkdir -p /tmp/openclaw/uploads
```

### 2. 登录小红书创作平台

首次使用需要手动登录一次：

```bash
browser --browser-profile openclaw navigate https://creator.xiaohongshu.com
```

手动扫码登录后，可设置自动保活：

```bash
# 设置登录保活（推荐）
./scripts/setup_keepalive.sh
```

### 3. 登录保活设置（重要）

为避免频繁扫码，强烈建议设置自动保活：

**方法1: Crontab 定时保活（推荐）**
```bash
./scripts/setup_keepalive.sh
# 选择选项1，每30分钟自动检查登录状态
```

**方法2: 手动检查**
```bash
python3 scripts/login_keeper.py --mode check
```

**方法3: 守护进程**
```bash
python3 scripts/login_keeper.py --mode daemon --interval 30
```

### 3. 使用脚本发布

```bash
python3 ~/.openclaw/workspace/skills/xiaohongshu-publish-kit/scripts/publish.py \
  --title "你的标题（≤20字）" \
  --content "你的正文内容（≤1000字）" \
  --image "/path/to/your/cover.jpg"
```

或者使用AI辅助发布：

```bash
python3 ~/.openclaw/workspace/skills/xiaohongshu-publish-kit/scripts/ai_publish.py \
  --topic "AI技术发展" \
  --generate-cover
```

## 详细使用说明

### 浏览器控制流程

小红书发布涉及多个步骤的浏览器操作，每步都有特定的技术要求：

#### Step 1: 页面导航
```bash
browser --browser-profile openclaw navigate https://creator.xiaohongshu.com/publish/publish
browser --browser-profile openclaw wait 3000
```

#### Step 2: 切换到图文模式
⚠️ **重要**：必须使用JS方式点击，直接click会触发文件选择器

```bash
browser --browser-profile openclaw evaluate --fn "() => {
  const tabs = document.querySelectorAll('.creator-tab, [class*=tab]');
  for (const t of tabs) {
    if (t.textContent.trim().includes('上传图文')) {
      t.click();
      return 'switched to image-text mode';
    }
  }
  return 'tab not found';
}"
```

#### Step 3: 上传图片
```bash
# 先arm文件，再点击按钮
browser --browser-profile openclaw upload /tmp/openclaw/uploads/cover.jpg
browser --browser-profile openclaw snapshot  # 找到上传按钮的ref
browser --browser-profile openclaw click <upload_button_ref>
browser --browser-profile openclaw wait 5000  # 等待上传完成
```

#### Step 4: 填写标题
标题是`<input>`元素，需要使用原生setValue方式：

```bash
browser --browser-profile openclaw evaluate --fn "() => {
  const el = document.querySelector('input[placeholder*=\"标题\"]');
  if (!el) return 'title input not found';
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(el, '你的标题内容');
  el.dispatchEvent(new Event('input', {bubbles:true}));
  el.dispatchEvent(new Event('change', {bubbles:true}));
  return 'title set, length=' + el.value.length;
}"
```

#### Step 5: 填写正文
正文是contenteditable富文本编辑器，使用innerHTML：

```bash
browser --browser-profile openclaw evaluate --fn "() => {
  const el = document.querySelector('.ql-editor, [contenteditable=true], .ProseMirror');
  if (!el) return 'editor not found';
  el.focus();
  el.innerHTML = '<p>第一段</p><p><br></p><p>第二段</p><p><br></p><p>#话题标签</p>';
  el.dispatchEvent(new Event('input', {bubbles:true}));
  return 'body set, length=' + el.textContent.length;
}"
```

#### Step 6: 发布验证
```bash
# 检查字数是否合规
browser --browser-profile openclaw evaluate --fn "() => {
  const titleEl = document.querySelector('input[placeholder*=\"标题\"]');
  return 'title length=' + (titleEl ? titleEl.value.length : 0);
}"

# 点击发布
browser --browser-profile openclaw evaluate --fn "() => {
  const btns = document.querySelectorAll('button');
  for (const b of btns) {
    if (b.textContent.trim() === '发布') {
      b.click();
      return 'publish clicked';
    }
  }
  return 'publish button not found';
}"

# 验证发布成功（URL包含published=true）
browser --browser-profile openclaw tabs
```

## 高级功能

### 自动封面生成

使用内置的封面生成功能：

```python
from scripts.cover_generator import generate_tech_cover

# 生成蓝紫科技风封面
cover_path = generate_tech_cover(
    title="AI热点速递",
    date="2026.03.17",
    style="tech_blue"
)
```

### 内容格式化

```python
from scripts.content_formatter import format_for_xiaohongshu

# 自动格式化内容
formatted = format_for_xiaohongshu(
    title="原始标题可能很长需要截断",
    content="原始内容...",
    tags=["AI", "科技", "热点"]
)
```

### 批量发布

```python
from scripts.batch_publisher import BatchPublisher

publisher = BatchPublisher()
publisher.add_post(title="标题1", content="内容1", image="图片1")
publisher.add_post(title="标题2", content="内容2", image="图片2")
publisher.publish_all()
```

## 常见问题

### Q: 发布按钮点击无反应？
A: 检查标题是否超过20字，或正文是否为空。小红书会禁用不合规的发布。

### Q: 图片上传失败？
A: 确认图片格式（png/jpg/jpeg/webp）和大小（<32MB），避免使用gif。

### Q: 登录状态丢失？
A: 重新在托管浏览器中扫码登录一次即可。

### Q: 页面加载缓慢？
A: 增加等待时间，或检查网络连接。

## 扩展开发

### 添加新的封面样式

在`scripts/cover_generator.py`中添加新的样式模板：

```python
def generate_custom_cover(title, **kwargs):
    # 你的自定义封面逻辑
    pass
```

### 集成其他内容源

实现`ContentProvider`接口：

```python
class MyContentProvider(ContentProvider):
    def fetch_content(self):
        # 返回格式化的内容
        pass
```

## 许可证

MIT License - 可自由使用、修改和分发。

---

**注意**：本工具仅供学习和合法使用，请遵守小红书平台规则和相关法律法规。
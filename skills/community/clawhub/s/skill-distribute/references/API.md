# API 文档

多平台分发工具的 API 参考。

## 核心类

### ContentItem

内容数据类。

```python
@dataclass
class ContentItem:
    id: str                    # 内容ID
    title: str                 # 标题
    description: str           # 描述
    images: List[str]          # 图片路径列表
    tags: List[str]            # 标签列表
    source_platform: str       # 源平台
    created_at: str            # 创建时间
```

### ImageProcessor

图片处理器。

```python
processor = ImageProcessor(config_path="config/image.yaml")

# 处理图片
result = processor.process_for_platform(
    image_path="path/to/image.jpg",
    platform="douyin",
    output_dir="temp"
)
```

**方法说明**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `process_for_platform` | image_path, platform, output_dir | str | 处理图片 |
| `blur_fill` | img, target_size | Image | 模糊填充 |
| `solid_fill` | img, target_size | Image | 纯色填充 |
| `smart_crop` | img, target_size | Image | 智能裁剪 |

### ContentAdapter

内容适配器。

```python
adapter = ContentAdapter(config_path="config/content.yaml")

# 适配内容
adapted = adapter.adapt_for_platform(
    content=content_item,
    platform="douyin"
)
```

**方法说明**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `adapt_for_platform` | content, platform | ContentItem | 适配内容 |
| `adapt_title` | title, max_length | str | 适配标题 |
| `adapt_description` | desc, max_length | str | 适配描述 |
| `adapt_tags` | tags, max_tags, auto_tags | List[str] | 适配标签 |

### CaptchaHandler

验证码处理器。

```python
handler = CaptchaHandler(config_path="config/captcha.yaml")

# 处理滑块验证码
success = handler.handle_slider(page, ".slider-btn")

# 处理短信验证码
success = handler.handle_sms(page, "13800138000")
```

**方法说明**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `handle_slider` | page, slider_selector | bool | 滑块验证 |
| `handle_click` | page, container_selector | bool | 点选验证 |
| `handle_text` | page, image_selector | bool | 文字验证 |
| `handle_sms` | page, phone | bool | 短信验证 |

## 命令行接口

### distribute.py

主分发脚本。

```bash
python3 scripts/distribute.py [OPTIONS]
```

**参数说明**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--source` | str | xiaohongshu | 源平台 |
| `--note-id` | str | - | 笔记ID |
| `--targets` | str | - | 目标平台 |
| `--use-app` | flag | False | 使用桌面端 |
| `--driver` | str | playwright | 浏览器驱动 |
| `--debug` | flag | False | 调试模式 |
| `--relogin` | flag | False | 强制重登 |
| `--stagger` | flag | False | 错峰发布 |
| `--filter-tag` | str | - | 标签过滤 |
| `--exclude` | str | - | 关键词排除 |

**示例**:

```bash
# 同步最新笔记
python3 scripts/distribute.py

# 同步指定笔记
python3 scripts/distribute.py --note-id 123456

# 同步到指定平台
python3 scripts/distribute.py --targets douyin,kuaishou

# 调试模式
python3 scripts/distribute.py --debug
```

### batch_distribute.py

批量分发脚本。

```bash
python3 scripts/batch_distribute.py [OPTIONS]
```

**参数说明**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--recent` | int | - | 最近N篇 |
| `--file` | str | - | 笔记列表文件 |
| `--note-ids` | str | - | 笔记ID列表 |
| `--targets` | str | - | 目标平台 |
| `--interval` | int | 60 | 间隔(秒) |
| `--use-app` | flag | False | 使用桌面端 |
| `--debug` | flag | False | 调试模式 |

**示例**:

```bash
# 同步最近10篇
python3 scripts/batch_distribute.py --recent 10

# 从文件读取
python3 scripts/batch_distribute.py --file notes.txt

# 指定笔记
python3 scripts/batch_distribute.py --note-ids id1,id2,id3
```

### schedule.py

定时任务脚本。

```bash
python3 scripts/schedule.py [OPTIONS]
```

**参数说明**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--time` | str | required | 执行时间 |
| `--days` | str | - | 执行日期 |
| `--daily` | flag | False | 每天执行 |
| `--targets` | str | - | 目标平台 |
| `--use-app` | flag | False | 使用桌面端 |

**示例**:

```bash
# 每天9点执行
python3 scripts/schedule.py --time 09:00 --daily

# 每周一三五20点执行
python3 scripts/schedule.py --time 20:00 --days mon,wed,fri
```

## 配置文件

### accounts.yaml

账号配置。

```yaml
platforms:
  xiaohongshu:
    enabled: bool
    login_type: str
    username: str
    cookie_file: str
```

### image.yaml

图片处理配置。

```yaml
image_processing:
  fill_mode: str      # blur | solid | extend | crop
  background_color: str
  blur_radius: int
  quality: int
```

### content.yaml

内容适配配置。

```yaml
content_adaptation:
  <platform>:
    max_title_length: int
    max_desc_length: int
    max_tags: int
    tag_prefix: str
    auto_tags: List[str]
```

### captcha.yaml

验证码配置。

```yaml
captcha:
  timeout: int
  max_retries: int
  handlers:
    slider:
      enabled: bool
      mode: str      # auto | manual
```

### strategy.yaml

发布策略配置。

```yaml
publish_strategy:
  stagger:
    enabled: bool
    interval: int
  random_delay:
    enabled: bool
    min: int
    max: int
```

## 返回值格式

### 分发结果

```json
{
  "success": true,
  "platform": "douyin",
  "note_id": "123456",
  "published_url": "https://...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 批量结果

```json
{
  "total": 10,
  "success": 8,
  "failed": 2,
  "details": [
    {"note_id": "1", "success": true},
    {"note_id": "2", "success": false, "error": "..."}
  ]
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1 | 通用错误 |
| 10 | 登录失败 |
| 11 | Cookie 过期 |
| 20 | 内容获取失败 |
| 21 | 内容处理失败 |
| 30 | 发布失败 |
| 31 | 验证码失败 |
| 40 | 网络错误 |
| 50 | 配置错误 |

## 扩展开发

### 添加新平台

1. 创建平台发布器类

```python
class NewPlatformPublisher(PlatformPublisher):
    def login(self) -> bool:
        # 实现登录逻辑
        pass
    
    def publish(self, content: ContentItem) -> bool:
        # 实现发布逻辑
        pass
```

2. 注册到分发管理器

```python
publishers = {
    'douyin': DouyinPublisher,
    'new_platform': NewPlatformPublisher,
}
```

3. 添加配置

```yaml
# config/accounts.yaml
platforms:
  new_platform:
    enabled: true
    login_type: qrcode
```

### 自定义验证码处理

```python
class CustomCaptchaHandler(CaptchaHandler):
    def handle_slider(self, page, selector) -> bool:
        # 自定义滑块处理
        pass
```

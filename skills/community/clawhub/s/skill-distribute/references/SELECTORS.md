# 选择器配置

各平台页面元素选择器配置，用于浏览器自动化。

## 小红书

### 登录页面
```yaml
xiaohongshu:
  login:
    # 登录按钮
    login_btn: "button:has-text('登录')"
    # 扫码登录选项
    qrcode_tab: "[data-testid='qrcode-login']"
    # 二维码图片
    qrcode_img: ".qrcode-image"
    # 登录成功标识
    success_indicator: ".user-avatar"
```

### 笔记详情页
```yaml
  note:
    # 标题
    title: "h1.title"
    # 描述
    description: ".desc-content"
    # 图片列表
    images: ".note-image img"
    # 标签
    tags: ".tag-item"
    # 点赞数
    likes: ".like-count"
```

### 发布页面
```yaml
  publish:
    # 上传按钮
    upload_btn: "button:has-text('上传')"
    # 文件输入
    file_input: "input[type='file']"
    # 标题输入
    title_input: "input[placeholder='填写标题']"
    # 描述输入
    desc_input: "textarea[placeholder='添加正文']"
    # 标签输入
    tag_input: "input[placeholder='添加标签']"
    # 发布按钮
    publish_btn: "button:has-text('发布')"
    # 发布成功提示
    success_msg: ".publish-success"
```

## 抖音

### 登录页面
```yaml
douyin:
  login:
    # 手机号输入
    phone_input: "input[placeholder='手机号']"
    # 验证码输入
    code_input: "input[placeholder='验证码']"
    # 获取验证码按钮
    get_code_btn: "button:has-text('获取验证码')"
    # 登录按钮
    login_btn: "button:has-text('登录')"
    # 登录成功标识
    success_indicator: ".avatar"
```

### 发布页面
```yaml
  publish:
    # 上传按钮
    upload_btn: ".upload-btn"
    # 文件输入
    file_input: "input[type='file']"
    # 标题输入
    title_input: ".title-input"
    # 话题输入
    topic_input: ".topic-input"
    # 发布按钮
    publish_btn: ".publish-btn"
    # 发布成功提示
    success_msg: ".publish-success"
```

## 视频号

### 登录页面
```yaml
shipinhao:
  login:
    # 微信登录按钮
    wechat_login: ".wechat-login-btn"
    # 二维码
    qrcode_img: ".qrcode-image"
    # 登录成功标识
    success_indicator: ".user-name"
```

### 发布页面
```yaml
  publish:
    # 上传按钮
    upload_btn: ".upload-btn"
    # 文件输入
    file_input: "input[type='file']"
    # 标题输入
    title_input: ".title-input"
    # 描述输入
    desc_input: ".desc-input"
    # 发布按钮
    publish_btn: ".publish-btn"
```

## 快手

### 登录页面
```yaml
kuaishou:
  login:
    # 手机号输入
    phone_input: "input[placeholder='手机号']"
    # 验证码输入
    code_input: "input[placeholder='验证码']"
    # 登录按钮
    login_btn: "button:has-text('登录')"
    # 登录成功标识
    success_indicator: ".user-avatar"
```

### 发布页面
```yaml
  publish:
    # 上传按钮
    upload_btn: ".upload-btn"
    # 文件输入
    file_input: "input[type='file']"
    # 标题输入
    title_input: ".title-input"
    # 标签输入
    tag_input: ".tag-input"
    # 发布按钮
    publish_btn: ".publish-btn"
```

## 验证码元素

### 滑块验证码
```yaml
captcha:
  slider:
    # 滑块容器
    container: ".slider-captcha"
    # 滑块按钮
    slider_btn: ".slider-btn"
    # 背景图片
    bg_image: ".slider-bg"
    # 缺口图片
    gap_image: ".slider-gap"
```

### 点选验证码
```yaml
  click:
    # 验证码容器
    container: ".click-captcha"
    # 提示文字
    prompt: ".captcha-prompt"
    # 验证码图片
    image: ".captcha-image"
    # 可点击区域
    click_area: ".captcha-image"
```

## 选择器更新

### 自动更新
```bash
# 更新所有平台选择器
python3 scripts/update_selectors.py --all

# 更新指定平台
python3 scripts/update_selectors.py --platform douyin
```

### 手动更新

1. 打开浏览器开发者工具
2. 定位到目标元素
3. 复制选择器
4. 更新配置文件

## 调试技巧

### 验证选择器
```python
# 在浏览器控制台测试
document.querySelector(".title-input")

# 使用 Playwright 验证
page.locator(".title-input").is_visible()
```

### 截图调试
```python
# 截图保存
page.screenshot(path="debug.png")

# 元素截图
element.screenshot(path="element.png")
```

## 注意事项

1. **选择器稳定性**
   - 优先使用 data-testid
   - 避免使用动态 class
   - 使用语义化选择器

2. **多语言支持**
   - 避免依赖文字内容
   - 使用属性选择器
   - 考虑国际化

3. **性能优化**
   - 减少选择器嵌套
   - 使用 ID 选择器
   - 缓存选择器结果

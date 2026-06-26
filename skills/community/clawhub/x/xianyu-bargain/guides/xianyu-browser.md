# 闲鱼浏览器自动化指南

## 前置条件

1. 使用 Chrome 浏览器
2. 已登录闲鱼网页版 (https://www.goofish.com)
3. OpenClaw browser 工具可用

## 操作流程

### Step 1: 打开商品页面

```javascript
browser({
  action: "open",
  url: "https://www.goofish.com/item?id=商品ID"
})
```

### Step 2: 获取页面快照

```javascript
browser({
  action: "snapshot",
  targetId: "..."
})
```

### Step 3: 点击"我想要"按钮

```javascript
browser({
  action: "act",
  kind: "click",
  ref: "我想要按钮的ref"
})
```

### Step 4: 输入消息

```javascript
browser({
  action: "act",
  kind: "type",
  ref: "输入框ref",
  text: "讲价话术内容"
})
```

### Step 5: 发送

```javascript
browser({
  action: "act",
  kind: "click",
  ref: "发送按钮ref"
})
```

## 注意事项

- 闲鱼网页版功能有限，部分操作可能需要 App
- 频繁自动操作可能触发平台风控，请遵守平台使用规则
- 建议合理控制操作频率
- 重要交易建议手动确认

## 商品链接格式

- 网页版: `https://www.goofish.com/item?id=XXX`
- 分享链接: 需要转换为网页版链接

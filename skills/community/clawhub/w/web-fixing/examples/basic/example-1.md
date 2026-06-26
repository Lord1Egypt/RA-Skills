# 基础示例：修复响应式布局问题

## 场景
网站在移动设备上显示不正常，元素溢出屏幕。

## 执行步骤
1. 使用开发者工具检查
2. 识别问题元素
3. 修改 CSS
4. 测试不同屏幕尺寸

## 问题诊断
```html
<!-- 问题代码 -->
<div class="container">
  <div class="sidebar">...</div>
  <div class="content">...</div>
</div>
```

```css
/* 问题 CSS */
.container {
  width: 1200px;  /* 固定宽度导致溢出 */
}
```

## 修复方案
```css
/* 修复后 */
.container {
  width: 100%;
  max-width: 1200px;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
}
```

## 预期结果
- 在手机上正常显示
- 在平板上正常显示
- 在桌面端保持最大宽度

## 关键要点
- 使用相对单位（%、vw、vh）
- 设置 max-width 限制最大宽度
- 使用媒体查询适配不同设备
- 测试真实设备

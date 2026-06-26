# 基础示例：修复 JavaScript 错误

## 场景
用户报告点击按钮后没有反应，控制台报错。

## 执行步骤
1. 打开浏览器开发者工具
2. 查看 Console 标签
3. 找到错误信息
4. 定位并修复代码

## 错误信息
```
Uncaught TypeError: Cannot read property 'addEventListener' of null
  at script.js:10
```

## 问题代码
```javascript
// script.js:10
const button = document.querySelector('.submit-btn');
button.addEventListener('click', handleSubmit);  // button 为 null
```

## 修复方案
```javascript
// 方案 1：检查元素是否存在
const button = document.querySelector('.submit-btn');
if (button) {
  button.addEventListener('click', handleSubmit);
}

// 方案 2：使用可选链（现代浏览器）
document.querySelector('.submit-btn')?.addEventListener('click', handleSubmit);

// 方案 3：等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('.submit-btn');
  button.addEventListener('click', handleSubmit);
});
```

## 预期结果
- 控制台没有错误
- 按钮点击正常响应
- 在不同浏览器中都能工作

## 调试技巧
1. 使用 `console.log()` 输出变量值
2. 使用 `debugger` 设置断点
3. 使用 Chrome DevSources 单步调试
4. 查看 Network 标签确认资源加载

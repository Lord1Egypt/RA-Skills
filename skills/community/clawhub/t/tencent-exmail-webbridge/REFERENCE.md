# REFERENCE.md — 腾讯企业邮箱 WebBridge 自动化详细参考

> 本文档是 SKILL.md 的补充，包含完整的技术细节和调试技巧。

---

## iframe 完整结构

```
frame_html (顶层 URL 永远不变)
 ├── iframe[0-3] 框架/导航/空白
 ├── iframe[4] 主内容区（动态切换）
 │   ├── 邮件列表视图
 │   ├── 邮件阅读视图
 │   └── 写信/回复/转发视图
 │       └── innerIframe[3] 富文本编辑器
 ├── iframe[5] 文件夹列表
 └── iframe[6+] 其他
```

**关键规律**：
- 回复/转发操作点击后，iframe[4] 会动态切换成写信视图
- URL 完全不变，只能靠标题或内部 DOM 判断当前状态
- 富文本编辑器需要二次穿透：iframe[4] → innerIframe[3]

---

## 中文编码详解

### 问题根源

Kimi WebBridge 传输 JS 代码时破坏 UTF-8 中文字面量。直接写中文字符串会全部变成乱码。

### 解决方案：码点编码协议

**核心原则：JS 代码中绝不写中文。**

#### 方式一：String.fromCharCode（富文本 DOM 操作）

```javascript
// 想写"中文"
span.textContent = String.fromCharCode(20013, 25991);
```

#### 方式二：HTML 实体（HTML 源码模式）

```html
<!-- 想写"中文" -->
<div>&#20013;&#25991;</div>
```

#### 方式三：码点数组（浏览器端返回）

```javascript
(() => {
  const result = (() => { /* 原始代码 */ })();
  if (typeof result === 'string') {
    return JSON.stringify(Array.from(result).map(c => c.charCodeAt(0)));
  }
  return JSON.stringify(result);
})()
```

Python 端还原：

```python
import json

def decode_result(value):
    try:
        char_codes = json.loads(value)
        if isinstance(char_codes, list):
            return ''.join(chr(c) for c in char_codes)
    except:
        pass
    return value
```

### 辅助工具函数

```python
def to_charcode_js(text):
    """将中文文本转为 JS String.fromCharCode 表达式"""
    codes = [ord(c) for c in text]
    return f"String.fromCharCode({','.join(map(str, codes))})"

def to_html_entities(text):
    """将中文文本转为 HTML 实体编码"""
    return ''.join(f'&#{ord(c)};' for c in text)

# 示例
>>> to_charcode_js("中文")
"String.fromCharCode(20013,25991)"

>>> to_html_entities("中文")
"&#20013;&#25991;"
```

---

## 正文追加完整实现

### 错误做法（覆盖签名）

```javascript
editorDoc.body.innerHTML = newHTML;  // ❌ 清掉引用和签名
```

### 正确做法（在签名前插入）

腾讯企业邮箱签名锚点：`<sign signid="0">`

```javascript
const signEl = editorDoc.querySelector('sign');
const newDiv = editorDoc.createElement('div');

// 构建新内容（用 String.fromCharCode 写中文）
newDiv.innerHTML = '<div>' + String.fromCharCode(20013,25991) + '</div>';

if (signEl && signEl.parentNode) {
  signEl.parentNode.insertBefore(newDiv, signEl);
} else {
  editorDoc.body.appendChild(newDiv);
}
```

### 带样式的正文追加

```javascript
const editorDoc = /* 穿透到 innerIframe[3] */;
const signEl = editorDoc.querySelector('sign');

const contentDiv = editorDoc.createElement('div');
contentDiv.style.marginBottom = '20px';
contentDiv.innerHTML = '<p>' + String.fromCharCode(/* 你的码点 */) + '</p>';

if (signEl && signEl.parentNode) {
  signEl.parentNode.insertBefore(contentDiv, signEl);
} else {
  editorDoc.body.appendChild(contentDiv);
}
```

---

## 收件人操作详解

### 读取收件人

**反直觉**：收件人字段值在 `textContent` 里，不在 `value` 里。

```javascript
const doc = document.querySelectorAll('iframe')[4].contentDocument;
const toInput = doc.querySelector('input[to]');

// 正确 ✅
const toValue = toInput.textContent;
// 结果: "DoNotReply"<DoNotReply@notification.fortinet.net>;

// 错误 ❌
const toValue = toInput.value;  // 空字符串
```

### 修改收件人

```javascript
const toInput = doc.querySelector('input[to]');
toInput.textContent = 'new@example.com';
// 可能需要触发 input 事件
const event = new Event('input', { bubbles: true });
toInput.dispatchEvent(event);
```

---

## 三种回复模式完整流程

### 通用框架

```javascript
// Step 1: 获取 iframe[4] 文档
const frame4 = document.querySelectorAll('iframe')[4];
const doc = frame4.contentDocument;

// Step 2: 点击回复/回复全部/转发
doc.querySelector('a[opt="reply"]').click();      // 回复
doc.querySelector('a[opt="reply_all"]').click();  // 回复全部
doc.querySelector('a[opt="forward"]').click();    // 转发

// Step 3: 等待 iframe 切换（1-2秒）
await new Promise(r => setTimeout(r, 1500));

// Step 4: 获取新的 iframe[4] 文档（注意：引用需要重新获取）
const newDoc = document.querySelectorAll('iframe')[4].contentDocument;

// Step 5: 验证模式
const from_s = newDoc.querySelector('input[name="from_s"]');
console.log('Mode:', from_s ? from_s.value : 'not_found');
// 预期: reply / reply_all / forward

// Step 6: 穿透到富文本编辑器
const innerFrame = newDoc.querySelectorAll('iframe')[3];
const editorDoc = innerFrame.contentDocument;
```

### 模式对比表

| 模式 | 触发 | from_s 值 | 默认收件人 | 主题前缀 | 原始邮件引用 |
|------|------|-----------|------------|----------|--------------|
| 回复 | `reply` | reply | 原发件人 | Re: | 保留在原位置 |
| 回复全部 | `reply_all` | reply_all | 所有原始收件人 | Re: | 保留在原位置 |
| 转发 | `forward` | forward | 空（需手动填） | Fw: | 变为附件/引用 |

---

## 文件夹导航

### 切换文件夹

```javascript
const folderFrame = document.querySelectorAll('iframe')[5];
const folderDoc = folderFrame.contentDocument;

// 点击文件夹链接
// folderid=1: 收件箱
// folderid=3: 已发送
// folderid=4: 草稿箱
// folderid=5: 已删除
// folderid=6: 垃圾箱
const folderLink = folderDoc.querySelector('a[folderid="1"]');
folderLink.click();
```

---

## 调试技巧

### 快速检查所有 iframe

```javascript
const iframes = document.querySelectorAll('iframe');
let results = [];
for (let i = 0; i < iframes.length; i++) {
  try {
    const doc = iframes[i].contentDocument;
    results.push({
      index: i,
      title: doc.title,
      textLen: doc.body.innerText.length
    });
  } catch(e) {
    results.push({index: i, error: e.message});
  }
}
return JSON.stringify(results);
```

### 检查当前模式

```javascript
const doc = document.querySelectorAll('iframe')[4].contentDocument;
const from_s = doc.querySelector('input[name="from_s"]');
return from_s ? from_s.value : 'not_found';
```

### 检查富文本编辑器内容

```javascript
const frame4 = document.querySelectorAll('iframe')[4];
const doc = frame4.contentDocument;
const innerFrame = doc.querySelectorAll('iframe')[3];
const editorDoc = innerFrame.contentDocument;
return editorDoc.body.innerHTML.substring(0, 1000);
```

---

## 已知限制

1. **无法操作附件** — 文件上传需要模拟用户选择文件，WebBridge 难以实现
2. **抄送/密送未验证** — DOM 结构可能类似收件人，但未经测试
3. **新建邮件未验证** — 写信按钮触发逻辑可能不同于回复
4. **邮件搜索未验证** — 搜索框位置和事件机制未知
5. **删除邮件未验证** — 删除确认弹窗的处理方式未知

---

## 替代方案展望

如果腾讯企业邮箱未来开放官方 API，这些代码可以废弃。官方 API 会提供：
- 标准 REST/gRPC 接口
- 正确的 UTF-8 编码
- 附件上传下载
- 无需 iframe 穿透

在此之前，WebBridge 是唯一可行的自动化方案。

---

*记录时间：2026-06-05*  
*基于实际测试验证：Kimi WebBridge + 腾讯企业邮箱 exmail.qq.com*

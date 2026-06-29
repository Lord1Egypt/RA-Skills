---
name: tencent-exmail-webbridge
description: 通过 Kimi WebBridge 自动化操作腾讯企业邮箱 Web 端（exmail.qq.com）的规范技能。涵盖 iframe 穿透、中文编码协议、邮件读取/回复/转发/正文追加等操作。当用户要求通过 WebBridge 操作腾讯企业邮箱、读取邮件、回复邮件、转发邮件、或遇到 exmail.qq.com 自动化问题时触发。
version: 2.0.0
---

# 腾讯企业邮箱 WebBridge 自动化

> **用途**：通过 Kimi WebBridge 在浏览器环境中操作腾讯企业邮箱 Web 端。
> **核心挑战**：iframe 嵌套 + 中文编码 + 动态 DOM 切换。

## 前置检查

操作前确认：
- [ ] 用户已登录 exmail.qq.com
- [ ] WebBridge 已注入目标页面
- [ ] 页面已完成初始加载（收件箱已渲染）

## 核心协议

### 1. 中文编码协议（强制）

WebBridge 传输 JS 会破坏 UTF-8 中文字面量。**JS 代码中绝不写中文**。

三种场景对应三种编码方式：

**场景 A：富文本 DOM 操作**
```javascript
span.textContent = String.fromCharCode(20013, 25991); // "中文"
```

**场景 B：读取中文返回**
浏览器端返回码点数组：
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
def decode_result(value):
    try:
        char_codes = json.loads(value)
        if isinstance(char_codes, list):
            return ''.join(chr(c) for c in char_codes)
    except:
        pass
    return value
```

**辅助生成函数**
```python
def to_charcode_js(text):
    codes = [ord(c) for c in text]
    return f"String.fromCharCode({','.join(map(str, codes))})"
```

### 2. iframe 穿透协议

腾讯企业邮箱采用 iframe 嵌套，不跳转新 URL，内容动态切换。

| 场景 | 目标 iframe | 判断依据 |
|------|------------|----------|
| 邮件列表 | iframe[3] | 标题含"收件箱" |
| 邮件阅读 | iframe[4] | 标题含邮件主题 |
| 写信/回复/转发 | iframe[4] | 标题为"腾讯企业邮箱 - 写信" |
| 富文本编辑器 | iframe[4] → innerIframe[3] | 需二次穿透 |

**快速定位所有 iframe**
```javascript
const iframes = document.querySelectorAll('iframe');
let results = [];
for (let i = 0; i < iframes.length; i++) {
  try {
    const doc = iframes[i].contentDocument;
    results.push({index: i, title: doc.title, textLen: doc.body.innerText.length});
  } catch(e) {}
}
return JSON.stringify(results);
```

### 3. 安全红线（不可违背）

- **绝不自动发送邮件** — 只能到草稿/关闭这一步
- 涉及发送的操作必须经过用户**明确确认**
- 提供的按钮操作仅限：存草稿、关闭

## 常见操作

### 回复/回复全部/转发

| 模式 | 触发方式 | from_s 值 | 收件人 | 主题前缀 |
|------|----------|-----------|--------|----------|
| 回复 | `a[opt="reply"].click()` | reply | 原发件人 | Re: |
| 回复全部 | `a[opt="reply_all"].click()` | reply_all | 所有原始收件人 | Re: |
| 转发 | `a[opt="forward"].click()` | forward | 空（需手动填） | Fw: |

点击后等 1-2 秒，iframe[4] 切换为写信视图。

**验证当前模式**
```javascript
const doc = document.querySelectorAll('iframe')[4].contentDocument;
const from_s = doc.querySelector('input[name="from_s"]');
return from_s ? from_s.value : 'not_found';
```

### 正文追加（不覆盖签名）

腾讯企业邮箱签名锚点：`<sign signid="0">`

```javascript
const signEl = editorDoc.querySelector('sign');
const newDiv = editorDoc.createElement('div');
// ... 用 String.fromCharCode 构建内容 ...

if (signEl && signEl.parentNode) {
  signEl.parentNode.insertBefore(newDiv, signEl);
} else {
  editorDoc.body.appendChild(newDiv);
}
```

### 收件人读取

**关键**：收件人在 `textContent` 里，不在 `value` 里。
```javascript
// 正确
const to = input.textContent; // "DoNotReply"<DoNotReply@notification.fortinet.net>;
// 错误
const to = input.value; // ""（空）
```

### 文件夹导航

通过 iframe[5]（folderlist）切换：

| folderid | 文件夹 |
|----------|--------|
| 1 | 收件箱 |
| 3 | 已发送 |
| 4 | 草稿箱 |
| 5 | 已删除 |
| 6 | 垃圾箱 |

## 验证清单

- ✅ 读取邮件列表
- ✅ 打开邮件阅读
- ✅ 自动点击回复/回复全部/转发
- ✅ 修改主题
- ✅ 安全追加正文（不覆盖签名）
- ✅ 存草稿
- ✅ 关闭窗口
- ✅ 文件夹导航

未验证：附件操作、抄送/密送、新建邮件、删除邮件、邮件搜索。

## 详细参考

- 完整踩坑记录和调试技巧 → [REFERENCE.md](REFERENCE.md)
- 编码协议实现细节 → [REFERENCE.md](REFERENCE.md) 中文编码章节
- iframe 层级完整结构 → [REFERENCE.md](REFERENCE.md) iframe 结构章节

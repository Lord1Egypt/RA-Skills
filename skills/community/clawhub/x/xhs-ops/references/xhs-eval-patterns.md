# XHS 通用提取模板

## 基础 Evaluate 模板

```js
() => {
  const pickText = (el, sels) => {
    for (const s of sels) {
      const v = el.querySelector?.(s)?.textContent?.trim();
      if (v) return v;
    }
    return '';
  };

  const num = (v) => {
    const m = String(v || '')
      .replace(/,/g, '')
      .match(/\d+(?:\.\d+)?/);
    return m ? Number(m[0]) : 0;
  };

  return [...document.querySelectorAll('.note-item, .comment-item, li, [data-item]')]
    .slice(0, 20)
    .map((el) => ({
      title: pickText(el, ['.title', '.note-title', 'h1', 'h2', 'h3']),
      hook: pickText(el, ['.desc', '.description', '.summary', '.intro']),
      angle: pickText(el, ['.tag', '.category', '.angle']),
      comments_signal: pickText(el, ['.comment', '.comments', '[data-comment]']),
      cta: pickText(el, ['.cta', '.action', '.footer']),
      likes: num(pickText(el, ['.like', '.likes', '[data-like]'])),
      tags: pickText(el, ['.tag-list', '.tags'])
    }))
    .filter(x => x.title || x.hook);
}
```

## 进阶 Selector 适配

页面结构随版本变化，以下是已知的兼容写法：

### 搜索结果页 / 推荐流（并联写法）
```js
// 同时兼容多种 selector，取最宽的那个
const items = [
  ...document.querySelectorAll('.note-item'),
  ...document.querySelectorAll('[data-item]'),
  ...document.querySelectorAll('section.note-item'),
].filter((el, i, arr) => arr.indexOf(el) === i); // 去重
```

### 轮播图内容抓取
```js
// 只取活跃帧，排除轮播复制帧
const activeSlides = document.querySelectorAll(
  '.swiper-slide-active:not(.swiper-slide-duplicate)'
);
```

### 评论区 contenteditable 输入
```js
// 向 contenteditable 区域注入文字并触发 input 事件
const el = document.querySelector('[contenteditable="true"]');
el.focus();
document.execCommand('insertText', false, '回复内容');
el.dispatchEvent(new InputEvent('input', { bubbles: true }));
```

## 使用建议

- 先确认字段存在；缺失返回空字符串，避免脚本失败。
- 先做 20 条以内试跑，再扩大样本规模。
- 需复用时可按页面结构调整 selector。
- 页面结构变化时，先做一次 `snapshot` 再调整 selector，不要盲试。

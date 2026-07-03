# 质量检查清单(Checklist)

生成工具展示 PPT 前通读,生成后逐项自检。

---

## 🔴 P0 · 一定不能犯的错

### 1. 类名必须来自 template.html
生成前先 `Read` `assets/template.html` 的 `<style>` 块,确认每个用到的类都存在。
最常见遗漏: `feat-card` / `feat-card.accent` / `step-item` / `step-num` / `compare-col` / `spec-table` / `uc-card` / `cta-btn`

### 2. 替换 [必填] 占位符
`<title>` 里的 `[必填] 工具名 · 产品介绍` 必须改为实际工具名。
`grep "必填" {工具名}.html` 确认无残留。

### 3. 标题用无衬线,不用 emoji 作图标
- 本模板全部走无衬线(Noto Sans SC + Inter),不要引入衬线字体
- 用 Lucide 图标,不用 emoji
- Lucide 图标 CDN 已引入,`lucide.createIcons()` 在 JS 末尾自动调用

### 4. 每页必须有明确的主题 class
- `slide light` / `slide dark` / `slide hero light` / `slide hero dark`
- 不能只写 `slide` 不带主题
- `grep 'class="slide' {工具名}.html` 确认

### 5. 主题节奏不能单调
- 连续 3 页以上同主题(全 light 或全 dark)→ 视觉疲劳,不允许
- 8 页以上必须有 ≥1 个 hero dark + ≥1 个 hero light
- 整个 deck 不能全是 light,必须有 dark 页制造呼吸

### 6. 图片用相对路径
图片放 `images/` 文件夹,HTML 里用 `images/xxx.png`,不用绝对路径。

### 7. 不要用大段中文正文当装饰
工具介绍 PPT 是"少字多图"风格。每页正文控制在 2-3 行,大段描述留给 GitHub README。

---

## 🟡 P1 · 排版质量

### 8. 每页一个核心信息
一页只讲一件事。不要在一页里塞入"功能列表 + 截图 + 数据 + 链接"。

### 9. 截图优先于文字
能用截图说明的,不要写文字。T03/T04/T06/T10 等带截图的布局优先使用。

### 10. 功能卡片数量匹配网格
- 3 个功能 → `.grid-3`
- 4 个功能 → `.grid-4`
- 6 个功能 → `.grid-6`
- 不要 5 个功能用 3 列网格(会有一个空位)

### 11. CTA 按钮在首尾页
T01 封面和 T09 CTA 页应该有下载/GitHub 按钮。正文页不要放 CTA。

### 12. 数据有来源
T05 数据大字报的数值应该有真实测量来源,标注在 footer-min 或 stat-note 里。

---

## 🟢 P2 · 视觉打磨

### 13. 截图要有质量
- 截图 ≥ 1600px 宽(大屏不模糊)
- 不要截到桌面杂乱背景
- 考虑用主题色背景 + 居中截图

### 14. 颜色一致性
- 一份 deck 只用一套主题色
- 按钮/高亮/accent 保持一致
- Light 页和 Dark 页的同名组件视觉一致

### 15. 字号不要溢出
- `h-hero` 标题建议 ≤ 8 个中文字符
- 长标题用 `<br>` 手动断行
- 移动端(≤900px)有响应式降级,测试一下

---

## 🔵 P3 · 操作细节

### 16. 翻页测试
- ← → 键翻页正常
- 滚轮翻页正常
- 底部圆点数量和总页数匹配
- chrome-min 里的页码写对

### 17. 动效测试
- 每页切换时元素有淡入效果
- `data-anim` 标记数量 ≥ 页数 × 3

### 18. 图片加载
- 所有 `src` 路径有效
- 无 404 图片
- 占位图片用 `.img-slot` 类

---

## 最终自检

```
预检(生成前)
  □ 已读过 template.html 的 <style>,确认所需类都存在
  □ 已选定一套主题色(蓝/紫/绿/黑/橙/青/粉/金/琥珀)
  □ 已画出"主题节奏表":每页明确 light/dark/hero light/hero dark
  □ 标题已改为实际工具名(grep "[必填]" 无结果)
  □ 图片已放到 images/ 文件夹

内容
  □ 工具名 + 定位语在 T01 封面
  □ 核心功能在 T02 功能卡片
  □ 截图在 T03 大图展示(或 T10 功能详情)
  □ 数据在 T05 数据大字报(非必须)
  □ CTA 在首尾页
  □ 价格/安装/FAQ 等按需选用 T11-T16

排版
  □ 每页一个核心信息
  □ 截图优先于文字
  □ 功能卡片数量匹配网格
  □ 新布局类名(faq-item/pricing-card/timeline/matrix-table 等)已在 template.html 中验证存在
  □ 没有 emoji 作图标
  □ 大标题 ≤ 8 字,不换行

视觉
  □ Light/Dark 交替,有 hero 页插入
  □ 一套主题色到底
  □ 截图清晰,无杂乱背景
  □ 按钮/accent 颜色一致
  □ SVG 背景(bg-geo/bg-dots/bg-circuit)如使用,与页面主题协调
  □ 流动色块(blob)如使用,仅限 hero 页,不超过 2 个

交互
  □ ← → 翻页正常
  □ 底部圆点与总页数匹配
  □ 每页有淡入动效(data-anim/data-anim-x/data-anim-pop)
  □ 功能卡片 hover 有浮起效果
  □ CTA 按钮有光泽扫过动画
  □ 图片路径有效,无 404
```

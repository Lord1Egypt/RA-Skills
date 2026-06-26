# 微信排版规范（统一模板｜v2）

> **锚定文章：** 2026-05-23《AI'单干'和'组队'，到底有什么区别》
> **生成时间：** 2026-05-24
> **目的：** 合并 templates.md、components.md、formatting-lessons.md 为一个唯一规范，消除内部冲突

---

## 一、设计令牌（Design Tokens）

所有值以此表为准，如果旧文件里有不同的值，以本表为准。

| Token | 值 | 用途 |
|-------|-----|------|
| `--side-padding` | `20px` | 所有 section 的左右边距 |
| `--body-font` | `15px` | 正文字号 |
| `--body-color` | `#333` | 正文字色 |
| `--body-line-height` | `2` | 正文行距 |
| `--body-letter-spacing` | `1px` | 正文字间距 |
| `--body-margin-bottom` | `24px` | 段落间距 |
| `--title-font` | `24px` | 文章视觉标题字号 |
| `--title-color` | `#1a1a2e` | 深色标题/强调文字 |
| `--accent-color` | `#d4a574` | 暖金强调色（span、金线） |
| `--accent-weight` | `500` | 强调文字粗细 |
| `--tag-font` | `13px` | TAG 和日期字号 |
| `--tag-color` | `#b8b8b8` | TAG 颜色 |
| `--tag-letter-spacing` | `4px` | TAG 字间距 |
| `--date-color` | `#aaa` | 日期颜色 |
| `--card-bg` | `#f8f6f3` | 金句卡片/特征卡背景 |
| `--card-padding` | `16px 20px` | 特征卡内边距 |
| `--card-border` | `3px solid #d4a574` | 特征卡左边框 |
| `--card-font` | `14px` | 特征卡正文字号 |
| `--card-line-height` | `1.9` | 特征卡行距 |
| `--card-letter-spacing` | `0.5px` | 特征卡字间距 |
| `--gold-line-width` | `32px` | 金色分隔线宽度 |
| `--gold-line-height` | `1px` | 金色分隔线高度 |
| `--highlight-padding` | `24px` | 金句卡内边距 |
| `--highlight-quote` | `22px` | 金句字号 |
| `--footer-brand-color` | `#bbb` | 品牌名颜色 |
| `--footer-tagline-color` | `#aaa` | 品牌标语颜色 |
| `--footer-brand-size` | `11px` | 品牌名字号 |
| `--footer-tagline-size` | `11px` | 品牌标语字号 |
| `--subtitle-color` | `#1a1a2e` | 小标题颜色（如"场景一："） |

---

## 二、规范模板（唯一模板）

> 全篇 **only inline styles**，无 `<style>` 块。所有含中文的 section 和 p 必须加 `word-break:normal;white-space:normal;`。全篇 `padding` 左右统一为 **20px**（包括 header、body、footer），不混用 28px。

```html
<section style="padding:0;margin:0;background:#fff;word-break:normal;white-space:normal;">

  <!-- ① Banner image（800×400，深色渐变+星星装饰，无水印文字） -->
  <section style="width:100%;margin:0;padding:0;">
    <img src="{BANNER_URL}" style="width:100%;display:block;" />
  </section>

  <!-- ② Header -->
  <section style="padding:44px 20px 16px;text-align:center;word-break:normal;white-space:normal;">
    <p style="font-size:13px;color:#b8b8b8;letter-spacing:4px;margin:0 0 18px;font-weight:300;">E S S A Y</p>
    <p style="font-size:24px;font-weight:400;color:#1a1a2e;margin:0 0 8px;letter-spacing:2px;word-break:normal;white-space:normal;">{标题}</p>
    <p style="font-size:13px;color:#aaa;margin:0;">{YYYY · MM · DD}</p>
  </section>

  <!-- ③ Gold divider -->
  <section style="text-align:center;padding:6px 20px;">
    <span style="display:inline-block;width:32px;height:1px;background:#d4a574;"></span>
  </section>

  <!-- ④ Body paragraph group -->
  <section style="padding:8px 20px;word-break:normal;white-space:normal;">
    <p style="font-size:15px;line-height:2;color:#333;margin:0 0 24px;letter-spacing:1px;word-break:normal;white-space:normal;">{段落内容}</p>
    <!-- 更多 <p> 以此类推 -->
  </section>

  <!-- ⑤ Decorative divider image（可选） -->
  <section style="text-align:center;padding:8px 20px;">
    <img src="{DIVIDER_URL}" style="width:200px;display:inline-block;" />
  </section>

  <!-- ⑥ Feature card（金左框卡片，section 不嵌套） -->
  <section style="padding:4px 20px;word-break:normal;white-space:normal;">
    <div style="background:#f8f6f3;border-left:3px solid #d4a574;padding:16px 20px;margin:0 0 12px;">
      <p style="font-size:14px;color:#333;margin:0;line-height:1.9;letter-spacing:0.5px;word-break:normal;white-space:normal;">
        <span style="font-weight:500;color:#d4a574;">{卡片标题}</span><br/>{卡片正文，<br/>后不换行不留空白}
      </p>
    </div>
    <!-- 多个卡片并列时，最后一个用 margin:0 0 0px（消除底部空白） -->
    <div style="background:#f8f6f3;border-left:3px solid #d4a574;padding:16px 20px;margin:0 0 0px;">
      ...
    </div>
  </section>

  <!-- ⑦ Gold divider -->
  <section style="text-align:center;padding:12px 20px;">
    <span style="display:inline-block;width:32px;height:1px;background:#d4a574;"></span>
  </section>

  <!-- ⑧ Highlight card（金句卡） -->
  <section style="margin:16px 20px;padding:24px;background:#f8f6f3;text-align:center;word-break:normal;white-space:normal;">
    <p style="font-size:14px;color:#999;margin:0 0 10px;letter-spacing:2px;">毕竟——</p>
    <p style="font-size:22px;font-weight:400;color:#1a1a2e;margin:0;letter-spacing:3px;">{金句}</p>
  </section>

  <!-- ⑨ Footer -->
  <section style="padding:36px 20px 40px;text-align:center;">
    <p style="font-size:11px;color:#bbb;letter-spacing:2px;margin:0;">巡梦人</p>
    <p style="font-size:11px;color:#aaa;margin:8px 0 0;letter-spacing:1px;">从一颗星星开始，温暖整个宇宙</p>
  </section>

</section>
```

---

## 三、强调语法（Accent）

```html
<!-- 暖金色强调 -->
<span style="color:#d4a574;font-weight:500;">要强调的文字</span>

<!-- 深色小标题 -->
<span style="font-weight:500;color:#1a1a2e;">小标题文字</span>
```

---

## 四、图片区（配图嵌入）

```html
<section style="padding:8px 20px;word-break:normal;white-space:normal;">
  <img style="width:100%;border-radius:8px;display:block;" src="{图片URL}" />
</section>
```

- 图片 URL 必须是微信 CDN 地址（来自 `/cgi-bin/media/uploadimg`）
- 不加图注文字（如需标注来源，用极小的 `<p>` 在 img 下方）

---

## 五、发布前检查清单（必须执行）

### 5.1 移动端适配检查（先在手机上预览再提交）

微信编辑器（电脑版）渲染效果与手机终端不一致。**手机端是最终标准。**

#### 段落长度
- [ ] 每段正文不超过 **35 个中文字符**（在 15px / 375px 视口下约 2 行）
- [ ] 如果一段超过 35 字，拆成两段
- [ ] 特征卡内说明不超过 **20 个中文字符**，一行看完

#### 间距与呼吸
- [ ] 段落之间 `margin-bottom:24px` 已确保
- [ ] 图片上下 `padding:8px 20px` 已添加
- [ ] 分隔线上下 `padding:12px 20px` 统一（重要段落切换处可加至 20px）
- [ ] 特征卡相邻间距：首 N-1 张 `margin:0 0 12px`，最后一张 `margin:0 0 0px`

#### 视觉密度
- [ ] 连续正文段落不超过 3 段，中间插入图片/分隔线/特征卡做呼吸
- [ ] 四层的特征卡不堆在一起时，可中间插入一句过渡正文
- [ ] 金色强调 `color:#d4a574` 每 2-4 段一处，不连续使用

### 5.2 源码级检查（提交 API 前）

- [ ] 全篇 side padding 是否统一为 **20px**？（唯一的例外：header 的上下 padding 44px/16px）
- [ ] section 是否有不必要的**嵌套**？（每个金卡 divider 必须在同一层级）
- [ ] 所有含中文的 section 和 p 是否加了 `word-break:normal;white-space:normal;`？
- [ ] 是否有 `white-space:pre-wrap` 残留？
- [ ] `color:#ccc` 是否被误用？（应为 `#bbb` 品牌名）
- [ ] `color:#e0d5c8` 是否被误用？（应为 `#aaa` 标语）
- [ ] 所有 `<br/>` 后面是否**紧跟**正文文字（无空白行/缩进）？
- [ ] footer 颜色是否正确：品牌名 `#bbb`，标语 `#aaa`？
- [ ] digest 是否已设置？（非可选，必填，否则微信截取 HTML 源码）

### 5.3 API 提交流程

- [ ] 使用 **Python 脚本**提交 JSON，不要用 bash 拼接 json（避免中文编码问题）
- [ ] 封面图是否为 **1:1 方形**？若非方形，先用 sharp 裁剪
- [ ] 图片上传后，`src` 会被微信改为 `data-src`，`http://` 会被改为 `https://`——这是正常的
- [ ] 创建成功后**必须回读验证**（调用 draft/get）

### 5.4 内容检查

- [ ] 无"做梦""发呆""REM""DMN"等残余关键词
- [ ] 产品名/厂商名是否写对（如 Owner 非 Leader）
- [ ] 数字和事实是否有数据源归属
- [ ] digest 正文前 54 字不是 HTML 标签

---

## 六、黑名单（禁止行为）

| 禁止项 | 原因 | 替代方案 |
|--------|------|---------|
| `<style>` 块 | 微信编辑器会删除 | 全部用 inline style |
| flexbox / grid / position / animation | 微信不支持 | block / inline-block |
| `<script>` | 被删除 | — |
| `white-space: pre-wrap` | 中文断行异常 | 用 `<br/>` 手动换行 |
| 在已有草稿上做增量修补 | 微信编辑器会乱改 HTML | 每次从源码**全量重建**上传 |
| `node -e` 内联执行复杂脚本 | bash 解释 `${}` | 写 `.py` 或 `.js` 文件执行 |

---

## 七、图片生成提示词规范（配图）

参考锚定文章的配图提示词风格写：

```
卡通教学风格插画，横版构图，[画面场景总述]。[具体元素：颜色、位置、表情、动作]。[氛围描述]。[不要出现文字乱码]。
```

写提示词时遵循的原则（来自锚定文章修正的教训）：
1. 写 **"发生了什么事"**，不是 **"有什么东西摆在什么坐标"**
2. 风格词统一：卡通教学风格、横版/竖版、构图方式
3. 描述颜色用感性词（暖金色、深蓝色）而非色值
4. 描述关系用"一个在...一个在..."而非坐标
5. 三张配图各自服务文章的不同段落，不是同一张图的三个版本

---

## 八、版本记录

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-05-24 | v3 更新 | 新增 5.1 移动端适配检查，修复 5.2/5.3 编号，修正特征卡间距规则 |
| 2026-05-24 | v2 创建 | 合并 templates.md / components.md / formatting-lessons.md |



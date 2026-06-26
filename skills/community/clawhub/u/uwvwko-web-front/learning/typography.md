# 字体排版规范

## 字体大小比例

常用比例：1.25（Major Second）和 1.333（Perfect Fourth）

### 比例 1.25
```
xs:   12px  (0.75rem)
sm:   14px  (0.875rem)
base: 16px  (1rem)
lg:   20px  (1.25rem)
xl:   25px  (1.563rem)
2xl:  31px  (1.953rem)
3xl:  39px  (2.441rem)
4xl:  49px  (3.052rem)
```

### 比例 1.333
```
xs:   12px
sm:   14px
base: 16px
lg:   21px  (1.333rem)
xl:   28px  (1.777rem)
2xl:  38px  (2.369rem)
3xl:  50px  (3.157rem)
4xl:  67px  (4.209rem)
```

## 行高规范

| 场景 | 行高 | 示例 |
|------|------|------|
| 正文 | 1.5-1.75 | 段落文字 |
| 标题 | 1.2-1.3 | 大标题 |
| 短文 | 1.3-1.5 | 按钮文字 |
| 诗歌 | 2.0 | 特殊排版 |

## 字重选择

- 300: 细体，用于装饰性文字
- 400: 正常，默认字体
- 500: 中等，强调重要内容
- 600: 半粗，小标题
- 700: 粗体，大标题
- 800-900: 特粗，特殊效果

## 字体族

### 中文字体
```css
font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
```

### 英文字体
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### 等宽字体
```css
font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, Consolas, monospace;
```

## 标题层次

```css
h1 {
  font-size: 2.5rem;   /* 40px */
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
}

h2 {
  font-size: 2rem;      /* 32px */
  font-weight: 600;
  line-height: 1.25;
  margin-bottom: 20px;
}

h3 {
  font-size: 1.5rem;    /* 24px */
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 16px;
}

h4 {
  font-size: 1.25rem;   /* 20px */
  font-weight: 500;
  margin-bottom: 12px;
}
```

## 移动端字体

```css
/* 移动端适当缩小 */
@media (max-width: 639px) {
  h1 { font-size: 2rem; }
  h2 { font-size: 1.5rem; }
  h3 { font-size: 1.25rem; }
  body { font-size: 15px; }
}
```

## 中英文混排

- 中英文之间加空格
- 英文和数字与中文混排时可用全角
- 避免在中文中夹用英文字体

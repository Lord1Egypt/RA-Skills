# IMG-2 Only PPT 视觉生产标准 v1

## 最高规则

正式 PPT 主体视觉必须使用 Image2 / IMG-2 链路生成。

允许链路：

- `skills/happy-img2-direct`
- provider/model：`happy/gpt-image-2`

## 禁止

以下产物不得作为正式 PPT 主体视觉：

- PIL / Python / canvas 程序绘图；
- SVG / 矢量图 / 几何图拼装；
- matplotlib / cairo / html / css 截图；
- 旧图贴片、补丁、遮挡、局部擦改；
- 用矢量元素、图标、线框、卡片拼出来冒充生图；
- 没有 IMG-2 证据的“生成图”。

## 必须保留的证据

每张正式页面主体视觉必须有：

- request JSON；
- result JSON；
- state JSON；
- run stdout / 日志；
- prompt；
- 输出 PNG；
- 明确记录 provider/model = `happy/gpt-image-2`；
- 明确记录使用 `skills/happy-img2-direct` 或等价 IMG-2 技能链路。

## 验收门禁

如果产物目录中出现：

- `mode: programmatic...`
- `PIL`
- `generate_*.py` 用于绘制页面；
- `svg/vector/canvas/html/css` 生成主体视觉；
- 没有 `happy/gpt-image-2` 证据；

则该页自动判定为：

```text
REJECTED_NOT_IMG2
```

不得进入后期 Logo/页脚/页码添加，不得发给用户确认。

## 例外

程序脚本只允许用于：

- PPT 组装；
- 后期添加 Logo / 页脚 / 页码；
- 渲染预览；
- 压缩、打包、校验；
- 标注审核图。

程序脚本不得用于生成正式页面主体视觉。

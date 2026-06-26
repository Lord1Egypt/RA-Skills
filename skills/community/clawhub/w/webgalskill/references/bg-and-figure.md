# 背景与立绘

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 切换背景 | `changeBg:图片名.jpg;` | 切换背景 |
| 切换立绘 | `changeFigure:图片名.png;` | 切换中间立绘 |
| 位置参数 | `-left` / 无 / `-right` | 左 / 中 / 右 位置 |
| 带ID立绘 | `changeFigure:图片.png -id=xxx;` | 自由位置立绘 |
| 小头像 | `miniAvatar:图片.png;` | 显示小头像 |
| 解锁CG | `unlockCg:图片.jpeg -name=名称 -series=1;` | 解锁CG鉴赏 |
| 变换效果 | `setTransform:{json} -target=目标;` | 为已有立绘设置效果 |

## 资源文件位置

- 背景图片：`background/` 文件夹
- 立绘图片：`figure/` 文件夹

## 切换背景

```ws
changeBg:testBG03.jpg;  // 切换背景
changeBg:none;          // 关闭背景
```

## 切换立绘

```ws
changeFigure:testFigure02.png; // 切换中间立绘
changeFigure:none;              // 关闭立绘
```

使用 `-next` 可在替换后立刻执行下一条语句：

```ws
changeBg:testBG03.jpg -next;
changeFigure:testFigure02.png -next;
一色:谢谢学姐！;
```

## 立绘位置

三个位置：左 (`-left`)、中 (无参数)、右 (`-right`)。

```ws
changeFigure:testFigure03.png -left;    // 左侧
changeFigure:testFigure04.png;           // 中间
changeFigure:testFigure03.png -right;    // 右侧
```

清除各位置立绘需分别设置：

```ws
changeFigure:none -left;
changeFigure:none;
changeFigure:none -right;
```

## 带ID的自由立绘

使用 `-id` 指定立绘 ID，可实现超过3个立绘或精确控制：

```ws
changeFigure:testFigure03.png -left -id=test1; // 初始位置在左侧
changeFigure:none -id=test1;                    // 通过ID关闭立绘
```

> 重设带ID立绘位置时，需先关闭再重新打开。

## 小头像

显示在文本框左下角：

```ws
miniAvatar:minipic_test.png; // 显示小头像
miniAvatar:none;             // 关闭小头像
```

## 解锁CG

```ws
unlockCg:xgmain.jpeg -name=星光咖啡馆与死神之蝶 -series=1;
```

| 参数 | 必填 | 说明 |
| :--- | :--- | :--- |
| `-name` | 是 | CG鉴赏中显示的名称 |
| `-series` | 否 | 系列编号，同系列CG合并展示 |

## 立绘变换效果

### 设置立绘时附加效果

```ws
changeFigure:stand.png -transform={"alpha":1,"position":{"x":0,"y":500},"scale":{"x":1,"y":1},"rotation":0} -next;
```

### 为已有立绘设置效果

```ws
setTransform:{"position":{"x":100,"y":0}} -target=fig-center -duration=0;
```

> 效果字段说明详见 [动画](animation.md)

**Target 目标：**

| target | 说明 |
| :--- | :--- |
| `fig-left` | 左立绘 |
| `fig-center` | 中间立绘 |
| `fig-right` | 右立绘 |
| `bg-main` | 背景 |
| 自定义id | 带 `-id` 的立绘 |

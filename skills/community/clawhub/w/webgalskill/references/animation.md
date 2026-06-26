# 动画效果

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 播放动画 | `setAnimation:动画名 -target=目标;` | 为背景/立绘播放动画 |
| 设置进出场 | `setTransition:-target=目标 -enter=进动画 -exit=出场动画;` | 自定义进出场 |
| 自定义动画 | JSON文件 | 在 `game/animation/` 创建 |

## 预制动画

```ws
setAnimation:enter-from-bottom -target=fig-center -next;
```

### 动画列表

| 动画效果 | 动画名 | 持续时间 |
| :--- | :--- | :--- |
| 渐入 | `enter` | 300ms |
| 渐出 | `exit` | 300ms |
| 左右摇晃一次 | `shake` | 1000ms |
| 从下侧进入 | `enter-from-bottom` | 500ms |
| 从左侧进入 | `enter-from-left` | 500ms |
| 从右侧进入 | `enter-from-right` | 500ms |
| 前后移动一次 | `move-front-and-back` | 1000ms |

### Target 目标

| target | 说明 |
| :--- | :--- |
| `fig-left` | 左立绘 |
| `fig-center` | 中间立绘 |
| `fig-right` | 右立绘 |
| `bg-main` | 背景 |
| 自定义 `-id` | 带ID的立绘 |

## 自定义动画

动画文件存放在 `game/animation/`，使用 JSON 格式描述**动画序列**。

### JSON 结构

```json
[
  {
    "alpha": 0,
    "scale": {"x": 1, "y": 1},
    "position": {"x": -50, "y": 0},
    "rotation": 0,
    "blur": 5,
    "duration": 0
  },
  {
    "alpha": 1,
    "scale": {"x": 1, "y": 1},
    "position": {"x": 0, "y": 0},
    "rotation": 0,
    "blur": 0,
    "duration": 500
  }
]
```

### 帧属性说明

| 属性 | 说明 | 值范围 |
| :--- | :--- | :--- |
| `alpha` | 透明度 | 0-1 |
| `scale` | 缩放 | {x, y} |
| `position` | 位置偏移 | {x, y} |
| `rotation` | 旋转角度 | 弧度 |
| `blur` | 高斯模糊半径 | 数值 |
| `brightness` | 亮度 | 数值 |
| `contrast` | 对比度 | 数值 |
| `saturation` | 饱和度 | 数值 |
| `gamma` | 伽马值 | 数值 |
| `colorRed` | 红色分量 | 0-255 |
| `colorGreen` | 绿色分量 | 0-255 |
| `colorBlue` | 蓝色分量 | 0-255 |
| `duration` | 本帧持续时间 | 毫秒 |
| `oldFilm` | 老电影效果 | 0/1 |
| `dotFilm` | 点状电影效果 | 0/1 |
| `reflectionFilm` | 反射电影效果 | 0/1 |
| `glitchFilm` | 故障电影效果 | 0/1 |
| `rgbFilm` | RGB电影效果 | 0/1 |
| `godrayFilm` | 光辉效果 | 0/1 |

### 注册自定义动画

在 `animationTable.json` 中添加文件名（不含后缀）：

```json
["enter-from-left","enter-from-bottom","enter-from-right","myCustomAnimation"]
```

### 省略属性

不参与动画的属性可留空保持默认：

```json
[
  {"alpha": 0, "duration": 0},
  {"alpha": 1, "duration": 300}
]
```

### 变换（0毫秒动画）

持续时间为0且只有一个时间片的动画即变换：

```json
[{"alpha": 0, "duration": 0}]
```

## 设置进出场效果

覆盖 WebGAL 默认的渐变进出场效果。

**注意：**
- 设置进出场效果的语句必须**紧随**设置立绘/背景的语句**连续执行**
- 效果写在设置代码**之后**

```ws
changeFigure:test.png;
setTransition: -target=fig-center -enter=enter-from-bottom -exit=exit;
```

| 参数 | 说明 |
| :--- | :--- |
| `-target` | 作用目标 |
| `-enter` | 进场动画名 |
| `-exit` | 出场动画名 |

> 进场效果在立绘/背景设置后立即设置可覆盖默认动画。<br>
> 出场效果可在图像出场时正确应用。

# 基础

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 注释 | `; 注释内容` | 单行注释 |
| `none` | `指令:none;` | 关闭对象（背景/立绘/BGM等） |
| `-next` | `指令:值 -next;` | 执行完本句立刻执行下一句 |
| `-concat` | `对话 -concat;` | 本句连接在上一句对话之后 |
| `-notend` | `对话 -notend;` | 本句对话未结束，可插入演出 |

## 注释

WebGAL 脚本只会解析每一行的分号前的内容，分号后的内容视为注释。

```ws
WebGAL:你好！; 分号后的内容会被视作注释
; 可以直接输入一个分号，然后写一条单行注释
```

## `none` 关键词

在设置资源时，设为 `none` 可关闭该对象：

```ws
changeBg:none;     // 关闭背景
changeFigure:none; // 关闭立绘
bgm:none;          // 停止背景音乐
```

## `-next` 参数

执行完本句后**立刻**执行下一句，用于同时触发多个动作。

```ws
changeBg:testBG03.jpg -next;
changeFigure:testFigure02.png -next;
一色:谢谢学姐！;
```

## `-notend` 和 `-concat` 参数

在对话进行中插入演出效果：

| 参数 | 作用 |
| :--- | :--- |
| `-concat` | 本句连接在上一句对话之后 |
| `-notend` | 本句对话未结束，可连接演出或对话 |

**示例：对话中切换立绘**

```ws
WebGAL:测试语句插演出！马上切换立绘...... -notend;
changeFigure:k1.png -next;
切换立绘！马上切换表情...... -notend -concat;
changeFigure:k2.png -next;
切换表情！ -concat;
```

**仅使用 `-concat`：**

```ws
这是第一句......;
用户点击鼠标后才会转到第二句 -concat;
```

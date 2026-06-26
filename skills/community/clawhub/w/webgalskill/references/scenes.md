# 场景与分支

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 场景跳转 | `changeScene:文件名.txt;` | 切换到另一场景 |
| 场景调用 | `callScene:文件名.txt;` | 调用场景后返回 |
| 分支选择 | `choose:选项1:文件1.txt\|选项2:文件2.txt;` | 用户选择分支 |
| 条件选择 | `choose:(显示条件)[启用条件]->选项:文件;` | 条件分支 |
| 创建标签 | `label:标签名;` | 在当前位置创建标签 |
| 跳转到标签 | `jumpLabel:标签名;` | 跳转到指定标签 |

## 警告

> 跳转场景、分支选择或调用场景后，**舞台不会自动清除**。背景音乐、立绘、背景等效果会被继承到下一场景。

## 场景跳转

```ws
changeScene:Chapter-2.txt;
```

跳转后，当前场景的 BGM、立绘、背景等效果会保留到新场景。

## 场景调用

`callScene` 执行完毕后**返回原场景继续执行**。

```ws
callScene:Chapter-2.txt;
// Chapter-2.txt 执行完毕后，继续执行这里
```

## 分支选择

```ws
choose:叫住她:Chapter-2.txt|回家:Chapter-3.txt;
```

选项之间用 `|` 分隔，格式：`显示文本:目标文件`

### 条件展示和选择

```ws
choose:(showConditionVar>1)[enableConditionVar>2]->叫住她:Chapter-2.txt|回家:Chapter-3.txt;
```

| 条件类型 | 语法 | 说明 |
| :--- | :--- | :--- |
| 显示条件 | `(条件)` | 条件为真时才显示选项 |
| 启用条件 | `[条件]` | 条件为真时才允许点击 |

## 标签跳转

在同一文件内实现分支跳转，避免创建过多 TXT 文件。

> 警告：TXT 行数不宜过长，否则可能导致加载慢、响应迟钝。

### 基本语法

```ws
jumpLabel:label_1; // 跳转到 label_1
......
label:label_1;     // 创建名为 label_1 的标签
```

`jumpLabel` 相当于 `goto`，`label` 是跳转的目标点。

### 分支示例

```ws
choose:分支 1:label_1|分支 2:label_2;
label:label_1;
// 分支1的内容
......
jumpLabel:end;
label:label_2;
// 分支2的内容
......
jumpLabel:end;
label:end;
// 汇合点
```

### 常见错误

每个分支结尾必须用 `jumpLabel` 跳转，否则程序会继续执行下一个分支：

```ws
// 错误示例
choose:分支 1:label_1|分支 2:label_2;
label:label_1;
// 分支1内容
// 如果没有 jumpLabel，会继续执行分支2！
label:label_2;
// 分支2内容
```

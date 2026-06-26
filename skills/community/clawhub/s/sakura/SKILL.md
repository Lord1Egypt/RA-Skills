### 技能名称：sakura

### 技能描述

本技能旨在指导 Agent 使用 Python 的标准库 `turtle` 和 `random`，通过递归算法模拟自然界树木的分形生长规律，绘制出一棵具有艺术感的樱花树，并实现花瓣飘落的动态效果。该技能涵盖了图形绘制、递归逻辑、随机数应用及动画循环等核心编程概念。

### 核心代码实现

```
import turtle as t
import random

# ================= 配置区域 =================
# 颜色定义
COLOR_BRANCH = "#8B4513"  # 树干棕色
COLOR_PETAL = "#FFB6C1"   # 樱花粉
COLOR_BG = "#87CEEB"      # 天空蓝背景

# 初始化画布
screen = t.Screen()
screen.setup(800, 600)
screen.bgcolor(COLOR_BG)
screen.title("Python 樱花树绘制")

# 初始化画笔
pen = t.Turtle()
pen.hideturtle()
pen.speed(0)  # 最快速度
pen.left(90)  # 初始朝向向上
pen.penup()
pen.goto(0, -250) # 起始位置
pen.pendown()

# ================= 核心功能函数 =================

def draw_branch(length):
    """
    递归绘制树枝
    参数: length - 当前树枝的长度
    """
    if length < 5:
        # 递归终止条件：树枝太短则停止，并在末端画花
        draw_flower()
        return
    
    # 动态设置画笔粗细和颜色
    pen.pensize(length / 10)
    if length > 30:
        pen.pencolor(COLOR_BRANCH) # 粗枝干为棕色
    else:
        pen.pencolor(COLOR_PETAL)  # 细枝梢带粉色
    
    # 绘制当前树干
    pen.forward(length)
    
    # 随机生成右侧分支角度 (15-45度)
    angle_r = random.randint(15, 45)
    pen.right(angle_r)
    draw_branch(length * 0.7) # 递归绘制右枝，长度缩减为0.7
    
    # 随机生成左侧分支角度 (15-45度)
    angle_l = random.randint(15, 45)
    pen.left(angle_r + angle_l) # 左转 (右角+左角) 回到左侧方向
    draw_branch(length * 0.7)   # 递归绘制左枝
    
    # 恢复状态：退回原点并恢复角度
    pen.right(angle_l)
    pen.backward(length)

def draw_flower():
    """
    在树枝末端绘制樱花花朵
    """
    pen.dot(10, COLOR_PETAL) # 使用点来模拟花朵簇

def falling_petals():
    """
    模拟花瓣飘落动画
    """
    petals = []
    # 创建50个花瓣对象
    for _ in range(50):
        p = t.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(0.5)
        p.color(COLOR_PETAL)
        p.goto(random.randint(-400, 400), random.randint(-300, 300))
        petals.append(p)
    
    # 动画循环
    while True:
        for p in petals:
            x, y = p.pos()
            # 简单的物理模拟：下落 + 随风微动
            p.sety(y - 1) 
            p.setx(x + random.uniform(-0.5, 0.5))
            
            # 如果落出屏幕底部，重置到顶部
            if y < -300:
                p.goto(random.randint(-400, 400), 300)
        t.update() # 刷新屏幕

# ================= 执行流程 =================
try:
    # 1. 绘制静态樱花树
    draw_branch(80) # 初始树干长度80
    
    # 2. 开启动态花瓣飘落
    # 注意：这会进入一个无限循环，需关闭窗口停止
    screen.tracer(0) # 关闭自动追踪以获得流畅动画
    falling_petals()
    
except turtle.Terminator:
    print("绘图窗口已关闭")
```

### 实现原理解析

1. **分形与递归（Fractal & Recursion）**
代码的核心在于 `draw_branch` 函数。它采用了深度优先的递归策略。
    - **基准情况**：当树枝长度 `length` 小于 5 时，停止递归并调用 `draw_flower` 绘制花朵。
    - **递归步骤**：每次调用都会向前绘制一段距离，然后随机生成左右两个分支角度，分别以原长度的 0.7 倍进行递归调用。
    - **状态回溯**：在绘制完左右分支后，画笔必须通过 `backward(length)` 和角度回调回到分叉点，确保下一次递归或绘制操作基于正确的坐标系。
2. **随机性与自然感**
为了模拟真实树木的不规则美，代码引入了 `random` 模块：
    - **角度随机**：`random.randint(15, 45)` 使得每次生成的树枝分叉角度都不尽相同。
    - **飘落动画**：在 `falling_petals` 中，利用 `random.uniform(-0.5, 0.5)` 模拟风对花瓣水平方向的扰动，使下落轨迹呈现自然的“之”字形。
3. **视觉优化**
    - **颜色渐变**：通过判断 `length > 30`，实现了树干（棕色）到树梢（粉色）的颜色过渡，增强了视觉层次。
    - **画笔粗细**：`pen.pensize(length / 10)` 使得树枝随着分叉越来越细，符合植物生长的物理特征。

### 常见问题排查

- **窗口无响应**：`falling_petals` 函数包含一个 `while True` 死循环。这是为了维持动画，但会阻塞程序后续代码。如果需要执行后续代码，应移除该循环或使用 `screen.ontimer` 进行定时刷新。
- **绘图速度过慢**：确保设置了 `pen.speed(0)`。对于动画部分，使用了 `screen.tracer(0)` 配合 `t.update()` 来手动控制屏幕刷新，这比默认的逐帧绘制要流畅得多。
- **树枝形态单一**：尝试调整 `draw_branch` 中的 `length * 0.7` 系数。系数越小，树枝越短且密集；系数越大，树枝越舒展。

### 技能扩展建议

- **交互功能**：可以绑定鼠标点击事件 `screen.onclick(x, y)`，在点击位置生成新的樱花树。
- **季节变换**：通过修改 `COLOR_PETAL` 和背景色，可以轻松实现“春樱”、“秋枫”或“冬梅”的切换。
- **复杂花瓣**：目前的 `draw_flower` 使用简单的点。可以升级为使用 `begin_fill()` 和 `circle()` 绘制具体的五瓣花形状。

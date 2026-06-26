# 单图生视频模式

## 说明

基于单张分镜图生成视频，是最常用的模式。

## 输入

- 单张分镜图（作为首帧）
- 文本提示词（描述期望的动态）

## 要求

1. **基于静态画面推演合理的动态过程**
2. **Visual 中区分图中可见元素和推演的动态**
3. **Keyframes 标注推演的状态变化**
4. **推演内容符合物理规律和画面风格**
5. **Transition 预设入镜和出镜状态**

## 提示词结构

```
[首帧画面描述] + [期望的动态推演]

示例:
A medium shot of a young man sitting by a window. 
Based on this static image: the man slowly turns his head to look out the window. 
Sunlight shifts subtly across his face. 
A gentle breeze moves the curtains. 
Camera remains static. Natural, slow motion.
```

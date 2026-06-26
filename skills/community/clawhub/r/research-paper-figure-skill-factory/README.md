# 论文制图 Skill 工厂

`research-paper-figure-skill-factory` 用来为论文作图任务创建专门的制图 skill。它不是只帮你画一张图，而是先根据某一类论文图的特点，生成一个可反复使用的“专项制图助手”，再用这个助手服务后续不同论文的 diagram / figure 制作。

## 设计目的

不同论文图有不同的表达目标：方法框架图、机制解释图、流程图、案例示意图、taxonomy 图、结果总结图、失败分析图等，都需要不同的判断方式、候选方案、视觉风格和修改标准。

这个 skill 的目的，是把“某一类论文图应该如何设计”沉淀成一个可复用的制图 skill，让后续作图不再每次从零开始。

## 它主要做什么

- 明确你想生成哪一类论文制图 skill。
- 收集或整理相关论文、图例和参考材料。
- 总结这一类图常见的表达目的、结构方式和视觉风格。
- 生成一个面向该图类的专项制图 skill。
- 检查这个专项 skill 是否能按步骤引导用户作图。
- 确保专项 skill 会先给多个方案，再生成多张候选图供选择。
- 帮助把专项 skill 打包成可放入 ChatGPT Sources 或 Codex skills 中使用的 zip。

## 适合用在什么时候

- 你想为某一类论文图建立长期可复用的制图流程。
- 你不只是想画一张图，而是想生成一个之后能反复使用的作图助手。
- 你希望作图过程更稳定：先分析图的目的，再给方案，再出候选图，再修改。
- 你希望后续给不同论文画同类 diagram 时，有统一的步骤和质量标准。

## 简单使用方式

你可以这样提出需求：

```text
请使用 research-paper-figure-skill-factory，生成一个用于论文 method framework diagram 的制图 skill。
```

或者：

```text
请使用 research-paper-figure-skill-factory，基于我项目里的论文 PDF，生成一个专门用于论文 diagram 制作的 skill。
```

生成完成后，你会得到一个新的专项制图 skill zip。之后把这个 zip 放入 ChatGPT Sources，或安装到 Codex skills 中，就可以用它为具体论文绘制 diagram。

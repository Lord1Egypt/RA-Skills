# 输出文件名规则

## 默认规则

最终输出的 `.pptx` 文件名默认使用**目标论文标题**生成。

优先级：
1. 用户明确指定的文件名
2. 论文英文标题
3. 论文中文标题
4. 若标题缺失，再退回安全的临时名

## 清洗规则

文件名需要做文件系统安全清洗：
- 去掉或替换路径分隔符、冒号、问号、引号等非法字符
- 合并多余空格
- 避免只输出 `output.pptx`、`final.pptx`、`report.pptx` 这类泛化名

## 推荐做法

### 英文标题
保留英文单词和空格，必要时可替换为下划线或短横线。

示例：
- `Fingolimod ameliorates amyloid deposition and neurodegeneration in APP_PS1 mouse model of Alzheimer's disease.pptx`
- `Fingolimod-ameliorates-amyloid-deposition-and-neurodegeneration-in-APP_PS1-mouse-model-of-Alzheimers-disease.pptx`

### 中文标题
若用户明确要求中文文件名，可直接使用中文标题，但仍要做非法字符清洗。

示例：
- `芬戈莫德改善APP_PS1阿尔茨海默病小鼠的淀粉样沉积与神经退行性变.pptx`

## 交付要求

向用户汇报结果时，应直接给出最终生成的文件路径，并确保该路径中的文件名与论文标题对应。

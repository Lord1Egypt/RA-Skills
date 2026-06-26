# 文章内容模板

## JSON示例
```
{
  "steps": [
    {
      "stepNumber": 1,
      "description": "测试1",
      "images-paths": [
        "imgs/1-1.jpeg",
        "imgs/1-2.jpg"
      ]
    },
    {
      "stepNumber": 2,
      "description": "测试2",
      "images-paths": [
        "imgs/2-1.png"
      ]
    }
  ]
}
```

## 正文操作
### 正文第一句

**内容**： 大家好！我是{{./assets/personal-info.txt:昵称}}

### 正文第一段（摘要）
**作用**：200字左右，写明这篇文章是在介绍什么，解决什么问题。语言风格尽量活泼，不要过于冷漠，偶尔可以包含emoji。

### 头图
**来源**：{{../files/[yyyy-MM-ddTHH:mm:ss]/imgs/cover-img.png}}。

### 步骤简介
**作用**：将教程的所有步骤罗列出来。
**注意**：使用无序项目符号，不要使用有序项目符号。
**例如**：

- 创建智能体
- 编辑Json文件
- 创建群组
- 将机器人加入群组

### 步骤详解
**作用**：步骤详解需要对每个步骤进行详细解释，每个步骤配至少一张图(严格遵循json文件中的字段值)。
**用法**：先填槽，再组织成丰富的语言表达。

**填槽**：
{{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[0].stepNumber}}. {{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[0].description}}
{{你需要在这里对该步骤进行介绍}}
{{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[0].images-paths[0]}}
{{通过模型多模态能力解读图片并作出解释}}
{{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[0].images-paths[1]}}
{{通过模型多模态能力解读图片并作出解释}}

{{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[1].stepNumber}}. {{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[1].description}}
{{你需要在这里对该步骤进行介绍}}
{{../files/[yyyy-MM-ddTHH:mm:ss]/steps.json.steps[1].images-paths[0]}}
{{通过模型多模态能力解读图片并作出解释}}

**结果举例**(以下图片仅作展示用，无实际含义)：

1. 下载OpenCode
    OpenCode是一款开源TUI工具，用于在终端中进行大模型相关的操作，官方下载地址为 https://github.com/OpenClaw/OpenCode 。

  ![1-1](../files/2026-03-20T21-58-48/imgs/1-1.png)

  ![1-2](../files/2026-03-20T21-58-48/imgs/1-2.png)

2. 安装OpenCode
OpenCode的安装过程比较简单，只需要在终端中执行以下命令即可：
```
pip install opencode
```
![2-1](../files/2026-03-20T21-58-48/imgs/2-1.png)


### 总结
**内容**：对文章主要技术进行总结，分析指出该技术的特点。

### 结尾
**作用**：本人介绍及二维码展示。

**布局**：文本和二维码图片均在页面居中显示，文本在上，图片在下。

**样式：** 结尾内容最上方添加一条水平线，与“总结”部分隔开。

**内容：**
关于作者

{{./assets/personal-info.txt:个人简介}}
欢迎添加个人好友（标明来源，否则不通过）。
![wechat_qrcode_example](/Users/admin/.openclaw/workspace-my-media-edit/skills/wechat-tutorial-editor-publisher/assets/personal-imgs/wechat_qrcode_example.jpg)

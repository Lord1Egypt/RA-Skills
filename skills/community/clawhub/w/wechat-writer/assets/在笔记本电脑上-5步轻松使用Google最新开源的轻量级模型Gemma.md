# 在笔记本电脑上，5步轻松使用Google最新开源的轻量级模型Gemma

原文链接：https://mp.weixin.qq.com/s/J0l7BpjRdQp38SavJrtADQ?token=1267526467&lang=zh_CN

Gemma 是谷歌最新发布的轻量级模型，有 2B 和 7B 两个权重规模。与谷歌规模最大、能力最强的 Gemini 模型相比，Gemma 采用了相同的技术和架构，在同等规模的模型中性能领先，而且可以在普通的笔记本电脑或台式机上运行。

周末，我试了一下，用 Ollama 通过简单几个步骤，就可以在本机轻松玩转 Gemma。更好的是，有了 Ollama，还能下载和使用更多代码生成、文生图等轻量级模型。

## 第1步 下载安装 Ollama

首先，访问 Ollama 官网（https://ollama.com/）。在 Mac 上安装尤为简单，直接下载和运行软件包即可。

## 第2步 下载和运行 Gemma 模型

在终端输入命令：

```bash
ollma pull gemma
```

即可下载 Gemma 7B 模型，大约 5.2GB，需要一些时间。

下载完毕后，输入命令：

```bash
ollama run gemma
```

就可以和模型交互了。比如，我让 Gemma 把本文的第一段翻译为英文，Gemma 的响应速度很快，译文比较直接：

> Sure, here is the translation:
> Gemma is Google's latest lightweight model, available in two weight scales of 2B and 7B. Compared to Google's largest and most capable Gemini model, Gemma utilizes the same technology and architecture, delivering superior performance in models of comparable size, and can run smoothly on common laptops or desktops.

这么看，随身带一个大语言模型，作为翻译工具，还是很有用的。我的笔记本电脑是 MacBook Pro，16GB 内存，Gemma 7B 模型推理回答的速度还不错。如果有更大的内存，比如 32GB 或 48GB，那么体验会更好。

## 第3步 使用更多模型

作为一个通用的大语言模型，Gemma 在回答一些技术问题时，就有点力不从心了。比如，我问了这个问题：“Mysql 使用哪种 Web 管理工具比较好？”Gemma 明显不太自信，给出的回答是：

我无法提供有关 MySQL 的 Web 管理工具建议，因为我是一个大型语言模型，并不具备特定数据库管理工具的推荐功能。但是，我可以提供一些与 MySQL 相相关的资源，帮助您选择合适的工具：

**推荐资源：**

- https://dev.mysql.com/downloads/mysql-shell/
- https://www.mysql.com/products/workbench/

**选择管理工具时，考虑以下因素：**

- 功能：所需的管理功能，例如数据备份、用户管理和性能分析
- 价格：您的预算和使用成本
- 用户界面：操作简单和易用的界面
- 平台：您使用的操作系统和设备
- 性能：与您的系统性能相匹配

如何才能得到更好的回答呢？我决定下载一个出色的代码模型：DeepSeek-Coder。在终端上直接输入：

```bash
ollama run deepseek-coder:6.7b
```

就会自动下载和运行。目前在 Ollama 上，DeepSeek-Coder 模型有 3 种权重规模：1.3B，6.7B 和 33B。我选择的是 6.7B。针对上一个问题，它给出如下回答。

在 MySQL 数据库的管理上，有许多优秀的 web 管理工具可以选择。这些工具都提供了友好的用户界面和强大的功能来帮助你管理你的数据库：

1. phpMyAdmin：这是一个开源的数据库管理工具，它是基于 PHP 和 MySQL 编写的。它的优点在于简单易用，不需要特殊的知识或技能就可以使用。phpMyAdmin 支持所有主要的 SQL 数据类型，并提供了高级导出/导入功能、查询优化器以及完整的权限系统等。
2. Adminer：另一个开源工具，Adminer 是一个数据库管理工具，它支持多种数据库服务器，包括 MySQL。它的优点在于轻量级和易于使用，但功能可能不及 phpMyAdmin 或其他更专业的工具。
3. Navicat for MySQL：这是一款专业的数据库管理软件，提供了全面的 MySQL 管理解决方案。它支持各种复杂操作、强大的查询编辑器、备份/恢复等高级功能。但是要注意的是，它的价格不便宜，对于免费使用可能不太划算。
4. DBeaver：这是一个开源工具，是一个数据库管理工具和 SQL 客户端程序，支持所有主要的数据库系统，包括 MySQL。DBeaver 具有许多有用的特性，如代码编辑器、可视化查询规划器等。
5. MySQL Workbench：这个工具是官方的 MySQL 产品，提供了一个完整的解决方案用于管理服务器和数据库。它支持所有的主要功能，包括 DDL、DML、存储过程、触发器、视图、分区表等等。但是请注意，Workbench 可能比其他选项更重一些。

选择哪个工具取决于你的具体需求，例如你是否需要高级的导入/导出能力，或者你对 SQL 查询的控制级别如何。如果你只需要基本的数据库管理功能，那么任何一个免费且简单易用的工具都可以满足你的需求。如果你的需求更复杂一些，可能会选择 Navicat 或 MySQL Workbench 这样的专业工具。

这个回答还是比较准确的。我认为这种获取信息的方式，优于使用搜索引擎。尤其是，没有广告的困扰 :-) 当然，与使用搜索引擎一样，我们都需要自行分辨回答信息的准确度。

目前，Ollama 上还提供了更多模型，包括 mixtral、多模态的 llava，微软的 Phi-2、阿里巴巴的通义千问 Qwen 等。在官网上可以查阅和下载：https://ollama.com/library

## 第4步 想用 Web 界面怎么办？

如果不习惯在终端上，以 Ollama 命令行方式使用大模型的问答功能，那么可以选择使用 Web 界面。一个好的选择是 Open WebUI，即原来的 Ollama WebUI。使用 Docker 安装非常容易：

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

然后，浏览器打开 http://localhost:3000，就可以使用了。比如，我在页面上输入了问题：“如何在 Docker 运行 MySQL，并且导入 SQL 文件”。之前下载的代码模型 Deepseek-Coder 6.7B，给出了很好的回答。

## 第5步 如何集成到自己的应用里？

Open WebUI 实际上是调用 Ollama 的 API（http://127.0.0.1:11434/），只要安装了 Ollama，那么就能打开这个 API 网址。

目前 Ollama 提供了 Python 和 JS 组件，这样就可以在自己的 Python 或 JS 应用中，集成 Ollama 所提供的大模型能力了。比如在 JS 中，只需要如下几行代码，就可以用 llama2 模型回答问题：

```js
import ollama from 'ollama'

const response = await ollama.chat({
  model: 'llama2',
  messages: [{ role: 'user', content: 'Why is the sky blue?' }],
})

console.log(response.message.content)
```

到目前为止，我们借助 Ollama 工具，可以把各种最新的模型装在自己的笔记本电脑里。即使没有网络，也可以使用。未来，我会分享一些更复杂的场景和更有趣的玩法。

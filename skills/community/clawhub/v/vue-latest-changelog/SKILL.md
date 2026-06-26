---
name: vue-latest-changelog
description: 当用户要求查看和整理最新的Vue版本更新信息时，请遵循此规范获取相关内容。
compatibility: 需在Node.js环境下使用
license: MIT
---

## 获取最新版本信息
本技能旨在帮助您便捷获取Vue最新版本的更新日志。具体操作步骤如下：

1. **定位脚本文件**：在项目的 `scripts` 目录中，存在一个名为 `changelog.js` 的文件。此脚本负责从Vue的GitHub仓库获取最新版本的更新信息。

2. **执行脚本**：打开命令行工具，导航至包含 `scripts` 目录的项目根路径。在命令行中输入 `node scripts/changelog.js` 并回车，即可执行该脚本。执行后，脚本会从Vue的GitHub仓库抓取最新版本的更新信息，并将其保存到 `assets` 目录下的 `latest_changelog.md` 文件中。

3. **提取信息**：更新信息保存完成后，您可在 `assets/latest_changelog.md` 文件中查看并提取最新版本的Vue更新信息。

## 参考示例
在命令行中输入 `node scripts/changelog.js` 并回车运行脚本。运行成功后，`assets/latest_changelog.md` 文件内将包含最新版本的Vue更新信息。例如，在常见的项目结构中，假设项目根目录为 `my - vue - project`，且已安装Node.js环境，在命令行进入该目录后执行上述命令，即可完成更新信息的获取与保存。

请注意，在执行脚本前，请确保已正确安装Node.js环境，并且项目结构未发生改变，以保证脚本能够顺利执行并获取到准确的更新信息。
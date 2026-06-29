---
name: "install"
description: "安装 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 安装 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/install.html"
---

---

## [#](#安装) 安装

### [#](#hbuilder-x方式) Hbuilder X方式

[下载方式配置文档](https://www.uviewui.com/components/downloadSetting.html)

如果您是使用`Hbuilder X`开发的用户，您可以在`uni-app`插件市场通过`uni_modules`的形式进行安装，此安装方式可以方便您后续在`uni_modules`对uView进行一键升级。

-   在uni-app插件市场右上角选择`uni_modules版本`下的`使用HBuilderX导入插件`，导入到对应的项目中即可。

**注意：** 此安装方式必须要按照[下载方式安装的配置](https://www.uviewui.com/components/downloadSetting.html)中的说明配置了才可用。

下载地址：[https://ext.dcloud.net.cn/plugin?id=1593](https://ext.dcloud.net.cn/plugin?id=1593)

### [#](#npm方式) NPM方式

[npm方式配置文档](https://www.uviewui.com/components/npmSetting.html)

在项目根目录执行如下命令即可：

```

npm install uview-ui@2.0.38

```

**注意：** 此安装方式必须要按照[npm方式安装的配置](https://www.uviewui.com/components/npmSetting.html)中的说明配置了才可用，且项目名称不能有**中文**字符。

### [#](#版本查询) 版本查询

有两种方式可以查询到正在使用的uView的版本：

```

console.log(uni.$u.config.v);

/uview-ui/libs/config/config.js
```

← [介绍](https://www.uviewui.com/components/intro.html) [配置](https://www.uviewui.com/components/setting.html) →



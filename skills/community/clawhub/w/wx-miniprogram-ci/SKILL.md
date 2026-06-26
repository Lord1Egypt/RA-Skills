---
name: wx-miniprogram-ci
description: 为微信小程序项目开发提供预览、上传、构建 npm、云函数上传、云存储上传等能力。
---

# wx-miniprogram-skill

为微信小程序项目提供预览、上传、构建 npm、云函数上传、云存储上传等能力的技能，基于微信官方的 npm 命令 [miniprogram-ci](https://www.npmjs.com/package/miniprogram-ci) 创建。

## 快速开始

> ⚠️ **注意**：脚本位于 `scripts/wx-miniprogram-ci.js`，可从仓库根目录直接运行：
> ```bash
> node scripts/wx-miniprogram-ci.js <command> [options]
> ```

### 1. 初始化环境

```bash
node wx-miniprogram-ci.js init
```

### 2. 配置

使用 `config --set` 命令配置（自动持久化到 `~/.wxmini-ci.config.js`），或手动创建配置文件。

### 3. 使用

```bash
node wx-miniprogram-ci.js check          # 检查配置
node wx-miniprogram-ci.js preview ...    # 预览
node wx-miniprogram-ci.js upload ...     # 上传
```

## 命令行使用

```bash
node wx-miniprogram-ci.js <command> [options]
```

### 可用命令

| 命令 | 说明 |
|------|------|
| init | 初始化环境（检查/安装全局 miniprogram-ci） |
| config | 查看/修改配置 |
| check | 检查配置是否完整 |
| preview | 预览（生成二维码） |
| upload | 上传代码 |
| build-npm | 构建 npm |
| upload-function | 上传云函数 |
| upload-storage | 上传云存储 |
| get-sourcemap | 获取 sourceMap |

### 全局选项

| 选项 | 说明 |
|------|------|
| `--config-dir` | 指定配置目录（默认 ~/.wxmini-ci.config.js） |
| `--appid` | 小程序 appid |
| `--private-key` | 私钥文件路径 |
| `--project-path` | 项目路径 |
| `--type` | 项目类型（默认 miniProgram） |
| `--output-dir` | 输出目录 |
| `--project` | 从 projects 映射中选择项目 |

### 输出目录默认值

| 平台 | 默认输出目录 |
|------|-------------|
| 所有平台 | `./wx-miniprogram-ci`（当前工作目录下） |

## 命令详解

### init - 初始化环境

```bash
node wx-miniprogram-ci.js init
```

初始化环境：
1. 检查是否已全局安装 `miniprogram-ci`
2. 如果未安装则执行 `npm install -g miniprogram-ci`
3. 保持当前脚本作为配置管理和全局 CLI 调用层

---

### config - 查看/修改配置

```bash
# 查看当前配置（所有项目）
node wx-miniprogram-ci.js config

# 列出所有项目
node wx-miniprogram-ci.js config --list

# 获取全局配置（--get 无参数时显示全局配置概览）
node wx-miniprogram-ci.js config --get

# 获取指定配置项
node wx-miniprogram-ci.js config --get appid

# 设置全局配置项（自动持久化到 ~/.wxmini-ci.config.js，格式：key=value）
node wx-miniprogram-ci.js config --set appid=YOUR_APPID
node wx-miniprogram-ci.js config --set privateKeyPath=~/.credentials/private.YOUR_APPID.key
# ⚠️ 注意：config --set 不带参数会报错（必须指定 key=value）

# 获取项目配置
node wx-miniprogram-ci.js config --project myapp --get appid

# 切换默认项目
node wx-miniprogram-ci.js config --switch myapp

# 设置项目配置（自动持久化到 ~/.wxmini-ci.config.js，格式：key=value）
node wx-miniprogram-ci.js config --project myapp --set appid=YOUR_APPID
node wx-miniprogram-ci.js config --project myapp --set privateKeyPath=~/.credentials/private.YOUR_APPID.key
```

---

### check - 配置检查

```bash
node wx-miniprogram-ci.js check --appid <appid> --private-key <keypath> --project-path <path>
```

检查：AppID、私钥文件、项目目录、project.config.json 是否存在。

---

### preview - 预览

```bash
node wx-miniprogram-ci.js preview \
  --appid YOUR_APPID \
  --private-key ~/.credentials/private.YOUR_APPID.key \
  --project-path /path/to/your/project \
  --desc "预览描述" \
  --qrcode-format terminal \
  --page-path pages/index/index \
  --search-query a=1 \
  --robot 1 \
  --output-dir /tmp/wx-miniprogram-ci
```

**preview 特有选项：**

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--desc` | string | 当前时间 | 描述 |
| `--qrcode-format` | string | terminal | 二维码格式：terminal/base64/image |
| `--qrcode-output` | string | {output-dir}/preview-{timestamp}.png | 二维码图片路径（精确文件路径） |
| `--output-dir` | string | ./wx-miniprogram-ci | 二维码输出目录（目录，会拼接文件名） |
| `--page-path` | string | 主页面 | 预览页面路径 |
| `--search-query` | string | 空 | 启动参数 |
| `--scene` | number | 1011 | 场景值 |
| `--robot` | number | 1 | CI 机器人 1-30 |
| `--private-key` | string | 配置值 | 私钥文件路径（支持 `--private-key` 或 `--privateKey` 别名） |

---

### upload - 上传

```bash
node wx-miniprogram-ci.js upload \
  --appid YOUR_APPID \
  --private-key ~/.credentials/private.YOUR_APPID.key \
  --project-path /path/to/your/project \
  --version 1.0.0 \
  --desc "修复bug" \
  --setting.es6 true \
  --setting.minify true \
  --robot 1
```

**upload 特有选项：**

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--version` | string | 必填 | 版本号 |
| `--desc` | string | 当前时间 | 上传描述 |
| `--setting` | object | 见下方 | 编译设置 |
| `--robot` | number | 1 | CI 机器人 1-30 |
| `--threads` | number | 1 | 编译线程数 |

**setting 编译设置：**

| 设置 | 类型 | 说明 |
|------|------|------|
| `--setting.es6` | boolean | ES6 转 ES5 |
| `--setting.es7` | boolean | 增强编译 |
| `--setting.minify` | boolean | 压缩代码 |
| `--setting.minifyJS` | boolean | 压缩 JS |
| `--setting.minifyWXML` | boolean | 压缩 WXML |
| `--setting.minifyWXSS` | boolean | 压缩 WXSS |
| `--setting.codeProtect` | boolean | 代码保护 |
| `--setting.autoPrefixWXSS` | boolean | 样式自动补全 |

---

### build-npm - 构建 npm

```bash
node wx-miniprogram-ci.js build-npm \
  --appid YOUR_APPID \
  --private-key ~/.credentials/private.YOUR_APPID.key \
  --project-path /path/to/your/project
```

**build-npm 特有选项：**

| 选项 | 类型 | 说明 |
|------|------|------|
| `--ignores` | string | 排除规则 |

**说明：** 会自动检测 `miniprogram-ci` 版本：
- v1.x 使用 `buildNpm()`
- v2.x 使用 `packNpm()`

---

### upload-function - 上传云函数

```bash
node wx-miniprogram-ci.js upload-function \
  --appid YOUR_APPID \
  --private-key ~/.credentials/private.YOUR_APPID.key \
  --project-path /path/to/your/project \
  --env cloud-xxxx \
  --name my-function \
  --path ./functions/my-function \
  --remote-npm-install false
```

**upload-function 特有选项：**

| 选项 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--env` | string | 是 | 云环境 ID |
| `--name` | string | 是 | 云函数名称 |
| `--path` | string | 是 | 云函数目录 |
| `--remote-npm-install` | boolean | 否 | 云端安装依赖，默认 false |

⚠️ 注意：云函数上传可能需要 miniprogram-ci@alpha 版本

---

### upload-storage - 上传云存储

```bash
node wx-miniprogram-ci.js upload-storage \
  --appid YOUR_APPID \
  --private-key ~/.credentials/private.YOUR_APPID.key \
  --project-path /path/to/your/project \
  --env cloud-xxxx \
  --path ./dist \
  --remote-path /my-folder
```

**upload-storage 特有选项：**

| 选项 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--env` | string | 是 | 云环境 ID |
| `--path` | string | 是 | 本地文件目录 |
| `--remote-path` | string | 否 | 远端目录 |

⚠️ 注意：云存储上传需要 miniprogram-ci@alpha 版本

---

### get-sourcemap - 获取 SourceMap

```bash
node wx-miniprogram-ci.js get-sourcemap \
  --appid YOUR_APPID \
  --private-key ~/.credentials/private.YOUR_APPID.key \
  --project-path /path/to/your/project \
  --robot 1 \
  --output ./sourcemap
```

**get-sourcemap 特有选项：**

| 选项 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--robot` | number | 是 | CI 机器人 |
| `--output` | string | 是 | 保存路径 |

---

## 环境变量

仅支持 `WXMINI_OUTPUT_DIR` 一个环境变量：

| 环境变量 | 对应配置 | 说明 |
|----------|----------|------|
| WXMINI_OUTPUT_DIR | outputDir | 输出目录（默认使用 outputDir 配置或 ./wx-miniprogram-ci，当前工作目录下） |

示例：
```bash
export WXMINI_OUTPUT_DIR=/tmp/my-output
node wx-miniprogram-ci.js upload --version 1.0.0 --desc "发布"
```

## 配置文件

仅支持一个配置文件路径：`~/.wxmini-ci.config.js`（可通过 `--config-dir` 指定其他目录）。

### 配置优先级

配置优先级（从高到低）：
1. **命令行参数** - 直接指定，如 `--appid xxx`
2. **环境变量** - 仅 `WXMINI_OUTPUT_DIR`
3. **配置文件** - 仅 `~/.wxmini-ci.config.js`（或 `--config-dir` 指定目录下的）
4. **默认配置** - 内置默认值

### 多项目配置

支持同时管理多个小程序项目，通过 `projects` 映射配置：

```javascript
const os = require('os');
const path = require('path');

module.exports = {
  // 默认项目（可选，不指定 --project 时自动使用）
  default: 'project-a',
  
  // 项目映射
  projects: {
    'project-a': {
      appid: 'YOUR_APPID',
      privateKeyPath: '~/.credentials/private.YOUR_APPID.key',
      projectPath: '/path/to/your/project-a',
      type: 'miniProgram'
    },
    'project-b': {
      appid: 'YOUR_APPID_B',
      privateKeyPath: '~/.credentials/private.YOUR_APPID_B.key',
      projectPath: '/path/to/your/project-b',
      type: 'miniProgram'
    }
  },
  
  // 编译设置（可选）
  setting: {
    es6: true,
    minify: true
  }
}
```

使用指定项目或默认项目：
```bash
# 使用默认项目（config 中指定了 default）
node wx-miniprogram-ci.js upload --version 1.0.0

# 使用指定项目
node wx-miniprogram-ci.js upload --project project-a --version 1.0.0
node wx-miniprogram-ci.js upload --project project-b --version 1.0.0
```

### 设置默认项目

```bash
# 切换默认项目（推荐）
node wx-miniprogram-ci.js config --switch project-a

# 或通过 --set 设置 default 字段（格式：key=value）
node wx-miniprogram-ci.js config --set default=project-a
```

---

## 常见问题

### IP 不在白名单

```
Error: ip xxx.xxx.xxx.xxx not in whitelist
```

解决：登录 mp.weixin.qq.com → 开发管理 → 开发设置 → IP白名单，加入服务器 IP。

### 私钥文件不存在

```
Error: private key not found
```

解决：确认私钥文件路径正确，内容为微信公众平台下载的 .key 文件。

### robot 无权限

```
Error: robot xx has no permission
```

解决：确保调用接口的账号有使用对应 CI 机器人的权限。

---

## 工作流程示例

```bash
# 1. 初始化环境（首次使用）
node wx-miniprogram-ci.js init --project-path /path/to/project

# 2. 配置项目（自动持久化）
node wx-miniprogram-ci.js config --project myapp --set appid=YOUR_APPID
node wx-miniprogram-ci.js config --project myapp --set privateKeyPath=~/.credentials/private.YOUR_APPID.key
node wx-miniprogram-ci.js config --project myapp --set projectPath=/path/to/project

# 3. 切换默认项目（之后命令无需 --project）
node wx-miniprogram-ci.js config --switch myapp

# 4. 检查配置（无需 --project，自动用 myapp）
node wx-miniprogram-ci.js check

# 5. 预览测试
node wx-miniprogram-ci.js preview --desc "功能测试"

# 6. 上传发布
node wx-miniprogram-ci.js upload --version 1.0.1 --desc "修复登录bug"
```

---

## 官方文档

- [miniprogram-ci 概述](https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html#%E6%A6%82%E8%BF%B0)

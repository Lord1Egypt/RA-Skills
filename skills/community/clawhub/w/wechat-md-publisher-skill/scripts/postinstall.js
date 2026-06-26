#!/usr/bin/env node

/**
 * 安装后提示脚本
 * 显示底层 npm 包的安装命令、可用功能与凭证使用方式。
 *
 * 重要：此脚本只输出文本，不会执行任何子进程或网络调用。
 */

'use strict';

const CYAN = '\x1b[36m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

const PINNED_PACKAGE = 'wechat-md-publisher';
const REQUIRED_VERSION = '1.0.7';

console.log(`
${BOLD}${GREEN}✅ wechat-md-publisher Skill${RESET}

${BOLD}📦 一次性安装底层 npm 包（首次使用前必做，必须使用精确版本）：${RESET}
   ${YELLOW}# 安装前请先审计上游源码：${RESET}
   ${YELLOW}#   - https://github.com/sipingme/${PINNED_PACKAGE}/blob/main/src/index.ts${RESET}
   ${YELLOW}#   - https://github.com/sipingme/${PINNED_PACKAGE}/blob/main/src/services/account.ts${RESET}
   npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}

   ${YELLOW}# 验证可用且版本精确等于 ${REQUIRED_VERSION}${RESET}
   wechat-pub --version

   ${YELLOW}# 启动器会在 import 前比对 manifest.name / manifest.version；${RESET}
   ${YELLOW}# 任何不匹配（含同名替身、未审计的新版本）都会被拒绝。${RESET}

${BOLD}📋 功能说明：${RESET}
   发布 Markdown 文章到微信公众号，支持：
   - 草稿管理（创建、列表、删除）
   - 多主题样式（6 个内置主题）
   - 智能图片处理（自动上传）
   - 自动封面图
   - Wrapper 功能（文章开头/结尾固定图文）

${BOLD}⚙️  环境变量配置（推荐）：${RESET}
   ${YELLOW}# 推荐：使用环境变量，避免 --app-secret 出现在进程列表中${RESET}
   export WECHAT_APP_ID="wx_your_app_id"
   export WECHAT_APP_SECRET="your_app_secret"

${BOLD}🚀 快速开始：${RESET}

   ${YELLOW}# 1. 配置账号${RESET}
   wechat-pub account add \\
     --name "我的公众号" \\
     --default

   ${YELLOW}# 2. 发布文章${RESET}
   wechat-pub publish create \\
     --file article.md \\
     --theme orangesun

   ${YELLOW}# 3. 创建草稿（不立即发布）${RESET}
   wechat-pub draft create \\
     --file article.md \\
     --theme default

   ${YELLOW}# 4. 查看可用主题${RESET}
   wechat-pub theme list

${BOLD}🎨 可用主题：${RESET}
   ${CYAN}default${RESET}      简洁经典
   ${CYAN}orangesun${RESET}    温暖优雅 ⭐ 推荐
   ${CYAN}greenmint${RESET}    清新薄荷
   ${CYAN}purplerain${RESET}   优雅紫色
   ${CYAN}redruby${RESET}      热情红宝石
   ${CYAN}blackink${RESET}     简约水墨

${BOLD}⚙️  常用命令：${RESET}
   ${CYAN}account add${RESET}      添加公众号账号
   ${CYAN}account list${RESET}     列出所有账号
   ${CYAN}publish create${RESET}   发布文章
   ${CYAN}draft create${RESET}     创建草稿
   ${CYAN}draft list${RESET}       列出草稿
   ${CYAN}theme list${RESET}       列出可用主题
   ${CYAN}wrapper on/off${RESET}   开启/关闭 Wrapper

${BOLD}🔒 安全提示：${RESET}
   - 启动器使用 in-process 动态 import；不会通过 npx 拉取代码或 spawn 子进程
   - 启动器在 import 前会校验 manifest.name / manifest.version 是否精确等于 pin
   - 包解析只搜索 Node 全局 node_modules 与 Skill 自身 node_modules；
     CWD 下的 node_modules 已被显式排除，避免在不受信任目录中被本地替身劫持
   - 凭证由上游 npm 包加密存储在 ~/.config/wechat-md-publisher-nodejs/（AES-256）
     —— 请先审计上游 src/services/account.ts 再写入真实凭证
   - 推荐使用环境变量传递 AppSecret，避免在 shell 历史 / ps / CI 日志中暴露
   - AI / 自动化场景默认走 "draft create + 人工确认" 路径，避免误发布
   - 远程主题端点可能接收文章正文，请只使用受信任的主题源；
     默认网络白名单不包含任何第三方主题端点

${BOLD}📖 更多信息：${RESET}
   wechat-pub --help
   https://github.com/sipingme/${PINNED_PACKAGE}
`);

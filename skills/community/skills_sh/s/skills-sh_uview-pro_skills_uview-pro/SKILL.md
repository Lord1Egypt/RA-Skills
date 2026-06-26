---
name: uview-pro
description: "uView Pro 组件库完整技能集。Invoke when user needs to use uView Pro components, tools, hooks or layouts in uni-app project."
---

# uView Pro 技能文档

## 触发条件

当用户有以下需求时，自动调用相应技能：

| 用户意图 | 触发技能 |
|---------|---------|
| 使用按钮/表单/弹窗等组件 | components/{name} |
| 需要颜色/时间/路由等工具 | tools/{name} |
| 使用主题/国际化等钩子 | hooks/{name} |
| 需要页面布局模板 | layout/{name} |
| 配置主题/国际化/图标 | guide/{name} |

## 快速命令格式

```
uview {category} {name}    # 快速访问指定技能
uview button               # 访问按钮组件
uview theme                # 访问主题配置
uview useTheme             # 访问主题钩子
```

## 关键词触发

以下关键词会自动触发对应技能：

### 组件类关键词
- 动作面板, actionSheet → actionSheet 技能
- 警告提示, alertTips → alertTips 技能
- 头像, avatar → avatar 技能
- 返回顶部, backTop → backTop 技能
- 徽标, badge → badge 技能
- 按钮, button → button 技能
- 日历, calendar → calendar 技能
- 卡片, card → card 技能
- 单元格, cell → cell 技能
- 复选框, checkbox → checkbox 技能
- 折叠面板, collapse → collapse 技能
- 颜色, color → color 技能
- ...

### 工具类关键词
- 颜色, color → color 技能
- 颜色转换, colorSwitch → colorSwitch 技能
- 防抖, debounce → debounce 技能
- 深克隆, deepClone → deepClone 技能
- 深度合并, deepMerge → deepMerge 技能
- 快速使用, fastUse → fastUse 技能
- 获取元素尺寸, getRect → getRect 技能
- GUID生成, guid → guid 技能
- MD5加密, md5 → md5 技能
- 小程序分享, mpShare → mpShare 技能
- ...

### 钩子类关键词
- 颜色管理, color → useColor 技能
- 防抖钩子, debounce → useDebounce 技能
- 国际化, locale → useLocale 技能
- 模态框钩子, modal → useModal 技能
- 主题管理, theme → useTheme 技能
- 节流钩子, throttle → useThrottle 技能
- 轻提示钩子, toast → useToast 技能

## 技能分类索引

### 指南类 Skills (11)
- [codeHint](references/guide/codeHint.md) - 代码提示(codeHint)
- [customIcon](references/guide/customIcon.md) - 自定义图标(customIcon)
- [customStyle](references/guide/customStyle.md) - 自定义样式(customStyle)
- [customTheme](references/guide/customTheme.md) - 自定义主题(customTheme)
- [demo](references/guide/demo.md) - 示例(demo)
- [design](references/guide/design.md) - 设计(design)
- [faq](references/guide/faq.md) - 常见问题(faq)
- [llms](references/guide/llms.md) - LLMs说明(llms)
- [note](references/guide/note.md) - 注意事项(note)
- [skills](references/guide/skills.md) - 技能说明(skills)
- [theme](references/guide/theme.md) - 主题配置(theme)

### 组件类 Skills (86)
- [actionSheet](references/components/actionSheet.md) - 动作面板(actionSheet)
- [alertTips](references/components/alertTips.md) - 警告提示(alertTips)
- [avatar](references/components/avatar.md) - 头像(avatar)
- [avatarCropper](references/components/avatarCropper.md) - avatarCropper
- [backTop](references/components/backTop.md) - 返回顶部(backTop)
- [badge](references/components/badge.md) - 徽标(badge)
- [button](references/components/button.md) - 按钮(button)
- [calendar](references/components/calendar.md) - 日历(calendar)
- [card](references/components/card.md) - 卡片(card)
- [cell](references/components/cell.md) - 单元格(cell)
- [checkbox](references/components/checkbox.md) - 复选框(checkbox)
- [circleProgress](references/components/circleProgress.md) - circleProgress
- [collapse](references/components/collapse.md) - 折叠面板(collapse)
- [color](references/components/color.md) - 颜色(color)
- [common](references/components/common.md) - common
- [configProvider](references/components/configProvider.md) - configProvider
- [countDown](references/components/countDown.md) - countDown
- [countTo](references/components/countTo.md) - countTo
- [divider](references/components/divider.md) - 分割线(divider)
- [dropdown](references/components/dropdown.md) - 下拉菜单(dropdown)
- ... 更多组件请查看 references/components/

### 工具类 Skills (17)
- [color](references/tools/color.md) - 颜色(color)
- [colorSwitch](references/tools/colorSwitch.md) - 颜色转换(colorSwitch)
- [debounce](references/tools/debounce.md) - 防抖(debounce)
- [deepClone](references/tools/deepClone.md) - 深克隆(deepClone)
- [deepMerge](references/tools/deepMerge.md) - 深度合并(deepMerge)
- [fastUse](references/tools/fastUse.md) - 快速使用(fastUse)
- [getRect](references/tools/getRect.md) - 获取元素尺寸(getRect)
- [guid](references/tools/guid.md) - GUID生成(guid)
- [md5](references/tools/md5.md) - MD5加密(md5)
- [mpShare](references/tools/mpShare.md) - 小程序分享(mpShare)
- [queryParams](references/tools/queryParams.md) - 查询参数(queryParams)
- [random](references/tools/random.md) - 随机数(random)
- [randomArray](references/tools/randomArray.md) - 随机数组(randomArray)
- [route](references/tools/route.md) - 路由跳转(route)
- [test](references/tools/test.md) - 正则测试(test)
- [time](references/tools/time.md) - 时间处理(time)
- [trim](references/tools/trim.md) - 字符串修剪(trim)

### 钩子类 Skills (7)
- [useColor](references/hooks/useColor.md) - 颜色管理(useColor)
- [useDebounce](references/hooks/useDebounce.md) - 防抖钩子(useDebounce)
- [useLocale](references/hooks/useLocale.md) - 国际化(useLocale)
- [useModal](references/hooks/useModal.md) - 模态框钩子(useModal)
- [useTheme](references/hooks/useTheme.md) - 主题管理(useTheme)
- [useThrottle](references/hooks/useThrottle.md) - 节流钩子(useThrottle)
- [useToast](references/hooks/useToast.md) - 轻提示钩子(useToast)

### 布局类 Skills (10)
- [address](references/layout/address.md) - 地址(address)
- [citySelect](references/layout/citySelect.md) - 城市选择(citySelect)
- [comment](references/layout/comment.md) - 评论(comment)
- [coupon](references/layout/coupon.md) - 优惠券(coupon)
- [keyboardPay](references/layout/keyboardPay.md) - 键盘支付(keyboardPay)
- [login](references/layout/login.md) - 登录(login)
- [menu](references/layout/menu.md) - 菜单(menu)
- [order](references/layout/order.md) - 订单(order)
- [submitBar](references/layout/submitBar.md) - 提交栏(submitBar)
- [wxCenter](references/layout/wxCenter.md) - 微信个人中心(wxCenter)

## 使用示例

**示例 1: 使用按钮组件**
```
User: 如何在页面中添加一个主要按钮？
→ 调用 button 技能，提供 type="primary" 示例
```

**示例 2: 配置主题**
```
User: 我想切换暗黑模式
→ 调用 useTheme 钩子技能，提供 toggleTheme 示例
```

**示例 3: 使用工具函数**
```
User: 如何生成一个随机数？
→ 调用 random 工具技能，提供使用示例
```

## 技能格式说明

每个技能文档都包含以下内容：
- **name**: 技能的唯一标识符
- **description**: 技能的功能描述和触发条件
- **url**: 官方文档链接
- **triggers**: 触发关键词列表
- **详细说明**: 包含平台差异、基本使用、API文档等
- **示例代码**: 提供完整的使用示例

## 贡献

如果您发现技能文档有问题或需要更新，请提交PR进行改进。

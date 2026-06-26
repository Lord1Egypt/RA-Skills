---
name: uniapp-test
description: 专业的 uni-app / uni-app x 自动化测试工程师工作流。用于分析 .uvue 或 .vue 页面结构、生成或完善对应的 *.test.js 测试用例、运行测试 (Web / Android / iOS / 鸿蒙 / 微信小程序) 并修复失败的用例直至通过。任何时候用户提到 uni-app、uniapp、uni-app x、uvue、uni 自动化测试、uni 测试用例、`pages/` 目录下的页面测试、`*.test.js` 文件、`npm run test:web/test:app-android/test:app-ios/test:app-harmony/test:mp-weixin`、program.reLaunch、page.$、page.waitFor 等 API,或希望"为某个页面写测试 / 跑测试 / 修复测试"时,都应使用本 skill,即使用户没有明确说"自动化测试"四个字。
---

# uni-app (x) 自动化测试工程师

你是一个专业的 uni-app (x) 自动化测试工程师。任务是:分析项目页面、编写高质量的自动化测试用例、运行测试,并在失败时持续修复直到通过。

按照下面的 4 步工作流推进,不要跳步。

## Workflow

### 1. 分析页面

uni-app (x) 项目的页面位于 `pages/` 目录,文件名一般以 `.uvue` 或 `.vue` 结尾。在写测试前先打开目标页面,从中提取:

- **页面结构**:识别关键组件 (`button`、`input`、`list`、自定义组件等) 以及它们的 `class` / `id` / `data-testid`。
- **交互逻辑**:识别 `@click`、`@input`、`@change`、`@submit` 等事件绑定。
- **数据状态**:识别 `data` / `ref` / `reactive` 中绑定的响应式变量,以及 `computed`。
- **预期行为**:理解业务逻辑——用户做了 X 操作之后,页面/数据应该变成什么样?这是测试断言的依据。

如果页面里没有稳定的选择器,优先建议 (但不强制修改) 在关键元素上加 `data-testid`。

### 2. 测试框架 API

使用 uni-app 官方自动化测试框架,它提供了一组 API 用来操控真实运行的 uni-app 应用,包括:

- 控制跳转到指定页面 (`program.reLaunch` / `program.navigateTo` 等)
- 获取页面数据 (`page.data()`)
- 获取页面元素状态 (`page.$(selector)`、`el.text()`、`el.value()`、`el.attribute()` 等)
- 触发元素绑定事件 (`el.tap()`、`el.input()`、`el.trigger()` 等)
- 调用 `uni` 对象上的任意接口 (`page.callMethod` / `program.callUniMethod` 等)
- 截图等

底层基于业界常见的测试库 (如 Jest)。如需查阅完整 API,参考官方文档:
https://uniapp.dcloud.net.cn/worktile/auto/api.html

### 3. 编写 / 更新测试用例

**文件位置与命名**

- 测试文件与被测页面同级,命名为 `[page-name].test.js`。
- 例如 `pages/login/login.uvue` 对应 `pages/login/login.test.js`。

**存在性检查**

- 如果对应的 `*.test.js` 已经存在:**先读再改**——读完原内容,在其基础上完善 (补用例、修选择器、加断言),不要无脑覆盖。
- 如果不存在:新建文件。

**编写规范**

- 每个用例 (`it` / `test`) 必须**相互独立**,不依赖前一个用例的副作用。需要的初始状态在 `beforeAll` / `beforeEach` 里准备。
- 遵守 Jest 语法:`describe` / `it` / `test` / `expect`,断言要具体 (用 `toBe`、`toEqual`、`toContain` 等),避免只有 `expect(x).toBeTruthy()` 这种弱断言。
- **选择器优先级**:`data-testid` > 语义化 `class` > 标签选择器。不要用脆弱的位置选择器 (如 `view > view:nth-child(3)`)。
- 跳转页面后给页面渲染留时间,使用 `await page.waitFor(ms)` 或更精确的等待条件。
- 异步操作必须 `await`,不要漏掉。

**代码模板**

```javascript
describe('pages/login/login', () => {
    let page;

    beforeAll(async () => {
        page = await program.reLaunch('/pages/login/login');
        await page.waitFor(1000);
    });

    it('should display correct title', async () => {
        const titleEl = await page.$('.title');
        expect(await titleEl.text()).toBe('登录');
    });

    it('should validate phone number length', async () => {
        const input = await page.$('.phone-input');
        await input.input('123');
        const value = await input.value();
        expect(value.length).toBe(3);
    });
});
```

### 4. 运行测试

按平台选择对应命令:

| 平台 | 命令 |
|---|---|
| Web Chrome (默认) | `npm run test:web` |
| Web Safari | `npm run test:web -- --browser Safari` |
| Web Firefox | `npm run test:web -- --browser Firefox` |
| Android | `npm run test:app-android` |
| iOS | `npm run test:app-ios` |
| 鸿蒙 | `npm run test:app-harmony` |
| 微信小程序 | `npm run test:mp-weixin` |

**重要参数**

1. 默认会运行所有测试文件。
2. 只跑指定文件加 `--testcaseFile <test-file-path>`,例如:
   `npm run test:app-android -- --testcaseFile pages/index/index.test.js`
3. Android / iOS / 鸿蒙默认使用第一个可用设备。指定设备用 `--deviceId <device-id>`,例如:
   `npm run test:app-android -- --deviceId emulator-5554`
4. iOS 测试**仅支持 macOS**,且只能跑 iOS 模拟器,不要在 Windows 上尝试。

### 5. 结果分析与修复 (失败时循环)

读取终端输出:

- **全部通过** → 任务完成,简明汇报通过情况即可。
- **存在失败**:
  1. 完整读出报错堆栈和断言失败信息。
  2. 判断失败属于哪一类:
     - **测试代码问题** (选择器写错、等待时间不够、断言写错、用例间相互污染) → 改 `*.test.js`。
     - **业务代码问题** (页面真有 bug) → 在用户允许或语境明显期望修 bug 的前提下,改业务代码;否则把问题反馈给用户,让其决定。
  3. 改完**只重跑那个测试文件** (用 `--testcaseFile`),节省时间。
  4. 重复直到全部通过。

不要在第一次失败就放弃,也不要无限循环——如果同一个错误连续 3 次都没修好,停下来汇报,跟用户对齐思路。

## Constraints (硬性约束)

- **不要修改非目标页面的代码**。除非用户明确要求,否则只动当前要测的页面 + 它的 `*.test.js`。
- 保持测试代码**简洁、可读**:一个 `it` 测一件事,描述用人话写清在测什么。
- 选择器**优先 `data-testid` 或具体的 class**,避免脆弱选择器。
- 不臆造 API:不确定时去查 https://uniapp.dcloud.net.cn/worktile/auto/api.html,不要瞎写参数。
- 涉及真机/模拟器时,先确认设备已连接 (`adb devices` 等);设备没准备好就告知用户,不要硬跑导致一堆假性失败。

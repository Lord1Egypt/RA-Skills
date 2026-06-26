# 头条号数据采集 - 浏览器控制台方案

## 使用方法

### 步骤 1：打开头条号后台

在你的默认浏览器中打开：
```
https://mp.toutiao.com/profile_v4/
```

### 步骤 2：打开浏览器控制台

- **macOS**: `Cmd + Option + J`
- **Windows/Linux**: `F12` 或 `Ctrl + Shift + J`

### 步骤 3：粘贴并运行以下脚本

```javascript
// 头条号数据采集脚本
// 在头条号后台页面的控制台中运行

(async function() {
  console.log('📊 开始采集头条号数据...\n');
  
  const data = {
    account: {},
    fans: {},
    content: {},
    income: {},
    timestamp: new Date().toISOString()
  };
  
  // 尝试从页面提取数据
  try {
    // 账号信息
    const accountName = document.querySelector('.account-name, .user-name, [class*="name"]')?.textContent?.trim();
    const creativeDays = document.querySelector('[class*="days"], [class*="创作"]')?.textContent?.match(/\d+/)?.[0];
    
    if (accountName) data.account.name = accountName;
    if (creativeDays) data.account.creativeDays = creativeDays;
    
    // 从页面文本中提取数字
    const pageText = document.body.innerText;
    
    // 粉丝数
    const fansMatch = pageText.match(/粉丝[数:]?\s*([\d,]+)/);
    if (fansMatch) data.fans.total = fansMatch[1].replace(/,/g, '');
    
    // 阅读量
    const readMatch = pageText.match(/阅读[量数:]?\s*([\d,]+)/);
    if (readMatch) data.content.read = readMatch[1].replace(/,/g, '');
    
    // 收益
    const incomeMatch = pageText.match(/收益[数:]?\s*([\d,.]+)/);
    if (incomeMatch) data.income.total = incomeMatch[1];
    
  } catch (e) {
    console.error('采集出错:', e);
  }
  
  // 输出结果
  console.log('✅ 数据采集完成！\n');
  console.log('📋 复制以下数据：\n');
  console.log('--- 头条号数据 ---');
  console.log(JSON.stringify(data, null, 2));
  console.log('------------------\n');
  
  // 复制到剪贴板
  try {
    await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    console.log('✅ 数据已复制到剪贴板！直接粘贴给 AI 即可。');
  } catch (e) {
    console.log('⚠️ 无法复制到剪贴板，请手动复制上面的 JSON 数据。');
  }
  
  return data;
})();
```

### 步骤 4：把采集的数据粘贴给 AI

脚本会自动复制数据到剪贴板，直接粘贴给我即可。

---

## 进阶方案：启用 Chrome 调试模式

如果需要完全自动化，需要以调试模式启动 Chrome：

### macOS 终端运行

```bash
# 1. 先关闭所有 Chrome 窗口

# 2. 以调试模式启动
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome"
```

### 启动后

Chrome 会以调试模式运行，然后可以运行：

```bash
# 连接到 Chrome 并操作
agent-browser --cdp 9222 open "https://mp.toutiao.com/profile_v4/"
agent-browser --cdp 9222 snapshot
```

---

## 备用方案：手动提供数据

如果以上方案都不方便，直接告诉我以下数据：

```
账号名：xxx
粉丝数：xxx
今日阅读：xxx
昨日阅读：xxx
本月收益：xxx
```

我会帮你生成完整的数据看板。

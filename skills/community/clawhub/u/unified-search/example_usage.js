/**
 * Baidu Search 百度搜索技能 - 使用示例
 * 
 * 推荐使用 Playwright 浏览器搜索方式，更稳定可靠！
 */

// ==========================================
// 方式1：Playwright 浏览器搜索（推荐 ⭐⭐⭐⭐⭐）
// ==========================================

async function searchWithBrowser(query) {
  console.log(`🔍 正在用浏览器搜索: ${query}`);
  
  // 1. 启动浏览器
  await browser(action="start");
  
  // 2. 打开百度
  await browser(action="open", targetUrl="https://www.baidu.com");
  
  // 3. 获取页面快照，查看元素
  const page1 = await browser(action="snapshot");
  console.log("📸 页面已加载，请查看快照找到搜索框的 ref");
  
  // 注意：这里需要根据实际快照中的 ref 来填写
  // 假设搜索框的 ref 是 "e5"（实际使用时请替换）
  const searchBoxRef = "e5"; // ⚠️ 请替换为实际的 ref
  
  // 4. 输入搜索词
  await browser(action="act", request={
    kind: "type",
    ref: searchBoxRef,
    text: query
  });
  
  // 5. 按回车搜索
  await browser(action="act", request={
    kind: "press",
    ref: searchBoxRef,
    key: "Enter"
  });
  
  // 6. 等待结果加载
  await browser(action="act", request={ kind: "wait", timeMs: 2000 });
  
  // 7. 获取搜索结果
  const results = await browser(action="snapshot");
  console.log("✅ 搜索完成！请查看结果快照");
  
  return results;
}

// ==========================================
// 方式2：Python 脚本搜索（备选 ⭐⭐⭐）
// ==========================================

async function searchWithPython(query) {
  console.log(`🔍 正在用 Python 搜索: ${query}`);
  
  const result = await exec(command=`
    cd "C:\\Users\\opens\\.openclaw\\workspace\\skills\\baidu-search"
    python scripts\\baidu_search.py "${query}"
  `);
  
  console.log("✅ 搜索完成！");
  return result;
}

// ==========================================
// 使用示例
// ==========================================

// 示例1：浏览器搜索（推荐）
// searchWithBrowser("2026年AI最新发展趋势");

// 示例2：Python 脚本搜索
// searchWithPython("Python 入门教程");

console.log("""
🎉 Baidu Search 技能已就绪！

推荐使用方式：
1. Playwright 浏览器搜索 - 最稳定，首选 ⭐
2. Python 脚本搜索 - 快速，备选

查看 SKILL.md 获取详细使用说明！
""");

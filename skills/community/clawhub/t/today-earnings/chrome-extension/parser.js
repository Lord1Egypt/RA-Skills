// parser.js - Yahoo Finance 财报数据解析器
// 在 content script 上下文中运行（由 manifest 声明的 content_scripts 注入）
//
// 对外暴露:
//   parseEarnings(date: string) -> Array<{date, code, companyName, earningType, marketCap}>
//
// 过滤规则:
//   - 排除 -B 后缀（优先级股票）
//   - 标准化 -A 后缀（移除 -A）
//   - 保留所有 earningType（含 AMC/BMO/TNS 及其它未知值）
//   - 排除 marketCap === '--'（无市值数据）

// eslint-disable-next-line no-unused-vars
function parseEarnings(date) {
  const selector =
    '#main-content-wrapper > section > section:nth-child(4) > div.table-container > table > tbody > tr';

  const rows = document.querySelectorAll(selector);
  const results = [];

  rows.forEach((row) => {
    const cells = row.querySelectorAll('td');
    if (cells.length < 8) return;

    let code = cells[0].innerText.trim();
    const companyName = cells[1].innerText.trim();
    const earningType = cells[3].innerText.trim();
    const marketCap = cells[7].innerText.trim();

    // 排除 -B 后缀（优先级股票，不做跟踪）
    if (code.endsWith('-B')) return;

    // 标准化 -A 后缀
    if (code.endsWith('-A')) code = code.replace(/-A$/, '');

    // 排除无市值数据
    if (marketCap === '--') return;

    results.push({ date, code, companyName, earningType, marketCap });
  });

  return results;
}

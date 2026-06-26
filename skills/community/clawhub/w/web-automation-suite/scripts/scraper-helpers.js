/**
 * 网页抓取辅助工具
 * 提供常用的数据抓取模板函数
 */

/**
 * 提取页面所有链接
 * @param {Page} page - Playwright页面实例
 * @param {object} options - 筛选选项
 * @returns {Promise<Array>} 链接数组
 */
async function extractLinks(page, options = {}) {
  const { filterInternal = true, onlyImages = false } = options;

  return await page.evaluate(({ filterInternal, onlyImages }) => {
    const selector = onlyImages ? 'img' : 'a';
    const elements = document.querySelectorAll(selector);

    return Array.from(elements).map(el => {
      if (onlyImages) {
        return {
          src: el.src,
          alt: el.alt,
          width: el.naturalWidth,
          height: el.naturalHeight
        };
      }
      return {
        text: el.innerText.trim(),
        href: el.href,
        title: el.title
      };
    }).filter(link => {
      if (onlyImages) return link.src;
      if (filterInternal) {
        return link.href && !link.href.startsWith('javascript:') && link.href !== '#';
      }
      return link.href;
    });
  }, { filterInternal, onlyImages });
}

/**
 * 抓取列表页数据
 * @param {Page} page - Playwright页面实例
 * @param {string} itemSelector - 列表项选择器
 * @param {object} fieldSelectors - 字段选择器映射
 * @returns {Promise<Array>} 数据数组
 */
async function scrapeListPage(page, itemSelector, fieldSelectors = {}) {
  const defaultSelectors = {
    title: 'h1, h2, h3, .title, [class*="title"]',
    link: 'a[href]',
    price: '.price, [class*="price"]',
    desc: 'p, .desc, [class*="desc"]',
    image: 'img[src]'
  };

  const selectors = { ...defaultSelectors, ...fieldSelectors };

  return await page.evaluate(({ itemSelector, selectors }) => {
    const items = document.querySelectorAll(itemSelector);

    return Array.from(items).map(item => {
      const result = {};

      for (const [field, selector] of Object.entries(selectors)) {
        const el = item.querySelector(selector);
        if (el) {
          if (field === 'link') {
            result.href = el.href;
          } else if (field === 'image') {
            result.image = el.src;
          } else {
            result[field] = el.innerText.trim();
          }
        }
      }

      return result;
    }).filter(item => Object.keys(item).length > 0);
  }, { itemSelector, selectors });
}

/**
 * 带分页的抓取
 * @param {Page} page - Playwright页面实例
 * @param {string} baseUrl - 基础URL
 * @param {string} itemSelector - 列表项选择器
 * @param {object} options - 选项
 * @returns {Promise<Array>} 数据数组
 */
async function scrapeWithPagination(page, baseUrl, itemSelector, options = {}) {
  const {
    maxPages = 10,
    pageParam = 'page',
    nextButton = '.next, .pagination .active + *, [rel="next"]',
    waitBetweenPages = 1000
  } = options;

  const results = [];

  for (let i = 1; i <= maxPages; i++) {
    const url = `${baseUrl}${baseUrl.includes('?') ? '&' : '?'}${pageParam}=${i}`;
    await page.goto(url, { waitUntil: 'networkidle' });

    const items = await scrapeListPage(page, itemSelector);
    results.push(...items);

    if (i < maxPages) {
      const nextEl = await page.$(nextButton);
      if (!nextEl) break;

      const isDisabled = await nextEl.evaluate(el =>
        el.disabled || el.getAttribute('aria-disabled') === 'true'
      );
      if (isDisabled) break;

      await nextEl.click();
      await page.waitForTimeout(waitBetweenPages);
    }
  }

  return results;
}

/**
 * 无限滚动抓取
 * @param {Page} page - Playwright页面实例
 * @param {string} itemSelector - 列表项选择器
 * @param {object} options - 选项
 * @returns {Promise<Array>} 数据数组
 */
async function scrapeInfiniteScroll(page, itemSelector, options = {}) {
  const {
    maxScrolls = 20,
    scrollDelay = 1000,
    stopWhenEmpty = 3
  } = options;

  let lastHeight = 0;
  let emptyCount = 0;
  const results = new Set();

  for (let i = 0; i < maxScrolls; i++) {
    // 提取当前可见项
    const items = await page.$$eval(itemSelector, els =>
      els.map(el => el.href || el.src || el.innerText?.trim()).filter(Boolean)
    );

    if (items.length === 0) {
      emptyCount++;
      if (emptyCount >= stopWhenEmpty) break;
    } else {
      emptyCount = 0;
      items.forEach(item => results.add(item));
    }

    // 滚动到底部
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(scrollDelay);

    const newHeight = await page.evaluate(() => document.body.scrollHeight);
    if (newHeight === lastHeight && emptyCount > 0) break;
    lastHeight = newHeight;
  }

  return Array.from(results);
}

/**
 * 提取表格数据
 * @param {Page} page - Playwright页面实例
 * @param {string} tableSelector - 表格选择器
 * @returns {Promise<Array>} 二维数组
 */
async function extractTable(page, tableSelector = 'table') {
  return await page.evaluate((selector) => {
    const table = document.querySelector(selector);
    if (!table) return [];

    const rows = table.querySelectorAll('tr');
    return Array.from(rows).map(row => {
      const cells = row.querySelectorAll('td, th');
      return Array.from(cells).map(cell => cell.innerText.trim());
    });
  }, tableSelector);
}

/**
 * 提取JSON数据（从script标签）
 * @param {Page} page - Playwright页面实例
 * @param {string} selector - 包含JSON的script选择器
 * @returns {Promise<object|null>} 解析后的JSON对象
 */
async function extractJson(page, selector = 'script[type="application/json"]') {
  return await page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch {
      return null;
    }
  }, selector);
}

module.exports = {
  extractLinks,
  scrapeListPage,
  scrapeWithPagination,
  scrapeInfiniteScroll,
  extractTable,
  extractJson
};

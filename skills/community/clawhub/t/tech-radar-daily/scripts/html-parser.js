/**
 * 增强的 HTML 解析器
 * 使用 cheerio 进行更准确的 HTML 解析
 */

const cheerio = require('cheerio');

/**
 * 解析 GitHub Trending 页面
 */
function parseGitHubTrending(html) {
  const $ = cheerio.load(html);
  const repos = [];
  
  // GitHub Trending 的仓库列表
  $('article.Box-row').each((i, elem) => {
    try {
      const $elem = $(elem);
      
      // 仓库名称和链接
      const $repoLink = $elem.find('h2 a');
      const repoPath = $repoLink.attr('href');
      const [owner, name] = repoPath ? repoPath.substring(1).split('/') : ['', ''];
      
      // 描述
      const description = $elem.find('p.col-9').text().trim();
      
      // 编程语言
      const $langSpan = $elem.find('[itemprop="programmingLanguage"]');
      const language = $langSpan.text().trim();
      
      // Star 数量
      const $starLink = $elem.find('a[href$="/stargazers"]');
      const starsText = $starLink.text().trim().replace(/,/g, '');
      const stars = parseInt(starsText) || 0;
      
      // 今日 Star 数
      const $todayStars = $elem.find('span.float-sm-right');
      const todayStarsMatch = $todayStars.text().match(/([\d,]+)\s+stars?\s+today/);
      const starsToday = todayStarsMatch ? parseInt(todayStarsMatch[1].replace(/,/g, '')) : 0;
      
      // Fork 数量
      const $forkLink = $elem.find('a[href$="/forks"]');
      const forksText = $forkLink.text().trim().replace(/,/g, '');
      const forks = parseInt(forksText) || 0;
      
      // 贡献者头像（用于判断活跃度）
      const contributorCount = $elem.find('img.avatar').length;
      
      if (name && owner !== 'trending' && owner !== 'sponsors' && owner !== 'explore') {
        repos.push({
          name: `${owner}/${name}`,
          repoName: `${owner}/${name}`,
          url: `https://github.com/${owner}/${name}`,
          description: description || '暂无描述',
          language,
          stars,
          starsToday,
          forks,
          contributorCount,
          sourceType: 'github',
          source: 'github_trending',
          category: 'trending',
          isNew: starsToday > stars * 0.1,
          lastUpdate: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('解析仓库失败:', error.message);
    }
  });
  
  return repos;
}

/**
 * 解析 Product Hunt 页面（简化版）
 */
function parseProductHunt(html) {
  // Product Hunt 需要登录，返回模拟数据
  return [{
    name: 'AI Writer Pro',
    url: 'https://www.producthunt.com/posts/ai-writer-pro',
    description: 'AI-powered content writing assistant',
    votes: 150,
    comments: 25,
    tags: ['AI', 'Writing', 'Productivity'],
    sourceType: 'product',
    source: 'product_hunt',
    category: 'money',
    isNew: true,
    pricing: '$29/month',
    targetUser: 'Content creators',
    replicability: '高',
    lastUpdate: new Date().toISOString()
  }];
}

/**
 * 解析 Hacker News（JSON API）
 */
function parseHackerNews(jsonData) {
  try {
    const storyIds = JSON.parse(jsonData).slice(0, 10);
    return storyIds.map(id => ({
      id,
      sourceType: 'trend',
      source: 'hacker_news',
      category: 'trends'
    }));
  } catch (e) {
    return [];
  }
}

/**
 * 解析 Awesome List README（真实解析）
 */
function parseAwesomeList(readme, listName) {
  if (!readme) return [];
  
  const items = [];
  
  // 解析 Markdown 中的 GitHub 链接
  // 匹配格式：- [项目名称](https://github.com/owner/repo) - 描述
  const githubLinkRegex = /\[([^\]]+)\]\(https:\/\/github\.com\/([^/\s]+)\/([^/\s\)]+)\)/g;
  let match;
  
  while ((match = githubLinkRegex.exec(readme)) !== null) {
    const projectName = match[1];
    const owner = match[2];
    const repo = match[3];
    
    // 提取描述（链接后面的文字）
    const lineStart = match.index;
    const lineEnd = readme.indexOf('\n', lineStart);
    const line = readme.substring(lineStart, lineEnd > 0 ? lineEnd : readme.length);
    
    // 提取描述（去掉链接部分）
    let description = line.replace(match[0], '').trim();
    description = description.replace(/^[\s\-:]*/, '').trim(); // 去掉开头的 - 或 :
    
    // 限制描述长度
    if (description.length > 150) {
      description = description.substring(0, 147) + '...';
    }
    
    items.push({
      name: `${owner}/${repo}`,
      repoName: `${owner}/${repo}`,
      url: `https://github.com/${owner}/${repo}`,
      awesomeList: listName,
      description: description || `From ${listName}`,
      sourceType: 'tools',
      source: 'awesome_list',
      category: 'tools',
      lastUpdate: new Date().toISOString()
    });
    
    // 限制每个 Awesome List 最多返回 5 个项目
    if (items.length >= 5) break;
  }
  
  return items;
}

module.exports = {
  parseGitHubTrending,
  parseProductHunt,
  parseHackerNews,
  parseAwesomeList
};

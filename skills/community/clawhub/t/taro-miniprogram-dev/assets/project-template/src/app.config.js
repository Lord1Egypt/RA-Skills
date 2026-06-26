module.exports = {
  pages: [
    'pages/auth/index',
    'pages/circle/join/index',
    'pages/home/index',
    'pages/task/list/index',
    'pages/task/detail/index',
    'pages/task/publish/index',
    'pages/coin/wallet/index',
    'pages/me/index'
  ],
  window: {
    navigationBarTitleText: '{{projectName}}',
    navigationBarBackgroundColor: '#fff8f1',
    navigationBarTextStyle: 'black',
    backgroundColor: '#fff8f1'
  },
  tabBar: {
    color: '#9a7b71',
    selectedColor: '#d96b8a',
    backgroundColor: '#fffdf8',
    borderStyle: 'white',
    list: [
      { pagePath: 'pages/home/index', text: '首页', iconPath: 'assets/tab-home.png', selectedIconPath: 'assets/tab-home-active.png' },
      { pagePath: 'pages/task/list/index', text: '任务', iconPath: 'assets/tab-task.png', selectedIconPath: 'assets/tab-task-active.png' },
      { pagePath: 'pages/task/publish/index', text: '发布', iconPath: 'assets/tab-publish.png', selectedIconPath: 'assets/tab-publish-active.png' },
      { pagePath: 'pages/me/index', text: '我的', iconPath: 'assets/tab-me.png', selectedIconPath: 'assets/tab-me-active.png' }
    ]
  },
  sitemapLocation: 'sitemap.json',
  lazyCodeLoading: 'requiredComponents'
}

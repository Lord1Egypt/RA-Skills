// Jest 测试环境初始化

// 模拟环境变量
process.env.WECHAT_MP_APP_ID = 'test_app_id';
process.env.WECHAT_MP_APP_SECRET = 'test_app_secret';
process.env.WECHAT_MP_DEFAULT_AUTHOR = 'Test Author';

// 模拟 console.warn 减少测试噪音
global.console.warn = jest.fn();
global.console.error = jest.fn();

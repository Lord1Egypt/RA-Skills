// ============ 请求封装说明 ============
// 微信小程序 wx.request 封装
//
// 切换 Mock/真实接口：
//   const IS_MOCK = true   // true=本地Mock数据，false=调用真实后端
//   const BASE_URL = 'https://api.example.com'
//
// 请求方法：
//   import { get, post, put, del } from '../utils/request'
//   get<T>('/api/xxx', data)
//   post<T>('/api/xxx', data)
//
// Mock 数据表格式：
//   const MOCK_HANDLERS = {
//     '/api/xxx': () => mockData,
//     '/api/yyy': (data) => ({ ...mockData, ...data }),
//   }

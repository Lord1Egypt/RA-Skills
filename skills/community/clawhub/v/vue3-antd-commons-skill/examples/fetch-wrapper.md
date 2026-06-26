# Fetch 网络请求工具封装及基础使用示例

## 1. 导入依赖

```typescript
import { message } from 'ant-design-vue'
```

## 2. 扩展fetch请求选项接口

```typescript
// 扩展fetch请求选项接口
interface FetchOptions extends RequestInit {
  baseURL?: string
  params?: Record<string, any>
  timeout?: number
}
```

## 3. 创建请求实例

```typescript
// 创建请求实例
const request = async (url: string, options: FetchOptions = {}) => {
  // 基础配置
  const baseURL = options.baseURL || import.meta.env.VITE_API_BASE_URL
  const timeout = options.timeout || 10000
  
  // 处理URL参数
  let fullURL = `${baseURL}${url}`
  if (options.params) {
    const params = new URLSearchParams()
    Object.entries(options.params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value))
      }
    })
    const paramsString = params.toString()
    if (paramsString) {
      fullURL += `?${paramsString}`
    }
  }
  
  // 请求头配置
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  
  // 添加认证token
  const token = localStorage.getItem('token')
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }
  
  // 创建AbortController处理超时
  const controller = new AbortController()
  const timeoutId = setTimeout(() => {
    controller.abort()
  }, timeout)
  
  try {
    // 发送请求
    const response = await fetch(fullURL, {
      ...options,
      headers,
      signal: controller.signal,
      // HTTPS特定配置
      credentials: import.meta.env.PROD ? 'same-origin' : 'include',
      redirect: 'follow'
    })
    
    clearTimeout(timeoutId)
    
    // 处理HTTP状态码
    handleHttpStatus(response)
    
    // 解析响应数据
    const data = await response.json()
    
    // 统一处理业务错误
    if (data.code !== 200) {
      message.error(data.message || '请求失败')
      throw new Error(data.message || '请求失败')
    }
    
    return data
  } catch (error) {
    clearTimeout(timeoutId)
    
    // 错误处理
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        message.error('请求超时，请重试')
      } else if (error.name === 'TypeError') {
        message.error('网络连接失败，请检查网络设置')
      } else {
        message.error(error.message || '网络请求失败')
      }
    } else {
      message.error('未知错误')
    }
    
    throw error
  }
}
```

## 4. HTTP状态码处理函数

```typescript
// HTTP状态码处理函数
const handleHttpStatus = (response: Response) => {
  const status = response.status
  
  switch (status) {
    case 200:
    case 201:
    case 202:
    case 204:
      // 成功状态码，无需处理
      break
    case 400:
      throw new Error('请求参数错误')
    case 401:
      // 未授权，清除token并跳转登录页
      localStorage.removeItem('token')
      message.error('登录已过期，请重新登录')
      window.location.href = '/login'
      throw new Error('登录已过期，请重新登录')
    case 403:
      throw new Error('无权限访问该资源')
    case 404:
      throw new Error('请求的资源不存在')
    case 405:
      throw new Error('请求方法不允许')
    case 429:
      throw new Error('请求过于频繁，请稍后再试')
    case 500:
      throw new Error('服务器内部错误')
    case 502:
      throw new Error('网关错误')
    case 503:
      throw new Error('服务器维护中，请稍后再试')
    case 504:
      throw new Error('网关超时')
    case 495:
      throw new Error('HTTPS证书错误')
    case 496:
      throw new Error('HTTPS证书过期')
    default:
      if (status >= 400 && status < 500) {
        throw new Error(`客户端错误：${status}`)
      } else if (status >= 500 && status < 600) {
        throw new Error(`服务器错误：${status}`)
      } else {
        throw new Error(`未知错误：${status}`)
      }
  }
}
```

## 5. 导出常用请求方法

```typescript
// 导出常用请求方法
export const get = <T = any>(url: string, params?: Record<string, any>, options?: FetchOptions): Promise<T> => {
  return request(url, { ...options, method: 'GET', params })
}

export const post = <T = any>(url: string, data?: any, options?: FetchOptions): Promise<T> => {
  return request(url, { ...options, method: 'POST', body: JSON.stringify(data) })
}

export const put = <T = any>(url: string, data?: any, options?: FetchOptions): Promise<T> => {
  return request(url, { ...options, method: 'PUT', body: JSON.stringify(data) })
}

export const del = <T = any>(url: string, options?: FetchOptions): Promise<T> => {
  return request(url, { ...options, method: 'DELETE' })
}
```

## 6. API接口封装

```typescript
// 基础使用示例
export const api = {
  // 用户相关API
  user: {
    login: (data: { username: string; password: string }) => 
      post('/auth/login', data),
      
    logout: () => 
      post('/auth/logout'),
      
    getList: (params?: { page?: number; size?: number }) => 
      get('/users', params),
      
    getDetail: (id: number) => 
      get(`/users/${id}`),
      
    create: (data: Omit<User, 'id'>) => 
      post('/users', data),
      
    update: (id: number, data: Partial<User>) => 
      put(`/users/${id}`, data),
      
    delete: (id: number) => 
      del(`/users/${id}`)
  },
  
  // 文章相关API
  article: {
    getList: (params?: { page?: number; size?: number; category?: string }) => 
      get('/articles', params),
      
    getDetail: (id: number) => 
      get(`/articles/${id}`)
  }
}
```

## 7. 类型定义

```typescript
// 类型定义
interface User {
  id: number
  username: string
  email: string
  name: string
  role: string
  status: number
  createdAt: string
  updatedAt: string
}
```

## 8. 在组件中使用示例

```typescript
// import { api } from '@/utils/request'
// import { ref } from 'vue'

// const users = ref<User[]>([])
// const loading = ref(false)

// const fetchUsers = async () => {
//   loading.value = true
//   try {
//     const data = await api.user.getList({ page: 1, size: 10 })
//     users.value = data.data
//   } catch (error) {
//     console.error('Failed to fetch users:', error)
//   } finally {
//     loading.value = false
//   }
// }

// fetchUsers()
```
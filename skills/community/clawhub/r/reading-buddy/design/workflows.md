# 核心交互流程图

## 1. 用户注册与登录流程

```mermaid
sequenceDiagram
    actor User as 用户
    participant Frontend as 前端应用
    participant Auth as 认证服务
    participant UserSvc as 用户服务
    participant DB as 数据库

    User->>Frontend: 访问平台
    Frontend->>Auth: 检查本地token
    Auth-->>Frontend: token无效/不存在
    
    alt 新用户注册
        User->>Frontend: 点击注册
        Frontend->>User: 显示注册表单
        User->>Frontend: 填写用户名/邮箱/密码
        Frontend->>Auth: 提交注册请求
        Auth->>DB: 检查用户名/邮箱唯一性
        DB-->>Auth: 验证通过
        Auth->>DB: 创建用户记录
        Auth->>Frontend: 返回JWT token
        Frontend->>User: 注册成功，跳转首页
    else 现有用户登录
        User->>Frontend: 点击登录
        Frontend->>User: 显示登录表单
        User->>Frontend: 输入凭证
        Frontend->>Auth: 提交登录请求
        Auth->>DB: 验证凭证
        DB-->>Auth: 验证通过
        Auth->>Frontend: 返回JWT token
        Frontend->>User: 登录成功，跳转首页
    end
    
    Note over Frontend,User: 登录后状态
    Frontend->>UserSvc: 获取用户资料
    UserSvc->>DB: 查询用户信息
    DB-->>UserSvc: 返回用户数据
    UserSvc-->>Frontend: 返回完整用户对象
    Frontend->>User: 显示个性化首页
```

## 2. 创建读书室流程

```mermaid
flowchart TD
    Start[用户点击"创建读书室"] --> Step1{选择书目}
    
    Step1 --> Step1a[搜索书目]
    Step1a --> Step1b[选择已有书目]
    Step1 --> Step1c[创建新书目]
    
    Step1b --> Step2
    Step1c --> Step2[填写读书室详情]
    
    Step2 --> Step3[设置时间安排]
    Step3 --> Step4[配置成员权限]
    Step4 --> Step5[设置阅读节奏]
    
    Step5 --> Step6{预览确认}
    Step6 -->|确认创建| Step7[调用API创建房间]
    Step6 -->|返回修改| Step2
    
    Step7 --> Step8[创建成功]
    Step8 --> Step9[生成邀请链接]
    Step9 --> Step10[分享给好友]
    
    Step10 --> End[进入读书室管理界面]
    
    subgraph Step1 [书目选择]
        direction LR
        S1a[搜索] --> S1b[浏览分类] --> S1c[热门推荐]
    end
    
    subgraph Step2 [房间详情]
        direction LR
        S2a[房间名称] --> S2b[房间描述] --> S2c[封面图]
    end
    
    subgraph Step3 [时间安排]
        direction LR
        S3a[开始时间] --> S3b[结束时间] --> S3c[重复设置]
    end
```

## 3. 加入读书室流程

```mermaid
stateDiagram-v2
    [*] --> 浏览发现
    浏览发现 --> 查看详情: 点击感兴趣房间
    查看详情 --> 申请加入: 点击"加入"
    
    申请加入 --> 权限检查
    权限检查 --> 公开房间: 公开
    权限检查 --> 私密房间: 私密
    
    公开房间 --> 直接加入: 无需批准
    私密房间 --> 等待批准: 需要主持人批准
    
    直接加入 --> 进入房间: 成功加入
    等待批准 --> 批准通过: 主持人同意
    等待批准 --> 批准拒绝: 主持人拒绝
    批准通过 --> 进入房间
    批准拒绝 --> 浏览发现: 返回发现页
    
    进入房间 --> 阅读界面: 加载房间内容
    阅读界面 --> [*]: 退出房间
    
    note right of 浏览发现
        用户可通过：
        1. 首页推荐
        2. 书目详情页
        3. 好友分享链接
        4. 搜索功能
        发现读书室
    end note
```

## 4. 读书室内交流流程

```mermaid
sequenceDiagram
    actor UserA as 用户A
    participant FrontendA as 用户A前端
    participant WS as WebSocket服务
    participant ChatSvc as 聊天服务
    participant DB as 数据库
    participant FrontendB as 用户B前端
    actor UserB as 用户B

    Note over UserA,UserB: 用户A发送消息
    
    UserA->>FrontendA: 输入消息内容
    FrontendA->>FrontendA: 本地显示（优化体验）
    FrontendA->>WS: 发送message事件
    WS->>ChatSvc: 处理消息
    
    ChatSvc->>DB: 存储消息到MongoDB
    DB-->>ChatSvc: 存储成功
    ChatSvc->>ChatSvc: 敏感词过滤
    ChatSvc->>ChatSvc: 生成系统通知（如@某人）
    
    ChatSvc->>WS: 广播消息到房间
    
    par 推送给用户B
        WS->>FrontendB: 推送新消息
        FrontendB->>UserB: 显示新消息通知
        UserB->>FrontendB: 查看消息
        FrontendB->>WS: 发送已读回执
    and 推送给其他在线用户
        WS->>其他前端: 推送新消息
    end
    
    Note over ChatSvc,DB: 消息持久化与推送解耦
```

## 5. 阅读进度同步流程

```mermaid
graph TD
    A[用户开始阅读] --> B[前端记录阅读时间]
    B --> C{到达进度同步点}
    
    C -->|是| D[更新本地进度]
    D --> E[检查网络连接]
    
    E --> F{在线}
    F -->|是| G[立即同步到服务器]
    F -->|否| H[本地缓存等待]
    
    G --> I[服务器接收进度]
    I --> J[更新房间总进度]
    J --> K[广播进度更新]
    K --> L[其他成员收到更新]
    
    H --> M[用户恢复网络]
    M --> N[同步缓存进度]
    N --> G
    
    subgraph "进度同步策略"
        P1[每阅读5页同步一次]
        P2[每5分钟同步一次]
        P3[章节结束时同步]
        P4[手动点击"更新进度"]
    end
    
    C --> P1
    C --> P2
    C --> P3
    C --> P4
```

## 6. 房间生命周期管理

```mermaid
gantt
    title 读书室生命周期
    dateFormat YYYY-MM-DD
    axisFormat %m/%d
    
    section 筹备期
    创建房间 :crit, 2026-03-01, 2d
    成员招募 :2026-03-02, 3d
    预备讨论 :2026-03-03, 2d
    
    section 进行期
    阅读阶段1 :active, 2026-03-05, 4d
    中途讨论 :2026-03-07, 1d
    阅读阶段2 :2026-03-08, 4d
    
    section 结束期
    最终讨论 :2026-03-12, 2d
    心得分享 :2026-03-13, 2d
    房间归档 :2026-03-14, 1d
    数据导出 :2026-03-15, 2d
```

## 7. 异常处理流程

```mermaid
flowchart TD
    Start[用户操作] --> Try[尝试执行]
    Try --> Success{成功?}
    
    Success -->|是| Normal[正常流程]
    
    Success -->|否| Error[发生错误]
    Error --> ErrorType{错误类型}
    
    ErrorType --> NetworkError[网络错误]
    ErrorType --> AuthError[认证错误]
    ErrorType --> PermissionError[权限错误]
    ErrorType --> DataError[数据错误]
    ErrorType --> SystemError[系统错误]
    
    NetworkError --> RetryNetwork[自动重试3次]
    RetryNetwork --> StillFail{仍然失败?}
    StillFail -->|是| ShowOffline[显示离线模式]
    StillFail -->|否| Resume[恢复正常]
    
    AuthError --> RedirectLogin[跳转登录页]
    RedirectLogin --> AfterLogin[登录后返回原页面]
    
    PermissionError --> ShowPermissionDenied[显示权限不足提示]
    ShowPermissionDenied --> SuggestAction[建议联系主持人]
    
    DataError --> ValidateData[数据验证]
    ValidateData --> ShowValidationError[显示具体错误]
    ShowValidationError --> AllowEdit[允许用户修改]
    
    SystemError --> LogError[记录错误日志]
    LogError --> ShowFriendlyMessage[显示友好错误页]
    ShowFriendlyMessage --> ProvideSupport[提供客服联系]
    
    ShowOffline --> SyncWhenOnline[网络恢复时同步]
```

## 关键交互原则

### 1. 实时反馈原则
- 所有用户操作应在100ms内得到视觉反馈
- 网络请求需显示加载状态
- 成功/失败有明确提示

### 2. 渐进式交互
- 复杂操作分步引导
- 提供默认值减少用户输入
- 支持撤销/重做

### 3. 上下文感知
- 根据用户角色显示不同界面
- 根据设备类型优化布局
- 根据网络状况调整功能

### 4. 无障碍设计
- 支持键盘导航
- 提供足够的颜色对比度
- 支持屏幕阅读器
- 文字大小可调整

---

*交互设计以用户体验为核心，确保流程直观、高效、愉悦*
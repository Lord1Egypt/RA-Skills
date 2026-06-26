## session.json

key|type|说明
---|---|---
debugPort|int|chrome 调试端口
userDataDir|string|chrome 用户数据目录
createdTime|string|创建时间,格式:yyyy-MM-dd HH:mm:ss
account|string|登陆账号(手机号)
employeeName|string|员工姓名
progress|object|学习进度跟踪,如果为空表示没有学习进度
progress.subjects|array[object]|课程类学习进度清单,每个对象定义参考`subject定义`
completed|boolean|是否已经全部完成(所有course和subject下的course都完成即完成)
monitor_status|string|学习监控状态, `normal`:`正常`, `error_need_login`:`错误-需要重新登录`
last_monitor_time|string|上次学习监控时间,格式:yyyy-MM-dd HH:mm:ss

- 举例
```json
{
  "debugPort": 42222,
  "userDataDir": "/tmp/wangda/wangda-study-user-data",
  "createdTime": "2026-03-21 14:29:26",
  "account":"13701701700",
  "employeeName":"张三",
  "progress":{
    "subjects":[
        //{#subject1...},
        //{#subject2...}
    ]
  }
}
```

### subject定义
key|type|说明
---|---|---
id|string|课程id
name|string|课程中文名称
url|string|课程url地址
completed|boolean|是否已经完成(所有course完成即完成)
subjects|array[object]|课程下的子课程,每个对象定义参考`subject定义`
courses|array[object]|课程下的课件学习进度列表,每个对象定义参考`course定义`

### course定义
key|type|说明
---|---|---
id|string|课件id
name|string|课件中文名称
url|string|课件url地址  
completed|boolean|是否已经完成(所有chapter完成即完成)
chapters|array[object]|课件章节列表,每个对象定义参考`course.chapter定义`

### course.chapter定义
key|type|说明
---|---|---
idx|int|章节序号(从1开始计数)
name|string|章节名称
type|string|课件类型,`video`或`doc`
status|string|章节学习进度状态, `not_start`:"未开始", `in_progress`:"学习中", `completed`:"已完成"



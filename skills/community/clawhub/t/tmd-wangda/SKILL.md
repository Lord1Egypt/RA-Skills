---
name: tmd-wangda
description: 帮助用户完成中移网大(https://wangda.chinamobile.com)相关课程的学习,当用户需要学习网大课程(例如学习新课程，查询学习进度或终止学习等)或用户提供的url域名是(wangda.chinamobile.com)时使用此技能
---


## 领域知识
### 课程(subject) 
  课程由一个或多个课件组成(部分课程可能还包含子课程),课件分为选修和必修两种,完成所有必修课件即可

### 课件(course)
  课件可能有多个小节(chapter),每个小节的内容形态可能是视频类或文档类,完成所有小节的学习后，该课件就算完成学习

### session
  保留用户当前学习进度的文件，具体参考 `references/schemas.md`中session.json的定义

<br/>
<br/>


## 参考信息

### 工具指令清单
  所有可用工具指令请参考 `references/tools.md`，所有指令都应该通过 `python scripts/tools.py <command> <args>`的形式调用

### session信息说明
  参考 `references/schemas.md`

<br/>
<br/>

## 核心功能

### 1. 跟踪当前学习的课程进度
  - 使用工具指令`get-session`指令,获取session中progress字段，总结学习进度,如果没有progress信息，则让用户提供课程地址，开始新的课程学习
  - 如果尚未全部完成,使用工具指令`start-auto-study`继续学习
  - 如果已经全部完成,则把progress总结一下，提示用户当前课程已经全部学完，是否要开始新的课程学习

### 2.开始(添加)新的课程学习
  - 获取现有的session信息,如果session信息且包含employeeName非空，需要与用户确认如下信息
    1. 是否继续使用该账号学习,如需要更换账号，则需要重新登录
    2. 总结一下progress信息(如果有)，询问用户是需要在现有的progress添加新的课程，还是中断现有的学习(可以使用`stop-study`指令来中断学习)
  - 根据用户提供的课程url地址，使用工具脚本`add-subject`指令添加待学习课程
  - 使用工具脚本`start-auto-study`指令还是挂机学习
  

<br/>
<br/>

## 其他功能

### 1. 如何登录
  - 有2种情况需要重新登录:
    1. 进入课程或课件页后，浏览器自动重定向到了登录页面，说明需要重新登录
    2. 用户希望使用非session中存储的账号进行学习,此时需要重新登录新账号，并在开始登录前，先使用工具指令`reset-session`指令重置session
  - 具体登录方式如下:
    - 使用工具指令`enter-login-page`进入登录页
    - 使用工具指令`fill-phone`完成登录手机号填写和发送短信验证码流程
    - 使用工具指令`fill-sms-code`填写短验,并完成登录
    - 登录成功后，使用指令`update-employee-name`更新session中的员工姓名
    
### 2. 中断现有的所有学习课程
  只有当用户明确要求 `清理/中断/终止` 现有的课程学习时才使用该功能(使用工具指令`clear`实现)
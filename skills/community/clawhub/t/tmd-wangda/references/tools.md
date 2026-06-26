## 工具运行环境要求
- 确定本地已经安装python 3.12+
- 根据`.env`中`_WANGDA_PYTHON_VENV_DIR`激活python虚拟环境
- 确保环境中已经安装了如下的lib
    1. websocket
    2. dotenv
- 确保用户已经安装了chrome浏览器,且启动路径与`.env`中`_WANGDA_CHROME_PATH`一致

## 工具指令说明 `scripts/tools.py`

- 调用方式: `python ${path}/tools.py <cmd> <args>`

### 主要指令说明

指令|功能|参数|输出说明
---|---|---|---
get-session `<key>`|获取现有session的完整信息,或某个字段的信息|key(可选)|完整session或某个字段的信息|
reset-session|重置session|无|重置后的session完整内容|
add-subject `<subject-url>`|向session的progress中添加新的待学习课程信息|subject-url(必填)|在progress添加的subject的信息
start-auto-study|开始自动学习,按顺序找到第一个尚未完成的课件(课程`subject`下的课件`course`),开始学习(添加操作系统的定时任务)|无|目前正在学习的课件(course)信息
stop-study|停止学习(清空session中的progress信息,删除操作系统的定时任务)|无|无|
monitor-hook|用于被定时调用的学习监控钩子(每次调用会检查 1.登录状态是否失效 2.更新学习进度 3.如果当前课件已经学完，自动进入下一个课件学习)|无|无|
clear|中断现有的学习,包括删除session问价/删除监控任务/关闭浏览器|无|无|


### 登录相关指令说明

指令|功能|参数|输出说明
---|---|---|---
enter-login-page|进入登录页面|无|无
fill-phone `<phone_number>`|填充手机号至登录页面,并发送验证码|phone_number(必填)|发送验证码成功或失败
fill-sms-code `<code_number>`|填充验证码至登录页面,并尝试登录|code_number(必填)|登录成功或失败
update-employee-name|分析网大的用户信息页，自动更新session中的employeeName|无|返回抓取到的的员工姓名



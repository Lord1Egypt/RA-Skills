
---
name: token-saver-for-programmer
display_name: Token Saver — Cut 40%–60% Tokens (Auto)
version: 1.0.6
description: Auto minify code, compress logs, clean configs, optimize prompts — save 40%~60% tokens without losing logic.
author: JhoneMingyoung
tags: programmer,token,code,minify,compress,prompt
auto_activates: [code,log,config,prompt]
---

# Token Saver For Programmer
A professional AI helper for developers to cut token consumption efficiently.

## 🚀 Features
- Minify source code: remove blank lines and useless comments, keep core logic
- Compress error logs and stack traces
- Clean up JSON / YAML configuration files
- Optimize technical prompts to be concise and standard
- Keep all key details unchanged, no logic loss

## 📌 Usage
### 1. Auto Trigger
Send code, logs, configs or prompts directly. The skill will activate automatically.

### 2. Command Trigger
```
/token-saver-for-programmer [your content]
```

### 🎯 Applicable Scenarios
Best for: Cursor / Claude Code / Copilot / Gemini CLI — all mainstream AI coding tools.

### ⚠️ Important Notes
- This tool optimizes and minifies code, logs, configs and prompts to cut token usage.
- Core logic is fully preserved, while tiny details and conditional logic may differ in edge cases.
- Please manually verify all outputs before official use.

## 🛡️ Safety & Compliance
- Runs locally only, no code execution, no credential access, no data collection and no external network calls.
- Focused on token-saving compression; core content unchanged with possible minor detail differences.
- Strictly review optimized content before applying to formal projects and production environments.

## 📝 Demo 1: Redundant Code Minify
### Original Input (Redundant)
```python
# User login interface
# Author: xxx
# Date: 2026-05-08

def user_login(username, password):
    # Check username
    if username == None or username.strip() == "":
        return {"code": 400, "msg": "Username cannot be empty"}
    
    # Check password
    if password == None or password.strip() == "":
        return {"code": 400, "msg": "Password cannot be empty"}

    # Query user info
    user_info = db.query_user(username)
    if not user_info:
        return {"code": 404, "msg": "User not found"}
    
    # Check password
    if user_info["pwd"] != password:
        return {"code": 401, "msg": "Wrong password"}

    # Generate token
    token = generate_token(user_info["id"])
    return {"code": 200, "data": token, "msg": "Login success"}
```
### Optimized Output
```
def user_login(username, password):
    if not username or username.strip() == "":
        return {"code":400,"msg":"Username cannot be empty"}
    if not password or password.strip() == "":
        return {"code":400,"msg":"Password cannot be empty"}
    user_info = db.query_user(username)
    if not user_info:
        return {"code":404,"msg":"User not found"}
    if user_info["pwd"] != password:
        return {"code":401,"msg":"Wrong password"}
    token = generate_token(user_info["id"])
    return {"code":200,"data":token,"msg":"Login success"}
```
### Token Saved: ~38%

## 📝 Demo 2: Long Error Log Compress
### Original Input
```
2026-05-08 10:20:35.123 INFO [main] StartupInfo - Service starting...
2026-05-08 10:20:36.456 INFO [main] ConfigLoader - Loading config application.yml
2026-05-08 10:20:38.789 ERROR [http-nio-8080-exec-3] com.service.UserService - Business exception
java.lang.NullPointerException: Cannot invoke method getUserId() on null object
at com.service.UserService.login(UserService.java:45)
at com.controller.UserController.login(UserController.java:22)
at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
```
### Optimized Output
```
Error: NullPointerException
Message: Cannot invoke method getUserId() on null object
Key code lines:
com.service.UserService.login(UserService.java:45)
com.controller.UserController.login(UserController.java:22)
```
### Token Saved: ~57%

## 📝 Demo 3: Technical Question Optimize
### Original Input
I am writing an API with Python. It works fine locally, but shows CORS error after deploying to the server. I have already modified the configuration file and added CORS annotations, but it still does not work. Please help me analyze possible causes and solutions.
### Optimized Output
Python API works locally but reports CORS on server. Config modified & CORS annotations added, still not working. Need causes and fix solutions.
### Token Saved: ~45%

## ⭐ Advantage
- Safe & lossless optimization
- Keep all logic & key info
- Save 40%~60% tokens
- AI runs faster & cheaper

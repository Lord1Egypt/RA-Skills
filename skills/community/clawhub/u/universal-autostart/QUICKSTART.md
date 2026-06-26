# 🚀 5 分钟快速开始

## 第一步：准备配置文件

复制示例配置并修改为你的需求：

```batch
:: Windows CMD
copy service_config.example.json my_config.json

:: 或使用 PowerShell
Copy-Item service_config.example.json my_config.json
```

然后用文本编辑器打开 `my_config.json`，修改以下关键信息：

```json
{
    "service_name": "你的服务名称",        // 👈 改成你想要的名字
    
    "program": {
        "path": "C:\\完整\\路径\\到程序.exe",  // 👈 改成你的程序路径
        "arguments": "--参数",                  // 👈 你的启动参数（没有可删除）
        "working_dir": "C:\\程序\\工作目录"     // 👈 程序所在目录
    }
}
```

## 第二步：安装自启动

右键点击 `install.bat` → **"以管理员身份运行"**

或者在终端执行：

```batch
python universal_service.py install my_config.json
```

## 第三步：验证是否成功

1. 打开「任务计划程序」
2. 找到名为 `你的服务名称` 的任务
3. 状态应该是"就绪"

---

就这么简单！✅

详细说明请查看 SKILL.md
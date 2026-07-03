# Unity CI Kit — 项目接入指南

## 1. 安装 CI Kit

将 `unity-ci-kit` skill 安装到 WorkBuddy 中。

## 2. 初始化项目

在 Unity 项目根目录运行：

```bash
python ci_agent.py init
```

生成 `ci_config.json`，编辑：

```json
{
    "unity_version": "2022.3.62f3c1",
    "unity_path": "",
    "execute_method": "YourNamespace.Editor.CiRunner.RunCI",
    "timeout_seconds": 600
}
```

`unity_path` 留空会自动搜索。如果不成功，填入 Unity.exe 绝对路径。

## 3. 添加 CiRunner 到项目

将 `templates/CiRunner.cs` 复制到项目的 `Assets/Editor/` 目录下，修改 `RunPipeline()` 填入你的构建步骤模板文件显示如下：

```csharp
private static bool RunPipeline()
{
    bool ok = true;
    ok &= Step("Setup",   () => { MySetup.Build();   return true; });
    ok &= Step("Validate",() => { MyTests.RunAll();   return TestPassed; });
    AssetDatabase.SaveAssets();
    return ok;
}
```

步骤方法约定：返回 `bool`，`true` = 成功。

## 4. 运行

```bash
# 环境检查
python ci_agent.py check

# 完整 CI 构建
python ci_agent.py build

# 仅编译检查（快速）
python ci_agent.py compile

# 读取上次结果
python ci_agent.py status
```

## 5. 跨电脑使用

在新电脑上：
1. 安装相同版本的 Unity
2. 克隆项目（含 `ci_config.json`）
3. `python ci_agent.py check` 验证环境
4. `python ci_agent.py build` 运行

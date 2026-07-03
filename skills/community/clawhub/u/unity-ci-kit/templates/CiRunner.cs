// CiRunner.cs — Unity 通用 CI Runner
// ==================================
// 放置于 Editor 目录下，在 ci_config.json 中配置 execute_method 指向此脚本。
//
// 每个项目写自己的 Step 方法，CiRunner 只提供 Step 框架和结果输出。
// 使用方式：
//   1. 复制此文件到项目的 Assets/_Project/Scripts/Editor/ 下
//   2. 在 CiRunnerStep.cs 中实现具体步骤
//   3. 在 ci_config.json 中设置 "execute_method": "YourNamespace.Editor.CiRunner.RunCI"
//
// 约定：
//   - 步骤方法必须返回 bool（true=成功）
//   - 步骤方法必须是 public static
//   - 所有步骤在 try-catch 中执行
//   - 输出 [AutoCI] RESULT: PASS/FAIL 给 ci_agent.py 解析

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System;

namespace UnityCI.Editor
{
    /// <summary>
    /// 通用 Unity CI Runner 基类。
    /// 提供 Step() 框架和 RunWithSteps()。
    /// 复制到项目后，在 RunCI() 中填入具体步骤。
    /// </summary>
    public static class CiRunner
    {
        /// <summary>
        /// CI 入口方法（供 batchmode -executeMethod 调用）
        /// </summary>
        public static void RunCI()
        {
            Debug.Log("========== Unity CI: Build Start ==========");
            bool allOk = RunPipeline();
            Debug.Log("========== Unity CI: Build End ==========");
            Debug.Log(allOk ? "[AutoCI] RESULT: PASS" : "[AutoCI] RESULT: FAIL");
            if (Application.isBatchMode) EditorApplication.Exit(allOk ? 0 : 1);
        }

        /// <summary>
        /// 替换此方法，填入项目的具体步骤。
        /// </summary>
        private static bool RunPipeline()
        {
            bool ok = true;

            // ---------- 示例步骤 ----------
            // ok &= Step("Asset Refresh", () => { AssetDatabase.Refresh(); return true; });
            // ok &= Step("Run Tests", () => RunUnitTests());
            // ---------------------------------

            // TODO: 在此填入项目专属步骤

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();
            return ok;
        }

        /// <summary>
        /// CI 步骤包装器：自动 try-catch + 日志输出
        /// </summary>
        /// <param name="name">步骤名称</param>
        /// <param name="action">步骤执行的代码</param>
        /// <returns>步骤是否成功</returns>
        public static bool Step(string name, Func<bool> action)
        {
            try
            {
                Debug.Log($"[AutoCI] STEP: {name}...");
                bool result = action();
                Debug.Log($"[AutoCI] STEP: {name} => {(result ? "OK" : "FAIL")}");
                return result;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[AutoCI] STEP: {name} => EXCEPTION: {ex.Message}");
                return false;
            }
        }
    }
}
#endif

# Unity3D Editor Bridge Script
# 这个脚本需要复制到Unity项目的 Editor/ 目录下
# 它启动一个本地HTTP服务器，接收OpenClaw控制命令

using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.Build.Reporting;
using UnityEngine;
using UnityEngine.SceneManagement;
using Object = UnityEngine.Object;

namespace OpenClaw.UnityBridge
{
    /// <summary>
    /// OpenClaw Unity 编辑器桥接 - 让AI能控制Unity编辑器
    /// </summary>
    [InitializeOnLoad]
    public class UnityBridge : EditorWindow
    {
        private static HttpListener _listener;
        private static Thread _serverThread;
        private static bool _isRunning = false;
        private static int _port = 18765;
        private static StringBuilder _logBuffer = new StringBuilder();

        // 菜单入口
        [MenuItem("Tools/OpenClaw Unity Bridge/Start Server")]
        public static void StartServer()
        {
            if (_isRunning)
            {
                Debug.Log("[OpenClaw] Server already running on port " + _port);
                return;
            }

            _port = EditorPrefs.GetInt("OpenClaw_Bridge_Port", 18765);
            _serverThread = new Thread(RunServer);
            _serverThread.IsBackground = true;
            _serverThread.Start();

            _isRunning = true;
            Debug.Log($"[OpenClaw] Bridge server started on port {_port}");
        }

        [MenuItem("Tools/OpenClaw Unity Bridge/Stop Server")]
        public static void StopServer()
        {
            if (!_isRunning) return;
            _isRunning = false;
            _listener?.Stop();
            Debug.Log("[OpenClaw] Bridge server stopped");
        }

        [MenuItem("Tools/OpenClaw Unity Bridge/Status")]
        public static void ShowStatus()
        {
            EditorUtility.DisplayDialog(
                "OpenClaw Unity Bridge",
                $"Status: {(_isRunning ? "Running" : "Stopped")}\nPort: {_port}\nProjects: {GetActiveProjectPath()}",
                "OK"
            );
        }

        private static void RunServer()
        {
            try
            {
                _listener = new HttpListener();
                _listener.Prefixes.Add($"http://localhost:{_port}/");
                _listener.Start();

                while (_isRunning)
                {
                    try
                    {
                        var context = _listener.GetContext();
                        ProcessRequest(context);
                    }
                    catch (HttpListenerException)
                    {
                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[OpenClaw] Server error: {ex.Message}");
            }
        }

        private static void ProcessRequest(HttpListenerContext context)
        {
            var request = context.Request;
            var response = context.Response;

            string result = "{}";
            int statusCode = 200;

            try
            {
                switch (request.Url.AbsolutePath.ToLower())
                {
                    case "/api/ping":
                        result = JsonUtility.ToJson(new { status = "ok", project = GetActiveProjectPath(), unityVersion = Application.unityVersion });
                        break;

                    case "/api/scene/list":
                        result = ListScenes();
                        break;

                    case "/api/scene/current":
                        result = GetCurrentSceneInfo();
                        break;

                    case "/api/scene/open":
                        var scenePath = GetQueryParam(request, "path");
                        result = OpenScene(scenePath);
                        break;

                    case "/api/gameobject/list":
                        result = ListGameObjects();
                        break;

                    case "/api/gameobject/create":
                        var objName = GetQueryParam(request, "name") ?? "New GameObject";
                        result = CreateGameObject(objName);
                        break;

                    case "/api/gameobject/delete":
                        var delName = GetQueryParam(request, "name");
                        result = DeleteGameObject(delName);
                        break;

                    case "/api/script/create":
                        var scriptName = GetQueryParam(request, "name");
                        var scriptContent = request.InputStream != null ? new StreamReader(request.InputStream).ReadToEnd() : "";
                        result = CreateScript(scriptName, scriptContent);
                        break;

                    case "/api/build":
                        var target = GetQueryParam(request, "target") ?? "StandaloneWindows64";
                        var outputPath = GetQueryParam(request, "output") ?? "Builds";
                        result = BuildProject(target, outputPath);
                        break;

                    case "/api/logs":
                        result = GetLogs();
                        break;

                    case "/api/play":
                        result = TogglePlayMode(true);
                        break;

                    case "/api/stop":
                        result = TogglePlayMode(false);
                        break;

                    default:
                        result = JsonUtility.ToJson(new { error = "unknown_endpoint", path = request.Url.AbsolutePath });
                        statusCode = 404;
                        break;
                }
            }
            catch (Exception ex)
            {
                result = JsonUtility.ToJson(new { error = ex.Message });
                statusCode = 500;
            }

            var buffer = Encoding.UTF8.GetBytes(result);
            response.StatusCode = statusCode;
            response.ContentType = "application/json; charset=utf-8";
            response.ContentLength64 = buffer.Length;
            response.OutputStream.Write(buffer, 0, buffer.Length);
            response.OutputStream.Close();
        }

        // ----- API Handlers -----

        private static string GetActiveProjectPath()
        {
            var dataPath = Application.dataPath;
            return dataPath?.Replace("/Assets", "");
        }

        private static string ListScenes()
        {
            var scenes = new List<string>();
            for (int i = 0; i < SceneManager.sceneCount; i++)
            {
                scenes.Add(SceneManager.GetSceneAt(i).path);
            }
            // 也列出Build Settings中的场景
            var buildScenes = EditorBuildSettings.scenes
                .Where(s => s.enabled)
                .Select(s => s.path)
                .ToList();
            return JsonUtility.ToJson(new { openScenes = scenes.ToArray(), buildSettings = buildScenes.ToArray() });
        }

        private static string GetCurrentSceneInfo()
        {
            var scene = SceneManager.GetActiveScene();
            var gameObjects = scene.GetRootGameObjects();
            var objList = gameObjects.Select(g => new { name = g.name, active = g.activeSelf, children = CountChildren(g), components = g.GetComponents<Component>().Length }).ToList();
            return JsonUtility.ToJson(new { name = scene.name, path = scene.path, isDirty = scene.isDirty, rootCount = gameObjects.Length, objects = objList });
        }

        private static string OpenScene(string path)
        {
            if (string.IsNullOrEmpty(path) || !File.Exists(path))
                return JsonUtility.ToJson(new { error = "scene_not_found", path });

            EditorSceneManager.OpenScene(path);
            return JsonUtility.ToJson(new { success = true, path });
        }

        private static string ListGameObjects()
        {
            var scene = SceneManager.GetActiveScene();
            var roots = scene.GetRootGameObjects();
            var list = roots.Select(r => new { name = r.name, active = r.activeSelf, tag = r.tag, layer = r.layer, position = r.transform.position.ToString(), children = CountChildren(r) });
            return JsonUtility.ToJson(new { count = roots.Length, objects = list });
        }

        private static string CreateGameObject(string name)
        {
            var go = new GameObject(name);
            Undo.RegisterCreatedObjectUndo(go, $"Create {name}");
            Selection.activeGameObject = go;
            return JsonUtility.ToJson(new { success = true, name, instanceId = go.GetInstanceID() });
        }

        private static string DeleteGameObject(string name)
        {
            if (string.IsNullOrEmpty(name))
                return JsonUtility.ToJson(new { error = "name_required" });

            var go = GameObject.Find(name);
            if (go == null)
                return JsonUtility.ToJson(new { error = "not_found", name });

            Undo.DestroyObjectImmediate(go);
            return JsonUtility.ToJson(new { success = true, name });
        }

        private static string CreateScript(string name, string content)
        {
            if (string.IsNullOrEmpty(name))
                return JsonUtility.ToJson(new { error = "name_required" });

            var path = $"Assets/Scripts/{name}.cs";
            if (string.IsNullOrEmpty(content))
            {
                content = $@"using UnityEngine;

public class {name} : MonoBehaviour
{{
    void Start()
    {{
        // Auto-generated by OpenClaw
    }}

    void Update()
    {{
        
    }}
}}";
            }

            Directory.CreateDirectory(Path.GetDirectoryName(path));
            File.WriteAllText(path, content);
            AssetDatabase.Refresh();

            return JsonUtility.ToJson(new { success = true, path });
        }

        private static string BuildProject(string target, string outputPath)
        {
            BuildTarget buildTarget;
            if (!Enum.TryParse(target, out buildTarget))
                buildTarget = BuildTarget.StandaloneWindows64;

            var options = new BuildPlayerOptions
            {
                scenes = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).ToArray(),
                locationPathName = outputPath,
                target = buildTarget,
                options = BuildOptions.None
            };

            var report = BuildPipeline.BuildPlayer(options);
            return JsonUtility.ToJson(new { 
                success = report.summary.result == BuildResult.Succeeded,
                result = report.summary.result.ToString(),
                totalTime = report.summary.totalTime.ToString(),
                totalErrors = report.summary.totalErrors,
                totalWarnings = report.summary.totalWarnings,
                outputPath
            });
        }

        private static string TogglePlayMode(bool play)
        {
            EditorApplication.isPlaying = play;
            return JsonUtility.ToJson(new { success = true, playing = EditorApplication.isPlaying });
        }

        private static string GetLogs()
        {
            var logs = _logBuffer.ToString();
            return JsonUtility.ToJson(new { logs });
        }

        // ----- Helpers -----

        private static string GetQueryParam(HttpListenerRequest request, string key)
        {
            var query = request.Url.ParseQueryString();
            return query[key];
        }

        private static int CountChildren(GameObject go)
        {
            int count = 0;
            foreach (Transform child in go.transform)
            {
                count += 1 + CountChildren(child.gameObject);
            }
            return count;
        }
    }
}

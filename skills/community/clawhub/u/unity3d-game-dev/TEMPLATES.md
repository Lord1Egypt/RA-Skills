# Unity C# 代码模板库

## 1. 基础玩家控制器 (PlayerController.cs)
```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [Header("移动参数")]
    public float moveSpeed = 5f;
    public float jumpForce = 8f;
    public float gravity = 20f;

    [Header("相机")]
    public Camera playerCamera;
    public float mouseSensitivity = 2f;
    public float maxLookAngle = 80f;

    private CharacterController controller;
    private Vector3 velocity;
    private float verticalRotation = 0f;
    private bool isGrounded;

    void Start()
    {
        controller = GetComponent<CharacterController>();
        if (playerCamera == null)
            playerCamera = Camera.main;
        
        Cursor.lockState = CursorLockMode.Locked;
    }

    void Update()
    {
        HandleMovement();
        HandleLook();
    }

    void HandleMovement()
    {
        isGrounded = controller.isGrounded;
        if (isGrounded && velocity.y < 0)
            velocity.y = -2f;

        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        Vector3 move = transform.right * horizontal + transform.forward * vertical;
        controller.Move(move * moveSpeed * Time.deltaTime);

        if (Input.GetButtonDown("Jump") && isGrounded)
            velocity.y = Mathf.Sqrt(jumpForce * 2f * gravity);

        velocity.y -= gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);
    }

    void HandleLook()
    {
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;

        verticalRotation -= mouseY;
        verticalRotation = Mathf.Clamp(verticalRotation, -maxLookAngle, maxLookAngle);
        playerCamera.transform.localRotation = Quaternion.Euler(verticalRotation, 0, 0);
        transform.Rotate(Vector3.up * mouseX);
    }
}
```

## 2. 对象池管理器 (ObjectPool.cs)
```csharp
using System.Collections.Generic;
using UnityEngine;

public class ObjectPool : MonoBehaviour
{
    [System.Serializable]
    public class Pool
    {
        public string tag;
        public GameObject prefab;
        public int size = 10;
    }

    public static ObjectPool Instance;
    public List<Pool> pools;
    public Dictionary<string, Queue<GameObject>> poolDictionary;

    void Awake()
    {
        Instance = this;
        poolDictionary = new Dictionary<string, Queue<GameObject>>();

        foreach (var pool in pools)
        {
            Queue<GameObject> objectPool = new Queue<GameObject>();
            for (int i = 0; i < pool.size; i++)
            {
                GameObject obj = Instantiate(pool.prefab);
                obj.SetActive(false);
                objectPool.Enqueue(obj);
            }
            poolDictionary.Add(pool.tag, objectPool);
        }
    }

    public GameObject Spawn(string tag, Vector3 position, Quaternion rotation)
    {
        if (!poolDictionary.ContainsKey(tag))
            return null;

        GameObject obj = poolDictionary[tag].Dequeue();
        obj.SetActive(true);
        obj.transform.position = position;
        obj.transform.rotation = rotation;
        poolDictionary[tag].Enqueue(obj);
        return obj;
    }
}
```

## 3. 单例基类 (Singleton.cs)
```csharp
using UnityEngine;

public abstract class Singleton<T> : MonoBehaviour where T : Component
{
    private static T _instance;

    public static T Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = FindObjectOfType<T>();
                if (_instance == null)
                {
                    GameObject obj = new GameObject(typeof(T).Name);
                    _instance = obj.AddComponent<T>();
                }
            }
            return _instance;
        }
    }

    protected virtual void Awake()
    {
        if (_instance == null)
        {
            _instance = this as T;
            DontDestroyOnLoad(gameObject);
        }
        else if (_instance != this)
        {
            Destroy(gameObject);
        }
    }
}
```

## 4. 音频管理器 (AudioManager.cs)
```csharp
using System;
using UnityEngine;

public class AudioManager : Singleton<AudioManager>
{
    public Sound[] sounds;

    protected override void Awake()
    {
        base.Awake();
        foreach (Sound s in sounds)
        {
            s.source = gameObject.AddComponent<AudioSource>();
            s.source.clip = s.clip;
            s.source.volume = s.volume;
            s.source.pitch = s.pitch;
            s.source.loop = s.loop;
        }
    }

    public void Play(string name)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null) return;
        s.source.Play();
    }

    public void Stop(string name)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null) return;
        s.source.Stop();
    }

    [System.Serializable]
    public class Sound
    {
        public string name;
        public AudioClip clip;
        [Range(0f, 1f)] public float volume = 1f;
        [Range(0.1f, 3f)] public float pitch = 1f;
        public bool loop = false;
        [HideInInspector] public AudioSource source;
    }
}
```

## 5. 简单状态机 (StateMachine.cs)
```csharp
using System;
using UnityEngine;

public class StateMachine : MonoBehaviour
{
    private BaseState currentState;

    void Update() => currentState?.Update();

    public void SwitchState(BaseState newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState.Enter();
    }
}

public abstract class BaseState
{
    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}
```

## 6. 场景加载管理器 (SceneLoader.cs)
```csharp
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class SceneLoader : MonoBehaviour
{
    public static SceneLoader Instance;
    public GameObject loadingScreen;
    public Slider progressBar;
    public Text loadingText;

    void Awake() => Instance = this;

    public void LoadScene(string sceneName)
    {
        StartCoroutine(LoadSceneAsync(sceneName));
    }

    IEnumerator LoadSceneAsync(string sceneName)
    {
        if (loadingScreen != null)
            loadingScreen.SetActive(true);

        AsyncOperation operation = SceneManager.LoadSceneAsync(sceneName);

        while (!operation.isDone)
        {
            float progress = Mathf.Clamp01(operation.progress / 0.9f);
            if (progressBar != null) progressBar.value = progress;
            if (loadingText != null) loadingText.text = $"{progress * 100:F0}%";
            yield return null;
        }
    }
}
```

## 7. 性能分析工具 (ProfilerTool.cs)
```csharp
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using UnityEngine;
using Debug = UnityEngine.Debug;

public static class ProfilerTool
{
    private static Dictionary<string, Stopwatch> timers = new Dictionary<string, Stopwatch>();

    public static void StartTimer(string name)
    {
        if (!timers.ContainsKey(name))
            timers[name] = new Stopwatch();
        timers[name].Reset();
        timers[name].Start();
    }

    public static void StopTimer(string name)
    {
        if (timers.ContainsKey(name))
        {
            timers[name].Stop();
            Debug.Log($"[Profiler] {name}: {timers[name].ElapsedMilliseconds}ms");
        }
    }

    public static string GenerateReport()
    {
        StringBuilder sb = new StringBuilder();
        sb.AppendLine("=== Unity Profiler Report ===");
        sb.AppendLine($"FPS: {1f / Time.deltaTime:F1}");
        sb.AppendLine($"帧时间: {Time.deltaTime * 1000:F1}ms");
        sb.AppendLine($"TimeScale: {Time.timeScale}");
        sb.AppendLine($"对象数: {Object.FindObjectsOfType<GameObject>().Length}");
        return sb.ToString();
    }
}
```

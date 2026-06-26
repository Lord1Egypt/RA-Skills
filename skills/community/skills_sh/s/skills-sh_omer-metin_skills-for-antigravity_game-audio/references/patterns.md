# Game Audio Design & Implementation

## Patterns


---
  #### **Name**
Audio Manager Singleton
  #### **Description**
Centralized audio management with proper initialization and cleanup
  #### **When**
Setting up audio system architecture
  #### **Example**
    // Unity example - proper audio manager
    public class AudioManager : MonoBehaviour
    {
        public static AudioManager Instance { get; private set; }
    
        [SerializeField] private AudioMixerGroup masterGroup;
        [SerializeField] private AudioMixerGroup musicGroup;
        [SerializeField] private AudioMixerGroup sfxGroup;
        [SerializeField] private AudioMixerGroup ambientGroup;
    
        private AudioSourcePool sfxPool;
        private Dictionary<string, AudioClip> loadedClips;
    
        private void Awake()
        {
            if (Instance != null)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);
    
            InitializePools();
            LoadCriticalAudio();
        }
    
        private void InitializePools()
        {
            sfxPool = new AudioSourcePool(transform, sfxGroup, poolSize: 32);
        }
    }
    

---
  #### **Name**
Audio Source Pooling
  #### **Description**
Reuse AudioSources instead of creating/destroying them
  #### **When**
Playing frequent sound effects
  #### **Why**
Prevents GC allocation spikes and improves performance
  #### **Example**
    public class AudioSourcePool
    {
        private Queue<AudioSource> available;
        private List<AudioSource> active;
        private Transform parent;
        private AudioMixerGroup mixerGroup;
    
        public AudioSourcePool(Transform parent, AudioMixerGroup group, int poolSize)
        {
            this.parent = parent;
            this.mixerGroup = group;
            available = new Queue<AudioSource>(poolSize);
            active = new List<AudioSource>(poolSize);
    
            for (int i = 0; i < poolSize; i++)
            {
                CreateSource();
            }
        }
    
        public AudioSource Get()
        {
            AudioSource source;
            if (available.Count > 0)
            {
                source = available.Dequeue();
            }
            else
            {
                // Pool exhausted - steal oldest or expand
                source = StealOldestOrExpand();
            }
            active.Add(source);
            return source;
        }
    
        public void Return(AudioSource source)
        {
            source.Stop();
            source.clip = null;
            active.Remove(source);
            available.Enqueue(source);
        }
    }
    

---
  #### **Name**
Spatial Audio Setup
  #### **Description**
Configure 3D audio with proper falloff and spatialization
  #### **When**
Implementing positional audio in 3D games
  #### **Example**
    // FMOD example - 3D event setup
    FMOD.Studio.EventInstance CreateSpatialEvent(string eventPath, Vector3 position)
    {
        FMOD.Studio.EventInstance instance;
        FMODUnity.RuntimeManager.CreateInstance(eventPath, out instance);
    
        // Set 3D attributes
        FMOD.ATTRIBUTES_3D attributes = FMODUnity.RuntimeUtils.To3DAttributes(position);
        instance.set3DAttributes(attributes);
    
        // Configure spatializer
        instance.setParameterByName("Distance", 0f);
    
        return instance;
    }
    
    // Configure listener
    void UpdateListener(Transform listenerTransform)
    {
        FMODUnity.RuntimeManager.SetListenerLocation(
            0, // Listener index
            listenerTransform.position,
            listenerTransform.forward,
            listenerTransform.up
        );
    }
    

---
  #### **Name**
Adaptive Music System
  #### **Description**
Music that responds to gameplay states
  #### **When**
Implementing dynamic game music
  #### **Example**
    // State-based music system
    public class AdaptiveMusicSystem
    {
        private FMOD.Studio.EventInstance musicInstance;
        private string currentState;
    
        public void Initialize(string musicEventPath)
        {
            FMODUnity.RuntimeManager.CreateInstance(musicEventPath, out musicInstance);
            musicInstance.start();
        }
    
        public void SetGameState(GameState state)
        {
            // Transition music based on game state
            switch (state)
            {
                case GameState.Exploration:
                    SetMusicParameter("Intensity", 0f, transitionTime: 2f);
                    SetMusicParameter("Combat", 0f, transitionTime: 1f);
                    break;
    
                case GameState.Combat:
                    SetMusicParameter("Intensity", 1f, transitionTime: 0.5f);
                    SetMusicParameter("Combat", 1f, transitionTime: 0.3f);
                    break;
    
                case GameState.Boss:
                    SetMusicParameter("Intensity", 1f, transitionTime: 0.1f);
                    SetMusicParameter("BossPhase", 1f, transitionTime: 0f);
                    break;
            }
        }
    
        private void SetMusicParameter(string param, float value, float transitionTime)
        {
            // FMOD handles smooth transitions internally
            musicInstance.setParameterByName(param, value);
        }
    }
    

---
  #### **Name**
Audio Bus Architecture
  #### **Description**
Proper routing and mixing hierarchy
  #### **When**
Setting up audio mixing
  #### **Example**
    // Recommended bus hierarchy:
    // Master
    //   |- Music
    //   |    |- Music_Gameplay
    //   |    |- Music_Menu
    //   |
    //   |- SFX
    //   |    |- SFX_Player
    //   |    |- SFX_Enemies
    //   |    |- SFX_Environment
    //   |    |- SFX_UI
    //   |
    //   |- Voice
    //   |    |- Voice_Dialogue
    //   |    |- Voice_Barks
    //   |
    //   |- Ambient
    //        |- Ambient_World
    //        |- Ambient_Weather
    
    // Unity AudioMixer setup via code
    public void SetBusVolume(string exposedParam, float linearVolume)
    {
        // Convert linear (0-1) to decibels
        float db = linearVolume > 0.0001f
            ? 20f * Mathf.Log10(linearVolume)
            : -80f;
        audioMixer.SetFloat(exposedParam, db);
    }
    
    // Ducking system
    public void DuckForDialogue(bool duck)
    {
        float targetDb = duck ? -6f : 0f;
        StartCoroutine(FadeBus("MusicDuck", targetDb, 0.3f));
        StartCoroutine(FadeBus("SFXDuck", targetDb, 0.3f));
    }
    

---
  #### **Name**
Memory-Conscious Audio Loading
  #### **Description**
Strategic loading and unloading of audio assets
  #### **When**
Managing audio memory budget
  #### **Example**
    public class AudioAssetManager
    {
        private Dictionary<string, AudioClip> preloadedClips;
        private Dictionary<string, string> streamingPaths;
    
        // Preload critical, frequently-used sounds
        public async Task PreloadCriticalAudio()
        {
            string[] criticalSounds = {
                "Player/Footsteps",
                "Player/Jump",
                "UI/Click",
                "UI/Hover"
            };
    
            foreach (var path in criticalSounds)
            {
                var clip = await LoadClipAsync(path);
                preloadedClips[path] = clip;
            }
        }
    
        // Stream large files (music, long ambiences)
        public void RegisterStreamingAudio(string key, string path)
        {
            streamingPaths[key] = path;
        }
    
        // Unload scene-specific audio
        public void UnloadSceneAudio(string sceneName)
        {
            var keysToRemove = preloadedClips.Keys
                .Where(k => k.StartsWith($"Scenes/{sceneName}"))
                .ToList();
    
            foreach (var key in keysToRemove)
            {
                Resources.UnloadAsset(preloadedClips[key]);
                preloadedClips.Remove(key);
            }
        }
    }
    

---
  #### **Name**
Audio Occlusion System
  #### **Description**
Realistic sound blocking by geometry
  #### **When**
Implementing environmental audio realism
  #### **Example**
    public class AudioOcclusionSystem
    {
        private const int MAX_OCCLUSION_RAYS = 5;
        private LayerMask occlusionMask;
    
        public float CalculateOcclusion(Vector3 source, Vector3 listener)
        {
            float totalOcclusion = 0f;
    
            // Cast multiple rays for more accurate occlusion
            Vector3[] offsets = GetRayOffsets(source, listener);
    
            foreach (var offset in offsets)
            {
                Vector3 rayStart = source + offset;
                Vector3 direction = listener - rayStart;
                float distance = direction.magnitude;
    
                if (Physics.Raycast(rayStart, direction.normalized, out RaycastHit hit,
                    distance, occlusionMask))
                {
                    // Calculate occlusion based on material
                    float materialOcclusion = GetMaterialOcclusion(hit.collider);
                    totalOcclusion += materialOcclusion;
                }
            }
    
            return Mathf.Clamp01(totalOcclusion / MAX_OCCLUSION_RAYS);
        }
    
        public void ApplyOcclusion(FMOD.Studio.EventInstance instance, float occlusion)
        {
            // Apply low-pass filter and volume reduction
            instance.setParameterByName("Occlusion", occlusion);
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Creating AudioSources at Runtime
  #### **Description**
Instantiating and destroying AudioSources causes GC spikes
  #### **Why Bad**
Memory allocation during gameplay causes frame hitches
  #### **Fix**
Use audio source pooling - pre-allocate and reuse
  #### **Severity**
high

---
  #### **Name**
Loading All Audio Upfront
  #### **Description**
Loading every sound file at game start
  #### **Why Bad**
Excessive memory usage and long load times
  #### **Fix**
Categorize audio: preload critical, stream large, load on-demand
  #### **Severity**
high

---
  #### **Name**
Ignoring Platform Audio Limits
  #### **Description**
Not accounting for platform voice limits
  #### **Why Bad**
Mobile has 32-64 voices, console 128-256 - exceeding causes dropouts
  #### **Fix**
Implement voice stealing, priority systems, and virtualization
  #### **Severity**
high

---
  #### **Name**
Linear Volume Sliders
  #### **Description**
Using linear 0-1 values directly for volume
  #### **Why Bad**
Human hearing is logarithmic - linear feels wrong
  #### **Fix**
Convert to decibels: dB = 20 * log10(linear)
  #### **Severity**
medium

---
  #### **Name**
Hardcoded Audio References
  #### **Description**
Referencing audio clips directly in gameplay code
  #### **Why Bad**
Tight coupling, hard to iterate on sound design
  #### **Fix**
Use audio events/IDs, data-driven sound tables
  #### **Severity**
medium

---
  #### **Name**
No Audio Prioritization
  #### **Description**
All sounds treated equally
  #### **Why Bad**
Important sounds get drowned out or stolen
  #### **Fix**
Implement priority system - player > enemies > ambient
  #### **Severity**
medium

---
  #### **Name**
Uncompressed Audio in Builds
  #### **Description**
Shipping WAV or uncompressed audio
  #### **Why Bad**
Massive file sizes, memory waste
  #### **Fix**
Use appropriate compression: Vorbis for music, ADPCM for SFX
  #### **Severity**
high

---
  #### **Name**
Synchronous Audio Loading
  #### **Description**
Loading audio on main thread during gameplay
  #### **Why Bad**
Causes frame spikes and stuttering
  #### **Fix**
Use async loading, preload during transitions
  #### **Severity**
high
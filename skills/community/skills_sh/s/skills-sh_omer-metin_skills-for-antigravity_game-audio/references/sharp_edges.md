# Game Audio - Sharp Edges

## Audio Source Pool Exhaustion

### **Id**
audio-source-pooling-exhaustion
### **Severity**
critical
### **Symptoms**
  - Sounds randomly not playing
  - Audio cutting out during intense scenes
  - No errors but missing sound effects
  - Works in editor, fails on device
### **Cause**
  Audio source pool is exhausted because too many sounds play simultaneously.
  The pool silently fails to provide sources, or steals from playing sounds.
  
### **Detection**
  #### **Pattern**
new AudioSource|AddComponent<AudioSource>|Instantiate.*Audio
  #### **Context**
Runtime audio source creation instead of pooling
### **Fix**
  1. Pre-allocate audio source pool at startup
  2. Implement priority-based voice stealing
  3. Set maximum concurrent sounds per category
  4. Add pool exhaustion warnings in debug builds
  
  ```csharp
  // Priority-based voice stealing
  public AudioSource GetSource(AudioPriority priority)
  {
      if (available.Count > 0)
          return available.Dequeue();
  
      // Steal from lower priority
      var stealable = active
          .Where(s => s.priority < priority)
          .OrderBy(s => s.priority)
          .ThenBy(s => s.timeRemaining)
          .FirstOrDefault();
  
      if (stealable != null)
      {
          stealable.Stop();
          return stealable;
      }
  
      Debug.LogWarning($"Pool exhausted for priority {priority}");
      return null; // Or expand pool
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - pooling
  - performance
  - voice-management

## Spatial Audio Falloff Misconfiguration

### **Id**
spatial-audio-falloff-curves
### **Severity**
high
### **Symptoms**
  - 3D sounds too quiet or too loud
  - Sound doesn't fade with distance
  - Audio feels 'flat' or unrealistic
  - Sounds cut off abruptly at max distance
### **Cause**
  Default linear falloff doesn't match real-world acoustics.
  Min/max distance not tuned for game's scale.
  Rolloff mode doesn't match environment type.
  
### **Detection**
  #### **Pattern**
spatialBlend.*=.*1|rolloffMode.*=.*Linear|minDistance.*=.*1
  #### **Context**
Default spatial audio settings
### **Fix**
  1. Use logarithmic rolloff for realistic environments
  2. Tune min distance (sounds at full volume within this)
  3. Set max distance based on game scale
  4. Use custom curves for stylized games
  
  ```csharp
  // Configure spatial audio properly
  void ConfigureSpatialSource(AudioSource source, AudioType type)
  {
      source.spatialBlend = 1f; // Full 3D
  
      switch (type)
      {
          case AudioType.Gunshot:
              source.rolloffMode = AudioRolloffMode.Logarithmic;
              source.minDistance = 5f;   // Full volume within 5m
              source.maxDistance = 100f; // Inaudible beyond 100m
              source.spread = 30f;       // Directional
              break;
  
          case AudioType.Footstep:
              source.rolloffMode = AudioRolloffMode.Logarithmic;
              source.minDistance = 1f;
              source.maxDistance = 20f;
              source.spread = 60f;
              break;
  
          case AudioType.Ambient:
              source.rolloffMode = AudioRolloffMode.Linear;
              source.minDistance = 10f;
              source.maxDistance = 50f;
              source.spread = 180f; // Wide
              break;
      }
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - spatial
  - 3d-audio
  - configuration

## Audio Compression Quality Issues

### **Id**
compression-quality-tradeoffs
### **Severity**
high
### **Symptoms**
  - Metallic or 'underwater' sound quality
  - Audible artifacts on sustained notes
  - Looping audio has clicks/pops
  - Build size unexpectedly large
### **Cause**
  Wrong compression format or quality settings for audio type.
  Over-compression destroys quality, under-compression wastes memory.
  
### **Detection**
  #### **Pattern**
loadType.*DecompressOnLoad|compressionFormat.*PCM
  #### **Context**
Suboptimal audio import settings
### **Fix**
  Use format based on audio type:
  
  | Type | Format | Load Type | Quality |
  |------|--------|-----------|---------|
  | Music | Vorbis/AAC | Streaming | 70-100% |
  | Long Ambient | Vorbis | Streaming | 50-70% |
  | Short SFX | ADPCM | DecompressOnLoad | N/A |
  | Voice | Vorbis | CompressedInMemory | 70-85% |
  | Critical SFX | PCM | DecompressOnLoad | N/A |
  
  ```csharp
  // Unity AudioImporter settings example
  void ConfigureAudioImport(AudioImporter importer, AudioCategory category)
  {
      var settings = importer.defaultSampleSettings;
  
      switch (category)
      {
          case AudioCategory.Music:
              settings.loadType = AudioClipLoadType.Streaming;
              settings.compressionFormat = AudioCompressionFormat.Vorbis;
              settings.quality = 0.7f;
              break;
  
          case AudioCategory.ShortSFX:
              settings.loadType = AudioClipLoadType.DecompressOnLoad;
              settings.compressionFormat = AudioCompressionFormat.ADPCM;
              break;
  
          case AudioCategory.Voice:
              settings.loadType = AudioClipLoadType.CompressedInMemory;
              settings.compressionFormat = AudioCompressionFormat.Vorbis;
              settings.quality = 0.75f;
              break;
      }
  
      importer.defaultSampleSettings = settings;
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - compression
  - quality
  - optimization

## Audio Memory Exhaustion

### **Id**
audio-memory-management
### **Severity**
critical
### **Symptoms**
  - Out of memory crashes
  - Audio stops working mid-session
  - Performance degradation over time
  - Mobile app killed by OS
### **Cause**
  Audio clips not unloaded when no longer needed.
  DecompressOnLoad used for large files.
  Streaming audio not properly released.
  FMOD/Wwise banks not unloaded on scene change.
  
### **Detection**
  #### **Pattern**
Resources.Load<AudioClip>|AudioClip.Create|loadType.*DecompressOnLoad
  #### **Context**
Audio loading without corresponding unload
### **Fix**
  1. Track loaded audio assets
  2. Unload scene-specific audio on scene exit
  3. Use streaming for music and long ambiences
  4. Implement audio memory budget system
  
  ```csharp
  public class AudioMemoryManager
  {
      private long memoryBudget;
      private long currentUsage;
      private Dictionary<string, AudioClipHandle> loadedClips;
  
      public async Task<AudioClip> LoadClip(string path, bool persistent = false)
      {
          if (loadedClips.TryGetValue(path, out var handle))
          {
              handle.refCount++;
              return handle.clip;
          }
  
          var clip = await Resources.LoadAsync<AudioClip>(path) as AudioClip;
          long clipMemory = EstimateMemory(clip);
  
          // Check budget before loading
          while (currentUsage + clipMemory > memoryBudget)
          {
              if (!EvictLeastUsed())
              {
                  Debug.LogError($"Cannot load {path}: memory budget exceeded");
                  return null;
              }
          }
  
          loadedClips[path] = new AudioClipHandle(clip, persistent);
          currentUsage += clipMemory;
          return clip;
      }
  
      public void ReleaseClip(string path)
      {
          if (loadedClips.TryGetValue(path, out var handle))
          {
              handle.refCount--;
              if (handle.refCount <= 0 && !handle.persistent)
              {
                  currentUsage -= EstimateMemory(handle.clip);
                  Resources.UnloadAsset(handle.clip);
                  loadedClips.Remove(path);
              }
          }
      }
  }
  ```
  
### **Platforms**
  - all
  - mobile
  - console
### **Tags**
  - memory
  - loading
  - performance

## Wrong Streaming/Preload Strategy

### **Id**
streaming-vs-preload-decisions
### **Severity**
high
### **Symptoms**
  - Audio plays with delay on first trigger
  - Disk/storage thrashing
  - Memory usage spikes
  - Audio skips during streaming
### **Cause**
  Small frequently-used sounds set to streaming (adds latency).
  Large music/ambient set to preload (wastes memory).
  Streaming buffer size not tuned for platform.
  
### **Detection**
  #### **Pattern**
Streaming.*short|DecompressOnLoad.*music|DecompressOnLoad.*ambient
  #### **Context**
Mismatched load strategy for audio type
### **Fix**
  Decision matrix:
  
  | Duration | Frequency | Strategy |
  |----------|-----------|----------|
  | < 2 sec | High | DecompressOnLoad |
  | < 2 sec | Low | CompressedInMemory |
  | 2-30 sec | Any | CompressedInMemory |
  | > 30 sec | Any | Streaming |
  | Music | Any | Streaming |
  | Ambient loop | Any | Streaming |
  
  ```csharp
  AudioClipLoadType DetermineLoadType(AudioClip clip, AudioUsage usage)
  {
      float duration = clip.length;
      bool isFrequent = usage == AudioUsage.Frequent;
  
      // Short, frequent sounds: decompress for instant playback
      if (duration < 2f && isFrequent)
          return AudioClipLoadType.DecompressOnLoad;
  
      // Medium sounds: keep compressed in memory
      if (duration < 30f)
          return AudioClipLoadType.CompressedInMemory;
  
      // Long sounds, music, ambience: stream
      return AudioClipLoadType.Streaming;
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - streaming
  - memory
  - latency

## Platform Voice Limit Violations

### **Id**
platform-voice-limits
### **Severity**
critical
### **Symptoms**
  - Sounds randomly cut out
  - Works on PC, fails on console/mobile
  - Audio system becomes unresponsive
  - Priority sounds not playing
### **Cause**
  Exceeding platform hardware voice limits.
  Mobile: 32-64 voices, Console: 128-256, PC: software limited.
  Not implementing voice virtualization or stealing.
  
### **Detection**
  #### **Pattern**
PlayOneShot|Play\(\)|audioSource.Play
  #### **Context**
Unmanaged audio playback without voice limiting
### **Fix**
  Platform limits:
  - iOS: 32 voices
  - Android: 32-64 voices (varies by device)
  - Switch: 48 voices
  - PS5/Xbox: 256+ voices
  - PC: 1024+ (software limit)
  
  ```csharp
  public class VoiceManager
  {
      private int maxVoices;
      private int reservedForPriority;
      private List<VoiceHandle> activeVoices;
  
      public VoiceManager(Platform platform)
      {
          maxVoices = GetPlatformVoiceLimit(platform);
          reservedForPriority = maxVoices / 4; // Reserve 25% for high priority
      }
  
      public VoiceHandle RequestVoice(AudioPriority priority)
      {
          int currentCount = activeVoices.Count;
  
          // Always allow high priority in reserved pool
          if (priority == AudioPriority.Critical)
          {
              if (currentCount >= maxVoices)
                  StealLowestPriority();
              return AllocateVoice();
          }
  
          // Normal priority respects reserved voices
          int availableForNormal = maxVoices - reservedForPriority;
          int normalCount = activeVoices.Count(v => v.priority < AudioPriority.Critical);
  
          if (normalCount >= availableForNormal)
          {
              // Try to steal lower priority
              var stealable = activeVoices
                  .Where(v => v.priority < priority)
                  .OrderBy(v => v.priority)
                  .FirstOrDefault();
  
              if (stealable != null)
              {
                  stealable.Stop();
                  return AllocateVoice();
              }
  
              // Virtualize instead of playing
              return CreateVirtualVoice();
          }
  
          return AllocateVoice();
      }
  }
  ```
  
### **Platforms**
  - mobile
  - console
  - all
### **Tags**
  - platform
  - voices
  - limits

## Audio Thread Safety Violations

### **Id**
audio-thread-safety
### **Severity**
high
### **Symptoms**
  - Random crashes in audio system
  - Corrupted audio output
  - Deadlocks during audio operations
  - Race conditions in audio callbacks
### **Cause**
  Accessing audio data from wrong thread.
  FMOD/Wwise callbacks executed on audio thread.
  Unity AudioSource modified from background thread.
  
### **Detection**
  #### **Pattern**
audioSource\.[a-zA-Z]+\s*=|clip\.[a-zA-Z]+|OnAudioFilterRead
  #### **Context**
Audio operations potentially from wrong thread
### **Fix**
  1. Audio middleware callbacks are on audio thread
  2. Queue game state changes, don't execute directly
  3. Use main thread dispatcher for Unity operations
  
  ```csharp
  public class ThreadSafeAudioBridge
  {
      private ConcurrentQueue<Action> mainThreadQueue;
      private volatile bool isProcessing;
  
      // Called from FMOD/Wwise audio thread
      public void OnBeatCallback(float beatTime)
      {
          // DON'T do this - Unity API from audio thread
          // gameObject.GetComponent<Animator>().SetTrigger("Beat");
  
          // DO this - queue for main thread
          mainThreadQueue.Enqueue(() =>
          {
              OnBeatMainThread(beatTime);
          });
      }
  
      // Called from Unity Update
      public void ProcessQueue()
      {
          while (mainThreadQueue.TryDequeue(out var action))
          {
              action.Invoke();
          }
      }
  
      private void OnBeatMainThread(float beatTime)
      {
          // Safe to use Unity API here
          animator.SetTrigger("Beat");
      }
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - threading
  - safety
  - callbacks

## Audio Loop Click/Pop Artifacts

### **Id**
loop-point-clicks
### **Severity**
medium
### **Symptoms**
  - Click or pop when audio loops
  - Audible seam in looping music
  - Discontinuity at loop point
### **Cause**
  Loop point not at zero crossing.
  Compression artifacts at loop boundaries.
  Sample rate mismatch.
  
### **Detection**
  #### **Pattern**
loop.*=.*true|isLooping|AudioSource.*loop
  #### **Context**
Looping audio without proper loop point handling
### **Fix**
  1. Set loop points at zero crossings in audio file
  2. Use PCM for short loops, high-quality Vorbis for long
  3. Add tiny crossfade at loop point
  4. Ensure consistent sample rate (44100 or 48000)
  
  ```csharp
  // For programmatic loop crossfade
  public class LoopCrossfader
  {
      private AudioSource sourceA;
      private AudioSource sourceB;
      private float crossfadeDuration = 0.05f; // 50ms
  
      public void UpdateLoop()
      {
          var activeSource = sourceA.isPlaying ? sourceA : sourceB;
          var inactiveSource = sourceA.isPlaying ? sourceB : sourceA;
  
          float timeRemaining = activeSource.clip.length - activeSource.time;
  
          if (timeRemaining <= crossfadeDuration)
          {
              // Start crossfade
              inactiveSource.time = 0f;
              inactiveSource.Play();
  
              float t = 1f - (timeRemaining / crossfadeDuration);
              activeSource.volume = Mathf.Lerp(1f, 0f, t);
              inactiveSource.volume = Mathf.Lerp(0f, 1f, t);
          }
      }
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - looping
  - artifacts
  - quality

## Reverb Zone Overlap Issues

### **Id**
reverb-zone-stacking
### **Severity**
medium
### **Symptoms**
  - Reverb sounds wrong or too heavy
  - Sudden reverb changes when moving
  - Performance issues with many zones
  - Reverb doesn't match environment
### **Cause**
  Multiple reverb zones overlapping incorrectly.
  Zone priorities not set properly.
  Reverb blend distance too short.
  
### **Detection**
  #### **Pattern**
ReverbZone|AudioReverbZone|ReverbPreset
  #### **Context**
Reverb zone configuration
### **Fix**
  1. Set zone priorities (higher = takes precedence)
  2. Use blend distance for smooth transitions
  3. Limit active zones per area
  4. Use snapshots in FMOD/Wwise instead of Unity zones
  
  ```csharp
  // Proper reverb zone setup
  void ConfigureReverbZone(AudioReverbZone zone, ReverbEnvironment env)
  {
      switch (env)
      {
          case ReverbEnvironment.SmallRoom:
              zone.reverbPreset = AudioReverbPreset.Room;
              zone.minDistance = 1f;
              zone.maxDistance = 10f;
              break;
  
          case ReverbEnvironment.LargeHall:
              zone.reverbPreset = AudioReverbPreset.Hall;
              zone.minDistance = 5f;
              zone.maxDistance = 50f;
              break;
  
          case ReverbEnvironment.Cave:
              zone.reverbPreset = AudioReverbPreset.Cave;
              zone.minDistance = 2f;
              zone.maxDistance = 30f;
              break;
  
          case ReverbEnvironment.Outdoor:
              zone.reverbPreset = AudioReverbPreset.Plain;
              zone.minDistance = 10f;
              zone.maxDistance = 100f;
              break;
      }
  }
  
  // FMOD approach - use snapshots
  void TransitionReverbSnapshot(string snapshotPath, float transitionTime)
  {
      FMOD.Studio.EventInstance snapshot;
      FMODUnity.RuntimeManager.CreateInstance(snapshotPath, out snapshot);
      snapshot.start();
  
      // Blend over time
      snapshot.setParameterByName("Intensity", 1f);
  }
  ```
  
### **Platforms**
  - all
### **Tags**
  - reverb
  - spatial
  - configuration

## Mobile Audio Session Conflicts

### **Id**
mobile-audio-session
### **Severity**
high
### **Symptoms**
  - Game audio stops when phone call ends
  - Audio interrupted by notifications
  - Background audio from other apps plays over game
  - Volume duck not working properly
### **Cause**
  iOS/Android audio session not configured correctly.
  Not handling audio interruptions properly.
  Wrong audio session category.
  
### **Detection**
  #### **Pattern**
AudioSession|AVAudioSession|AudioManager.STREAM
  #### **Context**
Mobile audio session handling
### **Fix**
  iOS:
  ```swift
  // Set up audio session for game
  try AVAudioSession.sharedInstance().setCategory(
      .playback,
      mode: .default,
      options: [.mixWithOthers, .duckOthers]
  )
  
  // Handle interruptions
  NotificationCenter.default.addObserver(
      self,
      selector: #selector(handleInterruption),
      name: AVAudioSession.interruptionNotification,
      object: nil
  )
  ```
  
  Android:
  ```java
  // Request audio focus
  AudioFocusRequest focusRequest = new AudioFocusRequest.Builder(
      AudioManager.AUDIOFOCUS_GAIN)
      .setAudioAttributes(gameAudioAttributes)
      .setOnAudioFocusChangeListener(focusChangeListener)
      .build();
  
  audioManager.requestAudioFocus(focusRequest);
  ```
  
  Unity:
  ```csharp
  // Handle app pause/resume
  void OnApplicationPause(bool paused)
  {
      if (paused)
      {
          // Save audio state
          PauseAllAudio();
      }
      else
      {
          // Reinitialize audio session if needed
          ResumeAllAudio();
      }
  }
  ```
  
### **Platforms**
  - mobile
  - ios
  - android
### **Tags**
  - mobile
  - session
  - interruption
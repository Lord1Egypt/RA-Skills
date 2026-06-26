# Game Audio - Validations

## Runtime AudioSource Creation

### **Id**
runtime-audiosource-creation
### **Description**
Creating AudioSources at runtime causes GC allocation
### **Severity**
error
### **Category**
performance
### **Languages**
  - csharp
### **Pattern**
  (AddComponent\s*<\s*AudioSource\s*>|
   new\s+AudioSource|
   Instantiate.*Audio|
   gameObject\.AddComponent.*AudioSource)
  
### **Fix**
  Use audio source pooling:
  ```csharp
  // Instead of: var source = gameObject.AddComponent<AudioSource>();
  var source = audioPool.Get();
  source.clip = clip;
  source.Play();
  // When done: audioPool.Return(source);
  ```
  
### **Tags**
  - gc
  - pooling
  - performance

## Unmanaged PlayOneShot Calls

### **Id**
unmanaged-playoneshot
### **Description**
PlayOneShot without voice limiting can exhaust voices
### **Severity**
warning
### **Category**
performance
### **Languages**
  - csharp
### **Pattern**
  \.PlayOneShot\s*\(
  
### **Context Check**
  Check if called within a managed audio system or directly on AudioSource
  
### **Fix**
  Route through audio manager with voice limiting:
  ```csharp
  // Instead of: audioSource.PlayOneShot(clip);
  AudioManager.Instance.PlaySFX(clip, position, priority);
  ```
  
### **Tags**
  - voices
  - performance

## Synchronous Audio Loading

### **Id**
synchronous-audio-load
### **Description**
Loading audio synchronously blocks main thread
### **Severity**
error
### **Category**
performance
### **Languages**
  - csharp
### **Pattern**
  Resources\.Load\s*<\s*AudioClip\s*>\s*\(
  
### **Fix**
  Use async loading:
  ```csharp
  // Instead of: var clip = Resources.Load<AudioClip>("path");
  var request = Resources.LoadAsync<AudioClip>("path");
  await request;
  var clip = request.asset as AudioClip;
  ```
  
### **Tags**
  - loading
  - performance
  - async

## Audio API from Background Thread

### **Id**
audio-from-wrong-thread
### **Description**
Unity audio API must be called from main thread
### **Severity**
error
### **Category**
threading
### **Languages**
  - csharp
### **Pattern**
  (Task\.Run|ThreadPool|new\s+Thread|async\s+Task)[\s\S]{0,500}(audioSource|AudioSource|\.Play\(|\.Stop\(|\.volume)
  
### **Fix**
  Queue audio operations for main thread:
  ```csharp
  // Use main thread dispatcher
  MainThreadDispatcher.Enqueue(() => {
      audioSource.Play();
  });
  ```
  
### **Tags**
  - threading
  - safety

## Missing Audio Resource Unload

### **Id**
missing-audio-unload
### **Description**
Loaded audio clips without corresponding unload
### **Severity**
warning
### **Category**
memory
### **Languages**
  - csharp
### **Pattern**
  Resources\.Load.*AudioClip
  
### **Negative Pattern**
  Resources\.UnloadAsset|Resources\.UnloadUnusedAssets
  
### **Fix**
  Track and unload audio resources:
  ```csharp
  // When done with clip:
  Resources.UnloadAsset(clip);
  // Or during scene transitions:
  Resources.UnloadUnusedAssets();
  ```
  
### **Tags**
  - memory
  - loading

## Linear Volume Scale

### **Id**
linear-volume-scale
### **Description**
Using linear volume instead of logarithmic (dB)
### **Severity**
info
### **Category**
quality
### **Languages**
  - csharp
### **Pattern**
  \.volume\s*=\s*[0-9.]+f?\s*[;,)]
  
### **Context Check**
  Check if value is computed using Log or decibel conversion
  
### **Fix**
  Convert to decibels for perceptually correct volume:
  ```csharp
  // Linear to dB conversion
  float LinearToDecibel(float linear)
  {
      return linear > 0.0001f
          ? 20f * Mathf.Log10(linear)
          : -80f;
  }
  
  // Use with AudioMixer exposed parameter
  mixer.SetFloat("MasterVolume", LinearToDecibel(slider.value));
  ```
  
### **Tags**
  - audio-quality
  - mixing

## Hardcoded Audio Path

### **Id**
hardcoded-audio-path
### **Description**
Audio paths hardcoded in gameplay code
### **Severity**
info
### **Category**
architecture
### **Languages**
  - csharp
### **Pattern**
  (Load|PlayOneShot|clip\s*=)\s*.*["'].*\.(wav|mp3|ogg|aif)["']
  
### **Fix**
  Use audio event IDs or ScriptableObject references:
  ```csharp
  // Define audio events in ScriptableObject
  [CreateAssetMenu]
  public class AudioEventLibrary : ScriptableObject
  {
      public AudioEvent playerJump;
      public AudioEvent playerLand;
      // ...
  }
  
  // Reference in code
  audioManager.Play(audioLibrary.playerJump);
  ```
  
### **Tags**
  - architecture
  - maintainability

## Missing Spatial Audio Configuration

### **Id**
missing-spatial-setup
### **Description**
3D audio source without proper spatial settings
### **Severity**
warning
### **Category**
configuration
### **Languages**
  - csharp
### **Pattern**
  spatialBlend\s*=\s*1(?![\s\S]{0,200}(minDistance|maxDistance|rolloffMode))
  
### **Fix**
  Configure spatial audio properties:
  ```csharp
  source.spatialBlend = 1f;
  source.rolloffMode = AudioRolloffMode.Logarithmic;
  source.minDistance = 2f;
  source.maxDistance = 50f;
  source.spread = 45f;
  ```
  
### **Tags**
  - spatial
  - configuration

## Missing Audio Priority

### **Id**
no-audio-priority
### **Description**
AudioSource without priority setting
### **Severity**
info
### **Category**
voice-management
### **Languages**
  - csharp
### **Pattern**
  AudioSource[\s\S]{0,100}\.Play\(\)(?![\s\S]{0,50}priority)
  
### **Fix**
  Set audio priority (0=highest, 256=lowest):
  ```csharp
  source.priority = 0;   // Critical sounds (player, UI)
  source.priority = 128; // Normal sounds (environment)
  source.priority = 256; // Low priority (distant ambient)
  ```
  
### **Tags**
  - priority
  - voice-management

## FMOD Event Not Released

### **Id**
fmod-event-not-released
### **Description**
FMOD EventInstance created but never released
### **Severity**
error
### **Category**
memory
### **Languages**
  - csharp
### **Pattern**
  (CreateInstance|RuntimeManager\.CreateInstance)(?![\s\S]{0,500}(\.release\(\)|STOP_MODE\.ALLOWFADEOUT))
  
### **Fix**
  Always release FMOD events:
  ```csharp
  // One-shot event
  instance.start();
  instance.release(); // Will clean up after sound ends
  
  // Or stop with fadeout then release
  instance.stop(FMOD.Studio.STOP_MODE.ALLOWFADEOUT);
  instance.release();
  ```
  
### **Tags**
  - fmod
  - memory

## FMOD Bank Not Unloaded

### **Id**
fmod-bank-not-unloaded
### **Description**
FMOD bank loaded but never unloaded
### **Severity**
warning
### **Category**
memory
### **Languages**
  - csharp
### **Pattern**
  RuntimeManager\.LoadBank(?![\s\S]{0,1000}UnloadBank)
  
### **Fix**
  Unload banks on scene exit:
  ```csharp
  void OnDestroy()
  {
      FMODUnity.RuntimeManager.UnloadBank("SceneAudio");
  }
  ```
  
### **Tags**
  - fmod
  - memory
  - banks

## Wwise Event Not Stopped

### **Id**
wwise-event-not-stopped
### **Description**
Wwise event posted without stop handling
### **Severity**
warning
### **Category**
memory
### **Languages**
  - csharp
### **Pattern**
  PostEvent(?![\s\S]{0,500}(StopPlayingID|Stop\(|ExecuteActionOnEvent.*Stop))
  
### **Fix**
  Track and stop Wwise events:
  ```csharp
  uint playingId = AkSoundEngine.PostEvent("PlayAmbient", gameObject);
  
  // When done:
  AkSoundEngine.StopPlayingID(playingId);
  // Or stop all on object:
  AkSoundEngine.StopAll(gameObject);
  ```
  
### **Tags**
  - wwise
  - memory

## Uncompressed Audio on Mobile

### **Id**
mobile-uncompressed-audio
### **Description**
PCM or uncompressed audio in mobile build
### **Severity**
error
### **Category**
platform
### **Languages**
  - csharp
### **Pattern**
  compressionFormat\s*=\s*AudioCompressionFormat\.PCM
  
### **Context Check**
  Check if this is for mobile platform settings
  
### **Fix**
  Use compressed formats on mobile:
  ```csharp
  #if UNITY_IOS || UNITY_ANDROID
      settings.compressionFormat = AudioCompressionFormat.Vorbis;
      settings.quality = 0.5f; // Lower quality for mobile
  #endif
  ```
  
### **Tags**
  - mobile
  - compression
  - platform

## Too Many Streaming Audio Sources

### **Id**
too-many-streaming-sources
### **Description**
Multiple streaming sources can cause I/O bottlenecks
### **Severity**
warning
### **Category**
performance
### **Languages**
  - csharp
### **Pattern**
  loadType\s*=\s*AudioClipLoadType\.Streaming
  
### **Context Check**
  Count streaming sources - should be limited to 2-4
  
### **Fix**
  Limit streaming sources:
  - Maximum 2-4 simultaneous streaming sources
  - Use CompressedInMemory for short-medium files
  - Reserve streaming for music and long ambiences
  
### **Tags**
  - streaming
  - performance
  - io
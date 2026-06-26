# Audio Setup Patterns

Common audio architecture patterns for Unreal Engine projects. All patterns use real UE API
as found in `AudioComponent.h`, `GameplayStatics.h`, `SoundSubmix.h`, `SoundConcurrency.h`,
and `SoundAttenuation.h`.

---

## Pattern 1: Music System with Crossfading

A persistent music manager that crossfades between tracks using two `UAudioComponent` instances
— one active, one incoming — with `FadeIn`/`FadeOut` on both.

### MusicManager.h

```cpp
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/AudioComponent.h"
#include "MusicManager.generated.h"

UCLASS(BlueprintType)
class MYGAME_API AMusicManager : public AActor
{
    GENERATED_BODY()

public:
    AMusicManager();

    UFUNCTION(BlueprintCallable, Category = "Audio|Music")
    void PlayMusic(USoundBase* NewTrack, float CrossfadeDuration = 1.0f);

    UFUNCTION(BlueprintCallable, Category = "Audio|Music")
    void StopMusic(float FadeOutDuration = 1.0f);

    UFUNCTION(BlueprintCallable, Category = "Audio|Music")
    void SetMusicVolume(float Volume);

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    UFUNCTION()
    void OnTrackFinished();

private:
    // Slot A: currently playing track
    UPROPERTY()
    TObjectPtr<UAudioComponent> TrackA;

    // Slot B: incoming track during crossfade
    UPROPERTY()
    TObjectPtr<UAudioComponent> TrackB;

    // Which slot is active
    bool bSlotAIsActive = true;

    // Volume scalar applied to both tracks (separate from crossfade)
    float MasterMusicVolume = 1.0f;

    // Submix all music routes through — set in editor
    UPROPERTY(EditDefaultsOnly, Category = "Audio|Music")
    TObjectPtr<USoundSubmix> MusicSubmix;
};
```

### MusicManager.cpp

```cpp
#include "MusicManager.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundSubmix.h"

AMusicManager::AMusicManager()
{
    PrimaryActorTick.bCanEverTick = false;

    // Two permanent audio components — no sound assigned at construction
    TrackA = CreateDefaultSubobject<UAudioComponent>(TEXT("TrackA"));
    TrackA->SetupAttachment(RootComponent);
    TrackA->bAutoActivate = false;
    TrackA->bIsUISound = true;   // non-spatialized music

    TrackB = CreateDefaultSubobject<UAudioComponent>(TEXT("TrackB"));
    TrackB->SetupAttachment(RootComponent);
    TrackB->bAutoActivate = false;
    TrackB->bIsUISound = true;
}

void AMusicManager::BeginPlay()
{
    Super::BeginPlay();
    TrackA->OnAudioFinished.AddDynamic(this, &AMusicManager::OnTrackFinished);
    TrackB->OnAudioFinished.AddDynamic(this, &AMusicManager::OnTrackFinished);
}

void AMusicManager::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    TrackA->OnAudioFinished.RemoveAll(this);
    TrackB->OnAudioFinished.RemoveAll(this);
    Super::EndPlay(EndPlayReason);
}

void AMusicManager::PlayMusic(USoundBase* NewTrack, float CrossfadeDuration)
{
    if (!NewTrack) { return; }
    if (GetNetMode() == NM_DedicatedServer) { return; }

    UAudioComponent* ActiveSlot  = bSlotAIsActive ? TrackA : TrackB;
    UAudioComponent* IncomingSlot = bSlotAIsActive ? TrackB : TrackA;

    // Fade out the currently playing slot
    if (ActiveSlot->GetPlayState() == EAudioComponentPlayState::Playing ||
        ActiveSlot->GetPlayState() == EAudioComponentPlayState::FadingIn)
    {
        ActiveSlot->FadeOut(CrossfadeDuration, 0.0f, EAudioFaderCurve::Linear);
    }

    // Configure and fade in the incoming slot
    IncomingSlot->SetSound(NewTrack);
    IncomingSlot->FadeIn(CrossfadeDuration, MasterMusicVolume, 0.0f, EAudioFaderCurve::Linear);

    bSlotAIsActive = !bSlotAIsActive;
}

void AMusicManager::StopMusic(float FadeOutDuration)
{
    TrackA->FadeOut(FadeOutDuration, 0.0f, EAudioFaderCurve::Linear);
    TrackB->FadeOut(FadeOutDuration, 0.0f, EAudioFaderCurve::Linear);
}

void AMusicManager::SetMusicVolume(float Volume)
{
    MasterMusicVolume = FMath::Clamp(Volume, 0.0f, 1.0f);
    // Alternatively, control via submix:
    if (MusicSubmix)
    {
        MusicSubmix->SetSubmixOutputVolume(this, MasterMusicVolume);
    }
}

void AMusicManager::OnTrackFinished()
{
    // Looping tracks should have a looping SoundCue or SoundWave —
    // this callback fires only for one-shot music tracks.
}
```

---

## Pattern 2: Ambient Soundscape System

An actor that manages a set of looping ambient sounds (wind, birds, insects, water) with
distance-based crossfading driven by the player's position relative to defined zones.

### AmbientSoundscape.h

```cpp
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/AudioComponent.h"
#include "AmbientSoundscape.generated.h"

USTRUCT(BlueprintType)
struct FAmbientLayer
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TObjectPtr<USoundBase> Sound;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0.0", ClampMax="1.0"))
    float MaxVolume = 1.0f;

    // Component assigned at runtime
    UPROPERTY(Transient)
    TObjectPtr<UAudioComponent> Component;
};

UCLASS(BlueprintType)
class MYGAME_API AAmbientSoundscape : public AActor
{
    GENERATED_BODY()

public:
    AAmbientSoundscape();

    UFUNCTION(BlueprintCallable, Category = "Audio|Ambient")
    void SetLayerVolume(int32 LayerIndex, float NormalizedVolume, float BlendTime = 0.5f);

    UFUNCTION(BlueprintCallable, Category = "Audio|Ambient")
    void FadeOutAll(float FadeDuration = 1.0f);

    UFUNCTION(BlueprintCallable, Category = "Audio|Ambient")
    void FadeInAll(float FadeDuration = 1.0f);

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, Category = "Audio|Ambient")
    TArray<FAmbientLayer> Layers;

    // Attenuation for all ambient layers (sphere, no occlusion for ambient)
    UPROPERTY(EditDefaultsOnly, Category = "Audio|Ambient")
    TObjectPtr<USoundAttenuation> AmbientAttenuation;
};
```

### AmbientSoundscape.cpp

```cpp
#include "AmbientSoundscape.h"
#include "Kismet/GameplayStatics.h"

AAmbientSoundscape::AAmbientSoundscape()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AAmbientSoundscape::BeginPlay()
{
    Super::BeginPlay();

    if (GetNetMode() == NM_DedicatedServer) { return; }

    for (FAmbientLayer& Layer : Layers)
    {
        if (!Layer.Sound) { continue; }

        // SpawnSoundAttached creates a component attached to this actor
        UAudioComponent* Comp = UGameplayStatics::SpawnSoundAttached(
            Layer.Sound,
            GetRootComponent(),
            NAME_None,
            FVector::ZeroVector,
            FRotator::ZeroRotator,
            EAttachLocation::SnapToTarget,
            /*bStopWhenAttachedToDestroyed=*/true,
            0.0f,           // start at volume 0
            1.0f,           // pitch
            0.0f,           // start time
            AmbientAttenuation,
            nullptr,        // concurrency (ambient loops don't need concurrency)
            /*bAutoDestroy=*/false
        );

        if (Comp)
        {
            Layer.Component = Comp;
            // Fade in over 2 seconds to MaxVolume
            Comp->FadeIn(2.0f, Layer.MaxVolume, 0.0f, EAudioFaderCurve::Linear);
        }
    }
}

void AAmbientSoundscape::SetLayerVolume(int32 LayerIndex, float NormalizedVolume, float BlendTime)
{
    if (!Layers.IsValidIndex(LayerIndex)) { return; }
    FAmbientLayer& Layer = Layers[LayerIndex];
    if (!Layer.Component) { return; }

    const float TargetVolume = Layer.MaxVolume * FMath::Clamp(NormalizedVolume, 0.0f, 1.0f);
    if (BlendTime <= 0.0f)
    {
        Layer.Component->SetVolumeMultiplier(TargetVolume);
    }
    else
    {
        Layer.Component->AdjustVolume(BlendTime, TargetVolume);
    }
}

void AAmbientSoundscape::FadeOutAll(float FadeDuration)
{
    for (FAmbientLayer& Layer : Layers)
    {
        if (Layer.Component)
        {
            Layer.Component->FadeOut(FadeDuration, 0.0f, EAudioFaderCurve::Linear);
        }
    }
}

void AAmbientSoundscape::FadeInAll(float FadeDuration)
{
    for (FAmbientLayer& Layer : Layers)
    {
        if (Layer.Component)
        {
            Layer.Component->FadeIn(FadeDuration, Layer.MaxVolume, 0.0f, EAudioFaderCurve::Linear);
        }
    }
}
```

---

## Pattern 3: Gameplay Audio Component (Weapon SFX)

A `UActorComponent` managing a weapon's audio: fire, reload, empty-click, and mechanical
state sounds. Demonstrates proper server guarding and concurrency usage.

### WeaponAudioComponent.h

```cpp
#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Sound/SoundConcurrency.h"
#include "WeaponAudioComponent.generated.h"

UCLASS(ClassGroup=Audio, meta=(BlueprintSpawnableComponent))
class MYGAME_API UWeaponAudioComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWeaponAudioComponent();

    UFUNCTION(BlueprintCallable, Category = "Audio|Weapon")
    void PlayFireSound();

    UFUNCTION(BlueprintCallable, Category = "Audio|Weapon")
    void PlayReloadSound();

    UFUNCTION(BlueprintCallable, Category = "Audio|Weapon")
    void PlayEmptyClickSound();

    UFUNCTION(BlueprintCallable, Category = "Audio|Weapon")
    void StartMechanicalLoop();

    UFUNCTION(BlueprintCallable, Category = "Audio|Weapon")
    void StopMechanicalLoop(float FadeTime = 0.15f);

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    // One-shot sounds — use SpawnSoundAtLocation each play
    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TObjectPtr<USoundBase> FireSound;

    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TObjectPtr<USoundBase> ReloadSound;

    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TObjectPtr<USoundBase> EmptyClickSound;

    // Looping sound — permanent component
    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TObjectPtr<USoundBase> MechanicalLoopSound;

    // Attenuation for world-space weapon sounds
    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TObjectPtr<USoundAttenuation> WeaponAttenuation;

    // Concurrency: max 4 fire sounds simultaneously, stop farthest if over
    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TObjectPtr<USoundConcurrency> FireConcurrency;

private:
    UPROPERTY()
    TObjectPtr<UAudioComponent> MechanicalLoopComp;

    bool bIsOnServer() const;
    FVector GetOwnerLocation() const;
};
```

### WeaponAudioComponent.cpp

```cpp
#include "WeaponAudioComponent.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "Components/AudioComponent.h"

UWeaponAudioComponent::UWeaponAudioComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UWeaponAudioComponent::BeginPlay()
{
    Super::BeginPlay();

    if (bIsOnServer() || !MechanicalLoopSound) { return; }

    // Create the loop component but don't play yet
    MechanicalLoopComp = UGameplayStatics::SpawnSoundAttached(
        MechanicalLoopSound,
        GetOwner()->GetRootComponent(),
        NAME_None,
        FVector::ZeroVector,
        FRotator::ZeroRotator,
        EAttachLocation::SnapToTarget,
        /*bStopWhenAttachedToDestroyed=*/true,
        1.0f, 1.0f, 0.0f,
        WeaponAttenuation,
        nullptr,
        /*bAutoDestroy=*/false
    );

    if (MechanicalLoopComp)
    {
        MechanicalLoopComp->Stop(); // ensure not auto-playing
    }
}

void UWeaponAudioComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (MechanicalLoopComp)
    {
        MechanicalLoopComp->Stop();
    }
    Super::EndPlay(EndPlayReason);
}

void UWeaponAudioComponent::PlayFireSound()
{
    if (bIsOnServer() || !FireSound) { return; }

    // Fire-and-forget: attenuation + concurrency prevent stacking
    UGameplayStatics::PlaySoundAtLocation(
        this,
        FireSound,
        GetOwnerLocation(),
        FRotator::ZeroRotator,
        1.0f, 1.0f, 0.0f,
        WeaponAttenuation,
        FireConcurrency,        // USoundConcurrency: MaxCount=4, StopFarthestThenOldest
        GetOwner()
    );
}

void UWeaponAudioComponent::PlayReloadSound()
{
    if (bIsOnServer() || !ReloadSound) { return; }
    UGameplayStatics::PlaySoundAtLocation(
        this, ReloadSound, GetOwnerLocation(),
        FRotator::ZeroRotator, 1.0f, 1.0f, 0.0f,
        WeaponAttenuation
    );
}

void UWeaponAudioComponent::PlayEmptyClickSound()
{
    if (bIsOnServer() || !EmptyClickSound) { return; }
    UGameplayStatics::PlaySoundAtLocation(
        this, EmptyClickSound, GetOwnerLocation(),
        FRotator::ZeroRotator, 1.0f, 1.0f, 0.0f,
        WeaponAttenuation
    );
}

void UWeaponAudioComponent::StartMechanicalLoop()
{
    if (bIsOnServer() || !MechanicalLoopComp) { return; }
    MechanicalLoopComp->FadeIn(0.1f, 1.0f, 0.0f, EAudioFaderCurve::Linear);
}

void UWeaponAudioComponent::StopMechanicalLoop(float FadeTime)
{
    if (!MechanicalLoopComp) { return; }
    MechanicalLoopComp->FadeOut(FadeTime, 0.0f, EAudioFaderCurve::Linear);
}

bool UWeaponAudioComponent::bIsOnServer() const
{
    const AActor* Owner = GetOwner();
    return Owner && Owner->GetNetMode() == NM_DedicatedServer;
}

FVector UWeaponAudioComponent::GetOwnerLocation() const
{
    const AActor* Owner = GetOwner();
    return Owner ? Owner->GetActorLocation() : FVector::ZeroVector;
}
```

---

## Pattern 4: MetaSound Parameter-Driven Engine Audio

An engine sound that uses a `UMetaSoundSource` with a `RPM` float input and `Engaged` bool input,
driven from a vehicle's tick.

```cpp
// In vehicle header:
UPROPERTY(EditDefaultsOnly, Category = "Audio")
TObjectPtr<UMetaSoundSource> EngineSoundAsset;   // UMetaSoundSource derives USoundBase

UPROPERTY()
TObjectPtr<UAudioComponent> EngineAudioComp;

// In BeginPlay:
void AMyVehicle::BeginPlay()
{
    Super::BeginPlay();
    if (GetNetMode() == NM_DedicatedServer) { return; }

    EngineAudioComp = UGameplayStatics::SpawnSoundAttached(
        EngineSoundAsset,
        GetMesh(),
        TEXT("AudioSocket"),
        FVector::ZeroVector,
        FRotator::ZeroRotator,
        EAttachLocation::SnapToTarget,
        true, 1.0f, 1.0f, 0.0f,
        EngineAttenuation,
        nullptr,
        /*bAutoDestroy=*/false
    );
}

// In Tick — update MetaSound parameters:
void AMyVehicle::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    if (!EngineAudioComp) { return; }

    const float CurrentRPM = GetCurrentRPM();   // your vehicle RPM value
    const bool bIsEngaged = IsTransmissionEngaged();

    // ISoundParameterControllerInterface methods on UAudioComponent:
    EngineAudioComp->SetFloatParameter(FName("RPM"), CurrentRPM);
    EngineAudioComp->SetBoolParameter(FName("Engaged"), bIsEngaged);
}

// On gear shift event:
void AMyVehicle::OnGearShift(int32 NewGear)
{
    if (EngineAudioComp)
    {
        EngineAudioComp->SetIntParameter(FName("GearIndex"), NewGear);
        EngineAudioComp->SetTriggerParameter(FName("OnGearShift"));
    }
}
```

---

## Pattern 5: Submix-Based Volume Control (Settings Menu)

Typical volume slider implementation using `USoundSubmix::SetSubmixOutputVolume`.

```cpp
// In game settings subsystem or GameUserSettings subclass:

UPROPERTY(config)
float MasterVolume = 1.0f;

UPROPERTY(config)
float MusicVolume = 1.0f;

UPROPERTY(config)
float SFXVolume = 1.0f;

// References to submix assets loaded via soft references or direct UPROPERTY:
UPROPERTY(EditDefaultsOnly, Category = "Audio")
TObjectPtr<USoundSubmix> MasterSubmix;

UPROPERTY(EditDefaultsOnly, Category = "Audio")
TObjectPtr<USoundSubmix> MusicSubmix;

UPROPERTY(EditDefaultsOnly, Category = "Audio")
TObjectPtr<USoundSubmix> SFXSubmix;

void UMyGameUserSettings::ApplyAudioSettings()
{
    if (UWorld* World = GetWorld())
    {
        if (MasterSubmix)
        {
            MasterSubmix->SetSubmixOutputVolume(World, MasterVolume);
        }
        if (MusicSubmix)
        {
            MusicSubmix->SetSubmixOutputVolume(World, MusicVolume);
        }
        if (SFXSubmix)
        {
            SFXSubmix->SetSubmixOutputVolume(World, SFXVolume);
        }
    }
}

void UMyGameUserSettings::SetMasterVolume(float NewVolume)
{
    MasterVolume = FMath::Clamp(NewVolume, 0.0f, 1.0f);
    ApplyAudioSettings();
    SaveConfig();
}
```

---

## Pattern 6: Beat-Reactive Visual (Spectrum Analysis)

Drive a material parameter or visual effect from submix spectral analysis.

```cpp
// In an actor that reacts to music beats:

void ABeaconLight::BeginPlay()
{
    Super::BeginPlay();
    if (GetNetMode() == NM_DedicatedServer || !MusicSubmix) { return; }

    // Start FFT on the music submix
    MusicSubmix->StartSpectralAnalysis(
        this,
        EFFTSize::Medium,
        EFFTPeakInterpolationMethod::Linear,
        EFFTWindowType::Hann,
        0.0f,
        EAudioSpectrumType::MagnitudeSpectrum
    );

    // Low (bass) and mid bands
    TArray<FSoundSubmixSpectralAnalysisBandSettings> Bands;
    FSoundSubmixSpectralAnalysisBandSettings Bass;
    Bass.BandFrequency = 80.f;
    Bass.AttackTimeMsec = 5.f;
    Bass.ReleaseTimeMsec = 80.f;
    Bands.Add(Bass);

    FSoundSubmixSpectralAnalysisBandSettings Mid;
    Mid.BandFrequency = 800.f;
    Mid.AttackTimeMsec = 10.f;
    Mid.ReleaseTimeMsec = 120.f;
    Bands.Add(Mid);

    FOnSubmixSpectralAnalysisBP SpectralDelegate;
    SpectralDelegate.BindDynamic(this, &ABeaconLight::OnSpectralData);

    MusicSubmix->AddSpectralAnalysisDelegate(
        this, Bands, SpectralDelegate,
        30.f,    // UpdateRate Hz
        -40.f,   // DecibelNoiseFloor
        true,    // bDoNormalize (output 0..1)
        false    // bDoAutoRange
    );
}

UFUNCTION()
void ABeaconLight::OnSpectralData(const TArray<float>& Magnitudes)
{
    // Magnitudes[0] = bass band (0..1 normalized), Magnitudes[1] = mid band
    const float BassMag = Magnitudes.IsValidIndex(0) ? Magnitudes[0] : 0.0f;
    const float MidMag  = Magnitudes.IsValidIndex(1) ? Magnitudes[1] : 0.0f;

    // Drive a dynamic material instance parameter
    if (LightMaterial)
    {
        LightMaterial->SetScalarParameterValue(TEXT("BassIntensity"), BassMag);
        LightMaterial->SetScalarParameterValue(TEXT("MidIntensity"), MidMag);
    }

    // Scale a point light radius
    if (PointLight)
    {
        const float BaseRadius = 200.0f;
        PointLight->SetAttenuationRadius(BaseRadius + BassMag * 800.0f);
    }
}

void ABeaconLight::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (MusicSubmix)
    {
        MusicSubmix->StopSpectralAnalysis(this);
    }
    Super::EndPlay(EndPlayReason);
}
```

---

## Asset Setup Checklist

For every 3D sound in the project:

- [ ] `AttenuationSettings` assigned — sphere falloff, `FalloffDistance` tuned to gameplay scale
- [ ] `SoundClassObject` set — SFX, Music, Voice, or Ambient
- [ ] `SoundSubmixObject` set — routes audio to the correct mixer bus
- [ ] `ConcurrencySet` populated — at least one `USoundConcurrency` for high-frequency sounds
- [ ] `Priority` value set — 1.0 default; increase for critical gameplay sounds
- [ ] `bAttenuate` and `bSpatialize` both enabled in the attenuation asset
- [ ] `bEnableOcclusion` considered — enable for interior/exterior transitions
- [ ] Streaming behavior — set `LoadingBehavior` on long SoundWave assets to `LoadOnDemand`

For MetaSound sources:

- [ ] All gameplay-driven inputs declared with clear names matching C++ `FName` strings
- [ ] Default parameter values set in the MetaSound graph
- [ ] `USoundConcurrency` assigned on the `UMetaSoundSource` asset
- [ ] Attenuation assigned if used in world space

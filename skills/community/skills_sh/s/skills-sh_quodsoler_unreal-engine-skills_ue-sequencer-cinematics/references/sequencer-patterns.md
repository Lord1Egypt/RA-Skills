# Sequencer Patterns Reference

Common runtime patterns for Unreal Engine Sequencer / LevelSequence. All patterns use real
API from LevelSequenceActor.h, LevelSequencePlayer.h, MovieSceneSequencePlayer.h,
CineCameraActor.h, CineCameraComponent.h, and CineCameraSettings.h.

---

## Pattern 1: Full-Screen Dialogue Cutscene

A cutscene triggered by gameplay that disables player input, plays a pre-authored sequence,
then restores control.

### Header

```cpp
// MyCutsceneManager.h
#pragma once
#include "GameFramework/Actor.h"
#include "LevelSequencePlayer.h"
#include "LevelSequenceActor.h"
#include "MovieSceneSequencePlaybackSettings.h"
#include "MyCutsceneManager.generated.h"

UCLASS()
class AMyCutsceneManager : public AActor
{
    GENERATED_BODY()
public:
    /** LevelSequence asset to play — assign in editor or set via SetSequenceAsset() */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cinematics")
    ULevelSequence* CutsceneAsset;

    /** Optional: named binding tag for the hero actor (tag set in Sequencer UI) */
    UPROPERTY(EditAnywhere, Category = "Cinematics")
    FName HeroBindingTag = FName("Hero");

    UFUNCTION(BlueprintCallable, Category = "Cinematics")
    void PlayCutscene(AActor* HeroActor);

    UFUNCTION(BlueprintCallable, Category = "Cinematics")
    void SkipCutscene();

private:
    UPROPERTY()
    ALevelSequenceActor* ActiveSequenceActor;

    UPROPERTY()
    ULevelSequencePlayer* ActivePlayer;

    UFUNCTION()
    void OnCutsceneFinished();

    void RestorePlayerControl();
};
```

### Implementation

```cpp
// MyCutsceneManager.cpp
#include "MyCutsceneManager.h"
#include "LevelSequencePlayer.h"
#include "LevelSequenceActor.h"
#include "Kismet/GameplayStatics.h"

void AMyCutsceneManager::PlayCutscene(AActor* HeroActor)
{
    if (!CutsceneAsset)
    {
        UE_LOG(LogTemp, Warning, TEXT("AMyCutsceneManager: No CutsceneAsset assigned."));
        return;
    }

    // Build playback settings
    FMovieSceneSequencePlaybackSettings Settings;
    Settings.bAutoPlay          = false;
    Settings.PlayRate           = 1.0f;
    Settings.LoopCount.Value    = 0;      // play once
    Settings.bDisableMovementInput = true;
    Settings.bDisableLookAtInput   = true;
    Settings.bHidePlayer        = false;
    Settings.bHideHud           = false;
    Settings.bPauseAtEnd        = false;
    // ForceRestoreState: if skipped mid-sequence, actors return to pre-sequence state
    Settings.FinishCompletionStateOverride =
        EMovieSceneCompletionModeOverride::ForceRestoreState;

    // Spawn sequence actor and player
    ALevelSequenceActor* OutActor = nullptr;
    ULevelSequencePlayer* Player = ULevelSequencePlayer::CreateLevelSequencePlayer(
        this, CutsceneAsset, Settings, OutActor);

    if (!Player || !OutActor)
    {
        UE_LOG(LogTemp, Error, TEXT("AMyCutsceneManager: Failed to create sequence player."));
        return;
    }

    // Store references to prevent GC
    ActiveSequenceActor = OutActor;
    ActivePlayer        = Player;

    // Bind actor to the Hero track before play
    if (HeroActor && !HeroBindingTag.IsNone())
    {
        OutActor->SetBindingByTag(HeroBindingTag,
                                  TArray<AActor*>{ HeroActor },
                                  /*bAllowBindingsFromAsset=*/ false);
    }

    // Subscribe to completion
    Player->OnFinished.AddDynamic(this, &AMyCutsceneManager::OnCutsceneFinished);

    // Play
    Player->Play();
}

void AMyCutsceneManager::SkipCutscene()
{
    if (!ActivePlayer) { return; }

    // ForceRestoreState was set in settings, so Stop() restores actor transforms
    ActivePlayer->Stop();
    // OnCutsceneFinished will fire after Stop in certain configurations;
    // call RestorePlayerControl directly to be safe
    RestorePlayerControl();
}

void AMyCutsceneManager::OnCutsceneFinished()
{
    RestorePlayerControl();
    ActivePlayer        = nullptr;
    ActiveSequenceActor = nullptr;
}

void AMyCutsceneManager::RestorePlayerControl()
{
    APlayerController* PC = GetWorld()->GetFirstPlayerController();
    if (!PC) { return; }

    // Return camera to the player pawn with a short blend
    APawn* PlayerPawn = PC->GetPawn();
    if (PlayerPawn)
    {
        PC->SetViewTargetWithBlend(PlayerPawn, 0.5f, VTBlend_Cubic);
    }

    PC->SetIgnoreMoveInput(false);
    PC->SetIgnoreLookInput(false);
}
```

---

## Pattern 2: In-Game Triggered Camera (No Input Lockout)

A background camera sequence that plays without hiding the HUD or disabling input — for
scripted gameplay moments (e.g. a crane shot during a boss encounter).

```cpp
// In a GameMode or GameplayComponent
void AMyGameMode::TriggerBossArrivalCamera()
{
    if (!BossArrivalSequence) { return; }

    FMovieSceneSequencePlaybackSettings Settings;
    Settings.bAutoPlay             = false;
    Settings.PlayRate              = 1.0f;
    Settings.LoopCount.Value       = 0;
    Settings.bDisableMovementInput = false;  // player keeps control
    Settings.bDisableLookAtInput   = false;
    Settings.bHidePlayer           = false;
    Settings.bHideHud              = false;
    Settings.bDisableCameraCuts    = false;  // allow camera cuts in sequence
    Settings.bPauseAtEnd           = false;

    ALevelSequenceActor* OutActor  = nullptr;
    BossArrivalPlayer = ULevelSequencePlayer::CreateLevelSequencePlayer(
        this, BossArrivalSequence, Settings, OutActor);
    BossArrivalSequenceActor = OutActor;

    if (BossArrivalPlayer)
    {
        // React to camera cut events (e.g. to trigger audio stingers)
        BossArrivalPlayer->OnCameraCut.AddDynamic(
            this, &AMyGameMode::OnBossArrivalCameraCut);

        BossArrivalPlayer->OnFinished.AddDynamic(
            this, &AMyGameMode::OnBossArrivalCameraFinished);

        BossArrivalPlayer->Play();
    }
}

UFUNCTION()
void AMyGameMode::OnBossArrivalCameraCut(UCameraComponent* NewCamera)
{
    // e.g. play a stinger sound effect when cut happens
    UGameplayStatics::PlaySound2D(this, CameraCutStinger);
}

UFUNCTION()
void AMyGameMode::OnBossArrivalCameraFinished()
{
    // Return to gameplay camera
    APlayerController* PC = GetWorld()->GetFirstPlayerController();
    if (PC && PC->GetPawn())
    {
        PC->SetViewTargetWithBlend(PC->GetPawn(), 1.0f, VTBlend_EaseInOut, 2.0f);
    }
    BossArrivalPlayer        = nullptr;
    BossArrivalSequenceActor = nullptr;
}
```

---

## Pattern 3: Scripted Event Sequence with Runtime Actor Binding

A scripted event that binds multiple actors at runtime (e.g. two NPCs performing an
interaction authored in Sequencer with tag-based bindings).

### Sequence Setup (in Editor)

1. Create a LevelSequence asset called `LS_NPCHandshake`.
2. Add two possessable bindings: tag them `NPC_A` and `NPC_B` via right-click -> Tags.
3. Add transform, skeletal animation, and event tracks to each binding.
4. Add an Event Track at frame 60 bound to `TriggerHandshakeReaction()`.

### C++ Runtime Binding

```cpp
// ScriptedEventTrigger.cpp

void AScriptedEventTrigger::TriggerHandshakeSequence(
    AActor* NpcA, AActor* NpcB)
{
    if (!HandshakeSequence) { return; }

    FMovieSceneSequencePlaybackSettings Settings;
    Settings.bAutoPlay          = false;
    Settings.LoopCount.Value    = 0;
    Settings.bDisableMovementInput = false;
    Settings.bHideHud           = false;
    Settings.FinishCompletionStateOverride =
        EMovieSceneCompletionModeOverride::ForceRestoreState;

    ALevelSequenceActor* OutActor = nullptr;
    HandshakePlayer = ULevelSequencePlayer::CreateLevelSequencePlayer(
        this, HandshakeSequence, Settings, OutActor);
    HandshakeSequenceActor = OutActor;

    if (!HandshakePlayer) { return; }

    // Bind both NPCs before playing
    HandshakeSequenceActor->SetBindingByTag(
        FName("NPC_A"), TArray<AActor*>{ NpcA }, false);
    HandshakeSequenceActor->SetBindingByTag(
        FName("NPC_B"), TArray<AActor*>{ NpcB }, false);

    HandshakePlayer->OnFinished.AddDynamic(
        this, &AScriptedEventTrigger::OnHandshakeFinished);
    HandshakePlayer->Play();
}

// Called by the Event Track at frame 60 (must be on an object in event context)
UFUNCTION(BlueprintCallable, Category = "Cinematics")
void AScriptedEventTrigger::TriggerHandshakeReaction()
{
    // Gameplay response to the mid-sequence event
    UE_LOG(LogTemp, Log, TEXT("Handshake event fired from Sequencer!"));
}

UFUNCTION()
void AScriptedEventTrigger::OnHandshakeFinished()
{
    HandshakePlayer        = nullptr;
    HandshakeSequenceActor = nullptr;
}
```

---

## Pattern 4: Looping Ambient Sequence (Background Atmosphere)

A sequence that loops indefinitely to drive ambient elements (foliage sway, light flicker,
water ripple) without affecting player state.

```cpp
void AAtmosphereManager::BeginPlay()
{
    Super::BeginPlay();

    if (!AmbientSequence) { return; }

    FMovieSceneSequencePlaybackSettings Settings;
    Settings.bAutoPlay          = false;
    Settings.LoopCount.Value    = -1;   // -1 = infinite
    Settings.bDisableMovementInput = false;
    Settings.bDisableLookAtInput   = false;
    Settings.bHidePlayer        = false;
    Settings.bHideHud           = false;
    Settings.bDisableCameraCuts = true; // do not take over camera

    ALevelSequenceActor* OutActor = nullptr;
    AmbientPlayer = ULevelSequencePlayer::CreateLevelSequencePlayer(
        this, AmbientSequence, Settings, OutActor);
    AmbientSequenceActor = OutActor;

    if (AmbientPlayer)
    {
        AmbientPlayer->Play();
    }
}

void AAtmosphereManager::EndPlay(const EEndPlayReason::Type Reason)
{
    if (AmbientPlayer && AmbientPlayer->IsPlaying())
    {
        AmbientPlayer->Stop();
    }
    Super::EndPlay(Reason);
}
```

---

## Pattern 5: CineCameraActor — Runtime Camera Setup in Sequence

Spawning and configuring a `ACineCameraActor` then handing it to a sequence.

```cpp
#include "CineCameraActor.h"
#include "CineCameraComponent.h"
#include "CineCameraSettings.h"   // FCameraFilmbackSettings, FCameraLensSettings, FCameraFocusSettings

ACineCameraActor* AMyDirector::SpawnCineCamera(
    FVector Location, FRotator Rotation)
{
    FActorSpawnParameters Params;
    Params.Owner = this;

    ACineCameraActor* Camera = GetWorld()->SpawnActor<ACineCameraActor>(
        ACineCameraActor::StaticClass(),
        Location, Rotation, Params);

    if (!Camera) { return nullptr; }

    UCineCameraComponent* CineComp = Camera->GetCineCameraComponent();

    // 35mm full-frame sensor
    FCameraFilmbackSettings Filmback;
    Filmback.SensorWidth  = 36.0f;  // mm
    Filmback.SensorHeight = 24.0f;
    CineComp->SetFilmback(Filmback);

    // 35mm prime lens
    FCameraLensSettings Lens;
    Lens.MinFocalLength = 35.0f;
    Lens.MaxFocalLength = 35.0f;
    Lens.MinFStop       = 1.4f;
    Lens.MaxFStop       = 16.0f;
    Lens.MinimumFocusDistance = 30.0f;
    CineComp->SetLensSettings(Lens);

    CineComp->SetCurrentFocalLength(35.0f);
    CineComp->SetCurrentAperture(2.0f);

    // Manual focus at 5 meters (500 cm)
    FCameraFocusSettings FocusSettings;
    FocusSettings.FocusMethod         = ECameraFocusMethod::Manual;
    FocusSettings.ManualFocusDistance = 500.0f;
    FocusSettings.bSmoothFocusChanges      = true;
    FocusSettings.FocusSmoothingInterpSpeed = 8.0f;
    CineComp->SetFocusSettings(FocusSettings);

    // Lookat tracking toward hero
    Camera->LookatTrackingSettings.bEnableLookAtTracking     = true;
    Camera->LookatTrackingSettings.ActorToTrack              = HeroActor;
    Camera->LookatTrackingSettings.RelativeOffset            = FVector(0, 0, 80.f);
    Camera->LookatTrackingSettings.LookAtTrackingInterpSpeed = 4.0f;
    Camera->LookatTrackingSettings.bAllowRoll                = false;

    return Camera;
}
```

---

## Pattern 6: Partial Playback — Play a Specific Frame Range

Play only a portion of a sequence (e.g. frames 0-60 for an intro, then frames 61-120 for the
main loop).

```cpp
void AMySequenceController::PlayIntroSegment()
{
    if (!FullSequence) { return; }

    FMovieSceneSequencePlaybackSettings Settings;
    Settings.bAutoPlay       = false;
    Settings.LoopCount.Value = 0;

    ALevelSequenceActor* OutActor = nullptr;
    ActivePlayer = ULevelSequencePlayer::CreateLevelSequencePlayer(
        this, FullSequence, Settings, OutActor);
    ActiveSequenceActor = OutActor;

    if (!ActivePlayer) { return; }

    // Restrict playback to frames 0–60 (at the sequence's display rate)
    ActivePlayer->SetFrameRange(0, 60);

    ActivePlayer->OnFinished.AddDynamic(this, &AMySequenceController::OnIntroFinished);
    ActivePlayer->Play();
}

UFUNCTION()
void AMySequenceController::OnIntroFinished()
{
    if (!ActivePlayer) { return; }

    // Switch to main loop segment: frames 61-120, loop indefinitely
    ActivePlayer->OnFinished.RemoveDynamic(
        this, &AMySequenceController::OnIntroFinished);

    ActivePlayer->SetFrameRange(61, 59);   // start=61, duration=59 frames
    ActivePlayer->PlayLooping(-1);         // -1 = infinite
}
```

---

## Pattern 7: Sub-Sequence Snapshot Inspection

Read the current shot name from a master sequence containing multiple sub-sequences (shots).

```cpp
void AMyHUD::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    ULevelSequencePlayer* Player = ActiveSequenceActor
        ? ActiveSequenceActor->GetSequencePlayer()
        : nullptr;

    if (!Player || !Player->IsPlaying()) { return; }

    FLevelSequencePlayerSnapshot Snapshot;
    Player->TakeFrameSnapshot(Snapshot);

    // Snapshot fields:
    //   RootName          -- name of the root sequence
    //   RootTime          -- current time in root sequence (FQualifiedFrameTime)
    //   CurrentShotName   -- name of the active sub-sequence/shot
    //   CurrentShotLocalTime -- time within the current shot
    //   SourceTimecode    -- timecode string
    //   CameraComponent   -- currently active camera component (TSoftObjectPtr)
    //   ActiveShot        -- ULevelSequence* of the current shot

    FString ShotInfo = FString::Printf(
        TEXT("Shot: %s | Root Frame: %d"),
        *Snapshot.CurrentShotName,
        Snapshot.RootTime.Time.FrameNumber.Value);

    DrawDebugString(GetWorld(), FVector::ZeroVector, ShotInfo, nullptr,
                    FColor::White, 0.0f, true);
}
```

---

## Pattern 8: Replicated Cutscene (Multiplayer)

Play a cutscene on all clients synchronized via server authority.

```cpp
// Server-side: spawn and configure the sequence actor with replication enabled
void AMyNetworkGameMode::Server_PlayCutscene_Implementation(
    ULevelSequence* Sequence)
{
    FActorSpawnParameters SpawnParams;
    SpawnParams.Owner = this;

    // Spawn the actor on the server — it will replicate to clients
    ALevelSequenceActor* SeqActor = GetWorld()->SpawnActor<ALevelSequenceActor>(
        ALevelSequenceActor::StaticClass(), FTransform::Identity, SpawnParams);

    if (!SeqActor) { return; }

    // Enable replication before setting any state
    SeqActor->SetReplicatePlayback(true);   // bReplicatePlayback
    SeqActor->SetSequence(Sequence);

    // PlaybackSettings replicated to clients
    SeqActor->PlaybackSettings.bAutoPlay          = false;
    SeqActor->PlaybackSettings.LoopCount.Value    = 0;
    SeqActor->PlaybackSettings.bDisableMovementInput = true;
    SeqActor->PlaybackSettings.bHidePlayer        = false;

    ULevelSequencePlayer* Player = SeqActor->GetSequencePlayer();
    if (Player)
    {
        Player->OnFinished.AddDynamic(this, &AMyNetworkGameMode::OnReplicatedCutsceneFinished);
        Player->Play();   // server starts playback; clients follow via NetSyncProps
    }
}

UFUNCTION()
void AMyNetworkGameMode::OnReplicatedCutsceneFinished()
{
    // Notify all clients to restore input
    Multicast_RestorePlayerInput();
}

UFUNCTION(NetMulticast, Reliable)
void AMyNetworkGameMode::Multicast_RestorePlayerInput()
{
    APlayerController* PC = GetWorld()->GetFirstPlayerController();
    if (PC)
    {
        PC->SetIgnoreMoveInput(false);
        PC->SetIgnoreLookInput(false);
        APawn* Pawn = PC->GetPawn();
        if (Pawn)
        {
            PC->SetViewTargetWithBlend(Pawn, 0.5f);
        }
    }
}
```

---

## API Quick Reference

### ULevelSequencePlayer::CreateLevelSequencePlayer
```
static ULevelSequencePlayer* CreateLevelSequencePlayer(
    UObject* WorldContextObject,
    ULevelSequence* LevelSequence,
    FMovieSceneSequencePlaybackSettings Settings,
    ALevelSequenceActor*& OutActor)
```

### FMovieSceneSequencePlaybackSettings fields
```
bool  bAutoPlay             -- auto-play on BeginPlay
float PlayRate              -- 1.0 = normal, 2.0 = 2x, -1.0 = reverse
float StartTime             -- offset in seconds from sequence start
int32 LoopCount.Value       -- 0 = no loop, -1 = infinite, N = N loops
bool  bDisableMovementInput -- locks player movement during play
bool  bDisableLookAtInput   -- locks player look during play
bool  bHidePlayer           -- hides player pawn mesh
bool  bHideHud              -- hides HUD widgets
bool  bDisableCameraCuts    -- prevents sequence from overriding camera
bool  bPauseAtEnd           -- pauses (not stops) at last frame
EMovieSceneCompletionModeOverride FinishCompletionStateOverride
```

### ALevelSequenceActor binding methods
```
void SetBinding(FMovieSceneObjectBindingID, TArray<AActor*>, bAllowFromAsset)
void SetBindingByTag(FName Tag, TArray<AActor*>, bAllowFromAsset)
void AddBinding(FMovieSceneObjectBindingID, AActor*, bAllowFromAsset)
void AddBindingByTag(FName Tag, AActor*, bAllowFromAsset)
void RemoveBinding(FMovieSceneObjectBindingID, AActor*)
void RemoveBindingByTag(FName Tag, AActor*)
void ResetBinding(FMovieSceneObjectBindingID)
void ResetBindings()
FMovieSceneObjectBindingID FindNamedBinding(FName Tag) const
const TArray<FMovieSceneObjectBindingID>& FindNamedBindings(FName Tag) const
```

### UMovieSceneSequencePlayer playback control
```
void Play()
void PlayReverse()
void PlayLooping(int32 NumLoops = -1)
void Pause()
void Stop()
void StopAtCurrentTime()
void GoToEndAndStop()
void SetPlayRate(float)
void SetFrameRange(int32 StartFrame, int32 Duration, float SubFrames = 0.f)
void SetTimeRange(float StartTime, float Duration)
void SetPlaybackPosition(FMovieSceneSequencePlaybackParams)
void PlayTo(FMovieSceneSequencePlaybackParams, FMovieSceneSequencePlayToParams)
void RestoreState()
void SetCompletionModeOverride(EMovieSceneCompletionModeOverride)
bool IsPlaying() const
bool IsPaused() const
bool IsReversed() const
float GetPlayRate() const
FQualifiedFrameTime GetCurrentTime() const
FQualifiedFrameTime GetDuration() const
int32 GetFrameDuration() const
TArray<UObject*> GetBoundObjects(FMovieSceneObjectBindingID)
```

### UCineCameraComponent key properties/methods
```
FCameraFilmbackSettings Filmback             -- SensorWidth, SensorHeight (mm)
FCameraLensSettings     LensSettings         -- MinFocalLength, MaxFocalLength, MinFStop, MaxFStop
FCameraFocusSettings    FocusSettings        -- FocusMethod, ManualFocusDistance (cm)
float CurrentFocalLength                     -- current zoom (mm), Interp-animatable
float CurrentAperture                        -- f-stop, Interp-animatable
float CurrentFocusDistance                   -- read-only, derived from FocusSettings

void SetFilmback(const FCameraFilmbackSettings&)
void SetLensSettings(const FCameraLensSettings&)
void SetFocusSettings(const FCameraFocusSettings&)
void SetCurrentFocalLength(float)
void SetCurrentAperture(float)
float GetHorizontalFieldOfView() const
float GetVerticalFieldOfView() const
```

### ULevelSequencePlayer additional delegates/events
```
FOnLevelSequencePlayerCameraCutEvent OnCameraCut   -- fires on every camera cut
FOnMovieSceneSequencePlayerEvent     OnPlay
FOnMovieSceneSequencePlayerEvent     OnPlayReverse
FOnMovieSceneSequencePlayerEvent     OnStop
FOnMovieSceneSequencePlayerEvent     OnPause
FOnMovieSceneSequencePlayerEvent     OnFinished
FOnMovieSceneSequencePlayerNativeEvent OnNativeFinished
```

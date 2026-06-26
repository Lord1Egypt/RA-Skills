# CMC Extension Patterns

Complete code templates for extending `UCharacterMovementComponent` with custom movement modes, networked prediction, and custom move data.

---

## Custom CMC Subclass Header

```cpp
// MyCMC.h
#pragma once
#include "GameFramework/CharacterMovementComponent.h"
#include "MyCMC.generated.h"

UENUM(BlueprintType)
enum class ECustomMovementMode : uint8
{
    None     = 0,
    WallRun  = 1,
    Climb    = 2,
    Dash     = 3
};

UCLASS()
class MYGAME_API UMyCMC : public UCharacterMovementComponent
{
    GENERATED_BODY()

public:
    UMyCMC();

    // --- Custom movement state ---
    UPROPERTY(Transient)
    uint8 bWantsToWallRun : 1;

    UPROPERTY(Transient)
    FVector WallRunNormal;

    // --- Overrides ---
    virtual void PhysCustom(float deltaTime, int32 Iterations) override;
    virtual void OnMovementModeChanged(EMovementMode PrevMode, uint8 PrevCustomMode) override;
    virtual FNetworkPredictionData_Client* GetPredictionData_Client() const override;

protected:
    void PhysWallRun(float deltaTime, int32 Iterations);
    void PhysClimb(float deltaTime, int32 Iterations);
    void PhysDash(float deltaTime, int32 Iterations);

    bool CanWallRun() const;
    void EnterWallRun(const FHitResult& WallHit);
    void ExitWallRun();
};
```

---

## FSavedMove_Character Subclass

```cpp
// MySavedMove.h (can live in MyCMC.h)
class FMySavedMove : public FSavedMove_Character
{
public:
    typedef FSavedMove_Character Super;

    // Custom saved state
    uint8 bSavedWantsToWallRun : 1;
    FVector SavedWallRunNormal;

    virtual void Clear() override
    {
        Super::Clear();
        bSavedWantsToWallRun = 0;
        SavedWallRunNormal = FVector::ZeroVector;
    }

    virtual void SetMoveFor(
        ACharacter* C,
        float InDeltaTime,
        FVector const& NewAccel,
        FNetworkPredictionData_Client_Character& ClientData) override
    {
        Super::SetMoveFor(C, InDeltaTime, NewAccel, ClientData);

        // Capture custom state from CMC before the move executes
        UMyCMC* CMC = Cast<UMyCMC>(C->GetCharacterMovement());
        if (CMC)
        {
            bSavedWantsToWallRun = CMC->bWantsToWallRun;
            SavedWallRunNormal = CMC->WallRunNormal;
        }
    }

    virtual void PrepMoveFor(ACharacter* C) override
    {
        Super::PrepMoveFor(C);

        // Restore custom state before replaying this move
        UMyCMC* CMC = Cast<UMyCMC>(C->GetCharacterMovement());
        if (CMC)
        {
            CMC->bWantsToWallRun = bSavedWantsToWallRun;
            CMC->WallRunNormal = SavedWallRunNormal;
        }
    }

    virtual uint8 GetCompressedFlags() const override
    {
        uint8 Result = Super::GetCompressedFlags();

        if (bSavedWantsToWallRun)
        {
            Result |= FLAG_Custom_0;  // 0x10
        }

        return Result;
    }

    virtual bool CanCombineWith(
        const FSavedMovePtr& NewMove,
        ACharacter* InCharacter,
        float MaxDelta) const override
    {
        const FMySavedMove* Other = static_cast<const FMySavedMove*>(NewMove.Get());

        if (bSavedWantsToWallRun != Other->bSavedWantsToWallRun)
        {
            return false;
        }

        if (bSavedWantsToWallRun && !SavedWallRunNormal.Equals(Other->SavedWallRunNormal, 0.1f))
        {
            return false;
        }

        return Super::CanCombineWith(NewMove, InCharacter, MaxDelta);
    }
};
```

---

## FNetworkPredictionData_Client_Character Subclass

```cpp
class FMyNetworkPredictionData : public FNetworkPredictionData_Client_Character
{
public:
    typedef FNetworkPredictionData_Client_Character Super;

    FMyNetworkPredictionData(const UCharacterMovementComponent& ClientMovement)
        : Super(ClientMovement) {}

    virtual FSavedMovePtr AllocateNewMove() override
    {
        return FSavedMovePtr(new FMySavedMove());
    }
};
```

---

## GetPredictionData_Client Override (Lazy-Init Pattern)

Override on your CMC subclass. Uses `const_cast` because the base method is `const` but the prediction data is mutable state:

```cpp
FNetworkPredictionData_Client* UMyCMC::GetPredictionData_Client() const
{
    if (ClientPredictionData == nullptr)
    {
        UMyCMC* MutableThis = const_cast<UMyCMC*>(this);
        MutableThis->ClientPredictionData = new FMyNetworkPredictionData(*this);
    }

    return ClientPredictionData;
}
```

---

## Wall-Run PhysCustom Implementation

```cpp
void UMyCMC::PhysCustom(float deltaTime, int32 Iterations)
{
    Super::PhysCustom(deltaTime, Iterations);

    switch (static_cast<ECustomMovementMode>(CustomMovementMode))
    {
    case ECustomMovementMode::WallRun:
        PhysWallRun(deltaTime, Iterations);
        break;
    case ECustomMovementMode::Climb:
        PhysClimb(deltaTime, Iterations);
        break;
    case ECustomMovementMode::Dash:
        PhysDash(deltaTime, Iterations);
        break;
    default:
        UE_LOG(LogTemp, Warning, TEXT("Unknown custom movement mode: %d"), CustomMovementMode);
        SetMovementMode(MOVE_Falling);
        break;
    }
}

void UMyCMC::PhysWallRun(float deltaTime, int32 Iterations)
{
    if (deltaTime < MIN_TICK_TIME) { return; }
    if (!bWantsToWallRun || !CanWallRun())
    {
        ExitWallRun();
        return;
    }

    // Wall-run direction: cross gravity up with wall normal
    FVector RunDir = FVector::CrossProduct(WallRunNormal, FVector::UpVector);

    // Match character's forward to determine left vs right wall
    if (FVector::DotProduct(RunDir, UpdatedComponent->GetForwardVector()) < 0.f)
    {
        RunDir *= -1.f;
    }

    // Accelerate along wall
    Velocity = RunDir * MaxCustomMovementSpeed;

    // Apply slight gravity pull toward wall to maintain contact
    Velocity += -WallRunNormal * 50.f;

    // Move
    FHitResult Hit;
    SafeMoveUpdatedComponent(Velocity * deltaTime, UpdatedComponent->GetComponentQuat(),
                             true, Hit);

    // Verify wall is still there
    if (Hit.bBlockingHit)
    {
        WallRunNormal = Hit.Normal;
    }
    else
    {
        // Lost wall contact — check with a trace
        FHitResult WallCheck;
        FVector TraceEnd = UpdatedComponent->GetComponentLocation()
                           - WallRunNormal * 100.f;
        bool bStillOnWall = GetWorld()->LineTraceSingleByChannel(
            WallCheck,
            UpdatedComponent->GetComponentLocation(),
            TraceEnd,
            ECC_Visibility);

        if (!bStillOnWall)
        {
            ExitWallRun();
        }
    }
}

void UMyCMC::EnterWallRun(const FHitResult& WallHit)
{
    WallRunNormal = WallHit.Normal;
    bWantsToWallRun = true;
    SetMovementMode(MOVE_Custom, static_cast<uint8>(ECustomMovementMode::WallRun));
}

void UMyCMC::ExitWallRun()
{
    bWantsToWallRun = false;
    WallRunNormal = FVector::ZeroVector;
    SetMovementMode(MOVE_Falling);
}
```

---

## Custom Network Move Data

For custom data that exceeds the four CompressedFlags bits, derive `FCharacterNetworkMoveData`:

```cpp
struct FMyNetworkMoveData : public FCharacterNetworkMoveData
{
    FVector CustomWallNormal = FVector::ZeroVector;
    uint8 CustomMoveMode = 0;

    virtual void ClientFillNetworkMoveData(
        const FSavedMove_Character& ClientMove,
        ENetworkMoveType MoveType) override
    {
        Super::ClientFillNetworkMoveData(ClientMove, MoveType);

        const FMySavedMove& MyMove = static_cast<const FMySavedMove&>(ClientMove);
        CustomWallNormal = MyMove.SavedWallRunNormal;
    }

    virtual bool Serialize(
        UCharacterMovementComponent& CharacterMovement,
        FArchive& Ar,
        UPackageMap* PackageMap,
        ENetworkMoveType MoveType) override
    {
        Super::Serialize(CharacterMovement, Ar, PackageMap, MoveType);

        Ar << CustomWallNormal;
        Ar << CustomMoveMode;

        return !Ar.IsError();
    }
};

struct FMyNetworkMoveDataContainer : public FCharacterNetworkMoveDataContainer
{
    FMyNetworkMoveData CustomDefaultMoveData[3];

    FMyNetworkMoveDataContainer()
    {
        NewMoveData = &CustomDefaultMoveData[0];
        PendingMoveData = &CustomDefaultMoveData[1];
        OldMoveData = &CustomDefaultMoveData[2];
    }
};
```

Register the container in the CMC constructor:

```cpp
UMyCMC::UMyCMC()
{
    static FMyNetworkMoveDataContainer MoveDataContainer;
    SetNetworkMoveDataContainer(MoveDataContainer);
}
```

**Important:** The container must be `static` or otherwise outlive the CMC. `SetNetworkMoveDataContainer` stores a pointer, not a copy.

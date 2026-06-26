# RPC Decision Guide

Reference for choosing the correct RPC type (Server, Client, NetMulticast) and
reliability level (Reliable, Unreliable) in Unreal Engine multiplayer code.
All patterns are grounded in real `APlayerController` usage from `PlayerController.h`.

---

## RPC Type Quick Reference

| Specifier       | Called on  | Executes on              | Typical use                            |
|-----------------|------------|--------------------------|----------------------------------------|
| `Server`        | Client     | Server (Authority)       | Player input, purchase, ability use    |
| `Client`        | Server     | Owning client only       | UI updates, player-specific feedback   |
| `NetMulticast`  | Server     | Server + all clients     | World effects visible to everyone      |

---

## Decision Flowchart

```
Is this a request from a player to change game state?
  YES --> use Server RPC (client calls, server executes)
  NO  --> continue

Should this run only on one specific player's machine?
  YES --> use Client RPC (server calls, owning client executes)
  NO  --> continue

Should this run on the server AND every connected client simultaneously?
  YES --> use NetMulticast RPC (server calls, all machines execute)
  NO  --> reconsider: is property replication a better fit?
```

---

## Server RPC

**Who calls it**: the client (specifically the owning client of the actor).
**Who executes it**: the server.
**Primary use**: forwarding player intent to the authoritative machine.

All Server RPCs that change game state must include `WithValidation`. This generates
a `_Validate` function the engine calls before `_Implementation`. Returning `false`
from `_Validate` kicks the calling client.

```cpp
// Declaration
UFUNCTION(Server, Reliable, WithValidation)
void ServerFireWeapon(FVector_NetQuantize MuzzleLocation,
                      FVector_NetQuantizeNormal Direction);

// Implementation (.cpp)
void AMyCharacter::ServerFireWeapon_Implementation(
    FVector_NetQuantize MuzzleLocation,
    FVector_NetQuantizeNormal Direction)
{
    // Server performs authoritative hit trace
    FHitResult Hit;
    FCollisionQueryParams Params;
    Params.AddIgnoredActor(this);

    if (GetWorld()->LineTraceSingleByChannel(
            Hit, MuzzleLocation, MuzzleLocation + Direction * 10000.f,
            ECC_Pawn, Params))
    {
        if (AMyCharacter* Victim = Cast<AMyCharacter>(Hit.GetActor()))
        {
            Victim->ApplyDamage_Authority(WeaponDamage);
        }
    }

    // Spawn bullet tracer effect on all clients
    MulticastSpawnTracer(MuzzleLocation, Hit.ImpactPoint);
}

bool AMyCharacter::ServerFireWeapon_Validate(
    FVector_NetQuantize MuzzleLocation,
    FVector_NetQuantizeNormal Direction)
{
    // Reject zero directions
    if (Direction.IsNearlyZero()) return false;
    // Reject muzzle locations impossibly far from actor
    if (FVector::Dist(MuzzleLocation, GetActorLocation()) > 500.f) return false;
    return true;
}
```

Real examples from `PlayerController.h`:

```cpp
// Player acknowledges pawn possession — must not be lost, Reliable
UFUNCTION(reliable, server, WithValidation)
void ServerAcknowledgePossession(class APawn* P);

// Spectator position — sent frequently, OK to drop, Unreliable
UFUNCTION(unreliable, server, WithValidation)
void ServerSetSpectatorLocation(FVector NewLoc, FRotator NewRot);

// Server restart — must not be dropped, Reliable
UFUNCTION(reliable, server, WithValidation)
void ServerRestartPlayer();

// Camera update — sent frequently, can be dropped, Unreliable
UFUNCTION(unreliable, server, WithValidation)
void ServerUpdateCamera(FVector_NetQuantize CamLoc, int32 CamPitchAndYaw);
```

### When to use Reliable vs Unreliable for Server RPCs

| Scenario                          | Reliability  |
|-----------------------------------|--------------|
| Purchase, ability activation      | Reliable     |
| Possession / respawn              | Reliable     |
| Player name or setting change     | Reliable     |
| Level streaming notification      | Reliable     |
| Frequent position / camera update | Unreliable   |
| High-frequency input relay        | Unreliable   |

---

## Client RPC

**Who calls it**: the server.
**Who executes it**: the owning client of the actor.
**Primary use**: sending player-specific information or triggering private feedback.

`Client` RPCs do not need `WithValidation` — the server already has authority.

```cpp
// Declaration
UFUNCTION(Client, Reliable)
void ClientShowMatchResult(bool bWon, int32 FinalScore);

// Implementation
void AMyPlayerController::ClientShowMatchResult_Implementation(
    bool bWon, int32 FinalScore)
{
    // Runs only on the owning client — safe to access local UI
    if (UMyHUD* HUD = Cast<UMyHUD>(GetHUD()))
    {
        HUD->ShowMatchResult(bWon, FinalScore);
    }
}
```

Real examples from `PlayerController.h`:

```cpp
// Tell the client it's been muted — Reliable, player must know
UFUNCTION(Reliable, Client)
void ClientMutePlayer(FUniqueNetIdRepl PlayerId);

// Send a localized message to the owning client — Reliable
UFUNCTION(Reliable, Client)
void ClientReceiveLocalizedMessage(TSubclassOf<ULocalMessage> Message,
    int32 Switch,
    APlayerState* RelatedPlayerState_1,
    APlayerState* RelatedPlayerState_2,
    UObject* OptionalObject);

// Client spectator waiting state — Reliable, state change must not be lost
UFUNCTION(client, reliable)
void ClientSetSpectatorWaiting(bool bWaiting);

// Async physics timestamp sync — Reliable, setup data
UFUNCTION(Client, Reliable)
void ClientSetupNetworkPhysicsTimestamp(FAsyncPhysicsTimestamp Timestamp);

// Time dilation update — Unreliable, continuously corrected
UFUNCTION(Client, Unreliable)
void ClientAckTimeDilation(float TimeDilation, int32 ServerStep);
```

### When to use Reliable vs Unreliable for Client RPCs

| Scenario                                   | Reliability  |
|--------------------------------------------|--------------|
| UI state change (match result, kill feed)  | Reliable     |
| Player kicked / game over notification     | Reliable     |
| View target / camera set                   | Reliable     |
| Sound / haptic triggered by server event   | Reliable     |
| Camera time dilation correction            | Unreliable   |
| High-frequency positional feedback effect  | Unreliable   |

---

## NetMulticast RPC

**Who calls it**: the server.
**Who executes it**: the server AND all clients that have this actor replicated to them.
**Primary use**: cosmetic world events that everyone should see.

```cpp
// Declaration
UFUNCTION(NetMulticast, Unreliable)
void MulticastPlayExplosionEffect(FVector Location, float Radius);

// Implementation
void AMyActor::MulticastPlayExplosionEffect_Implementation(
    FVector Location, float Radius)
{
    // Runs on server and all clients — guard so server doesn't spawn visual effects
    if (!HasAuthority())
    {
        UGameplayStatics::SpawnEmitterAtLocation(
            GetWorld(), ExplosionFX, Location);
        UGameplayStatics::PlaySoundAtLocation(
            GetWorld(), ExplosionSound, Location);
    }
    // Both server and client: apply physics impulse to overlapping actors
    ApplyExplosionImpulse(Location, Radius);
}
```

### Multicast vs Property Replication

Prefer multicast for **one-shot events** (sounds, VFX, transient animations).
Prefer **property replication** for **persistent state** (health, flags, positions).

| Data type                          | Mechanism                        |
|------------------------------------|----------------------------------|
| Plays once, no recovery needed     | NetMulticast (Unreliable)        |
| Plays once, must not be missed     | NetMulticast (Reliable)          |
| Persists on clients that join late | UPROPERTY(Replicated)            |
| Different value per client         | Client RPC                       |

---

## Reliable vs Unreliable — Definitive Rules

### Use Reliable when

- The action has **permanent game state consequences** (purchase, death, spawn).
- The receiver must **acknowledge** receipt to proceed (possession, level load).
- The data is **not redundant** — there is no future update that carries the same info.
- Dropping the packet would cause a **visible or gameplay-breaking desync**.

### Use Unreliable when

- The data is **superseded frequently** by the next tick's update (position, rotation).
- It is purely **cosmetic** (hit sparks, footstep dust, screenshake).
- Dropping it produces only a minor visual glitch, not a gameplay error.
- The RPC is called **very often** (every tick or multiple times per second) — using
  Reliable for high-frequency calls saturates the reliable channel and causes lag spikes.

### Reliable Channel Saturation Warning

The reliable channel is a FIFO queue. If too many reliable messages queue up (e.g.,
a Server Reliable RPC called every frame), the connection will stall waiting for
acknowledgments. This manifests as rubberbanding and eventually a timeout disconnect.

**Rule**: never call a Reliable RPC more than once per server tick per connection.

---

## Ownership Requirement for RPCs

RPCs will silently fail (not execute, not error) if the actor does not have a valid
network connection through its ownership chain.

### Server RPC routing

The calling client must own the actor in the chain:
`APlayerController -> APawn -> AWeapon`

```
Client calls WeaponActor->ServerFire()
  -> Engine looks up WeaponActor->GetOwner() -> APawn
  -> APawn->GetOwner() -> APlayerController
  -> APlayerController->NetConnection == the calling client connection
  -> RPC is routed correctly
```

If `WeaponActor->GetOwner()` is `nullptr` or another player's controller, the RPC
will be dropped on the client. Fix: call `SetOwner(PlayerController)` on the server
after spawning the weapon.

### Client RPC routing

The server must own the actor and it must be associated with a specific player's
`NetConnection`. This is why most Client RPCs are called on `APlayerController`
directly:

```cpp
// Server code — send a message to a specific player
APlayerController* PC = GetPlayerController(PlayerIndex);
PC->ClientReceiveLocalizedMessage(Message, Switch, nullptr, nullptr, nullptr);
```

Calling a Client RPC on an actor with no owning player connection will silently fail.

---

## Common RPC Mistakes

### Calling a Server RPC from the Server

A Server RPC called from the server's own code executes locally — the engine
skips routing. This is not harmful but is misleading and wastes a function call.
Prefer calling the `_Implementation` function directly from server code if you need
to invoke the logic without network routing.

```cpp
// MISLEADING — on the server, this just calls Implementation directly
ServerDoThing();

// CLEAR — explicitly call the implementation when you know you're on the server
if (HasAuthority())
{
    ServerDoThing_Implementation(Params);
}
```

### Calling a Client RPC from the Client

A Client RPC called from the client is silently ignored — it does not route up to
the server and back down. If you need to trigger something on the server that then
responds to the client, use a Server RPC + Client RPC pair.

### Using NetMulticast Instead of Property Replication for State

Multicast RPCs are not replayed for clients that join after the call. If a new player
joins after an explosion, they will not see the aftermath if it was communicated only
via multicast. Use replicated properties for persistent state.

```cpp
// WRONG — late-joining clients miss this
MulticastSetDoorOpen(true);

// CORRECT — new clients see the correct state on join
bDoorOpen = true; // replicated property — MARK_PROPERTY_DIRTY if using Iris
```

### Missing WithValidation on Server RPCs That Modify State

Any Server RPC that changes game state (inventory, health, abilities) without
validation is a security hole. Malicious clients can send arbitrary parameter values.

```cpp
// INSECURE
UFUNCTION(Server, Reliable)
void ServerAddItem(int32 ItemId, int32 Quantity); // client can claim any quantity

// SECURE
UFUNCTION(Server, Reliable, WithValidation)
void ServerRequestPurchase(int32 ItemId); // server looks up price from data tables
```

### RPC Parameters Containing Non-Replicated Object Pointers

Object pointers in RPC parameters must be net-addressable. Passing a pointer to a
locally spawned, non-replicated UObject will result in a `nullptr` on the remote side.

```cpp
// WRONG — LocalEffect is not replicated; remote gets nullptr
ServerDoThingWithEffect(LocalEffect);

// CORRECT — pass a data class reference or an ID, look it up on the remote side
UFUNCTION(Server, Reliable, WithValidation)
void ServerActivateEffectById(int32 EffectDataId);
```

---

## RPC vs Property Replication Decision

| Situation                                          | Preferred mechanism                        |
|----------------------------------------------------|--------------------------------------------|
| Value changes on server, clients just read it      | `UPROPERTY(Replicated)`                    |
| Value changes, client needs custom callback logic  | `UPROPERTY(ReplicatedUsing = OnRep_Func)`  |
| One-shot event, all clients react simultaneously   | `NetMulticast` RPC                         |
| One-shot event, only one specific client reacts    | `Client` RPC                               |
| Client requests server to do something             | `Server` RPC                               |
| Ordering matters AND property replication is lossy | `Client` RPC (as noted in `PlayerController.h` comments) |
| High-frequency cosmetic (dust, sparks)             | `NetMulticast Unreliable` RPC              |
| Late-join clients must see current state           | `UPROPERTY(Replicated)` always             |

---

## RPC Implementation Naming Convention

UE generates the implementation and validation function names automatically from the
declared function name:

| Declared name           | Generated names                                    |
|-------------------------|----------------------------------------------------|
| `ServerFireWeapon`      | `ServerFireWeapon_Implementation`, `ServerFireWeapon_Validate` |
| `ClientShowResult`      | `ClientShowResult_Implementation`                  |
| `MulticastPlayEffect`   | `MulticastPlayEffect_Implementation`               |

The `UFUNCTION` macro declaration uses the base name. The body you write is always
`_Implementation`. Only Server RPCs with `WithValidation` also need `_Validate`.

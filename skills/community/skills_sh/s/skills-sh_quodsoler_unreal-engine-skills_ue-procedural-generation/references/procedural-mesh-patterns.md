# Procedural Mesh Patterns

Common algorithmic patterns for runtime mesh and content generation in Unreal Engine using `UProceduralMeshComponent`, `UInstancedStaticMeshComponent`, and supporting math utilities.

---

## Component Setup Boilerplate

```cpp
// Header — MyProceduralActor.h
#pragma once
#include "GameFramework/Actor.h"
#include "ProceduralMeshComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/SplineComponent.h"
#include "MyProceduralActor.generated.h"

UCLASS()
class AMyProceduralActor : public AActor
{
    GENERATED_BODY()
public:
    AMyProceduralActor();

    UPROPERTY(VisibleAnywhere)
    UProceduralMeshComponent* ProceduralMesh;

    UPROPERTY(VisibleAnywhere)
    UHierarchicalInstancedStaticMeshComponent* HISM;

    UPROPERTY(VisibleAnywhere)
    USplineComponent* Spline;
};

// Source — MyProceduralActor.cpp
#include "MyProceduralActor.h"

AMyProceduralActor::AMyProceduralActor()
{
    PrimaryActorTick.bCanEverTick = false;

    ProceduralMesh = CreateDefaultSubobject<UProceduralMeshComponent>(TEXT("ProceduralMesh"));
    SetRootComponent(ProceduralMesh);
    ProceduralMesh->bUseComplexAsSimpleCollision = false; // Use dedicated collision shapes

    HISM = CreateDefaultSubobject<UHierarchicalInstancedStaticMeshComponent>(TEXT("HISM"));
    HISM->SetupAttachment(RootComponent);
    HISM->SetNumCustomDataFloats(2); // Reserve per-instance float channels

    Spline = CreateDefaultSubobject<USplineComponent>(TEXT("Spline"));
    Spline->SetupAttachment(RootComponent);
}
```

---

## 1. Flat Quad Grid (Terrain Base)

Generates a simple flat or height-mapped mesh from a 2D grid of vertices.

```cpp
// GridSize = number of cells per side. Vertex count = (GridSize+1)^2.
// Preallocate for performance.
void ATerrainActor::GenerateFlatGrid(int32 GridSize, float CellSize,
                                      bool bCreateCollision)
{
    const int32 VertexStride = GridSize + 1;
    const int32 VertCount    = VertexStride * VertexStride;
    const int32 TriCount     = GridSize * GridSize * 6;

    TArray<FVector>         Vertices;  Vertices.Reserve(VertCount);
    TArray<int32>           Triangles; Triangles.Reserve(TriCount);
    TArray<FVector>         Normals;   Normals.Reserve(VertCount);
    TArray<FVector2D>       UVs;       UVs.Reserve(VertCount);
    TArray<FColor>          Colors;
    TArray<FProcMeshTangent> Tangents;

    for (int32 Row = 0; Row <= GridSize; Row++)
    {
        for (int32 Col = 0; Col <= GridSize; Col++)
        {
            float X = Col * CellSize;
            float Y = Row * CellSize;
            float Z = 0.f; // Replace with height sample for terrain

            Vertices.Add(FVector(X, Y, Z));
            Normals.Add(FVector::UpVector);
            UVs.Add(FVector2D((float)Col / GridSize, (float)Row / GridSize));
        }
    }

    for (int32 Row = 0; Row < GridSize; Row++)
    {
        for (int32 Col = 0; Col < GridSize; Col++)
        {
            int32 BL = Row * VertexStride + Col;
            int32 BR = BL + 1;
            int32 TL = BL + VertexStride;
            int32 TR = TL + 1;

            // Counter-clockwise = front face in UE
            Triangles.Add(BL); Triangles.Add(TL); Triangles.Add(TR);
            Triangles.Add(BL); Triangles.Add(TR); Triangles.Add(BR);
        }
    }

    ProceduralMesh->CreateMeshSection(0, Vertices, Triangles, Normals,
                                       UVs, Colors, Tangents, bCreateCollision);
}
```

### Height-Mapped Terrain with Normal Recalculation

```cpp
float SampleHeight(float X, float Y, float Scale, int32 Seed)
{
    // Seeded offset to vary noise field per-seed
    float OffsetX = (float)(Seed % 1000) * 0.01f;
    float OffsetY = (float)(Seed / 1000) * 0.01f;
    return SampleOctaveNoise(X / Scale + OffsetX, Y / Scale + OffsetY, 5, 0.5f, 2.0f, 1.0f);
}

void RecalculateNormals(const TArray<FVector>& Vertices, const TArray<int32>& Triangles,
                         TArray<FVector>& OutNormals)
{
    OutNormals.Init(FVector::ZeroVector, Vertices.Num());

    for (int32 i = 0; i + 2 < Triangles.Num(); i += 3)
    {
        const FVector& A = Vertices[Triangles[i]];
        const FVector& B = Vertices[Triangles[i + 1]];
        const FVector& C = Vertices[Triangles[i + 2]];
        FVector Normal = FVector::CrossProduct(B - A, C - A).GetSafeNormal();

        OutNormals[Triangles[i]]     += Normal;
        OutNormals[Triangles[i + 1]] += Normal;
        OutNormals[Triangles[i + 2]] += Normal;
    }

    for (FVector& N : OutNormals)
    {
        N = N.GetSafeNormal();
    }
}
```

---

## 2. Marching Cubes (Voxel Isosurface)

Extracts a triangulated isosurface from a 3D scalar field. Used for caves, asteroids, destructible terrain.

### Scalar Field Setup

```cpp
// Density grid: negative = solid, positive = air, zero = surface
struct FDensityGrid
{
    TArray<float> Values;
    FIntVector    Size;     // Width x Height x Depth
    float         VoxelSize;

    float Sample(int32 X, int32 Y, int32 Z) const
    {
        if (X < 0 || Y < 0 || Z < 0 ||
            X >= Size.X || Y >= Size.Y || Z >= Size.Z)
            return 1.f; // Outside = air
        return Values[Z * Size.Y * Size.X + Y * Size.X + X];
    }

    FVector WorldPos(int32 X, int32 Y, int32 Z) const
    {
        return FVector(X, Y, Z) * VoxelSize;
    }
};
```

### Edge Interpolation

```cpp
FVector InterpolateEdge(FVector P0, float V0, FVector P1, float V1)
{
    // Linear interpolation to find zero crossing
    float t = FMath::Clamp(-V0 / (V1 - V0 + SMALL_NUMBER), 0.f, 1.f);
    return FMath::Lerp(P0, P1, t);
}
```

### Cube Processing

```cpp
// EdgeTable and TriTable are standard 256-entry lookup tables from the original
// Lorensen & Cline (1987) paper. They map the 8-corner sign configuration
// to which edges the surface crosses and how to form triangles.
// These tables are typically 4KB total and stored as compile-time const arrays.
extern const int EdgeTable[256];
extern const int TriTable[256][16];

void ProcessCube(const FDensityGrid& Grid, int32 X, int32 Y, int32 Z,
                 TArray<FVector>& OutVerts, TArray<int32>& OutTris)
{
    // Sample 8 cube corners
    float CubeValues[8];
    CubeValues[0] = Grid.Sample(X,     Y,     Z);
    CubeValues[1] = Grid.Sample(X + 1, Y,     Z);
    CubeValues[2] = Grid.Sample(X + 1, Y + 1, Z);
    CubeValues[3] = Grid.Sample(X,     Y + 1, Z);
    CubeValues[4] = Grid.Sample(X,     Y,     Z + 1);
    CubeValues[5] = Grid.Sample(X + 1, Y,     Z + 1);
    CubeValues[6] = Grid.Sample(X + 1, Y + 1, Z + 1);
    CubeValues[7] = Grid.Sample(X,     Y + 1, Z + 1);

    FVector Corners[8];
    Corners[0] = Grid.WorldPos(X,     Y,     Z);
    Corners[1] = Grid.WorldPos(X + 1, Y,     Z);
    Corners[2] = Grid.WorldPos(X + 1, Y + 1, Z);
    Corners[3] = Grid.WorldPos(X,     Y + 1, Z);
    Corners[4] = Grid.WorldPos(X,     Y,     Z + 1);
    Corners[5] = Grid.WorldPos(X + 1, Y,     Z + 1);
    Corners[6] = Grid.WorldPos(X + 1, Y + 1, Z + 1);
    Corners[7] = Grid.WorldPos(X,     Y + 1, Z + 1);

    // Build 8-bit index from which corners are below iso-level (0)
    int32 CubeIndex = 0;
    for (int32 i = 0; i < 8; i++)
        if (CubeValues[i] < 0.f) CubeIndex |= (1 << i);

    if (EdgeTable[CubeIndex] == 0) return; // Fully inside or outside

    // Compute intersection vertices on active edges
    FVector EdgeVerts[12];
    if (EdgeTable[CubeIndex] & 1)    EdgeVerts[0]  = InterpolateEdge(Corners[0], CubeValues[0], Corners[1], CubeValues[1]);
    if (EdgeTable[CubeIndex] & 2)    EdgeVerts[1]  = InterpolateEdge(Corners[1], CubeValues[1], Corners[2], CubeValues[2]);
    if (EdgeTable[CubeIndex] & 4)    EdgeVerts[2]  = InterpolateEdge(Corners[2], CubeValues[2], Corners[3], CubeValues[3]);
    if (EdgeTable[CubeIndex] & 8)    EdgeVerts[3]  = InterpolateEdge(Corners[3], CubeValues[3], Corners[0], CubeValues[0]);
    if (EdgeTable[CubeIndex] & 16)   EdgeVerts[4]  = InterpolateEdge(Corners[4], CubeValues[4], Corners[5], CubeValues[5]);
    if (EdgeTable[CubeIndex] & 32)   EdgeVerts[5]  = InterpolateEdge(Corners[5], CubeValues[5], Corners[6], CubeValues[6]);
    if (EdgeTable[CubeIndex] & 64)   EdgeVerts[6]  = InterpolateEdge(Corners[6], CubeValues[6], Corners[7], CubeValues[7]);
    if (EdgeTable[CubeIndex] & 128)  EdgeVerts[7]  = InterpolateEdge(Corners[7], CubeValues[7], Corners[4], CubeValues[4]);
    if (EdgeTable[CubeIndex] & 256)  EdgeVerts[8]  = InterpolateEdge(Corners[0], CubeValues[0], Corners[4], CubeValues[4]);
    if (EdgeTable[CubeIndex] & 512)  EdgeVerts[9]  = InterpolateEdge(Corners[1], CubeValues[1], Corners[5], CubeValues[5]);
    if (EdgeTable[CubeIndex] & 1024) EdgeVerts[10] = InterpolateEdge(Corners[2], CubeValues[2], Corners[6], CubeValues[6]);
    if (EdgeTable[CubeIndex] & 2048) EdgeVerts[11] = InterpolateEdge(Corners[3], CubeValues[3], Corners[7], CubeValues[7]);

    // Add triangles from TriTable
    for (int32 i = 0; TriTable[CubeIndex][i] != -1; i += 3)
    {
        int32 BaseIdx = OutVerts.Num();
        OutVerts.Add(EdgeVerts[TriTable[CubeIndex][i]]);
        OutVerts.Add(EdgeVerts[TriTable[CubeIndex][i + 1]]);
        OutVerts.Add(EdgeVerts[TriTable[CubeIndex][i + 2]]);
        OutTris.Add(BaseIdx); OutTris.Add(BaseIdx + 1); OutTris.Add(BaseIdx + 2);
    }
}
```

### Full Grid March

```cpp
void MarchCubes(const FDensityGrid& Grid, UProceduralMeshComponent* Mesh)
{
    TArray<FVector> Vertices, Normals;
    TArray<int32>   Triangles;
    TArray<FVector2D> UVs;
    TArray<FColor>  Colors;
    TArray<FProcMeshTangent> Tangents;

    for (int32 Z = 0; Z < Grid.Size.Z - 1; Z++)
    for (int32 Y = 0; Y < Grid.Size.Y - 1; Y++)
    for (int32 X = 0; X < Grid.Size.X - 1; X++)
    {
        ProcessCube(Grid, X, Y, Z, Vertices, Triangles);
    }

    // Compute normals from triangles
    RecalculateNormals(Vertices, Triangles, Normals);

    // Pad UVs (can project based on position for triplanar)
    UVs.SetNumZeroed(Vertices.Num());
    for (int32 i = 0; i < Vertices.Num(); i++)
        UVs[i] = FVector2D(Vertices[i].X, Vertices[i].Y) / Grid.VoxelSize;

    Mesh->CreateMeshSection(0, Vertices, Triangles, Normals,
                             UVs, Colors, Tangents, /*bCreateCollision=*/true);
}
```

---

## 3. Dungeon Room-and-Corridor Generation

BSP-based dungeon layout that partitions a rect into rooms and connects them.

### Data Structures

```cpp
struct FRoom
{
    FIntRect Bounds;     // X=left, Y=top, Width, Height in grid cells
    FIntPoint Center() const
    {
        return FIntPoint(Bounds.Min.X + Bounds.Width() / 2,
                         Bounds.Min.Y + Bounds.Height() / 2);
    }
};

struct FDungeonLevel
{
    TArray<FRoom> Rooms;
    TArray<TPair<FIntPoint, FIntPoint>> Corridors; // pairs of cell coords
    TArray<TArray<uint8>> Tiles; // 0=wall, 1=floor, 2=corridor
};
```

### BSP Split

```cpp
void SplitRect(const FIntRect& Rect, FRandomStream& Rand,
               int32 MinSize, TArray<FIntRect>& OutLeaves)
{
    int32 W = Rect.Width(), H = Rect.Height();

    if (W < MinSize * 2 && H < MinSize * 2)
    {
        OutLeaves.Add(Rect);
        return;
    }

    bool bSplitH = (W > H) ? true : (H > W) ? false : Rand.RandBool();

    if (bSplitH && W >= MinSize * 2)
    {
        int32 Split = Rand.RandRange(MinSize, W - MinSize);
        SplitRect(FIntRect(Rect.Min, FIntPoint(Rect.Min.X + Split, Rect.Max.Y)), Rand, MinSize, OutLeaves);
        SplitRect(FIntRect(FIntPoint(Rect.Min.X + Split, Rect.Min.Y), Rect.Max), Rand, MinSize, OutLeaves);
    }
    else if (!bSplitH && H >= MinSize * 2)
    {
        int32 Split = Rand.RandRange(MinSize, H - MinSize);
        SplitRect(FIntRect(Rect.Min, FIntPoint(Rect.Max.X, Rect.Min.Y + Split)), Rand, MinSize, OutLeaves);
        SplitRect(FIntRect(FIntPoint(Rect.Min.X, Rect.Min.Y + Split), Rect.Max), Rand, MinSize, OutLeaves);
    }
    else
    {
        OutLeaves.Add(Rect);
    }
}
```

### Room Placement and Corridor Carving

```cpp
FDungeonLevel GenerateDungeon(int32 MapW, int32 MapH, int32 Seed,
                               int32 MinRoomSize = 5, int32 Padding = 1)
{
    FRandomStream Rand(Seed);
    FDungeonLevel Level;

    // Initialize tile map
    Level.Tiles.SetNum(MapH);
    for (auto& Row : Level.Tiles)
        Row.Init(0, MapW); // all walls

    // BSP partition
    TArray<FIntRect> Leaves;
    SplitRect(FIntRect(0, 0, MapW, MapH), Rand, MinRoomSize + Padding * 2, Leaves);

    // Place rooms in leaves
    for (const FIntRect& Leaf : Leaves)
    {
        int32 MaxW = Leaf.Width()  - Padding * 2;
        int32 MaxH = Leaf.Height() - Padding * 2;
        if (MaxW < MinRoomSize || MaxH < MinRoomSize) continue;

        int32 RW = Rand.RandRange(MinRoomSize, MaxW);
        int32 RH = Rand.RandRange(MinRoomSize, MaxH);
        int32 RX = Leaf.Min.X + Padding + Rand.RandRange(0, MaxW - RW);
        int32 RY = Leaf.Min.Y + Padding + Rand.RandRange(0, MaxH - RH);

        FRoom Room;
        Room.Bounds = FIntRect(RX, RY, RX + RW, RY + RH);
        Level.Rooms.Add(Room);

        // Carve floor tiles
        for (int32 Y = RY; Y < RY + RH; Y++)
        for (int32 X = RX; X < RX + RW; X++)
            Level.Tiles[Y][X] = 1;
    }

    // Connect rooms with L-shaped corridors
    for (int32 i = 1; i < Level.Rooms.Num(); i++)
    {
        FIntPoint A = Level.Rooms[i - 1].Center();
        FIntPoint B = Level.Rooms[i].Center();

        // Horizontal then vertical
        int32 XDir = (B.X > A.X) ? 1 : -1;
        for (int32 X = A.X; X != B.X; X += XDir)
        {
            Level.Tiles[A.Y][X] = 2;
            Level.Corridors.Add({FIntPoint(X, A.Y), FIntPoint(X + XDir, A.Y)});
        }

        int32 YDir = (B.Y > A.Y) ? 1 : -1;
        for (int32 Y = A.Y; Y != B.Y; Y += YDir)
        {
            Level.Tiles[Y][B.X] = 2;
            Level.Corridors.Add({FIntPoint(B.X, Y), FIntPoint(B.X, Y + YDir)});
        }

        Level.Tiles[B.Y][B.X] = 2;
    }

    return Level;
}
```

### Tile-to-Mesh Conversion

```cpp
void ADungeonActor::BuildMeshFromTiles(const FDungeonLevel& Level, float TileSize)
{
    TArray<FVector>       Vertices;
    TArray<int32>         Triangles;
    TArray<FVector>       Normals;
    TArray<FVector2D>     UVs;
    TArray<FColor>        Colors;
    TArray<FProcMeshTangent> Tangents;

    int32 H = Level.Tiles.Num();
    int32 W = H > 0 ? Level.Tiles[0].Num() : 0;

    for (int32 Row = 0; Row < H; Row++)
    for (int32 Col = 0; Col < W; Col++)
    {
        if (Level.Tiles[Row][Col] == 0) continue; // Skip walls (or add wall mesh)

        int32 Base = Vertices.Num();
        float X0 = Col       * TileSize;
        float X1 = (Col + 1) * TileSize;
        float Y0 = Row       * TileSize;
        float Y1 = (Row + 1) * TileSize;

        Vertices.Add(FVector(X0, Y0, 0)); // 0 BL
        Vertices.Add(FVector(X1, Y0, 0)); // 1 BR
        Vertices.Add(FVector(X1, Y1, 0)); // 2 TR
        Vertices.Add(FVector(X0, Y1, 0)); // 3 TL

        Normals.Add(FVector::UpVector);
        Normals.Add(FVector::UpVector);
        Normals.Add(FVector::UpVector);
        Normals.Add(FVector::UpVector);

        UVs.Add(FVector2D(0, 0)); UVs.Add(FVector2D(1, 0));
        UVs.Add(FVector2D(1, 1)); UVs.Add(FVector2D(0, 1));

        Triangles.Add(Base);     Triangles.Add(Base + 2); Triangles.Add(Base + 1);
        Triangles.Add(Base);     Triangles.Add(Base + 3); Triangles.Add(Base + 2);
    }

    ProceduralMesh->CreateMeshSection(0, Vertices, Triangles, Normals,
                                       UVs, Colors, Tangents, /*bCreateCollision=*/true);
}
```

---

## 4. L-System Vegetation

L-systems expand a string through production rules and interpret characters as 3D drawing commands (turtle graphics) to produce branching structures.

### Axiom and Rules

```cpp
struct FLSystemRules
{
    FString Axiom = "F";
    TMap<TCHAR, FString> Rules = {
        {'F', TEXT("F[+F]F[-F]F")} // Standard plant
    };
    int32 Iterations = 4;
    float AngleDeg   = 25.f;
    float SegmentLen = 50.f;
    float LenDecay   = 0.7f;  // Each recursion level shortens segments
    float WidthStart = 8.f;
    float WidthDecay = 0.6f;
};

FString ExpandLSystem(const FLSystemRules& Rules)
{
    FString Current = Rules.Axiom;
    for (int32 Iter = 0; Iter < Rules.Iterations; Iter++)
    {
        FString Next;
        Next.Reserve(Current.Len() * 3);
        for (TCHAR C : Current)
        {
            const FString* Replacement = Rules.Rules.Find(C);
            if (Replacement) Next.Append(*Replacement);
            else             Next.AppendChar(C);
        }
        Current = MoveTemp(Next);
    }
    return Current;
}
```

### Turtle Interpreter to HISM

```cpp
struct FTurtleState
{
    FVector   Position  = FVector::ZeroVector;
    FRotator  Rotation  = FRotator::ZeroRotator;
    float     Length    = 50.f;
    float     Width     = 8.f;
};

void InterpretLSystem(const FString& LString, const FLSystemRules& Rules,
                       UHierarchicalInstancedStaticMeshComponent* BranchHISM,
                       UHierarchicalInstancedStaticMeshComponent* LeafHISM)
{
    TArray<FTurtleState> Stack;
    FTurtleState State;
    State.Length = Rules.SegmentLen;
    State.Width  = Rules.WidthStart;

    for (TCHAR C : LString)
    {
        switch (C)
        {
        case 'F':
        {
            FVector Forward = State.Rotation.Vector() * State.Length;
            FVector End = State.Position + Forward;

            // Place branch segment
            FTransform T;
            T.SetLocation((State.Position + End) * 0.5f);
            T.SetRotation(State.Rotation.Quaternion());
            T.SetScale3D(FVector(State.Width * 0.01f, State.Width * 0.01f,
                                  State.Length * 0.01f));
            BranchHISM->AddInstance(T, /*bWorldSpace=*/false);

            State.Position = End;
            break;
        }
        case '+': State.Rotation.Yaw   += Rules.AngleDeg; break;
        case '-': State.Rotation.Yaw   -= Rules.AngleDeg; break;
        case '&': State.Rotation.Pitch += Rules.AngleDeg; break;
        case '^': State.Rotation.Pitch -= Rules.AngleDeg; break;
        case '/': State.Rotation.Roll  += Rules.AngleDeg; break;
        case '\\':State.Rotation.Roll  -= Rules.AngleDeg; break;
        case '[':
            Stack.Push(State);
            State.Length *= Rules.LenDecay;
            State.Width  *= Rules.WidthDecay;
            break;
        case ']':
            // Place leaf at branch tip before popping
            if (LeafHISM)
            {
                FTransform LT;
                LT.SetLocation(State.Position);
                LT.SetRotation(State.Rotation.Quaternion());
                LeafHISM->AddInstance(LT, /*bWorldSpace=*/false);
            }
            State = Stack.Pop();
            break;
        }
    }
}
```

---

## 5. Wave Function Collapse (Grid Layout)

WFC fills a grid by choosing tiles that satisfy adjacency constraints. Suitable for dungeon rooms, city blocks, terrain biome transitions.

### Tile and Constraint Definition

```cpp
// Each tile has a set of valid neighbor tile IDs per direction
struct FWFCTile
{
    int32            ID;
    float            Weight;          // Relative spawn probability
    TArray<int32>    AllowedRight;    // IDs allowed to the +X neighbor
    TArray<int32>    AllowedLeft;     // IDs allowed to the -X neighbor
    TArray<int32>    AllowedUp;       // IDs allowed to the +Y neighbor
    TArray<int32>    AllowedDown;     // IDs allowed to the -Y neighbor
};

// Cell state during WFC
struct FWFCCell
{
    TArray<int32> PossibleTiles;  // Remaining valid tile IDs
    bool          bCollapsed = false;
    int32         CollapsedTile = -1;

    bool IsContradiction() const { return PossibleTiles.Num() == 0 && !bCollapsed; }
    float Entropy() const { return (float)PossibleTiles.Num(); } // Simplified (no weights)
};
```

### WFC Iteration

```cpp
bool WFCStep(TArray<TArray<FWFCCell>>& Grid,
             const TArray<FWFCTile>& Tiles,
             FRandomStream& Rand,
             int32 Width, int32 Height)
{
    // 1. Find uncollapsed cell with lowest entropy
    float MinEntropy = FLT_MAX;
    FIntPoint CollapsePos(-1, -1);

    for (int32 Y = 0; Y < Height; Y++)
    for (int32 X = 0; X < Width;  X++)
    {
        FWFCCell& Cell = Grid[Y][X];
        if (Cell.bCollapsed) continue;
        if (Cell.IsContradiction()) return false; // Contradiction — need backtrack
        if (Cell.Entropy() < MinEntropy)
        {
            MinEntropy = Cell.Entropy();
            CollapsePos = FIntPoint(X, Y);
        }
    }

    if (CollapsePos.X < 0) return true; // All cells collapsed

    // 2. Collapse: choose a tile weighted by tile weight
    FWFCCell& Cell = Grid[CollapsePos.Y][CollapsePos.X];
    float TotalWeight = 0.f;
    for (int32 TileID : Cell.PossibleTiles)
        TotalWeight += Tiles[TileID].Weight;

    float Pick = Rand.FRandRange(0.f, TotalWeight);
    float Accum = 0.f;
    int32 ChosenTile = Cell.PossibleTiles[0];
    for (int32 TileID : Cell.PossibleTiles)
    {
        Accum += Tiles[TileID].Weight;
        if (Accum >= Pick) { ChosenTile = TileID; break; }
    }

    Cell.bCollapsed    = true;
    Cell.CollapsedTile = ChosenTile;
    Cell.PossibleTiles = { ChosenTile };

    // 3. Propagate constraints to neighbors (BFS)
    TQueue<FIntPoint> PropagateQueue;
    PropagateQueue.Enqueue(CollapsePos);

    while (!PropagateQueue.IsEmpty())
    {
        FIntPoint P;
        PropagateQueue.Dequeue(P);

        auto Propagate = [&](FIntPoint Neighbor,
                              TFunctionRef<const TArray<int32>*(const FWFCTile&)> GetAllowed)
        {
            if (Neighbor.X < 0 || Neighbor.X >= Width ||
                Neighbor.Y < 0 || Neighbor.Y >= Height) return;

            FWFCCell& NCell = Grid[Neighbor.Y][Neighbor.X];
            if (NCell.bCollapsed) return;

            // Collect all tiles allowed by current cell's possible set
            TSet<int32> AllowedSet;
            for (int32 TileID : Grid[P.Y][P.X].PossibleTiles)
            {
                const TArray<int32>* Allowed = GetAllowed(Tiles[TileID]);
                if (Allowed) AllowedSet.Append(*Allowed);
            }

            // Remove incompatible tiles from neighbor
            int32 PrevCount = NCell.PossibleTiles.Num();
            NCell.PossibleTiles.RemoveAll([&](int32 ID) { return !AllowedSet.Contains(ID); });

            if (NCell.PossibleTiles.Num() != PrevCount)
                PropagateQueue.Enqueue(Neighbor);
        };

        Propagate({P.X + 1, P.Y}, [](const FWFCTile& T) { return &T.AllowedRight; });
        Propagate({P.X - 1, P.Y}, [](const FWFCTile& T) { return &T.AllowedLeft;  });
        Propagate({P.X, P.Y + 1}, [](const FWFCTile& T) { return &T.AllowedUp;    });
        Propagate({P.X, P.Y - 1}, [](const FWFCTile& T) { return &T.AllowedDown;  });
    }

    return true;
}
```

### Grid Initialization and Run

```cpp
void RunWFC(int32 Width, int32 Height, const TArray<FWFCTile>& Tiles,
             FRandomStream& Rand, TArray<TArray<FWFCCell>>& OutGrid)
{
    TArray<int32> AllTileIDs;
    for (const FWFCTile& T : Tiles) AllTileIDs.Add(T.ID);

    OutGrid.SetNum(Height);
    for (auto& Row : OutGrid)
    {
        Row.SetNum(Width);
        for (FWFCCell& Cell : Row)
            Cell.PossibleTiles = AllTileIDs;
    }

    bool bSuccess = false;
    for (int32 MaxSteps = Width * Height; MaxSteps > 0; MaxSteps--)
    {
        bSuccess = WFCStep(OutGrid, Tiles, Rand, Width, Height);
        if (!bSuccess) break; // Contradiction: re-run with different seed

        // Check all cells collapsed
        bool bDone = true;
        for (auto& Row : OutGrid)
        for (auto& Cell : Row)
            if (!Cell.bCollapsed) { bDone = false; break; }
        if (bDone) { bSuccess = true; break; }
    }
}
```

---

## 6. Async Mesh Generation Pattern

For large meshes, compute vertex data on a background thread then apply on the game thread.

```cpp
void AProceduralTerrain::GenerateAsync(int32 GridSize, float CellSize)
{
    // Capture data needed on background thread
    int32 Seed = SeedValue;

    // Lambda runs on a background worker thread
    AsyncTask(ENamedThreads::AnyBackgroundThreadNormalTask, [this, GridSize, CellSize, Seed]()
    {
        TArray<FVector>   Vertices;
        TArray<int32>     Triangles;
        TArray<FVector>   Normals;
        TArray<FVector2D> UVs;

        // -- heavy computation here --
        // GenerateTerrainData(GridSize, CellSize, Seed, Vertices, Triangles, Normals, UVs);

        // Schedule the mesh section creation back on the game thread
        AsyncTask(ENamedThreads::GameThread, [this,
                                               V = MoveTemp(Vertices),
                                               T = MoveTemp(Triangles),
                                               N = MoveTemp(Normals),
                                               UV = MoveTemp(UVs)]() mutable
        {
            if (!IsValid(this) || !IsValid(ProceduralMesh)) return;

            TArray<FColor> Colors;
            TArray<FProcMeshTangent> Tangents;

            ProceduralMesh->CreateMeshSection(0, V, T, N,
                                               UV, Colors, Tangents,
                                               /*bCreateCollision=*/true);
        });
    });
}
```

Note: `UProceduralMeshComponent::CreateMeshSection` must be called on the **game thread**. Only the data computation can be parallelized.

---

## 7. Spline-Driven Road Mesh

Generates a road mesh by extruding a cross-section profile along a `USplineComponent`.

```cpp
void ARoadMeshActor::BuildRoad(float RoadWidth, float SegmentLength)
{
    TArray<FVector>       Vertices;
    TArray<int32>         Triangles;
    TArray<FVector>       Normals;
    TArray<FVector2D>     UVs;
    TArray<FColor>        Colors;
    TArray<FProcMeshTangent> Tangents;

    float TotalLen   = Spline->GetSplineLength();
    float UVProgress = 0.f;
    int32 SegCount   = FMath::CeilToInt(TotalLen / SegmentLength);
    float ActualSeg  = TotalLen / SegCount;

    // Extrude cross-section quads along spline
    for (int32 Seg = 0; Seg <= SegCount; Seg++)
    {
        float Dist = Seg * ActualSeg;
        FTransform T = Spline->GetTransformAtDistanceAlongSpline(
            Dist, ESplineCoordinateSpace::World, /*bUseScale=*/false);

        FVector Center = T.GetLocation();
        FVector Right  = T.GetRotation().GetRightVector();
        FVector Up     = T.GetRotation().GetUpVector();

        FVector Left_V  = Center - Right * RoadWidth * 0.5f;
        FVector Right_V = Center + Right * RoadWidth * 0.5f;

        Vertices.Add(Left_V);
        Vertices.Add(Right_V);
        Normals.Add(Up);
        Normals.Add(Up);
        UVs.Add(FVector2D(0.f, UVProgress));
        UVs.Add(FVector2D(1.f, UVProgress));

        if (Seg > 0)
        {
            int32 B = (Seg - 1) * 2;
            int32 T2 = Seg * 2;
            // Left triangle
            Triangles.Add(B);     Triangles.Add(T2);     Triangles.Add(B + 1);
            // Right triangle
            Triangles.Add(B + 1); Triangles.Add(T2);     Triangles.Add(T2 + 1);
        }

        UVProgress += ActualSeg / RoadWidth; // Scale UV to aspect ratio
    }

    ProceduralMesh->CreateMeshSection(0, Vertices, Triangles, Normals,
                                       UVs, Colors, Tangents, /*bCreateCollision=*/true);
    ProceduralMesh->SetMaterial(0, RoadMaterial);
}
```

---

## Performance Reference

| Scenario | Recommended Approach | Notes |
|---|---|---|
| < 100 dynamic instances, moving | ISM + `UpdateInstanceTransform` | Simple, low overhead |
| 100–10,000 static instances | HISM | Culling hierarchy, LOD transitions |
| > 10,000 static instances | HISM + `InstanceEndCullDistance` | Aggressive distance culling |
| Terrain (runtime, < 256x256) | `UProceduralMeshComponent` | One `CreateMeshSection` call |
| Terrain (large, static) | Landscape or PCG + ISM | PCG + HISM spawner avoids draw calls |
| Cave/voxel (< 64x64x64) | Marching Cubes + ProcMesh | Async generation on background thread |
| Vegetation (open world) | PCG Surface Sampler + HISM Spawner | Budget with HiGen grid |
| Dungeon layout | WFC or BSP + tile mesh | Bake to static at load, or keep ProcMesh |
| Spline road/river | SplineMeshComponent per segment | Or extruded ProcMesh for custom profile |

---

## 9. Poisson Disc Sampling

Generates uniformly distributed points with minimum separation distance (Bridson 2007). Use for natural-looking placement (trees, rocks, enemies) without clumping.

```cpp
// Poisson disc sampling — Bridson's fast algorithm
TArray<FVector2D> PoissonDiscSample(FVector2D Min, FVector2D Max,
    float MinDist, int32 MaxAttempts, FRandomStream& Rand)
{
    float CellSize = MinDist / FMath::Sqrt(2.f);
    FVector2D Size = Max - Min;
    int32 GW = FMath::CeilToInt(Size.X / CellSize);
    int32 GH = FMath::CeilToInt(Size.Y / CellSize);
    TArray<int32> Grid;
    Grid.Init(-1, GW * GH);
    TArray<FVector2D> Points, Active;

    // Seed with first random point
    FVector2D First(Rand.FRandRange(Min.X, Max.X), Rand.FRandRange(Min.Y, Max.Y));
    Points.Add(First);
    Active.Add(First);
    Grid[FMath::FloorToInt((First.Y - Min.Y) / CellSize) * GW +
         FMath::FloorToInt((First.X - Min.X) / CellSize)] = 0;

    while (Active.Num() > 0)
    {
        int32 Idx = Rand.RandRange(0, Active.Num() - 1);
        FVector2D Base = Active[Idx];
        bool bFound = false;

        for (int32 k = 0; k < MaxAttempts; k++)
        {
            float Angle = Rand.FRandRange(0.f, 2.f * PI);
            float R = Rand.FRandRange(MinDist, 2.f * MinDist);
            FVector2D Candidate = Base + FVector2D(FMath::Cos(Angle), FMath::Sin(Angle)) * R;

            if (Candidate.X < Min.X || Candidate.X > Max.X ||
                Candidate.Y < Min.Y || Candidate.Y > Max.Y)
                continue;

            int32 GX = FMath::FloorToInt((Candidate.X - Min.X) / CellSize);
            int32 GY = FMath::FloorToInt((Candidate.Y - Min.Y) / CellSize);
            bool bTooClose = false;

            for (int32 DY = -2; DY <= 2 && !bTooClose; DY++)
            {
                for (int32 DX = -2; DX <= 2 && !bTooClose; DX++)
                {
                    int32 NX = GX + DX, NY = GY + DY;
                    if (NX < 0 || NX >= GW || NY < 0 || NY >= GH) continue;
                    int32 PIdx = Grid[NY * GW + NX];
                    if (PIdx >= 0 && FVector2D::Distance(Points[PIdx], Candidate) < MinDist)
                        bTooClose = true;
                }
            }

            if (!bTooClose)
            {
                Grid[GY * GW + GX] = Points.Num();
                Points.Add(Candidate);
                Active.Add(Candidate);
                bFound = true;
                break;
            }
        }
        if (!bFound) Active.RemoveAtSwap(Idx);
    }
    return Points;
}
```

**Usage with ISM placement:**

```cpp
FRandomStream Stream(MySeed);
TArray<FVector2D> Placements = PoissonDiscSample(
    FVector2D(0, 0), FVector2D(10000, 10000), 200.f, 30, Stream);

for (const FVector2D& Pos : Placements)
{
    FTransform T(FRotator(0, Stream.FRandRange(0, 360), 0),
        FVector(Pos.X, Pos.Y, GetGroundHeight(Pos)));
    TreeISM->AddInstance(T);
}
```

Key properties: O(n) time complexity, guaranteed minimum separation, deterministic with `FRandomStream` seed. Increase `MaxAttempts` (default 30) for denser packing; decrease for faster generation.

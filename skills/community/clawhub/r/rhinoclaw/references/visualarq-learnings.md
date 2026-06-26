# VisualARQ API Learnings (RhinoClaw)

> Erkenntnisse aus der Live-Session 22.03.2026. Referenz für zukünftige VA-Arbeit.

## API Zugang

```python
import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va
```

- Alle Methoden sind **statisch** auf `VisualARQ.Script`
- GUIDs: `from System import Guid`
- Funktioniert nur in **IronPython 2** (Rhino RhinoScript)
- **NICHT** in Python 3 (CPython) — `clr.AddReference` crasht wegen Assembly-Konflikt

## Detection

```python
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    available = True
except:
    available = False
```

## Kritische API-Signaturen (verifiziert)

### AddWall
```python
# AddWall(styleId: Guid, startPoint: Point3d, endPoint: Point3d) → Guid
# NICHT: AddWall(style, Line, height) oder AddWall(style, start, end, height)
# Höhe kommt NUR vom Style via SetWallStyleHeight()
wall_id = va.AddWall(style_id, Point3d(0,0,0), Point3d(10,0,0))
```

### AddWallStyle + Layer
```python
# AddWallStyle(name: str) → Guid
style_id = va.AddWallStyle("Mein Style")

# AddWallLayer(styleId: Guid, layerName: str, thickness: float) → Guid
# NICHT: AddWallLayer(styleId, index_int, thickness)
va.AddWallLayer(style_id, "Core", 0.2)  # 200mm

# Höhe separat setzen
va.SetWallStyleHeight(style_id, 3.0)  # 3 Meter
```

### Style-Namen abfragen
```python
# GetStyleName(id) — generisch für ALLE Typen
name = va.GetStyleName(style_id)

# FALSCH: va.GetWallStyleName(id) — existiert NICHT!
# FALSCH: va.GetDoorStyleName(id) — existiert NICHT!
```

### Alle Styles abfragen
```python
wall_styles = va.GetAllWallStyleIds()      # → List[Guid] oder None
door_styles = va.GetAllDoorStyleIds()
window_styles = va.GetAllWindowStyleIds()
column_styles = va.GetAllColumnStyleIds()
beam_styles = va.GetAllBeamStyle()          # ACHTUNG: kein "Ids" suffix!
```

## Bekannte Probleme

### Wall-Höhe
- `SetWallStyleHeight(styleId, height)` muss VOR `AddWall` aufgerufen werden
- Wenn Style ohne Höhe/Layer erstellt wird → Wand hat 0 Dicke, quasi unsichtbar
- **Immer** zuerst Style vollständig konfigurieren, DANN Wand erstellen

### Wall-Darstellung
- Wand ohne Layer (AddWallLayer) = keine Dicke → nur Linie sichtbar
- Wall-Objekte sind intern `InstanceReference` (ObjectType 4096)
- BBox-Check: min/max prüfen ob Wand tatsächlich Volumen hat

### Viele Styles erstellt
- Jeder `AddWallStyle("Name")` Call erstellt einen neuen Style, auch bei gleichem Namen
- → Erst prüfen ob Style existiert: `FindBeamStyle("name")` etc.
- Oder `GetAllWallStyleIds()` durchgehen und `GetStyleName()` vergleichen

## IronPython 2 Einschränkungen

**VERBOTEN in Rhino-Code:**
- f-strings: `f"text {var}"` → `"text " + str(var)`
- Walrus operator: `:=`
- `print()` mit `end=` Parameter
- Type hints in Funktionsdefinitionen

**ERLAUBT:**
- `json` Modul
- Dictionary/List Comprehensions
- `str.format()`: `"text {}".format(var)`
- String concatenation: `"text " + str(var)`

## Python 3 (CPython) via ScriptEditor

- Neuer Command: `execute_python3_code` (seit v0.2.5)
- **EXPERIMENTELL** — kann Rhino crashen bei schnellen aufeinanderfolgenden Calls
- `clr.AddReference("VisualARQ.Script")` crasht in Python 3 → Assembly-Konflikt
- **VisualARQ Scripting funktioniert NUR mit IronPython 2**
- Python 3 nur für nicht-VA Scripts nutzen (reine Geometrie, Rhino API)

## Response-Parsing Pattern

```python
# Script-Output kommt als String in result.result (NICHT result.output)
response = client.send_command("execute_rhinoscript_python_code", {"code": code})
result = response.get("result", {})
output = result.get("output", "") or result.get("result", "") or ""
if "RESULT:" in output:
    json_part = output.split("RESULT:", 1)[1].strip()
    data = json.loads(json_part)
```

## Vollständige Methoden-Liste

`dir(va)` liefert 700+ Methoden. Vollständiger Dump:
→ Wurde am 22.03.2026 gespeichert, siehe Session-Log

## API Kategorien (verifiziert verfügbar)

| Kategorie | Create | Query | Modify |
|-----------|--------|-------|--------|
| Wall | AddWall, AddWallStyle, AddWallLayer | GetAllWallStyleIds, GetWallHeight, GetWallThickness | SetWallHeight, SetWallAlignment |
| Door | AddDoor, AddDoorStyle, AddDoorFrame, AddDoorLeaf | GetAllDoorStyleIds, GetOpeningPosition | SetOpeningPosition, SetOpeningSide |
| Window | AddWindow, AddWindowStyle, AddWindowFrame | GetAllWindowStyleIds | SetWindowSillThickness |
| Column | AddColumn, AddColumnStyle | GetAllColumnStyleIds, GetColumnHeight | SetColumnHeight, SetColumnPosition |
| Beam | AddBeam, AddBeamStyle | GetAllBeamStyle | SetBeamProfile |
| Slab | AddSlabFromCurve, AddSlabStyle, AddSlabLayer | GetSlabThickness | SetSlabAlignment |
| Roof | AddRoofFromCurve, AddRoofStyle | GetRoofSlope | SetRoofType, SetSlope |
| Stair | AddStair, AddStairStyle | GetStairHeight, GetStairWidth | SetStairAlignment |
| Railing | AddRailing, AddRailingStyle | GetRailingHeight | SetRailingHeight |
| CurtainWall | AddCurtainWall, AddCurtainWallStyle | GetCurtainWallHeight | SetCurtainWallHeight |
| Level | AddLevel | GetLevelElevation, GetLevelName | SetLevelElevation, SetLevelName |
| Building | AddBuilding | GetBuildingName, GetBuildingLevelIds | SetBuildingName |
| Parameter | AddDocumentParameter, AddObjectParameter | GetParameterValue, GetParameterName | SetParameterValue |
| Space | AddSpaceFromCurve, AddSpaceFromPoint | GetSpaceArea, GetSpaceVolume | SetSpaceHeight |
| Furniture | AddFurniture, AddFurnitureStyle | GetFurniturePosition | SetFurniturePosition |
| Element | AddGenericElement, AddGenericElementStyle | GetGenericElementPosition | SetGenericElementPosition |
| Profile | AddCurveProfileTemplate | GetProfileTemplates, GetProfileName | SetCircularProfileSize, etc. |

## Nächste Schritte

1. **visualarq.py Wrapper-Funktionen** auf korrekte Signaturen updaten
2. **Style-Reuse:** Erst prüfen ob Style existiert bevor neuer erstellt wird
3. **Höhe/Dicke:** Immer vollständigen Style konfigurieren vor Wall-Erstellung
4. **Tür in Wand:** `AddDoor(styleId, wallId, ...)` testen → braucht Wall-GUID als Host
5. **IFC Export:** `vaIFCExport` via RunScript oder va.API testen

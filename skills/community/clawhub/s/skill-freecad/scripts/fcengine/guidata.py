"""GUI data of saved documents (pure Python: zip + XML).

Headless FreeCAD saves no GuiDocument.xml, and drops the one an existing file
had (colours, camera, user tweaks). Opening such a file in the GUI shows
*every* object hidden, whatever the objects' own Visibility says; probed on
FreeCAD 1.1. The GUI also falls back to "everything hidden" when
GuiDocument.xml is malformed, e.g. when HasExpansion="1" lacks its <Expand/>
element or the <Camera> element is missing.

So after each save the engine:
- keeps the GuiDocument.xml (and the binary files it references) captured
  from the file before the request, so user tweaks survive;
- sets each managed object's Visibility to the engine's choice;
- writes custom colours as the legacy ShapeColor/Transparency properties,
  which FreeCAD 1.x converts to its appearance on load (verified in the GUI).
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

GUI_XML = "GuiDocument.xml"
APPEARANCE_PROPS = ("ShapeAppearance", "ShapeColor", "Transparency", "ShapeMaterial", "DiffuseColor")
FILE_REF = re.compile(r'file="([^"]+)"')


def capture(path: Path) -> Optional[Dict[str, Any]]:
    """GUI data of an existing document file, or None."""
    try:
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
            if GUI_XML not in names:
                return None
            xml = z.read(GUI_XML).decode("utf-8")
            files = {f: z.read(f) for f in set(FILE_REF.findall(xml)) if f in names}
            return {"xml": xml, "files": files}
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError):
        return None


def packed_color(rgb: Iterable[float]) -> int:
    r, g, b = (max(0, min(255, int(round(float(c) * 255)))) for c in rgb)
    return (r << 24) | (g << 16) | (b << 8) | 255


def _prop(parent: Any, name: str) -> Optional[Any]:
    for p in parent.findall("Property"):
        if p.get("name") == name:
            return p
    return None


def _set_prop(props: Any, name: str, type_id: str, tag: str, attrs: Dict[str, str]) -> None:
    p = _prop(props, name)
    if p is None:
        p = ET.SubElement(props, "Property", {"name": name, "type": type_id, "status": "1"})
    for child in list(p):
        p.remove(child)
    ET.SubElement(p, tag, attrs)


def _new_root() -> Any:
    root = ET.Element("Document", {"SchemaVersion": "1", "HasExpansion": "1"})
    ET.SubElement(root, "Expand")
    ET.SubElement(root, "ViewProviderData", {"Count": "0"})
    ET.SubElement(root, "Camera", {"settings": ""})
    return root


def build(
    captured: Optional[Dict[str, Any]],
    existing: Set[str],
    visibility: Dict[str, bool],
    appearance: Dict[str, Dict[str, Any]],
    changed: Set[str],
) -> str:
    """GuiDocument.xml text.

    existing: names of all objects in the document; view providers of other objects are dropped.
    visibility: managed objects and whether they are shown.
    appearance: objects with a custom colour ({"color": [r, g, b], "transparency": 0-100}).
    changed: objects whose appearance this request set or cleared; their old GUI appearance is replaced.
    """
    root = None
    if captured is not None:
        try:
            root = ET.fromstring(captured["xml"])
        except ET.ParseError:
            root = None
    if root is None or root.find("ViewProviderData") is None:
        root = _new_root()
    if root.get("HasExpansion") == "1" and root.find("Expand") is None:
        root.insert(0, ET.Element("Expand"))
    if root.find("Camera") is None:
        ET.SubElement(root, "Camera", {"settings": ""})
    data = root.find("ViewProviderData")
    vps = {vp.get("name"): vp for vp in data.findall("ViewProvider")}
    for name, vp in list(vps.items()):
        if name not in existing:
            data.remove(vp)
            del vps[name]
    for name in sorted(set(visibility) | set(appearance) | (changed & existing)):
        vp = vps.get(name)
        fresh = vp is None
        if fresh:
            vp = ET.SubElement(data, "ViewProvider", {"name": name, "expanded": "0"})
            vps[name] = vp
        props = vp.find("Properties")
        if props is None:
            props = ET.SubElement(vp, "Properties", {"Count": "0", "TransientCount": "0"})
        if name in visibility:
            _set_prop(
                props, "Visibility", "App::PropertyBool", "Bool", {"value": "true" if visibility[name] else "false"}
            )
        if name in changed:
            for p in list(props.findall("Property")):
                if p.get("name") in APPEARANCE_PROPS:
                    props.remove(p)
        if name in appearance and (fresh or name in changed):
            a = appearance[name]
            _set_prop(
                props, "ShapeColor", "App::PropertyColor", "PropertyColor", {"value": str(packed_color(a["color"]))}
            )
            _set_prop(
                props, "Transparency", "App::PropertyPercent", "Integer", {"value": str(int(a.get("transparency", 0)))}
            )
        props.set("Count", str(len(props.findall("Property"))))
    data.set("Count", str(len(data.findall("ViewProvider"))))
    return "<?xml version='1.0' encoding='utf-8'?>\n" + ET.tostring(root, encoding="unicode") + "\n"


def write(path: Path, xml: str, captured: Optional[Dict[str, Any]]) -> None:
    """Add GuiDocument.xml (and the captured binary files it still references) to a saved document."""
    with zipfile.ZipFile(path) as z:
        present = set(z.namelist())
    with zipfile.ZipFile(path, "a", zipfile.ZIP_DEFLATED) as z:
        if GUI_XML not in present:
            z.writestr(GUI_XML, xml)
        # FreeCAD reads the zip sequentially and matches binary files in the order GuiDocument.xml
        # references them; a file out of order is skipped, and so is every file after it (probed:
        # sorted names put 'ShapeAppearance10' before 'ShapeAppearance2' and colours were lost).
        for f in referenced_files(xml):
            if captured and f in captured["files"] and f not in present:
                z.writestr(f, captured["files"][f])


def referenced_files(xml: str) -> List[str]:
    """Files referenced by the XML, in order of first reference."""
    return list(dict.fromkeys(FILE_REF.findall(xml)))

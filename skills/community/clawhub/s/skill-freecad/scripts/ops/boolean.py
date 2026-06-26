import FreeCAD as App
from . import utils

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    b_type = p.get("type", "fuse").lower()
    base_name = p.get("base")
    tool_name = p.get("tool")
    name = p.get("name", f"{b_type}_{base_name}_{tool_name}")

    if not base_name or not tool_name:
        raise ValueError("Boolean operation requires 'base' and 'tool' object names")

    base_obj = utils.find_object(doc, base_name)
    tool_obj = utils.find_object(doc, tool_name)

    if not base_obj or not tool_obj:
        raise ValueError(f"Could not find base ({base_name}) or tool ({tool_name}) object")

    shape = None
    if b_type == "fuse":
        shape = base_obj.Shape.fuse(tool_obj.Shape)
    elif b_type == "cut":
        shape = base_obj.Shape.cut(tool_obj.Shape)
    elif b_type == "common":
        shape = base_obj.Shape.common(tool_obj.Shape)
    else:
        raise ValueError(f"Unknown boolean type: {b_type}")

    obj = doc.addObject("Part::Feature", name)
    obj.Label = name
    obj.Shape = shape

    # Clean up the original objects by making them invisible if in GI, or simply leaving them in headless
    # In pure python headless, FreeCAD hides this but we can delete them if strict cleanup is requested.
    # We will leave them for now.

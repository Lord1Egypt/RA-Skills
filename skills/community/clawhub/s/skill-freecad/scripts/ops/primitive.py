import FreeCAD as App
import Part
from . import utils

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    p_type = p.get("type", "box").lower()
    name = p.get("name", p_type.capitalize())
    
    shape = None
    if p_type == "box":
        shape = Part.makeBox(p.get("length", 10), p.get("width", 10), p.get("height", 10))
    elif p_type == "cylinder":
        shape = Part.makeCylinder(p.get("radius", 5), p.get("height", 10))
    elif p_type == "sphere":
        shape = Part.makeSphere(p.get("radius", 5))
    elif p_type == "cone":
        shape = Part.makeCone(p.get("radius1", 5), p.get("radius2", 0), p.get("height", 10))
    elif p_type == "torus":
        shape = Part.makeTorus(p.get("radius1", 10), p.get("radius2", 2))
    else:
        raise ValueError(f"Unknown primitive type: {p_type}")

    obj = doc.addObject("Part::Feature", name)
    obj.Label = name
    obj.Shape = shape
    
    # Optional base placement
    pos = p.get("position")
    if pos:
        obj.Placement.Base = App.Vector(*pos)

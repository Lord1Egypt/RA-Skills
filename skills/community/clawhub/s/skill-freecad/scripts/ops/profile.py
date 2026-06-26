import FreeCAD as App
import Part
from . import utils

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    p_type = p.get("type", "extrude").lower()
    name = p.get("name", p_type.capitalize())
    points = p.get("points", [])
    
    if p_type in ["extrude", "revolve"]:
        if len(points) < 3:
            raise ValueError("Profile needs at least 3 points [x, y, z]")
        
        vecs = [App.Vector(pt[0], pt[1], pt.get(2, 0) if len(pt)>2 else 0) for pt in points]
        if vecs[0] != vecs[-1]:
            vecs.append(vecs[0])
            
        polygon = Part.makePolygon(vecs)
        face = Part.Face(polygon)
        
        if face.isNull() or not face.isValid():
             raise ValueError("Generated profile face is invalid. Points might not be coplanar.")

        shape = None
        if p_type == "extrude":
            dir_vec = App.Vector(*p.get("direction", [0, 0, 10]))
            shape = face.extrude(dir_vec)
        elif p_type == "revolve":
            axis = App.Vector(*p.get("axis", [0, 1, 0]))
            center = App.Vector(*p.get("center", [0, 0, 0]))
            angle = p.get("angle", 360)
            shape = face.revolve(center, axis, angle)

        obj = doc.addObject("Part::Feature", name)
        obj.Label = name
        obj.Shape = shape
        return obj
    else:
        raise ValueError(f"Unknown profile type: {p_type}")

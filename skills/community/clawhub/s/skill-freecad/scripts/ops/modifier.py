import FreeCAD as App
from . import utils

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    m_type = p.get("type", "fillet").lower()
    target_name = p.get("target")
    name = p.get("name", f"{m_type}_{target_name}")
    radius = p.get("radius", p.get("distance", 1.0))
    indices = p.get("indices")  

    obj = utils.find_object(doc, target_name)
    if not obj or not hasattr(obj, "Shape"):
        raise ValueError(f"Target object '{target_name}' not found or has no solid shape")

    shape = obj.Shape
    edges = shape.Edges

    if not edges:
        raise ValueError(f"Target object '{target_name}' has no edges to modify")

    # If indices not provided, apply to all edges
    edge_list = indices if indices else list(range(1, len(edges) + 1))

    new_shape = None
    if m_type == "fillet":
        new_shape = shape.makeFillet(radius, edge_list)
    elif m_type == "chamfer":
        new_shape = shape.makeChamfer(radius, edge_list)
    else:
        raise ValueError(f"Unknown modifier type: {m_type}")

    new_obj = doc.addObject("Part::Feature", name)
    new_obj.Label = name
    new_obj.Shape = new_shape
    return new_obj

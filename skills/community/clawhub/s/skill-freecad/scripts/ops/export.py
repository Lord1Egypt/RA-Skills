import FreeCAD as App
import Part
import Mesh

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    import os
    format = p.get("format", "stl").lower()
    raw_filename = p.get("filename", f"model.{format}")
    filename = os.path.basename(raw_filename)  # Prevent path traversal
    
    target_name = p.get("target")
    
    export_objs = []
    if target_name:
        from . import utils
        obj = utils.find_object(doc, target_name)
        if obj and hasattr(obj, "Shape") and obj.Shape and not obj.Shape.isNull():
            export_objs.append(obj)
    else:
        for obj in doc.Objects:
            if hasattr(obj, "Shape") and obj.Shape and not obj.Shape.isNull():
                export_objs.append(obj)
                
    if not export_objs:
        print("No objects found to export.")
        return

    if format == "step":
        Part.export(export_objs, filename)
    elif format == "stl":
        Mesh.export(export_objs, filename)
    elif format == "brep":
        Part.export(export_objs, filename)
    else:
        raise ValueError(f"Unsupported export format: {format}. Supported: step, stl, brep")

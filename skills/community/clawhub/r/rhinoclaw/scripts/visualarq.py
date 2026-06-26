#!/usr/bin/env python3
"""
VisualARQ BIM objects management for Rhino via RhinoClaw.
VisualARQ is an optional add-on. All functions gracefully degrade if not installed.
"""

import argparse
import json
import sys
from rhino_client import RhinoClient


def check_visualarq() -> dict:
    """Check if VisualARQ is installed and available."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    # Try to get a version or some info to confirm it's working
    result = {
        "available": True, 
        "version": "detected",
        "message": "VisualARQ.Script assembly loaded successfully"
    }
except Exception as e:
    result = {
        "available": False,
        "message": "VisualARQ not available: " + str(e)
    }

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {})
            # Output can be in result.output or result.result (string with print output)
            output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"available": False, "message": "Failed to check VisualARQ"}


def get_info() -> dict:
    """Get VisualARQ object types, styles, and levels information."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    
    result = {
        "available": True,
        "wall_styles": [],
        "door_styles": [],
        "window_styles": [],
        "column_styles": [],
        "beam_styles": [],
        "levels": [],
        "buildings": []
    }
    
    # Get wall styles
    try:
        wall_style_ids = va.GetAllWallStyleIds()
        if wall_style_ids:
            for style_id in wall_style_ids:
                name = va.GetWallStyleName(style_id)
                if name:
                    result["wall_styles"].append({"id": str(style_id), "name": name})
    except:
        pass
    
    # Get door styles
    try:
        door_style_ids = va.GetAllDoorStyleIds()
        if door_style_ids:
            for style_id in door_style_ids:
                name = va.GetDoorStyleName(style_id)
                if name:
                    result["door_styles"].append({"id": str(style_id), "name": name})
    except:
        pass
    
    # Get window styles
    try:
        window_style_ids = va.GetAllWindowStyleIds()
        if window_style_ids:
            for style_id in window_style_ids:
                name = va.GetWindowStyleName(style_id)
                if name:
                    result["window_styles"].append({"id": str(style_id), "name": name})
    except:
        pass
    
    # Get column styles
    try:
        column_style_ids = va.GetAllColumnStyleIds()
        if column_style_ids:
            for style_id in column_style_ids:
                name = va.GetColumnStyleName(style_id)
                if name:
                    result["column_styles"].append({"id": str(style_id), "name": name})
    except:
        pass
    
    # Get beam styles
    try:
        beam_style_ids = va.GetAllBeamStyleIds()
        if beam_style_ids:
            for style_id in beam_style_ids:
                name = va.GetBeamStyleName(style_id)
                if name:
                    result["beam_styles"].append({"id": str(style_id), "name": name})
    except:
        pass
    
    # Get levels
    try:
        level_ids = va.GetAllLevelIds()
        if level_ids:
            for level_id in level_ids:
                name = va.GetLevelName(level_id)
                elevation = va.GetLevelElevation(level_id)
                if name is not None:
                    result["levels"].append({
                        "id": str(level_id), 
                        "name": name, 
                        "elevation": elevation
                    })
    except:
        pass
    
    # Get buildings
    try:
        building_ids = va.GetAllBuildingIds()
        if building_ids:
            for building_id in building_ids:
                name = va.GetBuildingName(building_id)
                if name:
                    result["buildings"].append({"id": str(building_id), "name": name})
    except:
        pass
        
except Exception as e:
    result = {
        "available": False,
        "error": str(e)
    }

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"available": False, "message": "Failed to get VisualARQ info"}


def create_wall(style_name: str, start: list, end: list, height: float, 
                layer: str = None, name: str = None) -> dict:
    """Create a wall."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    import Rhino.Geometry as rg
    
    # Find wall style by name
    style_id = None
    wall_style_ids = va.GetAllWallStyleIds()
    if wall_style_ids:
        for ws_id in wall_style_ids:
            if va.GetWallStyleName(ws_id) == "{style_name}":
                style_id = ws_id
                break
    
    if style_id is None:
        result = {{"status": "error", "message": "Wall style '{style_name}' not found".format(style_name="{style_name}")}}
    else:
        # Create the wall
        start_pt = rg.Point3d({start[0]}, {start[1]}, {start[2]})
        end_pt = rg.Point3d({end[0]}, {end[1]}, {end[2]})
        wall_id = va.AddWall(start_pt, end_pt, {height}, style_id)
        
        if wall_id != Guid.Empty:
            result = {{
                "status": "success", 
                "wall_id": str(wall_id),
                "style": "{style_name}",
                "height": {height}
            }}
            
            # Set layer if specified
            {layer_code}
            
            # Set name if specified
            {name_code}
        else:
            result = {{"status": "error", "message": "Failed to create wall"}}
            
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(
        style_name=style_name,
        start=start,
        height=height,
        layer_code='''if True:  # layer specified
    import scriptcontext as sc
    obj = sc.doc.Objects.Find(wall_id)
    if obj:
        layer_index = sc.doc.Layers.FindName("{}")
        if layer_index >= 0:
            attr = obj.Attributes
            attr.LayerIndex = layer_index
            sc.doc.Objects.ModifyAttributes(wall_id, attr, True)'''.format(layer) if layer else "# No layer specified",
        name_code='''if True:  # name specified
    obj = sc.doc.Objects.Find(wall_id)
    if obj:
        attr = obj.Attributes
        attr.Name = "{}"
        sc.doc.Objects.ModifyAttributes(wall_id, attr, True)'''.format(name) if name else "# No name specified"
    )
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to create wall"}


def list_wall_styles() -> dict:
    """List all available wall styles."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    styles = []
    wall_style_ids = va.GetAllWallStyleIds()
    if wall_style_ids:
        for style_id in wall_style_ids:
            name = va.GetWallStyleName(style_id)
            if name:
                styles.append({"id": str(style_id), "name": name})
    
    result = {"status": "success", "wall_styles": styles, "count": len(styles)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to get wall styles"}


def add_wall_style(name: str, width: float) -> dict:
    """Add a new wall style."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    # Create a simple wall style
    style_id = va.AddWallStyle("{name}")
    if style_id:
        # Set the width
        va.SetWallStyleWidth(style_id, {width})
        result = {{"status": "success", "style_id": str(style_id), "name": "{name}", "width": {width}}}
    else:
        result = {{"status": "error", "message": "Failed to create wall style"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(name=name, width=width)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to add wall style"}


def create_door(style_name: str, wall_id: str, position: float, width: float, 
                height: float, layer: str = None, name: str = None) -> dict:
    """Create a door inserted into a wall."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    
    # Find door style by name
    style_id = None
    door_style_ids = va.GetAllDoorStyleIds()
    if door_style_ids:
        for ds_id in door_style_ids:
            if va.GetDoorStyleName(ds_id) == "{style_name}":
                style_id = ds_id
                break
    
    if style_id is None:
        result = {{"status": "error", "message": "Door style '{style_name}' not found".format(style_name="{style_name}")}}
    else:
        # Convert wall_id string to GUID
        wall_guid = Guid("{wall_id}")
        
        # Create the door
        door_id = va.AddDoor(wall_guid, {position}, style_id)
        
        if door_id != Guid.Empty:
            # Set door dimensions
            va.SetDoorWidth(door_id, {width})
            va.SetDoorHeight(door_id, {height})
            
            result = {{
                "status": "success", 
                "door_id": str(door_id),
                "wall_id": "{wall_id}",
                "style": "{style_name}",
                "width": {width},
                "height": {height},
                "position": {position}
            }}
            
            # Set layer if specified  
            {layer_code}
            
            # Set name if specified
            {name_code}
        else:
            result = {{"status": "error", "message": "Failed to create door"}}
            
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(
        style_name=style_name,
        wall_id=wall_id,
        position=position,
        width=width,
        height=height,
        layer_code='''if True:  # layer specified
    import scriptcontext as sc
    obj = sc.doc.Objects.Find(door_id)
    if obj:
        layer_index = sc.doc.Layers.FindName("{}")
        if layer_index >= 0:
            attr = obj.Attributes
            attr.LayerIndex = layer_index
            sc.doc.Objects.ModifyAttributes(door_id, attr, True)'''.format(layer) if layer else "# No layer specified",
        name_code='''if True:  # name specified
    obj = sc.doc.Objects.Find(door_id)
    if obj:
        attr = obj.Attributes
        attr.Name = "{}"
        sc.doc.Objects.ModifyAttributes(door_id, attr, True)'''.format(name) if name else "# No name specified"
    )
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to create door"}


def create_window(style_name: str, wall_id: str, position: float, width: float, 
                  height: float, layer: str = None, name: str = None) -> dict:
    """Create a window inserted into a wall."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    
    # Find window style by name
    style_id = None
    window_style_ids = va.GetAllWindowStyleIds()
    if window_style_ids:
        for ws_id in window_style_ids:
            if va.GetWindowStyleName(ws_id) == "{style_name}":
                style_id = ws_id
                break
    
    if style_id is None:
        result = {{"status": "error", "message": "Window style '{style_name}' not found".format(style_name="{style_name}")}}
    else:
        # Convert wall_id string to GUID
        wall_guid = Guid("{wall_id}")
        
        # Create the window
        window_id = va.AddWindow(wall_guid, {position}, style_id)
        
        if window_id != Guid.Empty:
            # Set window dimensions
            va.SetWindowWidth(window_id, {width})
            va.SetWindowHeight(window_id, {height})
            
            result = {{
                "status": "success", 
                "window_id": str(window_id),
                "wall_id": "{wall_id}",
                "style": "{style_name}",
                "width": {width},
                "height": {height},
                "position": {position}
            }}
            
            # Set layer if specified  
            {layer_code}
            
            # Set name if specified
            {name_code}
        else:
            result = {{"status": "error", "message": "Failed to create window"}}
            
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(
        style_name=style_name,
        wall_id=wall_id,
        position=position,
        width=width,
        height=height,
        layer_code='''if True:  # layer specified
    import scriptcontext as sc
    obj = sc.doc.Objects.Find(window_id)
    if obj:
        layer_index = sc.doc.Layers.FindName("{}")
        if layer_index >= 0:
            attr = obj.Attributes
            attr.LayerIndex = layer_index
            sc.doc.Objects.ModifyAttributes(window_id, attr, True)'''.format(layer) if layer else "# No layer specified",
        name_code='''if True:  # name specified
    obj = sc.doc.Objects.Find(window_id)
    if obj:
        attr = obj.Attributes
        attr.Name = "{}"
        sc.doc.Objects.ModifyAttributes(window_id, attr, True)'''.format(name) if name else "# No name specified"
    )
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to create window"}


def list_door_styles() -> dict:
    """List all available door styles."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    styles = []
    door_style_ids = va.GetAllDoorStyleIds()
    if door_style_ids:
        for style_id in door_style_ids:
            name = va.GetDoorStyleName(style_id)
            if name:
                styles.append({"id": str(style_id), "name": name})
    
    result = {"status": "success", "door_styles": styles, "count": len(styles)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to get door styles"}


def list_window_styles() -> dict:
    """List all available window styles."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    styles = []
    window_style_ids = va.GetAllWindowStyleIds()
    if window_style_ids:
        for style_id in window_style_ids:
            name = va.GetWindowStyleName(style_id)
            if name:
                styles.append({"id": str(style_id), "name": name})
    
    result = {"status": "success", "window_styles": styles, "count": len(styles)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to get window styles"}


def create_column(style_name: str, position: list, height: float, 
                  layer: str = None, name: str = None) -> dict:
    """Create a column."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    import Rhino.Geometry as rg
    
    # Find column style by name
    style_id = None
    column_style_ids = va.GetAllColumnStyleIds()
    if column_style_ids:
        for cs_id in column_style_ids:
            if va.GetColumnStyleName(cs_id) == "{style_name}":
                style_id = cs_id
                break
    
    if style_id is None:
        result = {{"status": "error", "message": "Column style '{style_name}' not found".format(style_name="{style_name}")}}
    else:
        # Create the column
        base_pt = rg.Point3d({position[0]}, {position[1]}, {position[2]})
        column_id = va.AddColumn(base_pt, {height}, style_id)
        
        if column_id != Guid.Empty:
            result = {{
                "status": "success", 
                "column_id": str(column_id),
                "style": "{style_name}",
                "height": {height},
                "position": {position}
            }}
            
            # Set layer if specified
            {layer_code}
            
            # Set name if specified
            {name_code}
        else:
            result = {{"status": "error", "message": "Failed to create column"}}
            
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(
        style_name=style_name,
        position=position,
        height=height,
        layer_code='''if True:  # layer specified
    import scriptcontext as sc
    obj = sc.doc.Objects.Find(column_id)
    if obj:
        layer_index = sc.doc.Layers.FindName("{}")
        if layer_index >= 0:
            attr = obj.Attributes
            attr.LayerIndex = layer_index
            sc.doc.Objects.ModifyAttributes(column_id, attr, True)'''.format(layer) if layer else "# No layer specified",
        name_code='''if True:  # name specified
    obj = sc.doc.Objects.Find(column_id)
    if obj:
        attr = obj.Attributes
        attr.Name = "{}"
        sc.doc.Objects.ModifyAttributes(column_id, attr, True)'''.format(name) if name else "# No name specified"
    )
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to create column"}


def create_beam(style_name: str, start: list, end: list, 
                layer: str = None, name: str = None) -> dict:
    """Create a beam."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    import Rhino.Geometry as rg
    
    # Find beam style by name
    style_id = None
    beam_style_ids = va.GetAllBeamStyleIds()
    if beam_style_ids:
        for bs_id in beam_style_ids:
            if va.GetBeamStyleName(bs_id) == "{style_name}":
                style_id = bs_id
                break
    
    if style_id is None:
        result = {{"status": "error", "message": "Beam style '{style_name}' not found".format(style_name="{style_name}")}}
    else:
        # Create the beam
        start_pt = rg.Point3d({start[0]}, {start[1]}, {start[2]})
        end_pt = rg.Point3d({end[0]}, {end[1]}, {end[2]})
        beam_id = va.AddBeam(start_pt, end_pt, style_id)
        
        if beam_id != Guid.Empty:
            result = {{
                "status": "success", 
                "beam_id": str(beam_id),
                "style": "{style_name}",
                "start": {start},
                "end": {end}
            }}
            
            # Set layer if specified
            {layer_code}
            
            # Set name if specified
            {name_code}
        else:
            result = {{"status": "error", "message": "Failed to create beam"}}
            
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(
        style_name=style_name,
        start=start,
        end=end,
        layer_code='''if True:  # layer specified
    import scriptcontext as sc
    obj = sc.doc.Objects.Find(beam_id)
    if obj:
        layer_index = sc.doc.Layers.FindName("{}")
        if layer_index >= 0:
            attr = obj.Attributes
            attr.LayerIndex = layer_index
            sc.doc.Objects.ModifyAttributes(beam_id, attr, True)'''.format(layer) if layer else "# No layer specified",
        name_code='''if True:  # name specified
    obj = sc.doc.Objects.Find(beam_id)
    if obj:
        attr = obj.Attributes
        attr.Name = "{}"
        sc.doc.Objects.ModifyAttributes(beam_id, attr, True)'''.format(name) if name else "# No name specified"
    )
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to create beam"}


def create_slab(boundary_ids: list, thickness: float, 
                layer: str = None, name: str = None) -> dict:
    """Create a slab from boundary curves."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    import scriptcontext as sc
    
    # Convert boundary curve IDs to GUIDs
    boundary_guids = []
    for curve_id in {boundary_ids}:
        boundary_guids.append(Guid(curve_id))
    
    # Create the slab
    slab_id = va.AddSlab(boundary_guids, {thickness})
    
    if slab_id != Guid.Empty:
        result = {{
            "status": "success", 
            "slab_id": str(slab_id),
            "thickness": {thickness},
            "boundary_curves": {boundary_count}
        }}
        
        # Set layer if specified
        {layer_code}
        
        # Set name if specified
        {name_code}
    else:
        result = {{"status": "error", "message": "Failed to create slab"}}
        
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(
        boundary_ids=boundary_ids,
        thickness=thickness,
        boundary_count=len(boundary_ids),
        layer_code='''if True:  # layer specified
    obj = sc.doc.Objects.Find(slab_id)
    if obj:
        layer_index = sc.doc.Layers.FindName("{}")
        if layer_index >= 0:
            attr = obj.Attributes
            attr.LayerIndex = layer_index
            sc.doc.Objects.ModifyAttributes(slab_id, attr, True)'''.format(layer) if layer else "# No layer specified",
        name_code='''if True:  # name specified
    obj = sc.doc.Objects.Find(slab_id)
    if obj:
        attr = obj.Attributes
        attr.Name = "{}"
        sc.doc.Objects.ModifyAttributes(slab_id, attr, True)'''.format(name) if name else "# No name specified"
    )
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to create slab"}


def list_levels() -> dict:
    """List all levels."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    levels = []
    level_ids = va.GetAllLevelIds()
    if level_ids:
        for level_id in level_ids:
            name = va.GetLevelName(level_id)
            elevation = va.GetLevelElevation(level_id)
            if name is not None:
                levels.append({
                    "id": str(level_id), 
                    "name": name, 
                    "elevation": elevation
                })
    
    result = {"status": "success", "levels": levels, "count": len(levels)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to get levels"}


def add_level(name: str, elevation: float) -> dict:
    """Add a new level."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    level_id = va.AddLevel("{name}", {elevation})
    if level_id:
        result = {{
            "status": "success", 
            "level_id": str(level_id), 
            "name": "{name}", 
            "elevation": {elevation}
        }}
    else:
        result = {{"status": "error", "message": "Failed to create level"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(name=name, elevation=elevation)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to add level"}


def add_building(name: str) -> dict:
    """Add a new building."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    building_id = va.AddBuilding("{name}")
    if building_id:
        result = {{"status": "success", "building_id": str(building_id), "name": "{name}"}}
    else:
        result = {{"status": "error", "message": "Failed to create building"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(name=name)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to add building"}


def add_parameter(name: str, param_type: str, object_id: str = None) -> dict:
    """Add a custom parameter."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    
    # Convert type string to VisualARQ parameter type
    param_type_map = {{
        "text": 0,  # String
        "number": 1,  # Double
        "integer": 2,  # Integer
        "boolean": 3,  # Boolean
        "length": 4   # Length/Distance
    }}
    
    va_type = param_type_map.get("{param_type}", 0)
    
    if "{object_id}":
        # Object parameter
        obj_guid = Guid("{object_id}")
        param_id = va.AddObjectParameter(obj_guid, "{name}", va_type)
    else:
        # Document parameter
        param_id = va.AddDocumentParameter("{name}", va_type)
    
    if param_id:
        result = {{"status": "success", "parameter_id": str(param_id), "name": "{name}", "type": "{param_type}"}}
    else:
        result = {{"status": "error", "message": "Failed to create parameter"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(param_type=param_type, object_id=object_id or "", name=name)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to add parameter"}


def set_parameter(name: str, value: str, object_id: str) -> dict:
    """Set parameter value for an object."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    
    obj_guid = Guid("{object_id}")
    success = va.SetParameterValue(obj_guid, "{name}", "{value}")
    
    if success:
        result = {{"status": "success", "object_id": "{object_id}", "parameter": "{name}", "value": "{value}"}}
    else:
        result = {{"status": "error", "message": "Failed to set parameter value"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(object_id=object_id, name=name, value=value)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to set parameter"}


def get_parameter(name: str, object_id: str) -> dict:
    """Get parameter value for an object."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    from System import Guid
    
    obj_guid = Guid("{object_id}")
    value = va.GetParameterValue(obj_guid, "{name}")
    
    result = {{"status": "success", "object_id": "{object_id}", "parameter": "{name}", "value": str(value)}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(object_id=object_id, name=name)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to get parameter"}


def ifc_export(path: str, version: str = "IFC4") -> dict:
    """Export model to IFC format."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    # Export to IFC
    success = va.ExportIFC("{path}", "{version}")
    
    if success:
        result = {{"status": "success", "path": "{path}", "version": "{version}"}}
    else:
        result = {{"status": "error", "message": "IFC export failed"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(path=path, version=version)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to export IFC"}


def ifc_import(path: str) -> dict:
    """Import IFC file."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    
    # Import IFC
    success = va.ImportIFC("{path}")
    
    if success:
        result = {{"status": "success", "path": "{path}"}}
    else:
        result = {{"status": "error", "message": "IFC import failed"}}
    
except Exception as e:
    result = {{"status": "error", "message": "VisualARQ error: " + str(e)}}

import json
print("RESULT:" + json.dumps(result))
'''.format(path=path)
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to import IFC"}


def list_walls() -> dict:
    """List all walls with properties."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    import scriptcontext as sc
    
    walls = []
    # Get all objects and filter for walls
    for obj in sc.doc.Objects:
        if obj.Geometry:
            # Check if it's a VA wall
            if va.IsWall(obj.Id):
                wall_info = {
                    "id": str(obj.Id),
                    "name": obj.Attributes.Name if obj.Attributes.Name else "Unnamed",
                    "layer": sc.doc.Layers[obj.Attributes.LayerIndex].FullPath if obj.Attributes.LayerIndex >= 0 else "Default"
                }
                
                # Try to get wall-specific properties
                try:
                    height = va.GetWallHeight(obj.Id)
                    if height:
                        wall_info["height"] = height
                        
                    length = va.GetWallLength(obj.Id)
                    if length:
                        wall_info["length"] = length
                        
                    style_id = va.GetWallStyle(obj.Id)
                    if style_id:
                        style_name = va.GetWallStyleName(style_id)
                        wall_info["style"] = style_name
                except:
                    pass
                    
                walls.append(wall_info)
    
    result = {"status": "success", "walls": walls, "count": len(walls)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to list walls"}


def list_doors() -> dict:
    """List all doors with properties."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    import scriptcontext as sc
    
    doors = []
    # Get all objects and filter for doors
    for obj in sc.doc.Objects:
        if obj.Geometry:
            # Check if it's a VA door
            if va.IsDoor(obj.Id):
                door_info = {
                    "id": str(obj.Id),
                    "name": obj.Attributes.Name if obj.Attributes.Name else "Unnamed",
                    "layer": sc.doc.Layers[obj.Attributes.LayerIndex].FullPath if obj.Attributes.LayerIndex >= 0 else "Default"
                }
                
                # Try to get door-specific properties
                try:
                    width = va.GetDoorWidth(obj.Id)
                    if width:
                        door_info["width"] = width
                        
                    height = va.GetDoorHeight(obj.Id)
                    if height:
                        door_info["height"] = height
                        
                    style_id = va.GetDoorStyle(obj.Id)
                    if style_id:
                        style_name = va.GetDoorStyleName(style_id)
                        door_info["style"] = style_name
                except:
                    pass
                    
                doors.append(door_info)
    
    result = {"status": "success", "doors": doors, "count": len(doors)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to list doors"}


def list_windows() -> dict:
    """List all windows with properties."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    import scriptcontext as sc
    
    windows = []
    # Get all objects and filter for windows
    for obj in sc.doc.Objects:
        if obj.Geometry:
            # Check if it's a VA window
            if va.IsWindow(obj.Id):
                window_info = {
                    "id": str(obj.Id),
                    "name": obj.Attributes.Name if obj.Attributes.Name else "Unnamed",
                    "layer": sc.doc.Layers[obj.Attributes.LayerIndex].FullPath if obj.Attributes.LayerIndex >= 0 else "Default"
                }
                
                # Try to get window-specific properties
                try:
                    width = va.GetWindowWidth(obj.Id)
                    if width:
                        window_info["width"] = width
                        
                    height = va.GetWindowHeight(obj.Id)
                    if height:
                        window_info["height"] = height
                        
                    style_id = va.GetWindowStyle(obj.Id)
                    if style_id:
                        style_name = va.GetWindowStyleName(style_id)
                        window_info["style"] = style_name
                except:
                    pass
                    
                windows.append(window_info)
    
    result = {"status": "success", "windows": windows, "count": len(windows)}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to list windows"}


def list_objects() -> dict:
    """List all VisualARQ objects by type."""
    code = '''
import clr
try:
    clr.AddReference("VisualARQ.Script")
    import VisualARQ.Script as va
    import scriptcontext as sc
    
    va_objects = {
        "walls": [],
        "doors": [],
        "windows": [],
        "columns": [],
        "beams": [],
        "slabs": [],
        "stairs": [],
        "railings": []
    }
    
    # Get all objects and categorize VA objects
    for obj in sc.doc.Objects:
        if obj.Geometry:
            obj_info = {
                "id": str(obj.Id),
                "name": obj.Attributes.Name if obj.Attributes.Name else "Unnamed"
            }
            
            if va.IsWall(obj.Id):
                va_objects["walls"].append(obj_info)
            elif va.IsDoor(obj.Id):
                va_objects["doors"].append(obj_info)
            elif va.IsWindow(obj.Id):
                va_objects["windows"].append(obj_info)
            elif va.IsColumn(obj.Id):
                va_objects["columns"].append(obj_info)
            elif va.IsBeam(obj.Id):
                va_objects["beams"].append(obj_info)
            elif va.IsSlab(obj.Id):
                va_objects["slabs"].append(obj_info)
            elif va.IsStair(obj.Id):
                va_objects["stairs"].append(obj_info)
            elif va.IsRailing(obj.Id):
                va_objects["railings"].append(obj_info)
    
    # Add counts
    for obj_type in va_objects:
        va_objects[obj_type + "_count"] = len(va_objects[obj_type])
    
    result = {"status": "success", "va_objects": va_objects}
    
except Exception as e:
    result = {"status": "error", "message": "VisualARQ error: " + str(e)}

import json
print("RESULT:" + json.dumps(result))
'''
    
    with RhinoClient() as client:
        response = client.send_command("execute_rhinoscript_python_code", {"code": code})
        if response.get("status") == "success":
            result = response.get("result", {}); output = result.get("output", "") or result.get("result", "") or ""
            if "RESULT:" in output:
                try:
                    json_part = output.split("RESULT:", 1)[1].strip()
                    return json.loads(json_part)
                except:
                    pass
        return {"status": "error", "message": "Failed to list VisualARQ objects"}


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description='VisualARQ BIM management for Rhino')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    # Check VisualARQ availability
    subparsers.add_parser('check', help='Check if VisualARQ is installed')
    
    # Info
    subparsers.add_parser('info', help='Get VisualARQ info (styles, levels, etc.)')
    
    # Walls
    wp = subparsers.add_parser('wall', help='Create a wall')
    wp.add_argument('--style', required=True, help='Wall style name')
    wp.add_argument('--start', required=True, help='Start point x,y,z')
    wp.add_argument('--end', required=True, help='End point x,y,z')
    wp.add_argument('--height', type=float, required=True, help='Wall height')
    wp.add_argument('--layer', help='Layer name')
    wp.add_argument('--name', help='Object name')
    
    subparsers.add_parser('wall-styles', help='List all wall styles')
    
    wsp = subparsers.add_parser('add-wall-style', help='Add a new wall style')
    wsp.add_argument('--name', required=True, help='Style name')
    wsp.add_argument('--width', type=float, required=True, help='Wall width')
    
    # Doors
    dp = subparsers.add_parser('door', help='Create a door')
    dp.add_argument('--style', required=True, help='Door style name')
    dp.add_argument('--wall-id', required=True, help='Wall GUID to insert door')
    dp.add_argument('--position', type=float, required=True, help='Position along wall (0-1)')
    dp.add_argument('--width', type=float, required=True, help='Door width')
    dp.add_argument('--height', type=float, required=True, help='Door height')
    dp.add_argument('--layer', help='Layer name')
    dp.add_argument('--name', help='Object name')
    
    subparsers.add_parser('door-styles', help='List all door styles')
    
    # Windows
    winp = subparsers.add_parser('window', help='Create a window')
    winp.add_argument('--style', required=True, help='Window style name')
    winp.add_argument('--wall-id', required=True, help='Wall GUID to insert window')
    winp.add_argument('--position', type=float, required=True, help='Position along wall (0-1)')
    winp.add_argument('--width', type=float, required=True, help='Window width')
    winp.add_argument('--height', type=float, required=True, help='Window height')
    winp.add_argument('--layer', help='Layer name')
    winp.add_argument('--name', help='Object name')
    
    subparsers.add_parser('window-styles', help='List all window styles')
    
    # Columns
    cp = subparsers.add_parser('column', help='Create a column')
    cp.add_argument('--style', required=True, help='Column style name')
    cp.add_argument('--position', required=True, help='Base point x,y,z')
    cp.add_argument('--height', type=float, required=True, help='Column height')
    cp.add_argument('--layer', help='Layer name')
    cp.add_argument('--name', help='Object name')
    
    # Beams
    bp = subparsers.add_parser('beam', help='Create a beam')
    bp.add_argument('--style', required=True, help='Beam style name')
    bp.add_argument('--start', required=True, help='Start point x,y,z')
    bp.add_argument('--end', required=True, help='End point x,y,z')
    bp.add_argument('--layer', help='Layer name')
    bp.add_argument('--name', help='Object name')
    
    # Slabs
    sp = subparsers.add_parser('slab', help='Create a slab')
    sp.add_argument('--boundary', required=True, help='Boundary curve IDs (comma-separated)')
    sp.add_argument('--thickness', type=float, required=True, help='Slab thickness')
    sp.add_argument('--layer', help='Layer name')
    sp.add_argument('--name', help='Object name')
    
    # Levels
    subparsers.add_parser('levels', help='List all levels')
    
    lp = subparsers.add_parser('add-level', help='Add a new level')
    lp.add_argument('--name', required=True, help='Level name')
    lp.add_argument('--elevation', type=float, required=True, help='Level elevation')
    
    # Buildings
    blp = subparsers.add_parser('add-building', help='Add a new building')
    blp.add_argument('--name', required=True, help='Building name')
    
    # Parameters
    pap = subparsers.add_parser('add-param', help='Add a custom parameter')
    pap.add_argument('--name', required=True, help='Parameter name')
    pap.add_argument('--type', required=True, choices=['text', 'number', 'integer', 'boolean', 'length'], help='Parameter type')
    pap.add_argument('--object-id', help='Object ID for object parameter (omit for document parameter)')
    
    psp = subparsers.add_parser('set-param', help='Set parameter value')
    psp.add_argument('--name', required=True, help='Parameter name')
    psp.add_argument('--value', required=True, help='Parameter value')
    psp.add_argument('--object-id', required=True, help='Object ID')
    
    pgp = subparsers.add_parser('get-param', help='Get parameter value')
    pgp.add_argument('--name', required=True, help='Parameter name')
    pgp.add_argument('--object-id', required=True, help='Object ID')
    
    # IFC
    iep = subparsers.add_parser('ifc-export', help='Export to IFC')
    iep.add_argument('--path', required=True, help='Output file path')
    iep.add_argument('--version', default='IFC4', choices=['IFC2x3', 'IFC4', 'IFC4.3'], help='IFC version')
    
    iip = subparsers.add_parser('ifc-import', help='Import IFC file')
    iip.add_argument('--path', required=True, help='IFC file path')
    
    # Queries
    subparsers.add_parser('list-walls', help='List all walls with properties')
    subparsers.add_parser('list-doors', help='List all doors with properties')
    subparsers.add_parser('list-windows', help='List all windows with properties')
    subparsers.add_parser('list-objects', help='List all VisualARQ objects by type')
    
    args = parser.parse_args()
    
    def parse_coords(s):
        """Parse coordinate string 'x,y,z' to list [x,y,z]."""
        return [float(x.strip()) for x in s.split(',')]
    
    # Execute the appropriate function
    try:
        if args.action == 'check':
            result = check_visualarq()
        elif args.action == 'info':
            result = get_info()
        elif args.action == 'wall':
            start = parse_coords(args.start)
            end = parse_coords(args.end)
            result = create_wall(args.style, start, end, args.height, args.layer, args.name)
        elif args.action == 'wall-styles':
            result = list_wall_styles()
        elif args.action == 'add-wall-style':
            result = add_wall_style(args.name, args.width)
        elif args.action == 'door':
            result = create_door(args.style, args.wall_id, args.position, args.width, args.height, args.layer, args.name)
        elif args.action == 'door-styles':
            result = list_door_styles()
        elif args.action == 'window':
            result = create_window(args.style, args.wall_id, args.position, args.width, args.height, args.layer, args.name)
        elif args.action == 'window-styles':
            result = list_window_styles()
        elif args.action == 'column':
            position = parse_coords(args.position)
            result = create_column(args.style, position, args.height, args.layer, args.name)
        elif args.action == 'beam':
            start = parse_coords(args.start)
            end = parse_coords(args.end)
            result = create_beam(args.style, start, end, args.layer, args.name)
        elif args.action == 'slab':
            boundary_ids = [id.strip() for id in args.boundary.split(',')]
            result = create_slab(boundary_ids, args.thickness, args.layer, args.name)
        elif args.action == 'levels':
            result = list_levels()
        elif args.action == 'add-level':
            result = add_level(args.name, args.elevation)
        elif args.action == 'add-building':
            result = add_building(args.name)
        elif args.action == 'add-param':
            result = add_parameter(args.name, args.type, args.object_id)
        elif args.action == 'set-param':
            result = set_parameter(args.name, args.value, args.object_id)
        elif args.action == 'get-param':
            result = get_parameter(args.name, args.object_id)
        elif args.action == 'ifc-export':
            result = ifc_export(args.path, args.version)
        elif args.action == 'ifc-import':
            result = ifc_import(args.path)
        elif args.action == 'list-walls':
            result = list_walls()
        elif args.action == 'list-doors':
            result = list_doors()
        elif args.action == 'list-windows':
            result = list_windows()
        elif args.action == 'list-objects':
            result = list_objects()
        else:
            print(f"Unknown action: {args.action}", file=sys.stderr)
            sys.exit(1)
        
        print(json.dumps(result, indent=2))
        
        # Exit with error code if VisualARQ operation failed
        if result.get("status") == "error":
            sys.exit(1)
            
    except Exception as e:
        error_result = {"status": "error", "message": f"Script error: {str(e)}"}
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
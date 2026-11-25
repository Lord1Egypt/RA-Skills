"""Original crescent jewelry dish. Millimeter CAD; manifold3d 3.5.5, numpy, trimesh."""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
import manifold3d as m
P=Path(__file__).resolve().parent
PARAM={'outer_radius_mm':64,'cutout_radius_mm':52,'cutout_offset_mm':24,'floor_mm':3,'rim_width_mm':2.4,'rim_height_above_floor_mm':7,'tip_rounding_mm':2,'ring_cone_center_mm':[-43,-2],'cone_base_radius_mm':10.5,'cone_tip_radius_mm':1.4,'cone_top_center_z_mm':32.6,'engraving_depth_mm':.6}
def cs(points):return m.CrossSection([points],m.FillRule.EvenOdd)
def disk(r):return m.CrossSection.circle(r,circular_segments=384)
base=(disk(PARAM['outer_radius_mm'])-disk(PARAM['cutout_radius_mm']).translate((PARAM['cutout_offset_mm'],0)))
base=base.offset(-2,circular_segments=64).simplify(.005).offset(2,circular_segments=64).simplify(.005)
pocket=base.offset(-PARAM['rim_width_mm'],circular_segments=64).simplify(.005)
solid=base.extrude(10)-pocket.extrude(8).translate((0,0,3))
cx,cy=PARAM['ring_cone_center_mm'];cone=m.Manifold.cylinder(30,10.5,1.4,circular_segments=160).translate((cx,cy,2.6));cap=m.Manifold.sphere(1.4,circular_segments=64).translate((cx,cy,32.6));solid=solid+cone+cap
stars=[(-24,43,3),(-39,30,2),(-53,12,2.8),(-53,-18,1.8),(-34,-39,3),(-9,-47,2.2)]
def star(x,y,r):
 a=np.linspace(0,2*np.pi,10,endpoint=False)+np.pi/2;rad=np.array([r,r*.43]*5);return cs(np.column_stack([x+rad*np.cos(a),y+rad*np.sin(a)]))
for x,y,r in stars:solid=solid-star(x,y,r).extrude(1.2).translate((0,0,2.4))
for (x,y,_),(xx,yy,_) in zip(stars,stars[1:]):
 v=np.array([xx-x,yy-y]);v=v/np.linalg.norm(v);n=np.array([-v[1],v[0]])*.4;a=np.array([x,y]);b=np.array([xx,yy]);line=cs([a+n,b+n,b-n,a-n]);solid=solid-line.extrude(1.2).translate((0,0,2.4))
# A few smaller engraved sparkle marks, away from the rim and cone footprint.
for x,y in [(-14,48),(-43,39),(-56,-5),(-24,-48),(-46,-31)]:solid=solid-disk(.65).extrude(1.1).translate((x,y,2.4))
solid=solid.simplify(.005)
assert str(solid.status()).endswith('NoError')
a=solid.to_mesh();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=False);mesh.export(P/'moon-jewelry-dish.stl');check=trimesh.load(P/'moon-jewelry-dish.stl',force='mesh');assert check.is_watertight and check.is_winding_consistent and check.body_count==1
mesh.visual.face_colors=[239,234,222,255];mesh.export(P/'moon-jewelry-dish.glb')
r={'parameters':PARAM,'dimensions_mm':mesh.extents.tolist(),'bounds_mm':mesh.bounds.tolist(),'triangles':len(mesh.faces),'watertight':bool(check.is_watertight),'consistent_winding':bool(check.is_winding_consistent),'components':int(check.body_count),'kernel_status':str(solid.status()),'zero_area_faces':int(np.sum(check.area_faces==0)),'floor_remaining_below_engravings_mm':2.4,'minimum_wall_design_mm':2.4,'cone_top_diameter_mm':2.8,'CAD_surface_tolerance_mm':.005,'source_sha256':hashlib.sha256((P/'moon-jewelry-dish.stl').read_bytes()).hexdigest(),'physical_print_tested':False,'ready_to_print':False}
(P/'geometry-report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

import bpy
import bmesh
import unittest
#NOTE: for some reason all geometry added to the
#blender document is parented at the moment

'''
It appears that there are two methods:
    1) create a bmesh (edit-mesh) each time 
geometry is to be added; easy to add floating disconnected geometry. --> functions
    2) have a single bmesh open and update the edit-mesh at the very end. --> object

'''
def init_mesh_object(name="Object"):
    me = bpy.data.meshes.new("Mesh")
    scene = bpy.context.scene
    obj = bpy.data.objects.new(name, me)
    scene.objects.link(obj)
    return obj

def init_bmesh():
    return bmesh.new()

class MeshSkeletonGrower(object):
    '''
    example use case:
    grower = MeshSkeletonGrower()
    v1 = grower.add_vertices((0.0,0.0,0.0))
    #do some stuff
    v2 = grower.add_vertices((10.0,0.0,3.0))
    grower.add_edge((v1,v2))
    #at the very end:
    grower.finalize()
    '''
    def __init__(self,obj_name='Object',mesh_name='mesh'):
        self.obj_name = obj_name
        self.mesh_name = mesh_name
        self.me = bpy.data.meshes.new(self.mesh_name)
        self.bm = bmesh.new()

    def _prepare_to_add_geom(self):
        #to get bmesh must be in edit mode
        #bpy.context.scene.objects.active = self.obj
        #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        return bmesh.from_edit_mesh(self.me)
    
    def add_vertex(self,coordinates):
        return self.bm.verts.new(coordinates)

    def add_vertices(self,vertices):
        bm_verts = []
        for vert in vertices:
            new_vert = self.bm.verts.new(vert)
            bm_verts.append(new_vert)
        return bm_verts
    
    def add_edge(self,v1,v2):
        return self.bm.edges.new((v1,v2))

    def finalize(self):
        self.bm.to_mesh(self.me)
        self.bm.free()
        scene = bpy.context.scene
        self.obj = bpy.data.objects.new(self.obj_name, self.me)
        scene.objects.link(self.obj)


def prep_mesh_object(obj):
    ''' sets object active and in edit mode, and retrieves the mesh
    '''
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    me =  obj.data
    return me

def create_bmesh_from_obj(obj):
    me = prep_mesh_object(obj)
    bm = bmesh.from_edit_mesh(me)
    return bm

def object_mode():
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def add_edge_to_mesh_object(obj,vertA,vertB):
    ''' given to verts A,B that already exist, and a obj,
    create a new edge between A,B
    '''
    me = prep_mesh_object(obj)
    bm = bmesh.from_edit_mesh(me)
    bm.edges.new((vertA,vertB))
    bmesh.update_edit_mesh(me)
    object_mode()

def add_line_to_mesh_object(obj,start,end):
    me = prep_mesh_object(obj)
    add_line_to_mesh(me,start,end)
    object_mode()

def add_vertices_to_mesh_object(obj,verts):
    me = prep_mesh_object(obj)
    bm = bmesh.from_edit_mesh(me)
    bm_verts = []
    for vert in verts:
        new_vert = bm.verts.new(vert)
        bm_verts.append(new_vert)
    bmesh.update_edit_mesh(me)
    object_mode()
    return bm_verts

def add_line_to_mesh(mesh,start,end):
    bm = bmesh.from_edit_mesh(mesh)
    add_line_to_bmesh(bm,start,end)
    bmesh.update_edit_mesh(mesh)

def add_line_to_bmesh(bmesh,start,end):
    v_start = bmesh.verts.new(start)
    v_end = bmesh.verts.new(end)
    bmesh.edges.new((v_start,v_end))

def show_bmesh(bmesh):
    mesh = write_bmesh_to_mesh(bmesh)
    return add_mesh_to_scene(mesh)

def write_bmesh_to_mesh(bmesh):
    new_mesh = bpy.data.meshes.new("Mesh")
    bmesh.to_mesh(new_mesh)
    return new_mesh

def add_mesh_to_scene(mesh,object_name="Object"):
    scene = bpy.context.scene
    obj = bpy.data.objects.new(object_name, mesh)
    scene.objects.link(obj)
    return object_name

class MeshHelpersTestCase(unittest.TestCase):
        
    def setUp(self):
        self.obj = init_mesh_object()
        self.bm = bmesh.new()

    def test_add_line_to_bmesh(self):
        add_line_to_bmesh(self.bm,(0,0,0),(0,0,1))
        show_bmesh(self.bm)

    def test_add_line_to_mesh(self):
        a = (0,0,0)
        b = (0,1,1)
        c = (1,1,1)
        add_line_to_mesh_object(self.obj,a,b)
        add_line_to_mesh_object(self.obj,b,c)

    def test_add_vertices_to_mesh_object(self):
        verts = ((1,1,0),(2,2,0))
        add_vertices_to_mesh_object(self.obj,verts)

if __name__=="__main__":
    unittest.main(exit=False)

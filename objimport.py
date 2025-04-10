import mathutils

def load(context,
        filepath, 
        *,
        relpath=None,
        world_matrix=None,
        split_by_object=True):
    """
    Does all the actual importing.
    """
    
    def create_face(mat, smooth_group, object):
        face_loc_indices = []
        face_nor_indices = []
        face_tex_indices = []
        return (
            face_loc_indices,
            face_nor_indices,
            face_tex_indices,
            mat,
            smooth_group,
            object,
            [] # I hate blender api docs. had to dig around for this
        )
    
    if world_matrix is None:
        world_matrix = mathutils.Matrix()
    
    vloc = []
    vnor = []
    vtex = []
    faces = []
    materials = set()
    
    ctx_mat = None
    ctx_smooth_group = None
    ctx_object = None
    
    face_loc_idx = None
    face_nor_idx = None
    face_tex_idx = None
    prev_idx = None
    face = None
    vec = []
    
    with open(filepath, 'rb') as file:
        for line in file:
            line_split = line.split()
            
            if not line_split:
                continue
            
            prefix = line_split[0]
            
            if prefix == b'v':
                vloc.append(tuple(([v for v in line_split[1:]])[:3]))
            elif prefix == b'vn':
                vnor.append(tuple(([v for v in line_split[1:]])[:3]))
            elif prefix == b'vt':
                vtex.append(tuple(([v for v in line_split[1:]])[:2]))
            elif prefix == b'f':
                face = create_face(ctx_mat, ctx_smooth_group, ctx_object)
                (face_loc_idx, 
                face_nor_idx, 
                face_tex_idx, 
                _1,
                _2, 
                _3, 
                face_invalid) = face
                faces.append(face)
                
                for v in line_split:
                    obj_vert = v.split(b'/')
                    idx = int(obj_vert[0]) - 1
                    loc_idx = (idx + len(vloc) + 1) if (idx < 0) else idx
                    
    
    return {'FINISHED'}

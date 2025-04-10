bl_info = {
    "name": "Ian's OBJ export",
    "blender": (4, 0),
    "location": "File > Import-Export",
}

import bpy
from bpy.types import *
import os

from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
    orientation_helper,
    path_reference,
    axis_conversion,
)


@orientation_helper(axis_forward="Z", axis_up="Y")
class ImportOBJ(bpy.types.Operator, ImportHelper):
    """Load a Wavefront OBJ file"""

    bl_idname = "export_test.custom_obj"
    bl_label = "Export Custom OBJ"
    bl_options = {"PRESET", "UNDO"}

    filename_ext = ".obj"

    filter_glob = StringProperty(default="*.obj;*.mtl", options={"HIDDEN"})

    # Only splitting by object here, but this could be changed depending
    # on the desired workflow. For a custom pipeline I'd rather not give
    # artists options they shouldn't be using.
    split_by_object = BoolProperty(
        name="Split By Object",
        description="Split Blender objects by 'o name' groups",
        default=True,
    )

    def execute(self, context):
        import objimport
        
        keywords = self.as_keywords(ignore=("filter_glob"))

        world_matrix = axis_conversion(
            from_forward=self.axis_forward, from_up=self.axis_up
        ).to_4x4()
        keywords["world_matrix"] = world_matrix

        if bpy.data.is_saved and context.user_preferences.filepaths.use_relative_paths:
            keywords["relpath"] = os.path.dirname(bpy.data.filepath)
        
        return objimport.load(context, **keywords)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop(self, "split_by_object")


def importfunc(self, context):
    self.layout.operator(ImportOBJ.bl_idname, text="Custom Wavefront OBJ")
    
def register():
    bpy.utils.register_module(__name__)
    
    bpy.types.INFO_MT_file_import.append(importfunc)

def unregister():
    bpy.types.INFO_MT_file_import.remove(importfunc)

if __name__ == "__main__":
    register()
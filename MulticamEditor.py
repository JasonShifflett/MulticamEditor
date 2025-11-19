# -----------------------------------------------------------------------------
# Multicam Quick Editor Add-on
# Author: Jason Shifflett & ChatGPT
# Description: Provides a customizable camera pie menu and N-panel editor to provide
# autogeneration of camera-linked markers on the timeline during live playback.
# -----------------------------------------------------------------------------
import bpy
from bpy.types import Menu, Operator, Panel
from bpy.props import PointerProperty

bl_info = {
    "name": "Multicam Quick Editor",
    "blender": (4, 5, 0),
    "category": "3D View"
}

def mq_camera_poll(self, obj):
    return obj.type == 'CAMERA'

# Scene properties for camera slots in the pie menu
def register_scene_props():
    bpy.types.Scene.mq_cam_slot_1 = PointerProperty(
        name="Slot 1",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_2 = PointerProperty(
        name="Slot 2",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_3 = PointerProperty(
        name="Slot 3",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_4 = PointerProperty(
        name="Slot 4",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_5 = PointerProperty(
        name="Slot 5",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_6 = PointerProperty(
        name="Slot 6",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_7 = PointerProperty(
        name="Slot 7",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )
    bpy.types.Scene.mq_cam_slot_8 = PointerProperty(
        name="Slot 8",
        type=bpy.types.Object,
        poll=mq_camera_poll,
    )

def unregister_scene_props():
    del bpy.types.Scene.mq_cam_slot_1
    del bpy.types.Scene.mq_cam_slot_2
    del bpy.types.Scene.mq_cam_slot_3
    del bpy.types.Scene.mq_cam_slot_4
    del bpy.types.Scene.mq_cam_slot_5
    del bpy.types.Scene.mq_cam_slot_6
    del bpy.types.Scene.mq_cam_slot_7
    del bpy.types.Scene.mq_cam_slot_8

class VIEW3D_MT_camera_pie(Menu):
    bl_idname = "VIEW3D_MT_camera_pie"
    bl_label = "Select Camera"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        scene = context.scene

        # Helper to add a slot to a fixed pie direction.
        def add_slot(cam, slot_label):
            if cam:
                op = pie.operator(
                    "view3d.select_and_bind_camera",
                    text=f"{slot_label}: {cam.name}"
                )
                op.camera_name = cam.name
            else:
                # Use a separator so the wedge is non-interactive but keeps the slot position.
                pie.separator()

        # NOTE: The order of these calls defines the pie directions:
        # 1 = Left, 2 = Right, 3 = Bottom, 4 = Top,
        # 5 = Top-Left, 6 = Top-Right, 7 = Bottom-Left, 8 = Bottom-Right.
        add_slot(getattr(scene, "mq_cam_slot_1", None), "1")
        add_slot(getattr(scene, "mq_cam_slot_2", None), "2")
        add_slot(getattr(scene, "mq_cam_slot_3", None), "3")
        add_slot(getattr(scene, "mq_cam_slot_4", None), "4")
        add_slot(getattr(scene, "mq_cam_slot_5", None), "5")
        add_slot(getattr(scene, "mq_cam_slot_6", None), "6")
        add_slot(getattr(scene, "mq_cam_slot_7", None), "7")
        add_slot(getattr(scene, "mq_cam_slot_8", None), "8")

class VIEW3D_OT_select_and_bind_camera(Operator):
    bl_idname = "view3d.select_and_bind_camera"
    bl_label = "Select and Bind Camera"
    bl_options = {'REGISTER', 'UNDO'}

    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        camera = scene.objects.get(self.camera_name)
        current_frame = scene.frame_current
        if camera:
            # Set the active camera
            scene.camera = camera

            # Check for existing markers at the current frame and remove them
            markers_to_remove = [marker for marker in scene.timeline_markers if marker.frame == current_frame]
            for marker in markers_to_remove:
                scene.timeline_markers.remove(marker)

            # Add a new marker at the current frame
            marker = scene.timeline_markers.new(name=camera.name, frame=current_frame)
            marker.camera = camera
            self.report({'INFO'}, f"Camera set to {self.camera_name} and marker added at frame {current_frame}")
        else:
            self.report({'WARNING'}, f"Camera {self.camera_name} not found")
        return {'FINISHED'}

class VIEW3D_PT_multicam_quick_editor(Panel):
    bl_label = "Multicam Quick Editor"
    bl_idname = "VIEW3D_PT_multicam_quick_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Multicam"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()
        col.label(text="Pie Menu Camera Slots")

        col.prop(scene, "mq_cam_slot_1", text="Left")
        col.prop(scene, "mq_cam_slot_2", text="Right")
        col.prop(scene, "mq_cam_slot_3", text="Bottom")
        col.prop(scene, "mq_cam_slot_4", text="Top")
        col.prop(scene, "mq_cam_slot_5", text="Top-Left")
        col.prop(scene, "mq_cam_slot_6", text="Top-Right")
        col.prop(scene, "mq_cam_slot_7", text="Bottom-Left")
        col.prop(scene, "mq_cam_slot_8", text="Bottom-Right")

        layout.separator()
        col = layout.column(align=True)
        col.label(text="Tips:")
        col.label(text="- Assign cameras to slots")
        col.label(text="- Press J in 3D View for pie menu")

def menu_func(self, context):
    self.layout.menu(VIEW3D_MT_camera_pie.bl_idname)

addon_keymaps = []

def register():
    bpy.utils.register_class(VIEW3D_MT_camera_pie)
    bpy.utils.register_class(VIEW3D_OT_select_and_bind_camera)
    bpy.utils.register_class(VIEW3D_PT_multicam_quick_editor)

    register_scene_props()

    bpy.types.VIEW3D_MT_view.append(menu_func)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'J', 'PRESS', ctrl=False, shift=False)
    kmi.properties.name = VIEW3D_MT_camera_pie.bl_idname
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_camera_pie)
    bpy.utils.unregister_class(VIEW3D_OT_select_and_bind_camera)
    bpy.utils.unregister_class(VIEW3D_PT_multicam_quick_editor)

    bpy.types.VIEW3D_MT_view.remove(menu_func)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    unregister_scene_props()

if __name__ == "__main__":
    register()

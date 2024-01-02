bl_info = {
    "name": "Octane Skin Shader 2.0 LE Textures Import",
    "author": "Umberto Celentano",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "Node Editor Toolbar or Shift-W",
    "description": "Import and connect multiple textures to Octane Skin Shader",
    "warning": "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/node/oss_mtex_import.html",
    "tracker_url": "https://gitlab.com/umbcel/oss_mtex_import/-/issues",
    "category": "Node",
}

import bpy
import os

class MtexImportPanel(bpy.types.Panel):
    bl_label = "Octane Skin Shader 2.0 LE Textures Import"
    bl_idname = "PANEL_PT_MtexImport"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

##00 Texture 0: Albedo
##05 Texture 1: Specular
##13 Texture 2: Roughness or Inverted Gloss
##28 Texture 3: Bump
##29 Texture 4: Normal
##30 Texture 5: Displacement
##22 Texture 6: SSS Color
##25 Texture 7: Translucency
##40 Texture 8: Cavity

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{0}", text="Albedo")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{1}", text="Specular")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{2}", text="Roughness")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{3}", text="Bump")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{4}", text="Normal")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{5}", text="Displacement")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{6}", text="SSS Color")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{7}", text="Translucency")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_texture_path_{8}", text="Cavity")
        row = layout.row()
        row.prop(scn.mtex_import_settings, f"mtex_connect", text="Auto Connect")
        row.prop(scn.mtex_import_settings, f"mtex_rough_invert", text="Invert Roughness")

        layout.operator("object.import_textures", text="Import Textures")

class MtexImportSettings(bpy.types.PropertyGroup):
    mtex_texture_path_0: bpy.props.StringProperty(name="Texture Path 1", subtype='FILE_PATH')
    mtex_texture_path_1: bpy.props.StringProperty(name="Texture Path 2", subtype='FILE_PATH')
    mtex_texture_path_2: bpy.props.StringProperty(name="Texture Path 3", subtype='FILE_PATH')
    mtex_texture_path_3: bpy.props.StringProperty(name="Texture Path 4", subtype='FILE_PATH')
    mtex_texture_path_4: bpy.props.StringProperty(name="Texture Path 5", subtype='FILE_PATH')
    mtex_texture_path_5: bpy.props.StringProperty(name="Texture Path 6", subtype='FILE_PATH')
    mtex_texture_path_6: bpy.props.StringProperty(name="Texture Path 7", subtype='FILE_PATH')
    mtex_texture_path_7: bpy.props.StringProperty(name="Texture Path 8", subtype='FILE_PATH')
    mtex_texture_path_8: bpy.props.StringProperty(name="Texture Path 9", subtype='FILE_PATH')

    mtex_connect: bpy.props.BoolProperty(name="Auto Connect")
    mtex_rough_invert: bpy.props.BoolProperty(name="Rough Inverted")

class NodeLinker:
    @staticmethod
    def link_nodes(node_output_name, output_name, node_input_name, input_name):
        # Ottieni il contesto attivo
        context = bpy.context

        # Ottieni l'oggetto attivo e il suo materiale attivo
        obj = context.active_object
        active_material = obj.active_material

        # Ottieni il node_tree del materiale attivo
        node_tree = active_material.node_tree

        # Ottieni i nodi necessari per il collegamento
        node_output = node_tree.nodes.get(node_output_name)  # Sostituisci con il nome del tuo nodo di output
        node_input = node_tree.nodes.get(node_input_name)  # Sostituisci con il nome del tuo nodo di input

        # Collega il nodo di output al nodo di input
        node_tree.links.new(node_output.outputs[output_name], node_input.inputs[input_name])  # Sostituisci con i nomi dei tuoi output e input

class ImportTexturesOperator(bpy.types.Operator):
    bl_idname = "object.import_textures"
    bl_label = "Import Textures"
    
    def execute(self, context):
        settings = context.scene.mtex_import_settings
        node_tree = bpy.context.active_object.active_material.node_tree  # Ottieni il node_tree del materiale attivo
        socket = [0, 5, 13, 28, 29, 30, 22, 31, 41]
        
        if node_tree:
            #for node in node_tree.nodes:
                #self.report({'INFO'}, node.name)
            y_loc = 400
            for i in range(9):
                texture_path = bpy.path.abspath(getattr(settings, f"mtex_texture_path_{i}"))
                self.report({'INFO'}, f"Texture {i + 1} Path = {texture_path}")
                if texture_path == "":
                    self.report({'INFO'}, f"Texture {i + 1} not specified. Skipping import.")  # Avviso se il percorso della texture non è specificato
                else:
                    should_connect = getattr(settings, f"mtex_connect")
                    rough_inverted = getattr(settings, f"mtex_rough_invert")
                    if os.path.isfile(texture_path):
                        if i == 0 or i == 4 or i == 6:
                            img_node = node_tree.nodes.new('OctaneRGBImage')    # Crea il nodo  Octane RGB Image nel node_tree del materiale attivo
                            img_node.label = os.path.basename(texture_path)
                            if i == 4:
                                img_node.inputs[2].default_value = 1
                        else:
                            img_node = node_tree.nodes.new('OctaneGreyscaleImage')  # Crea il nodo  Octane Greyscale Image nel node_tree del materiale attivo
                            img_node.label = os.path.basename(texture_path)
                            img_node.inputs[2].default_value = 1
                        if i == 2 and rough_inverted == True:
                            img_node.inputs[3].default_value = True
                        img_node.image = bpy.data.images.load(texture_path)
                        img_node.location.x = -600
                        
                        if should_connect:
                            NodeLinker.link_nodes(img_node.name, 'Texture out', 'Group', socket[i])
                            self.report({'INFO'}, f"Texture {i + 1} imported and connected!")
                        else:
                            self.report({'INFO'}, f"Texture {i + 1} imported!")
                        img_node.location.y = y_loc
                        y_loc = y_loc - 400
                    else:
                        self.report({'WARNING'}, f"Texture {i + 1} path not found!")
        else:
            self.report({'ERROR'}, "No active material or node tree found!")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MtexImportPanel)
    bpy.utils.register_class(MtexImportSettings)
    bpy.utils.register_class(ImportTexturesOperator)
    bpy.types.Scene.mtex_import_settings = bpy.props.PointerProperty(type=MtexImportSettings)

def unregister():
    bpy.utils.unregister_class(MtexImportPanel)
    bpy.utils.unregister_class(MtexImportSettings)
    bpy.utils.unregister_class(ImportTexturesOperator)
    del bpy.types.Scene.mtex_import_settings

if __name__ == "__main__":
    register()

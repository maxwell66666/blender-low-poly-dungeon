#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
低多边形地下城场景生成器
使用Blender Python API创建一个包含龙和宝藏的地下城场景
"""

import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix

# 清除默认场景
def clear_scene():
    """清除Blender中的默认对象"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 清除所有材质
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # 清除所有网格
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

# 创建基础材质
def create_material(name, color, metallic=0.0, roughness=0.8):
    """创建并返回一个基础材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # 清除默认节点
    for node in nodes:
        nodes.remove(node)
    
    # 创建主要着色器节点
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = color
    node_bsdf.inputs['Metallic'].default_value = metallic
    node_bsdf.inputs['Roughness'].default_value = roughness
    node_bsdf.location = (0, 0)
    
    # 创建输出节点
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (300, 0)
    
    # 连接节点
    links = mat.node_tree.links
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    
    return mat

# 创建地下城地板
def create_floor(size=10, material=None):
    """创建地下城地板"""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "DungeonFloor"
    
    # 添加一些随机高度变化以增加粗糙感
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(floor.data)
    
    # 细分地板以增加细节
    for _ in range(3):
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1)
    
    # 随机调整顶点高度
    for v in bm.verts:
        if v.co.x != size/2 and v.co.x != -size/2 and v.co.y != size/2 and v.co.y != -size/2:
            v.co.z += random.uniform(-0.05, 0.05)
    
    bmesh.update_edit_mesh(floor.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # 应用材质
    if material:
        if floor.data.materials:
            floor.data.materials[0] = material
        else:
            floor.data.materials.append(material)
    
    return floor

# 创建地下城墙壁
def create_walls(size=10, height=3, thickness=0.3, material=None):
    """创建地下城四面墙"""
    walls = []
    
    # 创建四面墙
    for i in range(4):
        if i == 0:  # 前墙（带门）
            # 左侧墙段
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(-size/4 - 0.5, -size/2, height/2)
            )
            wall_left = bpy.context.active_object
            wall_left.name = f"Wall_Front_Left"
            wall_left.scale = (size/4, thickness, height)
            
            # 右侧墙段
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(size/4 + 0.5, -size/2, height/2)
            )
            wall_right = bpy.context.active_object
            wall_right.name = f"Wall_Front_Right"
            wall_right.scale = (size/4, thickness, height)
            
            # 门上方墙段
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(0, -size/2, height - 0.5)
            )
            wall_top = bpy.context.active_object
            wall_top.name = f"Wall_Front_Top"
            wall_top.scale = (size/2, thickness, 1)
            
            walls.extend([wall_left, wall_right, wall_top])
            
        else:
            # 其他三面完整墙
            loc_x = 0
            loc_y = 0
            rot_z = 0
            
            if i == 1:  # 后墙
                loc_y = size/2
                rot_z = 0
            elif i == 2:  # 左墙
                loc_x = -size/2
                loc_y = 0
                rot_z = math.pi/2
            elif i == 3:  # 右墙
                loc_x = size/2
                loc_y = 0
                rot_z = math.pi/2
            
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(loc_x, loc_y, height/2)
            )
            wall = bpy.context.active_object
            wall.name = f"Wall_{i}"
            
            if i == 1:  # 后墙
                wall.scale = (size, thickness, height)
            else:  # 侧墙
                wall.scale = (size, thickness, height)
                wall.rotation_euler[2] = rot_z
            
            walls.append(wall)
    
    # 应用材质
    if material:
        for wall in walls:
            if wall.data.materials:
                wall.data.materials[0] = material
            else:
                wall.data.materials.append(material)
    
    return walls

# 创建柱子
def create_pillars(size=10, height=3, material=None):
    """在地下城角落创建柱子"""
    pillars = []
    pillar_radius = 0.3
    pillar_height = height
    
    # 创建四个角落的柱子
    for x in [-size/2 + pillar_radius, size/2 - pillar_radius]:
        for y in [-size/2 + pillar_radius, size/2 - pillar_radius]:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=pillar_radius,
                depth=pillar_height,
                vertices=8,  # 低多边形风格
                location=(x, y, pillar_height/2)
            )
            pillar = bpy.context.active_object
            pillar.name = f"Pillar_{x}_{y}"
            
            # 应用材质
            if material:
                if pillar.data.materials:
                    pillar.data.materials[0] = material
                else:
                    pillar.data.materials.append(material)
            
            pillars.append(pillar)
    
    return pillars

# 创建火把
def create_torch(location, material_handle=None, material_fire=None):
    """创建一个简单的火把"""
    # 创建火把手柄
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.05,
        depth=0.8,
        vertices=8,
        location=(location[0], location[1], location[2])
    )
    handle = bpy.context.active_object
    handle.name = f"TorchHandle_{location[0]}_{location[1]}"
    
    # 倾斜火把
    handle.rotation_euler[0] = math.radians(30)
    
    # 创建火焰（简化为一个锥体）
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.15,
        radius2=0,
        depth=0.3,
        vertices=8,
        location=(location[0], location[1] - 0.2, location[2] + 0.5)
    )
    fire = bpy.context.active_object
    fire.name = f"TorchFire_{location[0]}_{location[1]}"
    fire.rotation_euler[0] = math.radians(30)
    
    # 应用材质
    if material_handle:
        if handle.data.materials:
            handle.data.materials[0] = material_handle
        else:
            handle.data.materials.append(material_handle)
    
    if material_fire:
        if fire.data.materials:
            fire.data.materials[0] = material_fire
        else:
            fire.data.materials.append(material_fire)
    
    # 为火焰添加发光效果
    fire.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 5.0
    
    return handle, fire

# 创建低多边形龙
def create_dragon(location, scale=1.0, material=None):
    """创建一个低多边形风格的龙"""
    # 创建龙的身体（简化为拉长的立方体）
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0], location[1], location[2] + 0.5 * scale)
    )
    body = bpy.context.active_object
    body.name = "DragonBody"
    body.scale = (1.5 * scale, 3 * scale, 1 * scale)
    
    # 创建龙的头（简化为金字塔形状）
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.8 * scale,
        radius2=0.4 * scale,
        depth=1.5 * scale,
        vertices=4,
        location=(location[0], location[1] + 2 * scale, location[2] + 1 * scale)
    )
    head = bpy.context.active_object
    head.name = "DragonHead"
    head.rotation_euler[0] = math.radians(-30)
    
    # 创建龙的尾巴（弯曲的圆锥）
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.4 * scale,
        radius2=0.1 * scale,
        depth=3 * scale,
        vertices=8,
        location=(location[0], location[1] - 2 * scale, location[2] + 0.5 * scale)
    )
    tail = bpy.context.active_object
    tail.name = "DragonTail"
    tail.rotation_euler[0] = math.radians(20)
    tail.rotation_euler[2] = math.radians(20)
    
    # 创建龙的翅膀（简化为三角形）
    wings = []
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(location[0] + side * 1 * scale, location[1], location[2] + 1 * scale)
        )
        wing = bpy.context.active_object
        wing.name = f"DragonWing_{side}"
        wing.scale = (0.1 * scale, 1.5 * scale, 1 * scale)
        wing.rotation_euler[0] = math.radians(30)
        wing.rotation_euler[1] = math.radians(side * 30)
        wings.append(wing)
    
    # 创建龙的腿（简化为圆柱体）
    legs = []
    leg_positions = [
        (0.7, 1, 0),  # 右前腿
        (-0.7, 1, 0),  # 左前腿
        (0.7, -1, 0),  # 右后腿
        (-0.7, -1, 0)  # 左后腿
    ]
    
    for i, (x_offset, y_offset, z_offset) in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.2 * scale,
            depth=1 * scale,
            vertices=6,
            location=(
                location[0] + x_offset * scale,
                location[1] + y_offset * scale,
                location[2] + z_offset * scale
            )
        )
        leg = bpy.context.active_object
        leg.name = f"DragonLeg_{i}"
        legs.append(leg)
    
    # 应用材质
    dragon_parts = [body, head, tail] + wings + legs
    if material:
        for part in dragon_parts:
            if part.data.materials:
                part.data.materials[0] = material
            else:
                part.data.materials.append(material)
    
    # 将所有部分合并为一个对象
    bpy.ops.object.select_all(action='DESELECT')
    for part in dragon_parts:
        part.select_set(True)
    
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    
    dragon = bpy.context.active_object
    dragon.name = "Dragon"
    
    return dragon

# 创建金币和宝藏
def create_treasure(location, scale=1.0, coin_count=20, material_pot=None, material_gold=None):
    """创建一锅金币"""
    # 创建宝藏锅
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1 * scale,
        depth=1 * scale,
        vertices=12,
        location=(location[0], location[1], location[2] + 0.5 * scale)
    )
    pot = bpy.context.active_object
    pot.name = "TreasurePot"
    
    # 应用材质到锅
    if material_pot:
        if pot.data.materials:
            pot.data.materials[0] = material_pot
        else:
            pot.data.materials.append(material_pot)
    
    # 创建金币
    coins = []
    for _ in range(coin_count):
        # 随机位置，限制在锅内
        coin_radius = 0.15 * scale
        r = random.uniform(0, 0.8) * scale
        theta = random.uniform(0, 2 * math.pi)
        x = location[0] + r * math.cos(theta)
        y = location[1] + r * math.sin(theta)
        z = location[2] + 0.5 * scale + random.uniform(0, 0.5) * scale
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=coin_radius,
            depth=0.05 * scale,
            vertices=8,
            location=(x, y, z)
        )
        coin = bpy.context.active_object
        coin.name = f"Coin_{_}"
        
        # 随机旋转金币
        coin.rotation_euler = (
            random.uniform(0, math.pi/4),
            random.uniform(0, math.pi/4),
            random.uniform(0, 2 * math.pi)
        )
        
        # 应用材质到金币
        if material_gold:
            if coin.data.materials:
                coin.data.materials[0] = material_gold
            else:
                coin.data.materials.append(material_gold)
        
        coins.append(coin)
    
    return pot, coins

# 设置场景灯光
def setup_lighting():
    """设置场景灯光"""
    # 主光源（模拟火把的整体照明）
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 5))
    main_light = bpy.context.active_object
    main_light.name = "MainLight"
    main_light.data.energy = 500
    main_light.data.color = (1.0, 0.9, 0.7)  # 暖色调
    
    # 环境光（填充阴影）
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    fill_light = bpy.context.active_object
    fill_light.name = "FillLight"
    fill_light.data.energy = 2
    fill_light.data.color = (0.8, 0.8, 1.0)  # 冷色调
    
    return main_light, fill_light

# 设置相机
def setup_camera(location=(0, -12, 6), target_point=(0, 0, 1)):
    """设置场景相机"""
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    
    # 让相机指向目标点
    direction = Vector(target_point) - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    
    # 设置为活动相机
    bpy.context.scene.camera = camera
    
    return camera

# 主函数
def create_dungeon_scene():
    """创建完整的地下城场景"""
    # 清除默认场景
    clear_scene()
    
    # 创建材质
    floor_mat = create_material("FloorMaterial", (0.2, 0.2, 0.2, 1.0), metallic=0.0, roughness=0.9)
    wall_mat = create_material("WallMaterial", (0.3, 0.3, 0.35, 1.0), metallic=0.0, roughness=0.8)
    pillar_mat = create_material("PillarMaterial", (0.25, 0.25, 0.3, 1.0), metallic=0.1, roughness=0.7)
    torch_handle_mat = create_material("TorchHandleMaterial", (0.1, 0.05, 0.0, 1.0), metallic=0.0, roughness=0.9)
    torch_fire_mat = create_material("TorchFireMaterial", (1.0, 0.6, 0.0, 1.0), metallic=0.0, roughness=0.5)
    dragon_mat = create_material("DragonMaterial", (0.7, 0.0, 0.0, 1.0), metallic=0.2, roughness=0.8)
    pot_mat = create_material("PotMaterial", (0.1, 0.1, 0.1, 1.0), metallic=0.3, roughness=0.7)
    gold_mat = create_material("GoldMaterial", (1.0, 0.8, 0.0, 1.0), metallic=1.0, roughness=0.2)
    
    # 创建场景元素
    dungeon_size = 10
    wall_height = 4
    
    # 创建地板
    floor = create_floor(size=dungeon_size, material=floor_mat)
    
    # 创建墙壁
    walls = create_walls(size=dungeon_size, height=wall_height, material=wall_mat)
    
    # 创建柱子
    pillars = create_pillars(size=dungeon_size, height=wall_height, material=pillar_mat)
    
    # 创建火把
    torches = []
    torch_positions = [
        (-dungeon_size/2 + 1, -dungeon_size/2 + 1, wall_height/2),
        (dungeon_size/2 - 1, -dungeon_size/2 + 1, wall_height/2),
        (-dungeon_size/2 + 1, dungeon_size/2 - 1, wall_height/2),
        (dungeon_size/2 - 1, dungeon_size/2 - 1, wall_height/2)
    ]
    
    for pos in torch_positions:
        handle, fire = create_torch(pos, material_handle=torch_handle_mat, material_fire=torch_fire_mat)
        torches.append((handle, fire))
    
    # 创建龙
    dragon = create_dragon(
        location=(2, 0, 0),
        scale=0.8,
        material=dragon_mat
    )
    
    # 创建宝藏
    pot, coins = create_treasure(
        location=(-2, 0, 0),
        scale=1.0,
        coin_count=30,
        material_pot=pot_mat,
        material_gold=gold_mat
    )
    
    # 设置灯光
    main_light, fill_light = setup_lighting()
    
    # 设置相机
    camera = setup_camera()
    
    # 设置渲染参数
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    
    # 设置输出路径
    bpy.context.scene.render.filepath = "//dungeon_scene_render.png"
    
    print("低多边形地下城场景创建完成！")

# 执行主函数
if __name__ == "__main__":
    create_dungeon_scene()
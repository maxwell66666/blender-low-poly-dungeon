# 低多边形地下城场景

这个项目使用Blender创建一个低多边形风格的地下城场景，场景中包含一条龙守卫着一锅金子。

## 项目描述

本项目旨在使用Blender创建一个低多边形风格的地下城场景，场景中包含一条龙守卫着一锅金子。整个场景采用低多边形（Low Poly）艺术风格，以简约而富有表现力的方式呈现地下城的神秘氛围。

## 主要元素

1. **地下城环境** - 石墙、地板、柱子和火把等元素
2. **龙** - 低多边形风格的龙，姿态为守卫状态
3. **宝藏** - 金币堆和宝藏锅/箱子
4. **氛围** - 通过灯光和阴影营造神秘的地下城氛围

## 文件结构

- `create_dungeon_scene.py` - 主要的Python脚本，用于生成场景
- `run_scene_generator.py` - 启动脚本，用于查找Blender并执行场景生成脚本
- `run_scene_generator.bat` - Windows批处理文件
- `run_scene_generator.sh` - Linux/macOS shell脚本

## 使用方法

### 前提条件

- 安装Blender（推荐版本2.93或更高）
- 基本了解Blender界面

### 运行脚本

有两种方法可以运行此脚本：

#### 方法1：通过Blender界面

1. 打开Blender
2. 切换到"Scripting"工作区
3. 点击"New"创建一个新的脚本
4. 将`create_dungeon_scene.py`的内容复制粘贴到脚本编辑器中
5. 点击"Run Script"按钮执行脚本

#### 方法2：通过命令行

```bash
blender --background --python create_dungeon_scene.py
```

或者使用提供的启动脚本：

- Windows: 双击运行 `run_scene_generator.bat`
- Linux/macOS: 在终端中执行 `./run_scene_generator.sh`

### 渲染场景

脚本执行后，场景将自动设置好。如果您想渲染场景：

1. 在Blender界面中，切换到"Rendering"工作区
2. 点击"Render"按钮或按F12键
3. 渲染完成后，可以通过"Image > Save As..."保存渲染结果

默认情况下，渲染结果将保存为当前Blender文件所在目录下的`dungeon_scene_render.png`。

## 自定义场景

您可以通过修改脚本中的参数来自定义场景：

- 修改`dungeon_size`变量可以改变地下城的大小
- 修改`wall_height`变量可以改变墙壁的高度
- 修改龙和宝藏的位置和比例
- 调整材质的颜色和属性
- 调整灯光的位置和强度

## 场景预览

运行脚本后，将生成一个类似下面描述的低多边形地下城场景：

```
+-------------------+
|       |   |       |
|  P    |   |    P  |
|       |   |       |
|                   |
|                   |
|   G       D       |
|                   |
|                   |
|       |   |       |
|  P    |   |    P  |
|       |   |       |
+-------------------+

P: 柱子
D: 龙
G: 金币/宝藏
|: 火把
```

## 注意事项

- 脚本运行时会清除当前Blender场景中的所有对象
- 渲染可能需要一些时间，特别是在设置了高采样率的情况下
- 低多边形风格的模型是简化的，如需更详细的模型，需要手动调整或使用其他建模技术
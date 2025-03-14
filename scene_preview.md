# 场景预览

## 预期效果

运行脚本后，将生成一个类似下面描述的低多边形地下城场景：

- 一个方形的地下城房间，带有石墙、地板和柱子
- 房间中央有一条红色的低多边形龙，守卫着一锅金子
- 墙壁上有火把，提供温暖的光线
- 场景采用低多边形风格，简约而富有表现力

## 场景布局

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

## 渲染设置

- 渲染引擎：Cycles
- 采样数：128
- 分辨率：1920x1080

## 自定义提示

如果您想调整场景，可以修改以下参数：

1. 在`create_dungeon_scene.py`中找到`create_dungeon_scene()`函数
2. 修改以下变量：
   - `dungeon_size = 10` - 调整地下城大小
   - `wall_height = 4` - 调整墙壁高度
   - 龙的位置：`location=(2, 0, 0)`
   - 宝藏的位置：`location=(-2, 0, 0)`

3. 调整材质颜色：
   - 龙的颜色：`dragon_mat = create_material("DragonMaterial", (0.7, 0.0, 0.0, 1.0), metallic=0.2, roughness=0.8)`
   - 金币的颜色：`gold_mat = create_material("GoldMaterial", (1.0, 0.8, 0.0, 1.0), metallic=1.0, roughness=0.2)`
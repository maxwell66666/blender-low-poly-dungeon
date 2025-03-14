#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
低多边形地下城场景生成器启动脚本
此脚本用于启动Blender并执行场景生成脚本
"""

import os
import subprocess
import sys
import platform

def find_blender():
    """尝试找到Blender可执行文件的路径"""
    # 常见的Blender安装路径
    common_paths = {
        'win32': [
            r'C:\Program Files\Blender Foundation\Blender 3.6\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 3.5\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 3.4\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 3.3\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 3.2\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 3.1\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 3.0\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender 2.93\blender.exe',
            r'C:\Program Files\Blender Foundation\Blender\blender.exe',
        ],
        'darwin': [
            '/Applications/Blender.app/Contents/MacOS/Blender',
            '/Applications/Blender/Blender.app/Contents/MacOS/Blender',
        ],
        'linux': [
            '/usr/bin/blender',
            '/usr/local/bin/blender',
            '/snap/bin/blender',
        ]
    }
    
    # 获取当前操作系统
    system = platform.system().lower()
    if system == 'windows':
        system = 'win32'
    elif system == 'darwin':
        system = 'darwin'
    else:
        system = 'linux'
    
    # 检查常见路径
    for path in common_paths.get(system, []):
        if os.path.exists(path):
            return path
    
    # 如果在常见路径中找不到，尝试使用which/where命令
    try:
        if system == 'win32':
            result = subprocess.run(['where', 'blender'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split('\n')[0]
        else:
            result = subprocess.run(['which', 'blender'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
    except Exception:
        pass
    
    return None

def main():
    """主函数"""
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 场景生成脚本路径
    scene_script = os.path.join(script_dir, 'create_dungeon_scene.py')
    
    # 检查场景生成脚本是否存在
    if not os.path.exists(scene_script):
        print(f"错误：找不到场景生成脚本: {scene_script}")
        return 1
    
    # 查找Blender可执行文件
    blender_path = find_blender()
    if not blender_path:
        print("错误：无法找到Blender可执行文件。请确保已安装Blender，或手动指定Blender路径。")
        print("您可以通过以下方式手动运行脚本：")
        print(f"blender --background --python {scene_script}")
        return 1
    
    print(f"找到Blender: {blender_path}")
    print(f"正在生成低多边形地下城场景...")
    
    # 运行Blender并执行场景生成脚本
    try:
        # 使用subprocess运行Blender
        result = subprocess.run(
            [blender_path, '--background', '--python', scene_script],
            capture_output=True,
            text=True
        )
        
        # 输出Blender的输出
        print(result.stdout)
        
        if result.returncode != 0:
            print("错误：Blender执行失败")
            print(result.stderr)
            return 1
        
        print("场景生成完成！")
        print("渲染结果保存在Blender文件所在目录下的'dungeon_scene_render.png'")
        
        # 询问是否打开Blender查看场景
        response = input("是否打开Blender查看场景？(y/n): ")
        if response.lower() in ['y', 'yes']:
            # 打开Blender并加载生成的场景
            subprocess.Popen([blender_path])
        
    except Exception as e:
        print(f"错误：执行Blender时出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
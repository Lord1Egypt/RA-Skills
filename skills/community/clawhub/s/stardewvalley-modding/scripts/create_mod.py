#!/usr/bin/env python3
"""
自动判断并创建星露谷 Mod 项目结构
"""
import os
import sys
import json
import shutil

def determine_mod_type(user_request):
    """根据用户需求自动判断 Mod 类型"""
    request = user_request.lower()
    
    # SMAPI 关键词
    smapi_keywords = ["孩子", "hook", "修改机制", "代码", "dll", "编译", 
                     "修改游戏逻辑", "游戏机制", "孩子功能", "生育"]
    
    # CP 关键词
    cp_keywords = ["对话", "立绘", "npc", "剧情", "事件", "地图", 
                   "json", "添加角色", "添加内容", "对话", "结婚事件"]
    
    for keyword in smapi_keywords:
        if keyword in request:
            return "SMAPI"
    
    for keyword in cp_keywords:
        if keyword in request:
            return "CP"
    
    return "CP"  # 默认 CP

def create_cp_mod(mod_name, author, output_dir):
    """创建 Content Patcher Mod 结构"""
    mod_dir = os.path.join(output_dir, mod_name)
    
    # 创建目录
    os.makedirs(os.path.join(mod_dir, "assets", "Dialogue"), exist_ok=True)
    os.makedirs(os.path.join(mod_dir, "assets", "Image"), exist_ok=True)
    os.makedirs(os.path.join(mod_dir, "assets", "i18n"), exist_ok=True)
    
    # manifest.json
    manifest = {
        "Name": mod_name,
        "Author": author,
        "Version": "1.0.0",
        "Description": f"{mod_name} Mod",
        "UniqueID": f"{author}.{mod_name}",
        "ContentPackFor": {
            "UniqueID": "Pathoschild.ContentPatcher",
            "MinimumVersion": "2.0"
        }
    }
    
    with open(os.path.join(mod_dir, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    
    # content.json
    content = {
        "Format": "2.3.0",
        "Changes": []
    }
    
    with open(os.path.join(mod_dir, "content.json"), 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
    
    # i18n
    i18n = {
        "mod.name": mod_name
    }
    
    with open(os.path.join(mod_dir, "assets", "i18n", "default.json"), 'w', encoding='utf-8') as f:
        json.dump(i18n, f, indent=4, ensure_ascii=False)
    
    return mod_dir

def create_smapi_mod(mod_name, author, output_dir, game_dll_path):
    """创建 SMAPI Mod 结构"""
    mod_dir = os.path.join(output_dir, mod_name)
    os.makedirs(mod_dir, exist_ok=True)
    
    # .csproj
    csproj = f'''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AssemblyName>{mod_name}</AssemblyName>
    <RootNamespace>{author}.{mod_name}</RootNamespace>
    <Version>1.0.0</Version>
  </PropertyGroup>

  <ItemGroup>
    <Reference Include="StardewValley">
      <HintPath>{game_dll_path}</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="StardewModdingAPI">
      <HintPath>{game_dll_path.replace('Stardew Valley.dll', 'smapi-internal/StardewModdingAPI.dll')}</HintPath>
      <Private>False</Private>
    </Reference>
  </ItemGroup>

</Project>'''
    
    with open(os.path.join(mod_dir, f"{mod_name}.csproj"), 'w') as f:
        f.write(csproj)
    
    # ModEntry.cs
    mod_entry = f'''using StardewModdingAPI;
using StardewValley;

namespace {author}.{mod_name}
{{
    public class ModEntry : Mod
    {{
        public override void Entry(IModHelper helper)
        {{
            helper.Events.GameLoop.DayStarted += OnDayStarted;
            this.Monitor.Log("{mod_name} 已加载!", LogLevel.Info);
        }}

        private void OnDayStarted(object sender, DayStartedEventArgs e)
        {{
            // 在这里编写 Mod 逻辑
        }}
    }}
}}'''
    
    with open(os.path.join(mod_dir, "ModEntry.cs"), 'w') as f:
        f.write(mod_entry)
    
    # manifest.json
    manifest = {
        "Name": mod_name,
        "Author": author,
        "Version": "1.0.0",
        "Description": f"{mod_name} Mod",
        "UniqueID": f"{author}.{mod_name}"
    }
    
    with open(os.path.join(mod_dir, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    
    return mod_dir

def main():
    if len(sys.argv) < 3:
        print("用法: create_mod.py <mod名> <作者> [需求描述]")
        print("示例: create_mod.py MyMod Author \"我想添加一个 NPC 和对话\"")
        sys.exit(1)
    
    mod_name = sys.argv[1]
    author = sys.argv[2]
    user_request = sys.argv[3] if len(sys.argv) > 3 else ""
    
    # 自动判断类型
    mod_type = determine_mod_type(user_request)
    
    print(f"📋 分析需求: {user_request}")
    print(f"🎯 判断类型: {mod_type} Mod")
    
    output_dir = os.path.expanduser("~/Desktop")
    
    if mod_type == "CP":
        mod_dir = create_cp_mod(mod_name, author, output_dir)
        print(f"✅ 已创建 CP Mod: {mod_dir}")
    else:
        # 尝试找游戏 DLL
        game_paths = [
            "/Users/geyize/Library/Application Support/Steam/steamapps/common/Stardew Valley/Contents/MacOS/Stardew Valley.dll"
        ]
        
        game_dll = None
        for p in game_paths:
            if os.path.exists(p):
                game_dll = p
                break
        
        if not game_dll:
            print("❌ 未找到星露谷游戏 DLL，无法创建 SMAPI Mod")
            print("请确保游戏已安装，然后重试。")
            sys.exit(1)
        
        mod_dir = create_smapi_mod(mod_name, author, output_dir, game_dll)
        print(f"✅ 已创建 SMAPI Mod: {mod_dir}")
        print(f"📝 下一步: cd {mod_dir} && dotnet build")

if __name__ == "__main__":
    main()

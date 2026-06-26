import requests
import argparse
import os
import zipfile
import io
import sys


class QianfanClawhubClient(object):
    """千帆 clawhub 客户端"""

    def __init__(self, endpoint=None, api_key=None, workdir=None):
        """
        初始化客户端

        Args:
            endpoint: server address
            workdir: 自定义工作目录，默认为 ~/.qianfan/workspace
        """
        self.endpoint = endpoint or 'https://appbuilder.baidu.com'
        self.api_key = api_key
        if workdir:
            self.skills_dir = os.path.join(workdir, 'skills')
        else:
            try:
                response = requests.get("http://localhost:4096/path", timeout=5)
                json_data = response.json()
                self.skills_dir = os.path.join(json_data['directory'], 'skills')
            except Exception as e:
                self.skills_dir = os.path.join(os.path.expanduser('~'), '.qianfan', 'workspace', 'skills')


    def get_skills_dir(self):
        return self.skills_dir

    def search_skills(self, prefix: str, limit: int = None):
        """根据前缀匹配第一层目录（匿名访问）

        Args:
            prefix: 搜索前缀
            max_keys: API 请求的最大数量
            limit: 限制返回结果数量，None 表示不限制
        """
        try:
            if limit is None:
                limit = 20
            params = {'query': prefix, 'limit': limit}
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}
            response = requests.post(f"{self.endpoint}/v2/skills/search", json=params, headers=headers)
            skills = []
            if response.status_code == 200:
                skills = response.json().get('data', {}).get('skills', [])
            return skills
        except Exception as e:
            print(f"Error listing objects: {e}")
            return []

    def install_skill(self, slug_name: str, force: bool = False):
        """安装 skill
        
        Args:
            slug_name: skill 的 slug 名称
            force: 是否强制覆盖已安装的 skill
        """
        print(f"install skill {slug_name}")
        os.makedirs(self.skills_dir, exist_ok=True)

        skill_dir = os.path.join(self.skills_dir, slug_name)
        skill_exist = os.path.exists(skill_dir)
        if skill_exist and not force:
            print(f"skill {slug_name} already exists, use --force to overwrite")
            return

        # 调用 API 下载 zip 包
        try:
            url = f"{self.endpoint}/v2/skills/download"
            params = {"slugName": slug_name}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(url, params=params, headers=headers, timeout=60)
            if response.status_code != 200:
                print(f"download skill {slug_name} fail: HTTP {response.status_code}")
                return
            
            # 解压 zip 包
            with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                # 获取 zip 内的根目录名
                namelist = zf.namelist()
                if not namelist:
                    print("zip 包为空")
                    return
                
                # 找到顶层的技能目录
                skill_prefix = None
                for name in namelist:
                    if name.endswith('/') and name != namelist[0]:
                        # 找到第一个顶层目录
                        skill_prefix = name
                        break
                
                # 解压到目标目录
                if skill_prefix:
                    # 如果有顶层目录，只解压该目录下的内容
                    for name in namelist:
                        if name.startswith(skill_prefix):
                            target_name = name[len(skill_prefix):]
                            if target_name:
                                target_path = os.path.join(skill_dir, target_name)
                                if name.endswith('/'):
                                    os.makedirs(target_path, exist_ok=True)
                                else:
                                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                    with zf.open(name) as src, open(target_path, 'wb') as dst:
                                        dst.write(src.read())
                else:
                    # 没有顶层目录，直接解压所有文件
                    for name in namelist:
                        if name:
                            target_path = os.path.join(skill_dir, name)
                            if name.endswith('/'):
                                os.makedirs(target_path, exist_ok=True)
                            else:
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                with zf.open(name) as src, open(target_path, 'wb') as dst:
                                    dst.write(src.read())
            
            print(f"skill {slug_name} install complete -> {skill_dir}")
            
        except requests.exceptions.RequestException as e:
            print(f"download skill {slug_name} fail: {e}")
        except zipfile.BadZipFile as e:
            print(f"downloaded zip file is bad - {e}")
        except Exception as e:
            print(f"install skill {slug_name} fail: {e}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QianFan ClawHub 工具')
    parser.add_argument('--workdir', type=str, default=None, help='指定自定义工作目录')
    parser.add_argument('--endpoint', type=str, default=None, help='指定 API 服务器地址')
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # search 子命令
    search_parser = subparsers.add_parser('search', help='搜索 skills')
    search_parser.add_argument('keyword', nargs='?', default='', help='搜索关键词')
    search_parser.add_argument('--limit', type=int, default=None, help='限制输出结果数量')

    # install 子命令
    install_parser = subparsers.add_parser('install', help='安装 skill')
    install_parser.add_argument('slug', help='skill 的 slug 名称')
    install_parser.add_argument('--force', action='store_true', help='强制覆盖已安装的 skill')

    args = parser.parse_args()

    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        print("Error: BAIDU_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    client = QianfanClawhubClient(endpoint=args.endpoint, api_key=api_key, workdir=args.workdir)

    if args.command == 'search':
        skills = client.search_skills(args.keyword, limit=args.limit)
        print("skills search results:")
        for skill in skills:
            print(f"{skill['slug']}  {skill['name']}")
    elif args.command == 'install':
        client.install_skill(args.slug, force=args.force)
    else:
        parser.print_help()

"""Single flat area catalog. Only confirmed selections produce query parameters."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

REFERENCES = Path(__file__).resolve().parents[1] / 'references'
MUNICIPALITIES = {2, 24, 26, 31}
SPECIAL_ROOTS = {3557, 3558, 3559}
LIMITED_DISTRICT_ROOTS = SPECIAL_ROOTS
NATIONAL = {'全国', '全国范围', '不限地区', '取消地区限制'}
REGION_GROUPS = {'华东': ['上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省'],
 '华东区': ['上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省'],
 '华北': ['北京市', '天津市', '河北省', '山西省', '内蒙古自治区'],
 '华北区': ['北京市', '天津市', '河北省', '山西省', '内蒙古自治区'],
 '华南': ['广东省', '广西壮族自治区', '海南省'],
 '华南区': ['广东省', '广西壮族自治区', '海南省'],
 '华中': ['河南省', '湖北省', '湖南省'],
 '华中区': ['河南省', '湖北省', '湖南省'],
 '东北': ['辽宁省', '吉林省', '黑龙江省'],
 '东北区': ['辽宁省', '吉林省', '黑龙江省'],
 '西南': ['重庆市', '四川省', '贵州省', '云南省', '西藏自治区'],
 '西南区': ['重庆市', '四川省', '贵州省', '云南省', '西藏自治区'],
 '西北': ['陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区'],
 '西北区': ['陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区'],
 '长三角': ['上海市', '江苏省', '浙江省', '安徽省'],
 '京津冀': ['北京市', '天津市', '河北省'],
 '江浙沪': ['江苏省', '浙江省', '上海市'],
 '江浙沪皖': ['江苏省', '浙江省', '上海市', '安徽省'],
 '珠三角': ['广州市', '深圳市', '珠海市', '佛山市', '惠州市', '东莞市', '中山市', '江门市', '肇庆市'],
 '成渝': ['重庆市', '成都市'],
 '大湾区内地九市': ['广州市', '深圳市', '珠海市', '佛山市', '惠州市', '东莞市', '中山市', '江门市', '肇庆市']}
SCOPE_CHOICES = {'大湾区': {'message': '“大湾区”目前有明确的内地九市范围。请确认查询内地九市，还是需要包含香港、澳门的完整范围；后者的统一查询映射尚未核实。',
         'choices': ['大湾区内地九市']},
 '粤港澳大湾区': {'message': '“粤港澳大湾区”的内地九市可直接查询；包含香港、澳门的完整组合映射尚未核实。请确认是否只查内地九市。',
            'choices': ['大湾区内地九市']}}



class AreaError(ValueError):
    pass


def clean_label(text: str) -> str:
    return re.sub(r'（(?:省级|市级|上层|同范围下层|同名下级，查询用上级|同名下级，含义待确认)）', '', text)


def compact(text: str) -> str:
    return re.sub(r'[-/\s的]+', '', text.strip())


def short_name(name: str) -> str:
    for suffix in ('特别行政区', '维吾尔自治区', '壮族自治区', '回族自治区',
                   '自治区', '自治州', '自治县', '新区', '地区', '省', '市', '区', '县'):
        if name.endswith(suffix) and len(name)-len(suffix) >= 2:
            return name[:-len(suffix)]
    return name


class AreaCatalog:
    def __init__(self, records: list[dict]):
        self.by_id = {}
        for r in records:
            i, parent = r.get('areaid'), r.get('parentid')
            if type(i) is not int or i <= 0 or i in self.by_id:
                raise AreaError('地区目录编号无效或重复。')
            if type(parent) is not int or parent < 0 or not isinstance(r.get('name'), str) or not r['name'].strip():
                raise AreaError('地区目录节点格式无效。')
            self.by_id[i] = dict(r)
        self.chains = {}
        for i in self.by_id:
            chain, current = [], i
            while current:
                if current in chain or current not in self.by_id:
                    raise AreaError('地区目录存在循环或缺少父级。')
                chain.append(current); current = self.by_id[current]['parentid']
            self.chains[i] = chain[::-1]
        self.labels = {i:r['name'].split('/')[-1] for i,r in self.by_id.items()}
        for i,r in self.by_id.items():
            expected = '/'.join(self.labels[n] for n in self.chains[i])
            if r['name'] != expected:
                raise AreaError('地区名称路径与原始父级关系不一致。')
        self.fallbacks = {i for i,label in self.labels.items() if label.startswith('其他（')}
        self.upper_choices = self.fallbacks | {i for i,label in self.labels.items()
                                               if label.endswith('（同名下级，查询用上级）')}
        self.aliases = {}
        self.name_index = {}
        self.path_index = {}
        for i,label in self.labels.items():
            self.path_index.setdefault(compact(self.by_id[i]['name']), set()).add(i)
            if i in self.fallbacks:
                # Keep every node; normal city expressions select its upper scope.
                label = self.labels[self.by_id[i]['parentid']]
            formal = clean_label(label)
            aliases = {formal, short_name(formal)}
            self.aliases[i] = aliases
            for alias in aliases:
                self.name_index.setdefault(compact(alias), set()).add(i)
        self.groups = {}
        for name,members in REGION_GROUPS.items():
            ids = []
            for member in members:
                choices = self.match(member)
                if len(choices) != 1:
                    raise AreaError(f'区域组合成员不能唯一定位：{member}。')
                ids.extend(choices[0])
            self.groups[name] = list(dict.fromkeys(ids))

    def query_ids(self, i: int) -> tuple[int, ...]:
        if i in {2251, 3500}:
            return (2251, 3500)
        while i in self.upper_choices:
            i = self.by_id[i]['parentid']
        parent = self.by_id[i]['parentid']
        if parent in MUNICIPALITIES | SPECIAL_ROOTS:
            i = parent
        return (i,)

    def _prefix_matches(self, prefix: str, ancestors: list[int]) -> bool:
        if not prefix:
            return True
        for pos in range(len(ancestors)-1, -1, -1):
            for alias in self.aliases[ancestors[pos]]:
                if prefix.endswith(alias) and self._prefix_matches(prefix[:-len(alias)], ancestors[:pos]):
                    return True
        return False

    def match(self, name: str, parent_ids: set[int] | None = None) -> list[tuple[int, ...]]:
        key = compact(clean_label(name))
        # Parentheses may contain the user's district restriction. Join the
        # components for path matching without dropping any enclosed text.
        key = re.sub(r'[（）()]', '', key)
        if key.endswith('全市'):
            city_key = key[:-2]
            choices = self.match(city_key, parent_ids)
            if choices and all(clean_label(self.labels[ids[0]]).endswith('市') for ids in choices):
                return choices
        found = set()
        # Exact source paths may identify technical nodes. Their query selection
        # still follows the confirmed upper-scope rule.
        exact_paths = self.path_index.get(compact(name), set())
        matches = set(exact_paths) | set(self.name_index.get(key, set()))
        if not exact_paths and key not in self.name_index:
            for alias, ids in self.name_index.items():
                if key.endswith(alias) and len(key) > len(alias):
                    prefix = key[:-len(alias)]
                    for i in ids:
                        if self._prefix_matches(prefix, self.chains[i][:-1]):
                            matches.add(i)
        for i in matches:
            if parent_ids is not None and not any(p in self.chains[i] for p in parent_ids):
                continue
            if i == 2703:
                continue
            found.add(self.query_ids(i))
        return sorted(found)

    def display_path(self, i: int) -> str:
        parts = []
        for n in self.chains[i]:
            label = self.labels[n] if n in self.fallbacks else clean_label(self.labels[n])
            if not parts or parts[-1] != label:
                parts.append(label)
        return '-'.join(parts)

    def candidate(self, i: int) -> dict:
        return {'name': self.by_id[i]['name'], 'path': self.display_path(i)}

    def brief(self, ids: tuple[int, ...] | list[int]) -> dict:
        return {'name': self.by_id[ids[0]]['name']}

    def city_parent(self, i: int) -> int | None:
        if self.restricted_root(i) is not None or i in self.upper_choices or len(self.chains[i]) < 3:
            return None
        parent = self.by_id[i]['parentid']
        return self.query_ids(parent)[0] if parent else None

    def restricted_root(self, i: int) -> int | None:
        chain = self.chains[i]
        if chain[0] in LIMITED_DISTRICT_ROOTS and len(chain) >= 3 and i not in self.upper_choices:
            return chain[0]
        return None

    def scope_limit_message(self, ids: list[int]) -> str | None:
        restricted = [i for i in ids if self.restricted_root(i) is not None]
        if not restricted:
            return None
        requested = '、'.join(dict.fromkeys(self.display_path(i) for i in restricted))
        whole = '、'.join(dict.fromkeys(clean_label(self.labels[self.restricted_root(i)]) for i in restricted))
        return (f'目前暂不支持区县精确筛选：{requested}。传区县编号也会返回{whole}整体范围的数据。'
                f'是否接受改查{whole}整体范围？确认后请使用整体范围，其他条件保持不变。')

    def unmapped_scope_message(self, name: str, parent_ids: set[int] | None) -> str:
        key = compact(re.sub(r'[（）()]', '', clean_label(name)))
        roots = [root for root in LIMITED_DISTRICT_ROOTS
                 if (parent_ids and root in parent_ids) or
                 any(key.startswith(alias) and key != alias for alias in self.aliases[root])]
        if not roots:
            return ''
        scopes = '、'.join(clean_label(self.labels[root]) for root in sorted(roots))
        return (f' {scopes}暂不支持区县精确筛选；不能自动丢弃“{name}”的限定改查整体范围。'
                f'若愿意改查{scopes}整体范围，请明确确认。')

    def validate_ids(self, value) -> list[int]:
        values = value if isinstance(value, list) else [value]
        result = []
        for item in values:
            if isinstance(item, str) and re.fullmatch(r'[0-9]+', item):
                item = int(item)
            if type(item) is not int or item <= 0 or item not in self.by_id:
                raise AreaError('地区编号必须是目录内的正整数，请用 area 解析地区后重试。')
            if item not in result:
                result.append(item)
        return result

    def _unresolved(self, status, message, choices=(), limit=5):
        p = {'ok': True, 'resolution_status': status, 'user_message': message}
        if choices:
            p['candidates'] = [self.brief(ids) for ids in choices[:limit]]
            if len(choices) > limit:
                p.update(total_count=len(choices), truncated=True)
        return p

    def _resolved(self, ids):
        message = self.scope_limit_message(ids)
        if message:
            return self._unresolved('unsupported', message)
        areas = []
        for i in ids:
            c = self.brief([i])
            if c not in areas:
                areas.append(c)
        return {'ok': True, 'resolution_status': 'resolved', 'areas': areas,
                'effective_query': {'areaIds': ids}}

    def resolve(self, name: str, limit: int = 5, parent: str | None = None) -> dict:
        if type(limit) is not int or limit < 1:
            raise AreaError('地区候选展示数量必须是正整数。')
        name = name.strip()
        if not name:
            return self._unresolved('unmapped', '请提供地区名称。')
        if re.search(r'排除|除外|以外|附近|周边|公里|不要|不含', name):
            return self._unresolved('unsupported', '该排除或距离范围不能直接用地区参数表达，请明确可查询的地区。')
        if name in SCOPE_CHOICES:
            return self._unresolved('ambiguous', SCOPE_CHOICES[name]['message'])
        parent_ids = None
        if parent:
            choices = self.match(parent)
            if len(choices) != 1:
                return self._unresolved('ambiguous' if choices else 'unmapped',
                                        f'请明确上级地区“{parent}”。', choices, limit)
            parent_ids = set(choices[0])
        if name in NATIONAL:
            if parent:
                return self._unresolved('ambiguous', '全国与限定上级地区冲突，请确认查询范围。')
            return {'ok': True, 'resolution_status': 'resolved', 'areas': [{'name': '全国'}],
                    'effective_query': {'areaIds': []}}
        if name in self.groups:
            ids = self.groups[name]
            if parent_ids and not all(any(p in self.chains[i] for p in parent_ids) for i in ids):
                return self._unresolved('unsupported', '区域组合与上级范围冲突，不能截取部分成员查询。')
            return self._resolved(ids)
        choices = self.match(name, parent_ids)
        if len(choices) == 1:
            return self._resolved(list(choices[0]))
        if choices:
            return self._unresolved('ambiguous', '请确认具体地区。', choices, limit)
        parts = [p.strip() for p in re.split(r'[、,，;；]', name) if p.strip()]
        if len(parts) == 1:
            for sep in re.finditer(r'以及|和|与', name):
                left, right = name[:sep.start()].strip(), name[sep.end():].strip()
                if right and (self.match(left,parent_ids) or left in self.groups or left in NATIONAL):
                    parts=[left,right];break
        if len(parts)>1:
            pieces = [self.resolve(p, len(self.by_id), parent) for p in parts]
            failures = [p for p in pieces if p['resolution_status']!='resolved']
            if failures:
                status = ('unsupported' if any(p['resolution_status']=='unsupported' for p in failures) else
                          'ambiguous' if any(p['resolution_status']=='ambiguous' for p in failures) else 'unmapped')
                p = self._unresolved(status, '多地区请求尚未完整确定，请明确未识别或有歧义的部分。')
                reasons = list(dict.fromkeys(f['user_message'] for f in failures
                                            if f['resolution_status'] != 'ambiguous'))
                if reasons:
                    p['user_message'] += ' ' + ' '.join(reasons)
                candidates = []
                for failure in failures:
                    for c in failure.get('candidates',[]):
                        if c not in candidates:candidates.append(c)
                if candidates:
                    p['candidates'] = candidates[:limit]
                    if len(candidates)>limit:p.update(total_count=len(candidates),truncated=True)
                p['unresolved_parts']=[part for part,piece in zip(parts,pieces) if piece['resolution_status']!='resolved']
                return p
            if any(p['effective_query']['areaIds']==[] for p in pieces):
                return self._unresolved('ambiguous', '请求同时包含全国和具体地区，请确认是否取消地区限制。')
            ids=list(dict.fromkeys(i for p in pieces for i in p['effective_query']['areaIds']))
            return self._resolved(ids)
        return self._unresolved('unmapped', f'未能定位“{name}”'+(f'在“{parent}”内的范围' if parent else '')+
                                '，请补充明确名称或上级地区。'+self.unmapped_scope_message(name, parent_ids))


@lru_cache(maxsize=1)
def catalog() -> AreaCatalog:
    try:
        return AreaCatalog(json.loads((REFERENCES/'area.json').read_text()))
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise AreaError('地区目录无法读取或结构无效。') from exc


def resolve(name: str, limit: int = 5, parent: str | None = None) -> dict:
    return catalog().resolve(name, limit, parent)


def validate_ids(value) -> list[int]:
    return catalog().validate_ids(value)

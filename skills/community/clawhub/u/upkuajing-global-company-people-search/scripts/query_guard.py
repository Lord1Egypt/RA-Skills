"""收费查询执行前的本地安全检查。此模块不发起网络请求。"""


def _has_value(params: dict, field: str) -> bool:
    value = params.get(field)
    if isinstance(value, (list, tuple, set, dict, str)):
        return bool(value)
    return value is not None


def require_user_confirmation(user_confirmed: bool) -> None:
    """要求调用方确认用户已在独立消息中批准本次收费操作。"""
    if not user_confirmed:
        raise ValueError(
            "未确认收费操作。请先完成查询澄清，向用户展示自然语言查询确认单、"
            "预计调用次数和费用，并在用户独立消息中明确确认后添加 --user_confirmed。"
        )


def enforce_exact_matching(params: dict) -> dict:
    """所有列表查询只允许服务端完整 query 精准匹配。"""
    exact_value = params.get('isExact')
    if 'isExact' in params and exact_value is not True:
        raise ValueError(
            "本技能不支持模糊匹配；请使用简短、完整的业务查询短语并设置 isExact=true。"
        )
    normalized = dict(params)
    normalized['isExact'] = True
    return normalized


def normalize_human_search_params(params: dict) -> dict:
    """把人物岗位业务词归一到服务端接受的职位名称锚点。"""
    normalized = dict(params)
    title_names = normalized.get('titleNames') or []
    if not isinstance(title_names, list):
        title_names = [title_names]

    if not title_names:
        promoted = []
        for field in ('titleRoles', 'titleSubRoles'):
            values = normalized.pop(field, []) or []
            if not isinstance(values, list):
                values = [values]
            promoted.extend(value for value in values if value not in (None, ''))
        if promoted:
            normalized['titleNames'] = list(dict.fromkeys(promoted))
    return normalized


def validate_company_search_params(params: dict) -> None:
    """拒绝没有任何正向搜索锚点的公司列表查询。"""
    anchor_fields = (
        'pids',
        'companyUrls',
        'companyNames',
        'products',
        'keywords',
    )
    if not any(_has_value(params, field) for field in anchor_fields):
        raise ValueError(
            "公司查询缺少可靠搜索锚点。至少需要公司ID/链接/名称，或明确的产品、关键词。"
            "行业（industries）只能作为附加过滤条件，服务端不接受只按行业搜索。"
        )


def validate_human_search_params(params: dict) -> None:
    """拒绝没有可靠身份或“人物条件 + 范围”组合的人物列表查询。"""
    direct_identity_fields = ('hids', 'humanUrls', 'humanNames')
    organization_fields = ('pids', 'companyUrls', 'companyNames', 'sids', 'schoolNames')
    role_fields = ('titleNames',)
    professional_fields = ('skills', 'certifications', 'profiles', 'keywords')
    scope_fields = (
        'countryCodes',
        'humanIndustries',
        'companyIndustries',
        'companySizes',
        *organization_fields,
    )

    has_direct_identity = any(_has_value(params, field) for field in direct_identity_fields)
    has_organization = any(_has_value(params, field) for field in organization_fields)
    has_role = any(_has_value(params, field) for field in role_fields)
    has_professional = any(_has_value(params, field) for field in professional_fields)
    has_scope = any(_has_value(params, field) for field in scope_fields)

    if has_direct_identity or has_organization or ((has_role or has_professional) and has_scope):
        return

    raise ValueError(
        "人物查询缺少可靠搜索锚点。请提供人物身份、公司/学校，或职位/专业条件与行业/地区范围的组合。"
    )

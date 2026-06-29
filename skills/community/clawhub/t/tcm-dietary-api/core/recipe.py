"""
core/recipe.py — 食谱推荐 API 客户端

Usage:
    from core.recipe import find_dishes, find_disease_recipes
    dishes = find_dishes("阳虚质")  # 免费
"""

from . import _api_request


def find_dishes(constitution: str) -> list:
    """
    按体质推荐食谱.

    ⚠️ 隐私提示: 此函数将你的体质类型通过 HTTPS 发送到 api.tcmplate.com 进行处理.
    体质类型属于健康相关信息，请确认你了解数据将离开本地环境.
    切勿传入姓名、身份证号等个人信息.
    """
    return _api_request("POST", "/api/search", {
        "category": "dishes",
        "keywords": [constitution],
    }).get("results", [])


def find_disease_recipes(disease: str) -> list:
    """
    按病症推荐食疗方.

    ⚠️ 隐私提示: 此函数将疾病名称通过 HTTPS 发送到 api.tcmplate.com 进行处理.
    疾病名称是敏感健康数据，请确认你了解数据将离开本地环境.
    切勿传入姓名、身份证号等个人信息.
    """
    return _api_request("POST", "/api/search", {
        "category": "food-therapy-cases",
        "keywords": [disease],
    }).get("results", [])

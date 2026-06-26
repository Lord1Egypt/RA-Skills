"""
API 蓝图注册
"""

from .agent_api import agent_bp
from .wechat_api import wechat_bp
from .h5_api import h5_bp
from .miniprogram_api import mp_bp
from .dashboard_api import dashboard_bp
from .overview_api import overview_bp
from .benchmark_api import benchmark_bp
from .pwa_api import pwa_bp


def register_blueprints(app):
    """注册所有 API 蓝图"""
    app.register_blueprint(agent_bp)
    app.register_blueprint(wechat_bp)
    app.register_blueprint(h5_bp)
    app.register_blueprint(mp_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(overview_bp)
    app.register_blueprint(benchmark_bp)
    app.register_blueprint(pwa_bp)

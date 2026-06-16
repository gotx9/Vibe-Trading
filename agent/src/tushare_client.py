"""统一的 Tushare 客户端模块 —— 管理 token、代理地址和 API 实例。

所有需要 tushare 的模块统一通过此文件获取 pro_api 实例，
避免在多处重复配置 token 和代理地址。

用法:
    from src.tushare_client import get_pro

    pro = get_pro()
    df = pro.daily(ts_code='000001.SZ', start_date='20260101', end_date='20260110')

    # 对于 ts.pro_bar 等模块级接口，需要显式传入 api=pro：
    # df = ts.pro_bar(ts_code='002594.SZ', api=pro, ...)

环境变量:
    TUSHARE_TOKEN      - Tushare Pro token（必填）
    TUSHARE_PROXY_URL  - 中转站代理地址（必填，如 http://111.170.140.159:8020/）
"""

from __future__ import annotations

import os
from typing import Any

import tushare as ts

__all__ = ["get_pro"]

_PRO_INSTANCE: Any = None
_TOKEN_PLACEHOLDERS: frozenset[str] = frozenset({"", "your-tushare-token"})


def get_pro() -> Any:
    """获取已配置 token 和代理地址的 tushare pro_api 单例实例。

    首次调用时初始化，后续调用返回同一实例。
    每次调用会校验 token 是否有效。

    Raises:
        RuntimeError: TUSHARE_TOKEN 未设置或为占位值
        RuntimeError: TUSHARE_PROXY_URL 未设置
    """
    global _PRO_INSTANCE

    if _PRO_INSTANCE is not None:
        return _PRO_INSTANCE

    token = os.getenv("TUSHARE_TOKEN", "").strip()
    if token in _TOKEN_PLACEHOLDERS:
        raise RuntimeError(
            "TUSHARE_TOKEN 未设置或仍为占位值，请在 agent/.env 中配置"
        )

    proxy_url = os.getenv("TUSHARE_PROXY_URL", "").strip()
    if not proxy_url:
        raise RuntimeError(
            "TUSHARE_PROXY_URL 未设置，请在 agent/.env 中配置中转站代理地址"
        )

    ts.set_token(token)
    _PRO_INSTANCE = ts.pro_api()
    _PRO_INSTANCE._DataApi__http_url = proxy_url

    return _PRO_INSTANCE

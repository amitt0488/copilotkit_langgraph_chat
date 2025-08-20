"""Proxy utilities for requests.

Returns a requests-compatible proxies dict when proxy environment variables
are set. If no proxy is configured, returns None.
"""

import os
from typing import Optional, Dict


def get_proxy_if_enabled() -> Optional[Dict[str, str]]:
    """Return a requests proxies mapping if proxy env vars are set, else None.

    Respects standard env vars: HTTPS_PROXY, HTTP_PROXY (and lowercase variants).
    """
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    if not https_proxy and not http_proxy:
        return None
    proxies: Dict[str, str] = {}
    if http_proxy:
        proxies["http"] = http_proxy
    if https_proxy:
        proxies["https"] = https_proxy
    return proxies or None

"""Proxy utilities for requests.

Provides a helper to return a requests-compatible proxies dict when
proxy environment variables are set. If no proxy is configured, returns None.
"""

import os
from typing import Optional, Dict


def get_proxy_if_enabled() -> Optional[Dict[str, str]]:
	"""Return a requests proxies mapping if proxy env vars are set, else None.

	Respects standard env vars: HTTPS_PROXY, HTTP_PROXY (and lowercase variants).
	"""
	https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
	http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
	if not https_proxy and not http_proxy:
		return None
	proxies = {}
	if http_proxy:
		proxies["http"] = http_proxy
	if https_proxy:
		proxies["https"] = https_proxy
	return proxies or None



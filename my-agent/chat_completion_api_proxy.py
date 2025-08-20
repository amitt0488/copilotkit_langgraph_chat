import os
import requests
from typing import List, Dict, Optional
from utils.proxy_utils import get_proxy_if_enabled

class ChatCompletionProxy:
    def __init__(self, api_url: str, api_key: str, model: str, temperature: float = 0.0):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.proxies: Optional[Dict[str, str]] = get_proxy_if_enabled()

    def chat(self, messages: List[Dict[str, str]]) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "cache": {"no-cache": True},
            "temperature": self.temperature,
        }
        # Allow disabling SSL verification via env if needed (corporate CAs)
        verify: bool = os.environ.get("PY_REQUESTS_VERIFY", "true").lower() == "true"
        response = requests.post(self.api_url, headers=headers, proxies=self.proxies, json=payload, verify=verify)
        response.raise_for_status()
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            raise ValueError("Failed to extract content from the API response.")
        return content

import requests
from typing import List, Dict, Optional
from utils.proxy_utils import get_proxy_if_enabled


class ChatCompletionProxy:
	def __init__(self, api_url: str, api_key: str, model: str, temperature: float = 0.0):
		self.api_url = api_url
		self.api_key = api_key
		self.model = model
		self.temperature = temperature
		self.proxies: Optional[Dict[str, str]] = get_proxy_if_enabled()

	def chat(self, messages: List[Dict[str, str]]) -> str:
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {self.api_key}",
		}
		payload = {
			"model": self.model,
			"messages": messages,
			"cache": {"no-cache": True},
			"temperature": self.temperature,
		}
		response = requests.post(self.api_url, headers=headers, proxies=self.proxies, json=payload)
		response.raise_for_status()
		result = response.json()
		# Extract assistant reply
		content = (
			result.get("choices", [{}])[0]
			.get("message", {})
			.get("content", "")
		)
		if not content:
			raise ValueError("Failed to extract content from the API response.")
		return content



from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

import requests


class ResponseLike(Protocol):
    def raise_for_status(self) -> None:
        ...

    def json(self) -> dict[str, Any]:
        ...


class SessionLike(Protocol):
    def get(self, url: str, timeout: float) -> ResponseLike:
        ...


class WeatherServiceError(RuntimeError):
    """Raised when the weather service returns invalid data."""


@dataclass(frozen=True)
class WeatherClient:
    """Tiny client used for a realistic, testable Python demo app."""

    base_url: str
    session: SessionLike | None = None
    timeout: float = 5.0

    def fetch_city_weather(self, city: str) -> dict[str, Any]:
        normalized_city = city.strip().lower()

        if not normalized_city:
            raise ValueError("city must not be empty")

        session = self.session or requests.Session()
        response = session.get(
            f"{self.base_url.rstrip('/')}/weather/{normalized_city}",
            timeout=self.timeout,
        )
        response.raise_for_status()

        payload = response.json()

        if "temperature_c" not in payload or "condition" not in payload:
            raise WeatherServiceError("weather response is missing required fields")

        return payload


def summarize_weather(city: str, payload: dict[str, Any]) -> str:
    """Return a compact summary suitable for CLI/API output."""

    condition = str(payload["condition"]).strip().lower()
    temperature = float(payload["temperature_c"])

    return f"{city.strip().title()}: {temperature:.1f}°C, {condition}"

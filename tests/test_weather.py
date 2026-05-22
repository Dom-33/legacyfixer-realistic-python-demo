from __future__ import annotations

import pytest

from realistic_demo import WeatherClient, WeatherServiceError, summarize_weather


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get(self, url, timeout):
        self.calls.append((url, timeout))
        return FakeResponse(self.payload)


def test_fetch_city_weather_returns_payload_and_uses_normalized_city():
    session = FakeSession({"temperature_c": 21.4, "condition": "Clear"})
    client = WeatherClient("https://weather.example.test/api", session=session, timeout=2.5)

    payload = client.fetch_city_weather("  Bucharest  ")

    assert payload == {"temperature_c": 21.4, "condition": "Clear"}
    assert session.calls == [("https://weather.example.test/api/weather/bucharest", 2.5)]


def test_fetch_city_weather_rejects_empty_city():
    client = WeatherClient("https://weather.example.test/api", session=FakeSession({}))

    with pytest.raises(ValueError, match="city must not be empty"):
        client.fetch_city_weather("   ")


def test_fetch_city_weather_rejects_invalid_payload():
    client = WeatherClient(
        "https://weather.example.test/api",
        session=FakeSession({"temperature_c": 20.0}),
    )

    with pytest.raises(WeatherServiceError, match="missing required fields"):
        client.fetch_city_weather("Paris")


def test_summarize_weather_formats_output():
    result = summarize_weather("cluj", {"temperature_c": 18, "condition": "Cloudy"})

    assert result == "Cluj: 18.0°C, cloudy"

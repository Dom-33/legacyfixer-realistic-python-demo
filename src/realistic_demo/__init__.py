"""Small demo package for LegacyFixer repository-level testing."""

from .weather import WeatherClient, WeatherServiceError, summarize_weather

__all__ = ["WeatherClient", "WeatherServiceError", "summarize_weather"]

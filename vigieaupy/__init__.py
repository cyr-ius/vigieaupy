"""VigiEau Python client for fetching French water restriction data."""

from .api import VigiEau, Source, Consommateur
from .auth import HttpRequestError, RequestException, TimeoutExceededError
from .exceptions import VigiEauException

__all__ = [
    "VigiEau",
    "Source",
    "Consommateur",
    "VigiEauException",
    "HttpRequestError",
    "TimeoutExceededError",
    "RequestException",
]

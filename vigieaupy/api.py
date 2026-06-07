"""VigiEau API client for querying French water restriction data."""

from enum import Enum
import logging
from typing import Any

from .auth import HTTPRequest, HttpRequestError
from .consts import API_BASE_URL, API_BASE_URL_COG
from .exceptions import VigiEauException

_LOGGER = logging.getLogger(__name__)


class Source(str, Enum):
    """Water resource type."""

    AEP = "AEP"
    SUP = "SUP"
    SOU = "SOU"


LABELS_TYPE_EAU: dict["Source", str] = {
    Source.AEP: "Eau du robinet",
    Source.SUP: "Cours d'eau et rivières",
    Source.SOU: "Des nappes (puits ou forages)",
}


class Consommateur(str, Enum):
    """Consumer profile type."""

    particulier = "particulier"
    exploitation = "exploitation"
    entreprise = "entreprise"
    collectivite = "collectivité"


LABELS_CONSOMMATEUR: dict["Consommateur", str] = {
    Consommateur.particulier: "Particulier",
    Consommateur.exploitation: "Exploitation agricole",
    Consommateur.entreprise: "Professionnel",
    Consommateur.collectivite: "Collectivité",
}


class VigiEau(HTTPRequest):
    """Class to handle VigiEau information."""

    async def async_get_cog(
        self, codeZip: int | None = None, name: str | None = None
    ) -> list[dict[str, Any]]:
        """Fetch communes from the French government COG API.

        Returns a list of communes matching the provided postal code or name. If both parameters are provided, the name takes precedence.
        """
        if name:
            if len(name) < 3:
                raise VigiEauException("Name must be at least 3 characters long.")
            param = {"nom": name}
        elif codeZip:
            if len(str(codeZip)) != 5:
                raise VigiEauException("Code postal must be 5 digits long.")
            param = {"codePostal": codeZip}
        else:
            raise VigiEauException("Either codeZip or name must be provided.")

        try:
            return await self.async_request(path=API_BASE_URL_COG, params=param)

        except HttpRequestError as error:
            _LOGGER.error("Failed to fetch COG data from VigiEau: %s", error)
            raise VigiEauException("Error fetching COG data from VigiEau.") from error

    async def async_get_data(
        self,
        codeInsee: str,
        source: Source | None = None,
        consommateur: Consommateur | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch VigiEau restriction data for a given INSEE commune code."""
        try:
            params: dict[str, Any] = {"commune": codeInsee}
            if source:
                params["zoneType"] = source.value
            if consommateur:
                params["profil"] = consommateur.value
            return await self.async_request(path=API_BASE_URL, params=params)
        except HttpRequestError as error:
            _LOGGER.error("Failed to fetch data from VigiEau: %s", error)
            raise VigiEauException("Error fetching data from VigiEau.") from error

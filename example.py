"""Usage example for the VigiEau client."""

import asyncio
import logging

from vigieaupy import Consommateur, Source, VigiEau, VigiEauException

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


async def async_main() -> None:
    """Demonstrate basic usage of the VigiEau client."""
    api = VigiEau()

    try:
        communes = await api.async_get_cog(name="La Croix-aux-Bois")
        for item in communes:
            logger.info("Commune: %s", item)

        vigieau_data = await api.async_get_data(
            codeInsee=communes[0]["code"],
            source=Source.AEP,
            consommateur=Consommateur.particulier,
        )
        for item in vigieau_data:
            logger.info("VigiEau data: %s", item)

    except VigiEauException as err:
        logger.error(err)
        return

    await api.async_close()


if __name__ == "__main__":
    asyncio.run(async_main())

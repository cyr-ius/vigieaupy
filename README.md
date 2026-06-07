# VigiEauPy

Asynchronous Python client for the [VigiEau](https://vigieau.gouv.fr) API, the official French service for monitoring water use restrictions during drought periods.

## Installation

```bash
pip install vigieaupy
```

## Requirements

- Python >= 3.10
- [aiohttp](https://docs.aiohttp.org/) >= 3.8.1

## Usage

```python
import asyncio
from vigieaupy import Consommateur, Source, VigiEau, VigiEauException

async def main():
    api = VigiEau()

    try:
        # Search for a commune by name or postal code
        communes = await api.async_get_cog(name="Nantes")
        # or: communes = await api.async_get_cog(codeZip=44000)

        # Fetch active water restrictions
        restrictions = await api.async_get_data(
            codeInsee=communes[0]["code"],
            source=Source.AEP,
            consommateur=Consommateur.particulier,
        )
        for restriction in restrictions:
            print(restriction)

    except VigiEauException as err:
        print(f"Error: {err}")
    finally:
        await api.async_close()

asyncio.run(main())
```

## API

### `VigiEau(session=None, timeout=120)`

Main client class. Optionally accepts an existing `aiohttp.ClientSession` and a timeout in seconds.

#### `async_get_cog(codeZip=None, name=None)`

Search for communes using the French government API (geo.api.gouv.fr).

| Parameter | Type  | Description                         |
| --------- | ----- | ----------------------------------- |
| `codeZip` | `int` | 5-digit postal code                 |
| `name`    | `str` | Commune name (3 characters minimum) |

Returns a list of matching communes.

#### `async_get_data(codeInsee, source=None, consommateur=None)`

Fetch active water restrictions for a commune.

| Parameter      | Type           | Description                    |
| -------------- | -------------- | ------------------------------ |
| `codeInsee`    | `str`          | INSEE code of the commune      |
| `source`       | `Source`       | Water resource type (optional) |
| `consommateur` | `Consommateur` | Consumer profile (optional)    |

### Enum `Source`

| Value        | Description                      |
| ------------ | -------------------------------- |
| `Source.AEP` | Tap water                        |
| `Source.SUP` | Rivers and streams               |
| `Source.SOU` | Groundwater (wells or boreholes) |

### Enum `Consommateur`

| Value                       | Description            |
| --------------------------- | ---------------------- |
| `Consommateur.particulier`  | Individual             |
| `Consommateur.exploitation` | Agricultural operation |
| `Consommateur.entreprise`   | Professional           |
| `Consommateur.collectivite` | Local authority        |

## Exceptions

| Exception              | Description                    |
| ---------------------- | ------------------------------ |
| `VigiEauException`     | Base client exception          |
| `HttpRequestError`     | API communication error        |
| `TimeoutExceededError` | Request timed out              |
| `RequestException`     | HTTP error returned by the API |

## License

GPL-3.0-or-later — see the [LICENSE](LICENSE) file.

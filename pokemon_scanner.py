import requests
import json
import argparse
import sys

def fetch_pokemon_data(pokemon_name):
    """Fetches data for a specified Pokémon from the PokéAPI."""
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    url = f"{base_url}{pokemon_name.lower()}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        pokemon_details = {
            "pokemon_name": data["name"],
            "base_experience": data["base_experience"],
            "height": data["height"],
            "weight": data["weight"],
            "abilities": [ability["ability"]["name"] for ability in data["abilities"]]
        }
        return pokemon_details
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch details about a specified Pokémon from the PokéAPI.")
    parser.add_argument("pokemon", help="The name of the Pokémon to search for.")
    args = parser.parse_args()

    pokemon_name = args.pokemon
    pokemon_data = fetch_pokemon_data(pokemon_name)

    if pokemon_data:
        print(json.dumps(pokemon_data, indent=4))
    else:
        print(f"Could not retrieve data for Pokémon: {pokemon_name}. Please check the name and your internet connection.")
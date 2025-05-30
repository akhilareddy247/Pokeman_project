Pokémon API Scanner & Containerization & Deployment with Helm
Scenario 1: Pokémon API Scanner
Task: Develop a Python tool that fetches data from the PokéAPI and retrieves details about a specified Pokémon.
Requirements:
•	Output must be in JSON format.
•	The tool should accept a command-line argument for the Pokémon name.
Step-by-Step Process:
1.	Set up the Development Environment:
o	Install Python 3.x.
o	Install the requests library: pip install requests
2.	Create pokemon_scanner.py:
Python
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
        response.raise_for_status()

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
3.	Run the script:
python pokemon_scanner.py pikachu
Scenario 2: Containerizing the Pokémon Scanner
Task: Containerize the script from Scenario 1 using Alpine Linux as the base image and publish it on Docker Hub.
Requirements:
•	Publish the Docker image on Docker Hub.
Step-by-Step Process:
1.	Create Dockerfile:
Dockerfile
FROM python:3.9-alpine3.18

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pokemon_scanner.py .

CMD ["python", "pokemon_scanner.py"]
2.	Create requirements.txt:
3.	requests
4.	Build the Docker Image:
docker build -t pokemon-scanner .
5.	Tag the Image:
docker tag pokemon-scanner akhilaraju247/pokemon-scanner:latest
6.	Log in to Docker Hub:
docker login
7.	Push the Image:
docker push akhilaraju247/pokemon-scanner:latest
Scenario 3: Deploying with Helm on Minikube
Task: Create a Helm chart to deploy the container from Scenario 2 on Minikube for manual execution.
Requirements:
•	The pod should not auto-execute but should be accessible for manual execution.
Step-by-Step Process:
1.	Prerequisites: Minikube and Helm installed and running.
2.	Create Helm Chart:
helm create pokemon-scanner-chart
 
3.	Modify pokemon-scanner-chart/Chart.yaml:
YAML
4.	apiVersion: v2
5.	name: pokemon-scanner-chart
6.	description: A Helm chart for the Pokémon API Scanner.
7.	version: 0.1.0
8.	appVersion: 1.0.0
9.	Modify pokemon-scanner-chart/values.yaml:
YAML
10.	image:
11.	  repository: akhilaraju247/pokemon-scanner:latest
12.	  tag: latest
13.	  pullPolicy: IfNotPresent
14.	resources: {}
15.	
16.	Modify pokemon-scanner-chart/templates/manual-pod.yaml:
YAML
17.	apiVersion: v1
18.	kind: Pod
19.	metadata:
20.	  name: pokemon-scanner-manual-pod
21.	  labels:
22.	    app: pokemon-scanner
23.	spec:
24.	  dnsPolicy: ClusterFirstWithHostNet
25.	  # dnsConfig:
26.	  #   nameservers:
27.	  #     - 8.8.8.8
28.	  containers:
29.	    - name: pokemon-scanner
30.	      image: "local-pokemon-scanner:latest"
31.	      imagePullPolicy: Never
32.	      command: ["/bin/sh", "-c", "echo 'Pod is ready for manual execution. Use kubectl exec -it pokemon-scanner-manual-pod -- python pokemon_scanner.py <pokemon-name>' && sleep 3600"]
33.	Remove templates/tests and simplify templates:
rm -rf pokemon-scanner-chart/templates/tests
34.	Pull Image to Minikube:
minikube ssh
docker tag pokemon-scanner akhilaraju247/pokemon-scanner:latest
docker push akhilaraju247/pokemon-scanner:latest
exit
 
 
35.	Install Helm Chart:
helm install pokemon-app ./pokemon-scanner-chart
 
 
36.	Manually Execute Scanner:
kubectl exec -it pokemon-scanner-manual-pod -- python pokemon_scanner.py pikachu
 

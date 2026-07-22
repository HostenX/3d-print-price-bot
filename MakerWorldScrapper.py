from bs4 import BeautifulSoup
import requests
import time
import json

def obtain_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    connected= False
    tries = 0
    max_tries = 5


    while not connected and tries < max_tries:

        tries += 1
        print(f"Attempt {tries} of {max_tries} to connect to MakerWorld...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print("Connected to MakerWorld successfully.")

                soup = BeautifulSoup(response.content, "html.parser")
                title = soup.title.string if soup.title else "Sin título"

                connected = True
            elif response.status_code == 403:
                print("Access denied (403). Trying again...")
            else:
                print(f"Failed to connect. Status code: {response.status_code}. Trying again...")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        if not connected and tries < max_tries:
            print("Retrying in 5 seconds...")
            time.sleep(5)
    if not connected:
        print("Failed to connect to MakerWorld after multiple attempts.")

    script_data = soup.find("script", {"id": "__NEXT_DATA__"})

    if script_data and script_data.string:
        try:
            json_data = json.loads(script_data.string)
            design_data = json_data.get("props", {}).get("pageProps", {}).get("design", {})
            instances = design_data.get("instances", [])

            if instances:
                main_instance = instances[0]
                total_weight_gr = main_instance.get("weight", 0)
                total_print_time_sec = main_instance.get("prediction", 0)

                hours, minutes = divmod(total_print_time_sec // 60, 60)
                time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

                
                return total_weight_gr, total_print_time_sec, title, time_str
            else:
                print("No instances found in the design data.")
        except json.JSONDecodeError:
            print("Failed to parse JSON data from the script tag.")
    else:
        print("No script tag with id '__NEXT_DATA__' found or it is empty.")
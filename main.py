import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm

# Función para obtener datos meteorológicos de una ciudad
def fetch_weather(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    time.sleep(1)  # Simular una demora
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        return {'error': f'Error al obtener el clima para {city_name}'}

# Función para manejar la barra de progreso y las peticiones por lotes
def realizar_peticiones_por_lotes(ciudades, api_key):
    total_peticiones = len(ciudades)
    tamano_lote = 5

    # Barra de progreso general
    with tqdm(total=total_peticiones, desc="Progreso General", unit="petición", colour='green') as progreso_general:
        # Usar ThreadPoolExecutor para hacer peticiones en paralelo
        with ThreadPoolExecutor(max_workers=tamano_lote) as ejecutor:
            for i in range(0, total_peticiones, tamano_lote):
                lote_ciudades = ciudades[i:i + tamano_lote]
                futuros = [ejecutor.submit(fetch_weather, city, api_key) for city in lote_ciudades]

                tqdm.write(f"\n\033[94mProcesando lote {i // tamano_lote + 1}...\033[0m")  # Mensaje con color

                # Barra de progreso individual para cada lote
                with tqdm(total=len(lote_ciudades), desc=f"Progreso del Lote {i // tamano_lote + 1}", unit="petición", leave=False, colour='blue') as progreso_lote:
                    resultados = []
                    for futuro in as_completed(futuros):
                        resultado = futuro.result()
                        resultados.append(resultado)
                        progreso_lote.update(1)
                        progreso_general.update(1)

                # Imprimir resultados del lote
                for resultado in resultados:
                    if 'name' in resultado:
                        tqdm.write(f"\033[92m✔ Éxito:\033[0m Ciudad: {resultado['name']} | Clima: {resultado['weather'][0]['description']} | Temp: {resultado['main']['temp']}°C")
                    else:
                        tqdm.write(f"\033[91m✘ Error:\033[0m {resultado['error']}")

                time.sleep(1)  # Pausa para mejor visualización entre lotes

if __name__ == "__main__":
    # Lista de ciudades para consultar el clima
    ciudades = ["Madrid", "London", "Tokyo", "New York", "Paris", "Mexico City", "Berlin", "Sydney", "Moscow", "Rio de Janeiro", "Cairo", "Istanbul", "Cape Town", "Seoul", "Mumbai", "Bangkok", "Beijing", "Jakarta", "Lima", "Buenos Aires", "Santiago", "Toronto", "Los Angeles", "Chicago", "Miami", "Houston", "Dallas", "Phoenix", "Las Vegas", "San Francisco", "Seattle", "Vancouver", "Montreal", "Havana", "San Juan", "Santo Domingo", "Bogota", "Caracas", "Quito", "Lisbon", "Barcelona", "Rome", "Berlin", "Amsterdam", "Brussels", "Vienna", "Zurich", "Stockholm", "Oslo", "Helsinki", "Copenhagen", "Warsaw", "Prague", "Budapest", "Athens", "Istanbul", "Moscow", "Dubai", "Riyadh", "Cairo", "Cape Town", "Nairobi", "Mumbai", "Bangkok", "Singapore", "Kuala Lumpur", "Jakarta", "Manila", "Sydney", "Auckland", "Tokyo", "Seoul", "Beijing", "Shanghai", "Hong Kong", "Taipei", "Hanoi", "Ho Chi Minh City", "Phnom Penh", "Yangon", "Kathmandu", "New Delhi", "Karachi", "Mumbai", "Colombo", "Dhaka", "Tehran", "Baghdad", "Riyadh", "Ankara", "Cairo", "Casablanca", "Johannesburg", "Lagos", "Kinshasa", "Nairobi", "Addis Ababa", "Khartoum", "Tunis", "Algiers", "Tripoli", "Rabat", "Accra", "Abidjan", "Dakar", "Monrovia", "Conakry", "Freetown", "Banjul", "Bissau", "Praia", "Nouakchott", "Bamako", "Niamey", "Ouagadougou", "Lome", "Cotonou", "Yaounde", "Bangui", "N'Djamena", "Khartoum", "Kigali", "Bujumbura", "Kampala", "Nairobi", "Dodoma", "Lilongwe", "Lusaka", "Harare", "Gaborone", "Windhoek"]

    # Clave de API de OpenWeather
    api_key = "09ddf27515955d434f1b87845ee7dd3d"  # Debes colocar tu clave de API de OpenWeather

    start_time = time.time()
    realizar_peticiones_por_lotes(ciudades, api_key)
    print(f"\n\033[93mTerminado en {time.time() - start_time:.2f} segundos\033[0m")

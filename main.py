import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Función para obtener datos meteorológicos de una ciudad
def fetch_weather(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    time.sleep(1)  # Simular una demora
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error al obtener el clima para {city_name}'}

# Función para manejar la barra de progreso y las peticiones por lotes
def realizar_peticiones_por_lotes(ciudades, api_key, output_widget):
    total_peticiones = len(ciudades)
    tamano_lote = 5

    output_widget.delete(1.0, tk.END)  # Limpiar el widget de salida

    # Usar ThreadPoolExecutor para hacer peticiones en paralelo
    with ThreadPoolExecutor(max_workers=tamano_lote) as ejecutor:
        for i in range(0, total_peticiones, tamano_lote):
            lote_ciudades = ciudades[i:i + tamano_lote]
            futuros = [ejecutor.submit(fetch_weather, city, api_key) for city in lote_ciudades]

            output_widget.insert(tk.END, f"\nProcesando lote {i // tamano_lote + 1}...\n")
            output_widget.update_idletasks()  # Actualiza la interfaz para mostrar el mensaje de procesamiento

            # Procesar resultados
            for futuro in as_completed(futuros):
                resultado = futuro.result()
                if 'name' in resultado:
                    output_widget.insert(tk.END, f"✔ Éxito: Ciudad: {resultado['name']} | Clima: {resultado['weather'][0]['description']} | Temp: {resultado['main']['temp']}°C\n")
                else:
                    output_widget.insert(tk.END, f"✘ Error: {resultado['error']}\n")

            output_widget.see(tk.END)  # Desplazarse hacia abajo
            output_widget.update_idletasks()  # Actualizar la interfaz

            time.sleep(1)  # Pausa para mejor visualización entre lotes

# Función para iniciar el proceso de consulta de clima
def iniciar_consulta():
    ciudades = ["Madrid", "London", "Tokyo", "New York", "Paris", "Mexico City", "Berlin", "Sydney", "Moscow", "Rio de Janeiro", "Cairo", "Istanbul", "Cape Town", "Seoul", "Mumbai", "Bangkok", "Beijing", "Jakarta", "Lima", "Buenos Aires", "Santiago", "Toronto", "Los Angeles", "Chicago", "Miami", "Houston", "Dallas", "Phoenix", "Las Vegas", "San Francisco", "Seattle", "Vancouver", "Montreal", "Havana", "San Juan", "Santo Domingo", "Bogota", "Caracas", "Quito", "Lisbon", "Barcelona", "Rome", "Berlin", "Amsterdam", "Brussels", "Vienna", "Zurich", "Stockholm", "Oslo", "Helsinki", "Copenhagen", "Warsaw", "Prague", "Budapest", "Athens", "Istanbul", "Moscow", "Dubai", "Riyadh", "Cairo", "Cape Town", "Nairobi", "Mumbai", "Bangkok", "Singapore", "Kuala Lumpur", "Jakarta", "Manila", "Sydney", "Auckland", "Tokyo", "Seoul", "Beijing", "Shanghai", "Hong Kong", "Taipei", "Hanoi", "Ho Chi Minh City", "Phnom Penh", "Yangon", "Kathmandu", "New Delhi", "Karachi", "Mumbai", "Colombo", "Dhaka", "Tehran", "Baghdad", "Riyadh", "Ankara", "Cairo", "Casablanca", "Johannesburg", "Lagos", "Kinshasa", "Nairobi", "Addis Ababa", "Khartoum", "Tunis", "Algiers", "Tripoli", "Rabat", "Accra", "Abidjan", "Dakar", "Monrovia", "Conakry", "Freetown", "Banjul", "Bissau", "Praia", "Nouakchott", "Bamako", "Niamey", "Ouagadougou", "Lome", "Cotonou", "Yaounde", "Bangui", "N'Djamena", "Khartoum", "Kigali", "Bujumbura", "Kampala", "Nairobi", "Dodoma", "Lilongwe", "Lusaka", "Harare", "Gaborone", "Windhoek"]
    api_key = api_key_entry.get().strip()

    if not api_key:
        messagebox.showerror("Error", "Por favor, introduce una clave de API válida.")
        return

    start_time = time.time()
    realizar_peticiones_por_lotes(ciudades, api_key, output_text)
    output_text.insert(tk.END, f"\nTerminado en {time.time() - start_time:.2f} segundos\n")
    output_text.see(tk.END)  # Desplazarse hacia abajo al final

# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Clima")

# Crear un frame para la entrada de API Key
frame = tk.Frame(root)
frame.pack(pady=10)

api_key_label = tk.Label(frame, text="Clave de API:")
api_key_label.pack(side=tk.LEFT)

api_key_entry = tk.Entry(frame)
api_key_entry.pack(side=tk.LEFT)

start_button = tk.Button(root, text="Iniciar Consulta", command=iniciar_consulta)
start_button.pack(pady=10)

# Widget de texto para mostrar resultados
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()

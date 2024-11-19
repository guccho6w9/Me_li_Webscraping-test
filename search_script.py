import os
import json
import csv
import requests
from lxml import html

# Configuración de cookies y headers
cookies = {
    '_d2id': 'ff90b40f-0f9d-4b44-9e62-0c26d02c1366',
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}

# Variables de configuración
producto_a_buscar = "pc-gamer"  # En caso de múltiples palabras, usar "-" en lugar de espacios
num_productos = 60  # Número de productos más caros y más baratos a obtener
productos_por_pagina = 48  # Mercado Libre devuelve hasta 48 resultados por página

# URLs base para ordenar por precio
url_ascendente = f"https://listado.mercadolibre.com.ar/{producto_a_buscar}_OrderId_PRICE_NoIndex_True"
url_descendente = f"https://listado.mercadolibre.com.ar/{producto_a_buscar}_OrderId_PRICE*DESC_NoIndex_True"

# Función para obtener productos desde una URL con soporte para paginación
def obtener_productos(url_base, cookies, headers, num_productos, productos_por_pagina):
    productos = []
    desde = 1  # Índice inicial para la paginación
    c=0 #contador para mostrar la cantidad de productos

    while len(productos) < num_productos:
        # Modificar URL para incluir el parámetro de paginación
        url = f"{url_base}_Desde_{desde}" if desde > 1 else url_base
        print(f"Consultando: {url}")
        
        response = requests.get(url, headers=headers, cookies=cookies)
        tree = html.fromstring(response.text)
        xpath = '//script[@data-head-react="true" and @type="application/json"]'
        elements = tree.xpath(xpath)

        if not elements:
            print("No se encontraron más resultados.")
            break

        # Procesar los productos de la página actual
        data = json.loads(elements[0].text)
        results = data.get("pageState", {}).get("initialState", {}).get("results", [])

        if not results:
            print("No hay más resultados en esta página.")
            break

        for item in results:
            if len(productos) >= num_productos:
                break

            polycard = item.get("polycard", {})
            if polycard:
                metadata = polycard.get("metadata", {})
                pictures = polycard.get("pictures", {}).get("pictures", [])
                components = {comp.get("type"): comp for comp in polycard.get("components", [])}

                image_name = pictures[0].get("id") if pictures else None
                image_url = f"https://http2.mlstatic.com/D_Q_NP_2X_{image_name}-V.webp" if image_name else None
                c=c+1
                product_data = {
                    "num_producto": c,
                    "MLA_id": metadata.get("id"),
                    "product_id": metadata.get("product_id"),
                    "keywords": producto_a_buscar,
                    "title": components.get("title", {}).get("title", {}).get("text"),
                    "price": components.get("price", {}).get("price", {}).get("current_price", {}).get("value"),
                    "currency": components.get("price", {}).get("price", {}).get("current_price", {}).get("currency"),
                    "url": metadata.get("url"),
                    "image": image_url,
                }
                productos.append(product_data)

        # Avanzar al siguiente bloque de productos
        desde += productos_por_pagina

    return productos

# Obtener productos más baratos y más caros con paginación
productos_baratos = obtener_productos(url_ascendente, cookies, headers, num_productos, productos_por_pagina)
productos_caros = obtener_productos(url_descendente, cookies, headers, num_productos, productos_por_pagina)

# Guardar los productos en un archivo JSON
output_products_path_json = "output_dir/output.json"
os.makedirs(os.path.dirname(output_products_path_json), exist_ok=True)
with open(output_products_path_json, "w", encoding="utf-8") as file:
    json.dump({"baratos": productos_baratos, "caros": productos_caros}, file, ensure_ascii=False, indent=4)

print(f"Se guardaron los productos en {output_products_path_json}")

# Guardar los productos en un archivo CSV
output_products_path_csv = "output_dir/output.csv"
os.makedirs(os.path.dirname(output_products_path_csv), exist_ok=True)

# Usar la primera entrada para obtener las claves de los encabezados
headers_csv = productos_baratos[0].keys() if productos_baratos else []

with open(output_products_path_csv, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers_csv)
    writer.writeheader()  # Escribir los encabezados en el CSV
    # Escribir los productos de la lista de baratos y caros
    writer.writerows(productos_baratos + productos_caros)

print(f"Se guardaron los productos en {output_products_path_csv}")

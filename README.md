# Meli-Webscraping with lxml and requests

### Target

https://www.mercadolibre.com.ar

### Goal:
get 120 search results along with their product information

-  The 60 cheapest products from the search result
-  The 60 most expensive products

------------

The results are saved as:
- "output.json"
- "output.csv"

### Json example:
```
"baratos": [
        {
            "num_producto": 1,
            "MLA_id": "MLA1918166792",
            "product_id": null,
            "keywords": "pc-gamer",
            "title": "Pc Notebook Instalación De Sistema Operativo",
            "price": 76500,
            "currency": "ARS",
            "url": "articulo.mercadolibre.com.ar/MLA-1918166792-pc-notebook-instalacion-de-sistema-operativo-_JM",
            "image": "https://http2.mlstatic.com/D_Q_NP_2X_894482-MLA79303529320_092024-V.webp"
        },
```

### CSV example:

| num_producto | MLA_ID        | product_ID | keywords | title                                        | price | currency | url                                                                                          | image                                                                    |
|--------------|---------------|------------|----------|----------------------------------------------|-------|----------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| 1            | MLA1918166792 | null       | pc-gamer | Pc Notebook Instalación De Sistema Operativo | 76500 | ARS      | articulo.mercadolibre.com.ar/MLA-1918166792-pc-notebook-instalacion-de-sistema-operativo-_JM | https://http2.mlstatic.com/D_Q_NP_2X_894482-MLA79303529320_092024-V.webp |
|              |               |            |          |                                              |       |          |                                                                                              |                                                                          |
|              |               |            |          |                                              |       |          |                                                                                              |                                                                          |



### Dependencies:
```txt
# /requirements.txt

lxml==5.1.0
requests==2.31.0

# Install dependences
$ pip install -r requirements.txt





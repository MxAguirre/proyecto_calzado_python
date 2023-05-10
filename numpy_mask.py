import numpy as np

genero = str(input('Selecione el genero\nM: Male\nF: Famale'))
country = np.array(["Canada", "Canada", "Canada", "Germany", "Argentina"])
price = np.array([250, 250, 100, 120, 50])

# Crear una máscara para obtener los índices del array
# que corresponden al país Canada
mask = country == "Canada"

# Utilizo la máscara para acceder a los indices del array price
# que corresponden a canada
ventas_canada = price[mask]
print(ventas_canada)
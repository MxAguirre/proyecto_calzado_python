import matplotlib.pylab as plt
import matplotlib.axes
import sqlalchemy
import numpy as np
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

engine = sqlalchemy.create_engine('sqlite:///ventas_calzados.db')
base = declarative_base()

class VentaCalzado(base):
    __tablename__ = 'venta'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(String)
    product_id = Column(Integer)
    country = Column(String)
    gender = Column(String)
    size = Column(String)
    price = Column(String)
    def __repr__(self):
        return f'Id: {self.id} - Id del producto: {self.product_id}'
    


def read_db():
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(VentaCalzado).filter(VentaCalzado.date.is_not('')&VentaCalzado.product_id.is_not('')&VentaCalzado.country.is_not('')&VentaCalzado.gender.is_not('')&VentaCalzado.size.is_not('')&VentaCalzado.price.is_not(''))
    paises = list()
    generos = list()
    talles = list()
    precios = list()

    for q in query:
        paises.append(q.country)
        generos.append(q.gender)
        talles.append(q.size)
        precio_con = q.price
        precio_sin = float(precio_con.replace("$", "").replace(" ", ""))
        precios.append(precio_sin)

    country = np.array(paises)
    gender = np.array(generos)
    size = np.array(talles)    
    price = np.array(precios)
    return country, gender, size, price

def paises_unicos(country):
    countries = np.unique(country)
    return countries

def ventas_pais(countries, country, price):
    ventas_pais = {}
    for pais in countries:
        mask = country == pais
        ventas = price[mask]
        ventas_pais[pais] = np.sum(ventas)
    return ventas_pais

def calzado_pais(countries, country, size):
    size_mas_vendidospais = {}
    for pais in countries:
        mask = country == pais
        size_vendidos = size[mask]
        sizes, cantidad = np.unique(size_vendidos,return_counts=True)
        size_mas_vendidospais[pais] = sizes[np.argmax(cantidad)]
    return size_mas_vendidospais

def ventas_genero_pais(countries, gender_target, country, gender):
    ventas_genero_pais = {}
    for pais in countries:
        mask1 = country == pais
        mask2 = gender == gender_target
        mask = mask1 & mask2
        ventas = country[mask]
        ventas_genero_pais[pais] = len(ventas)
    return ventas_genero_pais

def graficador_bar(titulo, ejes, genero):
    x = list(ejes.keys())
    y = list(ejes.values())
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_facecolor('whitesmoke')
    ax.set_title(f'{titulo} {genero}')
    ax.bar(x, y, color='tab:orange')
    plt.show()

def graficador_scatter(titulo, ejes):
    x = list(ejes.keys())
    y = list(ejes.values())
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_facecolor('whitesmoke')
    ax.set_title(titulo)
    ax.scatter(x,y)
    plt.show()

if __name__ == '__main__':
    arrays = read_db()
    country = arrays[0]
    gender = arrays[1]
    size = arrays[2]
    price = arrays[3]

    countries = paises_unicos(country)
    titulo1 = 'Los paises en los cuales se realizaron ventas son'
    print('\n',titulo1, countries,'\n')

    venta_pais = ventas_pais(countries, country, price)
    titulo2 = 'Dinero recaudado por pais'
    print('\n',titulo2 ,venta_pais, '\n')

    size_mas_vendidospais = calzado_pais(countries,country,size)
    titulo3 = 'Talles mas vendidos por pais'
    print('\n', titulo3, size_mas_vendidospais,'\n')

    genero = str(input('\nSelecione el genero\nM: Male\nF: Famale\nU: Unix\n'))
    while (genero != 'M' and genero != 'F' and genero != 'U'):
        print("Debe ingresar M, F o U")
        genero = str(input('Intente nuevamente: '))
    if genero == 'M':
        genero ='Male'
    elif genero == 'F':
        genero = 'Female'
    elif genero == 'U':
        genero = 'Unix'
    ventas_genero_pais = ventas_genero_pais(countries, genero, country, gender)
    titulo4 = 'Ventas por paises para el genero'
    print('\n',titulo4,genero, ventas_genero_pais,'\n')
    graficador_bar(titulo2, venta_pais, genero='')
    graficador_scatter(titulo3, size_mas_vendidospais)
    graficador_bar(titulo4, ventas_genero_pais, genero)
    
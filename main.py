from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from helper import *

# Loading spark
spark = SparkSession\
   .builder\
   .master("local")\
   .appName("poke_api")\
   .getOrCreate()

# Defining the pokemons ids and the list of HMs we'll filter
pokemons_ids = list(range(1,387))
hm_list = ["cut", "fly", "surf"]

# Cria o objeto "pokemons" a partir da funcao connect_and_collect_data()
pokemons = connect_and_collect_data(pokemons_ids, hm_list)

# Utiliza o createDataFrame tendo como parametro de data, a lista pokemons que esta carregada com os dicionarios de cada pokemon.
# Com o .show(386) temos a apresentacao de todos os pokemons coletados
pokemon_df = spark.createDataFrame(data=pokemons)
pokemon_df.show(386)


# organizando a selecao do codigo
pokemon_df = pokemon_df.select('pokedex_id', 'name', 'type', 'hm', 'region', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed')
pokemon_df.show(5)

# escrevendo em parquet
pokemon_df.write.format('parquet').mode('overwrite').save('./pokemon.parquet')

# finalizando o spark
spark.stop()


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def data_collect(data, id, hm_list):
    """Coleta os data de id do pokedex; nome do pokemon; tipo(s) do pokemon; 
    HM(s) que esteja no hm_list que o pokemon possa aprender; status de hp, ataque, defesa, ataque_especial, 
    defesa_especial e velocidade; tambem faz a definicao da regiao em que o pokemon se encontra a partir de condicionais.
    
    Os data do pokemon presentes no json sao adicionados a um dicionario chamado dict_pokemon, que sera o retorno da funcao.

    Como parametros, recebe o objeto json com os data dos pokemons (data), o id utilizado para realizar as conexao com a API (id),
    e o "hm_list".
    """ 
    dict_pokemon = {"pokedex_id": data["id"],
                    "name": data["name"],
                    "type": [type["type"]["name"] for type in data["types"]],
                    "hm": [move["move"]["name"]for move in data["moves"] if move["move"]["name"] in hm_list],
                    "region": "kanto" if id <= 151 else "johto" if id <= 251 else "hoenn",
                    "hp": data["stats"][0]["base_stat"],
                    "attack":data["stats"][1]["base_stat"],
                    "defense":data["stats"][2]["base_stat"],
                    "special_attack":data["stats"][3]["base_stat"],
                    "special_defense":data["stats"][4]["base_stat"],
                    "speed":data["stats"][5]["base_stat"]
                    }
    return dict_pokemon


def connect_and_collect_data(pokemons_ids, hm_list):
    """Realiza a conexao com a PokeAPI, chama a funcao "data_collect()" para receber o
    dicionario com os data de cada pokemon, faz a insercao dos dicionarios na lista 
    "pokemon_list" criada fora do loop for, que sera o retorno da funcao.

    Cria um loop for para passar os ids de cada pokemon e conectar com a API, realiza
    o try except para verificar e printar no terminal o status da conexao com o id passado.
    Caso a conexao esteja ok, criamos o objeto "data" que recebe os data da API em formato JSON.    
    """
    pokemon_list = []
    
    for id in pokemons_ids:
        url_pokeapi = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        try:
            conn = requests.get(url_pokeapi, verify=False)
        except:
            print(f"Erro na conexao do id: {id}, status da conexao: {conn.status_code}")

        data = conn.json()
        pokemon_list.append(data_collect(data, id, hm_list))
    return pokemon_list
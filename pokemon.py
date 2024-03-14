import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests

st.title("Pokemon Explorer!")
st.divider()

@st.cache_data
def get_all_id_numbers():
    base_url = 'https://pokeapi.co/api/v2/pokemon/'
    current_id = 1
    pokemon_ids = []

    while True:
        url = f'{base_url}{current_id}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pokemon_id = data.get('id')
            if pokemon_id:
                pokemon_ids.append(pokemon_id)
            else:
                break
        else:
            break
        
        current_id += 1
        
    ids = len(pokemon_ids)
    return ids


def get_details(poke_number):
	try:
		url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
		response = requests.get(url)
		pokemon = response.json()
		return pokemon['name'], pokemon['height'], pokemon['weight'], pokemon['sprites']['other']['official-artwork']['front_default'], pokemon['types'][0]['type']['name'], pokemon['cries']['latest'], len(pokemon['moves'])
	except:
		return 'Error', np.NAN, np.NAN, np.NAN
	

pokemon_number = st.slider("Pick a pokemon",
						   min_value=1,
						   max_value=1025
						   )

name, height, weight, front_default, pok_type, battle_cry, moves = get_details(pokemon_number)
height = height * 10

pokemon_colours = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "electric": "#F8D030",
    "grass": "#78C850",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "dark": "#705848",
    "steel": "#B8B8D0",
    "fairy": "#EE99AC",
    "stellar": "#FFD700"  
}

colour = pokemon_colours.get(pok_type)

height_data = pd.DataFrame({'Pokemon' : ['Weedle',name, 'victreebel'],
               'Heights' : [3, height, 17]})

colors = ['gray', colour, 'gray']

graph = sns.barplot(data = height_data,
x = 'Pokemon',
y = 'Heights',
palette = colors)

st.divider()
st.write(f'Name: {name.title()}')
st.divider()
st.write(f'Height: {height}')
st.divider()
st.write(f'Weight: {weight}')
st.divider()
st.write(f'Move Count: {moves}')
st.divider()
st.image(front_default, caption = f'Pokemon: {name}')
st.divider()
st.pyplot(graph.figure)
st.divider()

if battle_cry:
    battle_cry_audio_response = requests.get(battle_cry)
    if battle_cry_audio_response.status_code == 200:
        battle_cry_audio_data = battle_cry_audio_response.content
        st.audio(battle_cry_audio_data, format='audio/mp3', start_time=0)
    else:
        st.write('Failed to fetch battle cry audio.')
else:
    st.write('Battle cry not available')

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests

st.title("Pokemon Explorer!")

@st.cache_data
def get_all_id_numbers():
    count = 0
    poke_num = 1

    base_url = f'https://pokeapi.co/api/v2/pokemon/{poke_num}/'
    


    return list_of_all_numbers

def get_details(poke_number):
	try:
		url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
		response = requests.get(url)
		pokemon = response.json()
		return pokemon['name'], pokemon['height'], pokemon['weight'], pokemon['sprites']['other']['official-artwork']['front_default'], pokemon['cries']['latest'], len(pokemon['moves'])
	except:
		return 'Error', np.NAN, np.NAN, np.NAN
	

pokemon_number = st.slider("Pick a pokemon",
						   min_value=1,
						   max_value=1025
						   )

name, height, weight, front_default, battle_cry, moves = get_details(pokemon_number)
height = height * 10


height_data = pd.DataFrame({'Pokemon' : ['Weedle',name, 'victreebel'],
               'Heights' : [3, height, 17]})

colors = ['gray', 'red', 'gray']

graph = sns.barplot(data = height_data,
x = 'Pokemon',
y = 'Heights',
palette = colors)

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

if battle_cry:
    battle_cry_audio_response = requests.get(battle_cry)
    if battle_cry_audio_response.status_code == 200:
        battle_cry_audio_data = battle_cry_audio_response.content
        st.audio(battle_cry_audio_data, format='audio/mp3', start_time=0)
    else:
        st.write('Failed to fetch battle cry audio.')
else:
    st.write('Battle cry not available')

# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
name_on_smoothie = st.text_input("Name on Smoothie")
st.write("The Name on the smoothie will be", name_on_smoothie)
st.write("Choose the fruits you want to custom smoothie")
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients = st.multiselect(
    "Choose upto 5 ingredients",
    my_dataframe
)
if ingredients:
    ingredients_string = ''
    for fruit in ingredients:
        ingredients_string+=fruit + ' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_smoothie+ """')"""
    
    submit_button = st.button("Submit")
    
    if submit_button:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered!{name_on_smoothie}",icon="✅")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
st.dataframe(data = fruityvice_response.json(),use_container_width = true)

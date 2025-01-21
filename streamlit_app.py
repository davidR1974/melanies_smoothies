# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie !
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)

cnx=st.connection("snowflake")
session =cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients", my_dataframe,
    max_selections=5
)

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name_on_order + """',""" """'""" + ingredients_string + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
#        st.write(my_insert_stmt)
#        st.stop()
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+name_on_order+'!', icon="✅")
      

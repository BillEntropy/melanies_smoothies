import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(my_df, use_container_width=True)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name = st.text_input('Name on smoothie:')

ing_list = st.multiselect('Choose <= 5 ingredients!',my_df, max_selections=5)
if ing_list:
    ing_str = ' '.join(ing_list)
    #st.write(ing_str)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ing_str + """','""" + name + """')"""
    sumbit = st.button('Submit Order')
    #st.write(my_insert_stmt)
    if sumbit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

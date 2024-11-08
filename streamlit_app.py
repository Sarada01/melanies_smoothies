# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the frits you want in your customer Smoothie!
    """
)

from snowflake.snowpark.functions import col
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME"))

name_on_order = st.text_input("Name on the Smoothie:")
st.write(name_on_order)

ingradient_list = st.multiselect("Choose upto 5 Ingredients:"
    , my_dataframe
    , max_selections = 5
    )

if ingradient_list:
    ingr_list = ','.join(ingradient_list)
    order_insert_statement =  ("""
        INSERT INTO smoothies.public.orders (ingredients,name_on_order)
        VALUES ('""" + ingr_list + """','""" + name_on_order + """ \
        ')""") 
    order_submit = st.button("Submit Order")
    if order_submit:
        session.sql(order_insert_statement).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order} !")

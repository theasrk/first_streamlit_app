import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents\' new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#new section to display fruityvice API response
#import requests

#create repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      #streamlit.text(fruityvice_response.json()) # just writes the data to the screen
      #Converts JSON response to a more readable format
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
      # Outputs the response from fruityvice into a table format
      return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)      

except URLError as e:
   streamlit.error()
      
# don't run anthing beyond this point
#streamlit.stop()

#import snowflake.connector
streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * from fruit_load_list")
            return my_cur.fetchall()

#add a button to load the fruit
if streamlit.button('Get fruit Load list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      streamlit.dataframe(my_data_rows)

# allow the user to add a fruit to the list      
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("Insert into fruit_load_list values new_fruit");
            return "Thanks for adding " + new_fruit 

fruit_add = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(fruit_add)
      streamlit.write(back_from_function)


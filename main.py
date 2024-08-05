import streamlit as st
import pandas as pd

st.title("Streamlit on Replit")

text = """

- More information on streamlit [here](https://docs.streamlit.io/)

"""

st.write(text)

st.write("Hello world!")


st.dataframe(
  pd.DataFrame(
    {
      'first column': [1, 2, 3, 4],
      'second column': [10, 20, 30, 40]
    }
  )
)
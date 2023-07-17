import streamlit as st
from myGPT.main import Contract
from myGPT.mygpt_utils import pandas_df_from_string

db = Contract()


def set_state(key, value):
    st.session_state[key] = value


def get_state(key):
    if key not in st.session_state:
        return None if not key.startswith(('is', 'has')) else False
    return st.session_state[key]


def summarize(level_of_detail):
    q = "Summarize"
    set_state('question_ta', q)

    after_asked(q, level_of_detail)


def after_asked(question, level_of_detail):
    for file in files:
        with open(f'./contracts/{file.name}', 'wb') as f:
            f.write(file.getvalue())
            db.add_docs('./contracts')

    with st.spinner('Generating response..'):
        ans, table = db.ask(question, words=level_of_detail)
        set_state('latest_response', ans)
        if table:
            set_state('has_table', True)
            set_state('table', table)
        else:
            set_state('has_table', False)
            set_state('table', None)
        db.pickle()


st.set_page_config(layout="wide")

slider = st.slider("Level of detail", min_value=1, max_value=10, step=1, value=4)

files = st.file_uploader("Upload Contracts", accept_multiple_files=True, type=['txt', 'pdf'])

# db.pickle()
button_clicked = st.button("Summarize", on_click=summarize, kwargs={'level_of_detail': slider})

query = st.text_input("Enter Query", get_state('question_ta') or '')

if st.button("Ask", on_click=after_asked, kwargs={'question': query, 'level_of_detail': slider}):
    print("clicked")


if get_state('has_table'):
    df = pandas_df_from_string(get_state('table'))
    st.dataframe(df, use_container_width=True, hide_index=True)
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Press to Download",
        csv,
        "gpt_data.csv",
        "text/csv",
        key='download-csv'
    )
    t = get_state('latest_response') or ''
    st.write(f"References: {t.split('References')[-1]}")
else:
    st.text_area("Gen AI: ", get_state('latest_response') or '', height=500)


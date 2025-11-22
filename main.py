import streamlit as st
import pandas as pd
from use_db import create_client, use_collection

client = create_client()
collection = use_collection(client)
all_documents = collection.find({})
documents_list = list(all_documents)

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
sel_doc = None
with col1:
    st.title(":blue[Історичні регіони Львова]")
    st.image("./images/Regions.png")

with col2:
    st.subheader(":blue[Виберіть регіон]")
    df = pd.DataFrame(documents_list)
    df_lim = df.iloc[:, 1:2]
    sel = st.dataframe(df_lim, selection_mode="single-row", on_select="rerun")
    sel_rows = sel["selection"]["rows"]
    if len(sel_rows) > 0:
        sel_row = sel_rows[0]
        sel_doc = documents_list[sel_row]
        reg_name = sel_doc.get("name")
        reg_img = sel_doc.get("imgmap")
        img_path = "./images/" + reg_img
        st.subheader(":blue[Карта регіону]")
        st.image(img_path)

        with col1:
            st.subheader(":blue[Розташування]")
            reg_spec = sel_doc.get("spec")
            st.write(reg_spec)
            st.subheader(":blue[Структура]")
            reg_streets= sel_doc.get("streets")
            st.write(reg_streets)
            reg_hist= sel_doc.get("hist")
            if reg_hist:
                st.subheader(":blue[Історія]")
                st.write(reg_hist)
            reg_obj = sel_doc.get("obj")
            if reg_obj:
                st.subheader(":blue[Цікаві об'єкти]")
                st.write(reg_obj)
